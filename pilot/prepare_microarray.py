"""prepare_microarray.py — 芯片数据通用预处理。

输入：
  --series-matrix  GEO series matrix（含探针 × 样本表达值 + !Sample_title）
  --platform-annot GPL 平台注释（SOFT 文本，含 Gene Symbol 列）
  --title-pattern  从 !Sample_title 提取样本属性的正则（如 'Patient_(\\d+)_(normal|cancer)')
  --title-groups   对应分组名（如 'patient,condition'）

输出：
  --out-matrix     基因符号 × 样本 矩阵（log2 值，同符号取最大平均表达探针）
  --out-design     每个样本一行：sample_id + 提取的属性

用法：
  python -m pilot.prepare_microarray \
    --series-matrix pilot/data/gse110224/series_matrix.txt.gz \
    --platform-annot /tmp/gpl570.soft \
    --title-pattern 'Patient_(\d+)_(normal|cancer)' --title-groups patient,condition \
    --out-matrix pilot/data/gse110224/matrix.tsv.gz \
    --out-design pilot/data/gse110224/design.json
"""
from __future__ import annotations

import argparse
import gzip
import json
import re
from io import StringIO
from pathlib import Path

import numpy as np
import pandas as pd


def _open_text(path: Path):
    if str(path).endswith(".gz"):
        return gzip.open(path, "rt", encoding="utf-8", errors="ignore")
    return open(path, "r", encoding="utf-8", errors="ignore")


def read_series_matrix(path: Path) -> tuple[pd.DataFrame, list[str]]:
    """返回 (探针 × 样本 表达表, 样本标题列表)。"""
    lines = []
    titles: list[str] = []
    in_table = False
    with _open_text(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("!Sample_title"):
                titles = [x.strip('"') for x in line.split("\t")[1:]]
            if line.startswith("!series_matrix_table_begin"):
                in_table = True
                continue
            if line.startswith("!series_matrix_table_end"):
                break
            if in_table:
                lines.append(line)
    if not lines:
        raise ValueError("series matrix 中没有表达表（可能只有元数据）")
    df = pd.read_csv(StringIO("\n".join(lines)), sep="\t", index_col=0)
    df.index = df.index.astype(str)
    df = df.apply(pd.to_numeric, errors="coerce")
    return df, titles


def read_platform_symbols(annot_path: Path) -> dict[str, str]:
    """从 GPL SOFT 文本解析 探针ID → 基因符号。"""
    with _open_text(annot_path) as f:
        lines = f.readlines()
    header_idx = None
    for i, line in enumerate(lines):
        if line.startswith("!platform_table_begin"):
            header_idx = i + 1
            break
    if header_idx is None:
        raise ValueError("找不到 !platform_table_begin")
    header = lines[header_idx].rstrip("\n").split("\t")
    if "Gene Symbol" not in header:
        raise ValueError("注释表缺少 Gene Symbol 列")
    sym_col = header.index("Gene Symbol")
    id_col = header.index("ID")
    mapping: dict[str, str] = {}
    for line in lines[header_idx + 1:]:
        if line.startswith("!platform_table_end"):
            break
        parts = line.rstrip("\n").split("\t")
        if len(parts) <= max(sym_col, id_col):
            continue
        probe, sym = parts[id_col].strip(), parts[sym_col].strip()
        if not probe or not sym:
            continue
        # 多符号用 /// 分隔，取第一个
        mapping[probe] = sym.split("///")[0].strip()
    return mapping


def main() -> None:
    ap = argparse.ArgumentParser(description="芯片数据预处理")
    ap.add_argument("--series-matrix", required=True)
    ap.add_argument("--platform-annot", required=True)
    ap.add_argument("--title-pattern", required=True)
    ap.add_argument("--title-groups", required=True)
    ap.add_argument("--out-matrix", required=True)
    ap.add_argument("--out-design", required=True)
    args = ap.parse_args()

    expr, titles = read_series_matrix(Path(args.series_matrix))
    mapping = read_platform_symbols(Path(args.platform_annot))
    groups = [g.strip() for g in args.title_groups.split(",")]
    pattern = re.compile(args.title_pattern)

    print(f"probes x samples: {expr.shape}; titles: {len(titles)}; mapping: {len(mapping)}")
    if len(titles) != expr.shape[1]:
        raise SystemExit("样本标题数与表达表列数不一致")

    # 探针 → 符号；同符号保留平均表达最高的探针
    probe_sym = [mapping.get(p, "") for p in expr.index]
    keep = [i for i, s in enumerate(probe_sym) if s]
    expr2 = expr.iloc[keep].copy()
    expr2.index = [probe_sym[i] for i in keep]
    expr2["_mean"] = expr2.mean(axis=1)
    expr2 = expr2.sort_values("_mean", ascending=False).drop_duplicates(keep="first").drop(columns="_mean")
    expr2.index.name = "feature"
    expr2.to_csv(args.out_matrix, sep="\t", compression="gzip")
    print(f"mapped matrix: {expr2.shape}")

    design = []
    for j, title in enumerate(titles):
        m = pattern.search(title)
        rec = {"sample_id": str(expr.columns[j])}
        for gi, gname in enumerate(groups):
            rec[gname] = m.group(gi + 1) if m else None
        design.append(rec)
    Path(args.out_design).write_text(json.dumps(design, ensure_ascii=False, indent=1), encoding="utf-8")
    from collections import Counter
    for gname in groups:
        print(gname, Counter(d[gname] for d in design))
    print("design ->", args.out_design)


if __name__ == "__main__":
    main()