"""replication_matrix.py — 多队列 × 多签名规模 复现矩阵。

设计：
  签名来源（默认 GSE50760 的 Atlas DE），取 top-N 上调/下调基因；
  在 N 个独立队列上检验（配对设计），输出"规模 × 队列"的判定矩阵。

用法：
  python -m pilot.replication_matrix \
    --de-file pilot/data/gse50760/atlas_de.txt \
    --cohorts pilot/cohorts.json \
    --sizes 50,100,200 \
    --out pilot/results/replication_matrix.md
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from .audit import render_markdown, run_claims


def load_de(path: Path) -> pd.DataFrame:
    """读取 Atlas DE 表（跳过 # 注释行），返回 gene symbol + fold change。"""
    df = pd.read_csv(path, sep="\t", skiprows=3)
    col_fc = [c for c in df.columns if "primary tumor" in c and "foldChange" in c][0]
    fc = df[["Gene Name", col_fc]].dropna()
    fc.columns = ["gene", "fc"]
    fc = fc[fc.gene.astype(str).str.strip() != ""]
    return fc


def build_signatures(fc: pd.DataFrame, sizes: list[int]) -> dict[str, dict[int, list[str]]]:
    up_all = fc[fc.fc >= 1.5].sort_values("fc", ascending=False)
    down_all = fc[fc.fc <= -1.5].sort_values("fc", ascending=True)
    out = {"up": {}, "down": {}}
    for n in sizes:
        out["up"][n] = up_all.gene.head(n).tolist()
        out["down"][n] = down_all.gene.head(n).tolist()
    return out


def build_claims(cohorts: list[dict], sigs: dict[str, dict[int, list[str]]],
                 sizes: list[int], alpha: float, min_effect: float, min_stable: float,
                 asset_dir: Path) -> list[dict]:
    asset_dir.mkdir(parents=True, exist_ok=True)
    claims: list[dict] = []
    for n in sizes:
        for direction, files in (("up", sigs["up"][n]), ("down", sigs["down"][n])):
            sig_path = asset_dir / f"de_{direction}_top{n}.txt"
            sig_path.write_text("\n".join(files) + "\n", encoding="utf-8")
            for ch in cohorts:
                claims.append({
                    "id": f"{direction}{n}-{ch['name']}",
                    "name": f"{direction} top{n} -> {ch['name']}",
                    "type": "signature",
                    "dataset": {"matrix": ch["matrix"], "metadata": ch["metadata"],
                                 "value_type": ch.get("value_type", "log")},
                    "group": ch["group"],
                    "signature": {"features_file": str(sig_path)},
                    "alpha": alpha,
                    "min_effect": min_effect,
                    "claimed_direction": "a_gt_b" if direction == "up" else "a_lt_b",
                    "robustness": {"covariates": [], "min_stable_fraction": min_stable},
                })
    return claims


def render_matrix(results, cohorts: list[dict], sizes: list[int]) -> str:
    by_id = {r.claim_id: r for r in results}
    lines = ["# 多队列复现矩阵", "",
             "> 单元格式：判定（效应）。robust=通过主检验+留一稳健性；fragile=主检验过但稳健性不足；"
             "not_reproduced=主检验失败；inconclusive=数据不足。", ""]
    for direction in ("up", "down"):
        lines.append(f"## {'上调' if direction == 'up' else '下调'}签名")
        lines.append("")
        header = "| 签名规模 | " + " | ".join(ch["name"] for ch in cohorts) + " |"
        lines.append(header)
        lines.append("|---|" + "---|" * len(cohorts))
        for n in sizes:
            cells = []
            for ch in cohorts:
                r = by_id.get(f"{direction}{n}-{ch['name']}")
                cells.append(f"{r.verdict} ({r.effect:+.2f})" if r else "-")
            lines.append(f"| top-{n} | " + " | ".join(cells) + " |")
        lines.append("")

    # 复现率汇总
    lines.append("## 复现率汇总")
    lines.append("")
    lines.append("| 签名 | " + " | ".join(f"top-{n}" for n in sizes) + " |")
    lines.append("|---|" + "---|" * len(sizes))
    for direction in ("up", "down"):
        row = []
        for n in sizes:
            ok = sum(1 for ch in cohorts
                     if (r := by_id.get(f"{direction}{n}-{ch['name']}")) and r.verdict == "robust")
            row.append(f"{ok}/{len(cohorts)}")
        lines.append(f"| {'上调' if direction == 'up' else '下调'} | " + " | ".join(row) + " |")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="多队列复现矩阵")
    ap.add_argument("--de-file", required=True)
    ap.add_argument("--cohorts", required=True, help="cohorts JSON")
    ap.add_argument("--sizes", default="50,100,200")
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--min-effect", type=float, default=0.5)
    ap.add_argument("--min-stable", type=float, default=0.8)
    ap.add_argument("--out", default="pilot/results/replication_matrix.md")
    args = ap.parse_args()

    fc = load_de(Path(args.de_file))
    cohorts = json.loads(Path(args.cohorts).read_text(encoding="utf-8"))["cohorts"]
    sizes = [int(x) for x in args.sizes.split(",")]
    sigs = build_signatures(fc, sizes)
    asset_dir = Path(args.out).parent / "matrix_assets"
    claims = build_claims(cohorts, sigs, sizes, args.alpha, args.min_effect, args.min_stable, asset_dir)
    results = run_claims(claims)
    md = render_matrix(results, cohorts, sizes)
    # 附完整明细表（方法学元数据 + 判定）
    md += "\n" + render_markdown(results)
    outp = Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(md, encoding="utf-8")
    print(md)


if __name__ == "__main__":
    main()