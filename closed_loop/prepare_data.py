"""prepare_data.py — 把 ArrayExpress 原始文件转换为任务规格的 prepared 形态。

输入（closed_loop/data/inputs/）：
  MK_readcountMatrix.txt.gz       原始 counts（Geneid + 12 样本列）
  E-MTAB-8316.sdrf.txt            SDRF（样本元数据）

输出（closed_loop/data/prepared/）：
  E-MTAB-8316.counts.tsv.gz      prepared counts：第一列 feature + 样本列（规格第 3 节契约）
  E-MTAB-8316.design.json        prepared design：JSON 数组
                                  [ {sample_id, donor_id, condition, cell_type,
                                     specimen, source_metadata{...}}, ... ]

说明：任务包的 sha256（counts 9ceb4b7c...）是发布方内部的 prepared 形态哈希，我们无法精确复现
其变换细节；本脚本按规格第 3/4/5 节的行为要求自建 prepared 流程，正确性以 verifier 为判据
（见方案 v0.3 第 8 节注记）。
"""
from __future__ import annotations

import gzip
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
INPUTS = ROOT / "data" / "inputs"
PREPARED = ROOT / "data" / "prepared"

COUNTS_IN = INPUTS / "MK_readcountMatrix.txt.gz"
SDRF_IN = INPUTS / "E-MTAB-8316.sdrf.txt"
COUNTS_OUT = PREPARED / "E-MTAB-8316.counts.tsv.gz"
DESIGN_OUT = PREPARED / "E-MTAB-8316.design.json"


def prepare_counts() -> pd.DataFrame:
    df = pd.read_csv(COUNTS_IN, sep="\t", compression="gzip")
    # 规格要求第一列名为 feature
    df = df.rename(columns={df.columns[0]: "feature"})
    # 去掉全零行（featureCounts 常含大量未测到基因），保留样本列顺序
    sample_cols = [c for c in df.columns if c != "feature"]
    df = df[["feature"] + sample_cols]
    df = df[df[sample_cols].sum(axis=1) > 0]
    return df


def parse_sdrf() -> pd.DataFrame:
    sdrf = pd.read_csv(SDRF_IN, sep="\t", dtype=str)
    # SDRF 中同一 assay 的 source/assay 分列展开：按 Source Name 折叠为每样本一行
    cols = {
        "Source Name": "sample_id",
        "Characteristics[individual]": "donor_id",
        "Characteristics[specimen]": "specimen",
        "Characteristics[cell type]": "cell_type",
        "Factor Value[compound]": "condition",
    }
    samples = (
        sdrf.groupby("Source Name", sort=False)
        .agg({k: "first" for k, v in cols.items()})
        .reset_index(drop=True)
    )
    samples = samples.rename(columns=cols)
    return samples


def build_design() -> list[dict]:
    sdrf = pd.read_csv(SDRF_IN, sep="\t", dtype=str)
    rows: list[dict] = []
    seen: set[str] = set()
    for _, r in sdrf.iterrows():
        sid = str(r.get("Source Name", "")).strip()
        if not sid or sid in seen:
            continue
        seen.add(sid)
        rows.append(
            {
                "sample_id": sid,
                "donor_id": str(r.get("Characteristics[individual]", "")).strip(),
                "condition": str(r.get("Factor Value[compound]", "")).strip(),
                "cell_type": str(r.get("Characteristics[cell type]", "")).strip(),
                "specimen": str(r.get("Characteristics[specimen]", "")).strip(),
                "source_metadata": {
                    "ena_sample": str(r.get("Comment[ENA_SAMPLE]", "")).strip(),
                    "biosd_sample": str(r.get("Comment[BioSD_SAMPLE]", "")).strip(),
                    "age": str(r.get("Characteristics[age]", "")).strip(),
                    "sex": str(r.get("Characteristics[sex]", "")).strip(),
                    "disease": str(r.get("Characteristics[disease]", "")).strip(),
                    "stimulus": str(r.get("Characteristics[stimulus]", "")).strip(),
                    "organism_part": str(r.get("Characteristics[organism part]", "")).strip(),
                    "library_strategy": str(r.get("Comment[LIBRARY_STRATEGY]", "")).strip(),
                },
            }
        )
    return rows


def main() -> None:
    PREPARED.mkdir(parents=True, exist_ok=True)

    counts = prepare_counts()
    with gzip.open(COUNTS_OUT, "wt", encoding="utf-8") as f:
        counts.to_csv(f, sep="\t", index=False)
    print(f"counts  -> {COUNTS_OUT}  ({counts.shape[0]} features x {counts.shape[1]-1} samples)")

    design = build_design()
    with open(DESIGN_OUT, "w", encoding="utf-8") as f:
        json.dump(design, f, ensure_ascii=False, indent=2)
    print(f"design  -> {DESIGN_OUT}  ({len(design)} samples)")

    # 诊断
    cond_counts = {}
    donors = set()
    for d in design:
        cond_counts[d["condition"]] = cond_counts.get(d["condition"], 0) + 1
        donors.add(d["donor_id"])
    print("conditions:", cond_counts)
    print("donors:", sorted(donors))
    print("sample_ids:", [d["sample_id"] for d in design])


if __name__ == "__main__":
    main()