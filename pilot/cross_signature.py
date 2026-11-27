"""cross_signature.py — 交叉签名矩阵：每个队列各选签名，互相检验。

诊断价值：
  若"复现"只依赖某个队列选出的签名，说明结论对签名定义敏感；
  若任意来源的签名都能在任意队列复现，说明现象是跨队列稳健的。

矩阵：行=签名来源队列，列=验证队列。对角线=自验证（方法检查），非对角线=跨队列复现。

用法：
  python -m pilot.cross_signature \
    --cohorts pilot/cohorts.json \
    --size 100 --min-delta 1.5 \
    --out pilot/results/cross_signature.md
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from .audit import load_matrix, load_metadata, render_markdown, run_claims, to_log2x


def valid_pairs(meta: pd.DataFrame, col: str, a: str, b: str, pair_col: str) -> list[str]:
    keys = []
    for key, grp in meta.groupby(pair_col):
        if (grp[col] == a).sum() == 1 and (grp[col] == b).sum() == 1:
            keys.append(str(key))
    return sorted(keys, key=lambda x: (len(x), x))


def load_cohort(ch: dict):
    expr = to_log2x(load_matrix(Path(ch["matrix"])), ch.get("value_type", "log"))
    meta = load_metadata(Path(ch["metadata"]))
    meta["sample_id"] = meta["sample_id"].astype(str)
    g = ch["group"]
    meta["_pair"] = meta[g["paired_by"][0]].astype(str) if len(g["paired_by"]) == 1 else meta["sample_id"]
    return expr, meta, g


def derive(ch: dict, size: int, min_delta: float) -> dict[str, list[str]]:
    expr, meta, g = load_cohort(ch)
    pair_col = g["paired_by"][0]
    keys = valid_pairs(meta, g["column"], g["a"], g["b"], pair_col)
    deltas = []
    for k in keys:
        grp = meta[meta[pair_col].astype(str) == k]
        a_id = grp[grp[g['column']] == g['a']]["sample_id"].iloc[0]
        b_id = grp[grp[g['column']] == g['b']]["sample_id"].iloc[0]
        deltas.append(expr[a_id] - expr[b_id])
    D = pd.DataFrame(deltas)
    mean_d = D.mean(axis=0)
    up = mean_d[mean_d >= min_delta].nlargest(size).index.tolist()
    down = mean_d[mean_d <= -min_delta].nsmallest(size).index.tolist()
    return {"up": up, "down": down, "n_pairs": len(keys)}


def main() -> None:
    ap = argparse.ArgumentParser(description="交叉签名矩阵")
    ap.add_argument("--cohorts", required=True)
    ap.add_argument("--size", type=int, default=100)
    ap.add_argument("--min-delta", type=float, default=1.5)
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--min-effect", type=float, default=0.5)
    ap.add_argument("--min-stable", type=float, default=0.8)
    ap.add_argument("--out", default="pilot/results/cross_signature.md")
    args = ap.parse_args()

    cohorts = json.loads(Path(args.cohorts).read_text(encoding="utf-8"))["cohorts"]
    asset = Path(args.out).parent / "cross_assets"
    asset.mkdir(parents=True, exist_ok=True)

    sigs: dict[str, dict] = {}
    for ch in cohorts:
        sigs[ch["name"]] = derive(ch, args.size, args.min_delta)
        print(f"{ch['name']}: pairs={sigs[ch['name']]['n_pairs']} "
              f"up={len(sigs[ch['name']]['up'])} down={len(sigs[ch['name']]['down'])}")

    claims = []
    for src in cohorts:
        for direction in ("up", "down"):
            genes = sigs[src["name"]][direction]
            path = asset / f"{src['name']}_{direction}.txt"
            path.write_text("\n".join(genes) + "\n", encoding="utf-8")
            for tgt in cohorts:
                claims.append({
                    "id": f"{src['name']}-{direction}->{tgt['name']}",
                    "name": f"{src['name']} {direction} -> {tgt['name']}",
                    "type": "signature",
                    "dataset": {"matrix": tgt["matrix"], "metadata": tgt["metadata"],
                                 "value_type": tgt.get("value_type", "log")},
                    "group": tgt["group"],
                    "signature": {"features_file": str(path)},
                    "alpha": args.alpha,
                    "min_effect": args.min_effect,
                    "claimed_direction": "a_gt_b" if direction == "up" else "a_lt_b",
                    "robustness": {"covariates": [], "min_stable_fraction": args.min_stable},
                })

    results = run_claims(claims)
    by_id = {r.claim_id: r for r in results}
    names = [c["name"] for c in cohorts]

    lines = ["# 交叉签名矩阵", "",
             f"> 签名规模 top-{args.size}，|delta|≥{args.min_delta}；行=签名来源队列，列=验证队列。",
             "> 对角线=自验证（方法检查，必然偏大）；非对角线=跨队列复现。", ""]
    for direction, label in (("up", "上调"), ("down", "下调")):
        lines += [f"## {label}签名", "", "| 来源 \\ 验证 | " + " | ".join(names) + " |",
                  "|---|" + "---|" * len(names)]
        for src in names:
            cells = []
            for tgt in names:
                r = by_id.get(f"{src}-{direction}->{tgt}")
                cell = f"{r.verdict} ({r.effect:+.2f})" if r else "-"
                if src == tgt:
                    cell = f"**{cell}**（自验证）"
                cells.append(cell)
            lines.append(f"| {src} | " + " | ".join(cells) + " |")
        lines.append("")

    # 非对角线复现率
    lines += ["## 非对角线复现率（跨队列）", "",
              "| 签名方向 | 复现 robust / 非对角单元数 |", "|---|---|"]
    for direction, label in (("up", "上调"), ("down", "下调")):
        ok = total = 0
        for src in names:
            for tgt in names:
                if src == tgt:
                    continue
                r = by_id.get(f"{src}-{direction}->{tgt}")
                total += 1
                if r and r.verdict == "robust":
                    ok += 1
        lines.append(f"| {label} | {ok}/{total} |")
    lines.append("")
    md = "\n".join(lines) + "\n\n" + render_markdown(results)
    outp = Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(md, encoding="utf-8")
    print(md[:1200])


if __name__ == "__main__":
    main()