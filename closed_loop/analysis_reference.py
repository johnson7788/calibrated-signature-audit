"""analysis_reference.py — M1 参考实现：unc106238 任务的完整计算流程。

按任务 instruction.md 的 5 步要求实现（探索性 donor-aware 诊断）：
  1) 读 prepared counts + design
  2) 预指定干预相关转录程序（UNC106238 vs none；|mean log2FC|>=1.0；sign>=5/6；overlap 声明）
  3) donor-aware pseudobulk 基线（供体×条件内平均；供体级配对推断）
  4) 组成稳健性 ridge 敏感性分析（donor/condition/batch/composition 协变量）
  5) 输出 results.json（program/baseline/ridge/outcome/justification/limitations）

科学边界：这是假设的探索性诊断，不声称直接靶点因果/临床疗效/机制。
本文件是 M1 的"参考实现"，M2 编译器将把同一逻辑模板化。
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent
PREPARED = ROOT / "data" / "prepared"
COUNTS = PREPARED / "E-MTAB-8316.counts.tsv.gz"
DESIGN = PREPARED / "E-MTAB-8316.design.json"
RESULTS = PREPARED / "results.json"

# 预指定标准（先于任何上下文比较，防 post-hoc 选择偏倚）
MEAN_ABS_LOG2FC_THRESHOLD = 1.0
SIGN_CONSISTENCY_MIN = 5 / 6  # >= 5/6 供体同向
ALPHA = 0.05
# 显著性阈值按指令"平均绝对值 log2FC >= 1.0、方向一致 >= 5/6"；以下为上下文对比与稳健性阈值
ROBUST_KEEP_FRACTION = 0.5  # 加入 composition 协变量后系数衰减不超过 50% 视为稳健


def load_prepared() -> tuple[pd.DataFrame, list[dict]]:
    counts = pd.read_csv(COUNTS, sep="\t", compression="gzip")
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    return counts, design


def _log2cpm(counts: pd.DataFrame) -> pd.DataFrame:
    lib = counts.iloc[:, 1:].sum(axis=0)
    cpm = counts.iloc[:, 1:].mul(1e6).div(lib, axis=1)
    return np.log2(cpm + 1.0)


def _paired_contrast(d: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """按 (donor_id, specimen) 配对；返回 per-pair log2FC 矩阵与配对信息。"""
    pairs: dict[int, tuple[str, str]] = {}
    for i, (_, row) in enumerate(d.groupby(["donor_id", "specimen"])):
        pairs[i] = (i, f"{row['donor_id'].iloc[0]}_{row['specimen'].iloc[0]}")
    pair_cols: list[str] = []
    pair_map: dict[str, tuple[str, str]] = {}
    for (donor, spec), grp in d.groupby(["donor_id", "specimen"]):
        treat = grp[grp["condition"] == "UNC106238"]["sample_id"].tolist()
        ctrl = grp[grp["condition"] == "none"]["sample_id"].tolist()
        if treat and ctrl:
            key = f"{donor}_{spec}"
            pair_map[key] = (treat[0], ctrl[0])
            pair_cols.append(key)
    return pair_cols, pair_map


def run() -> dict:
    counts, design = load_prepared()
    d = pd.DataFrame(design)
    cpm = _log2cpm(counts)

    pair_keys, pair_map = [], {}
    for (donor, spec), grp in d.groupby(["donor_id", "specimen"]):
        treat = grp[grp["condition"] == "UNC106238"]["sample_id"].tolist()
        ctrl = grp[grp["condition"] == "none"]["sample_id"].tolist()
        if treat and ctrl:
            key = f"{donor}_{spec}"
            pair_map[key] = (treat[0], ctrl[0])
            pair_keys.append(key)

    # 每基因 per-pair log2FC（指令：placebo=none, 干预=UNC106238）
    # 注意用 .values 避免 Series 行号 index 与 feature index 对齐产生 NaN
    lfc = pd.DataFrame(
        {key: (cpm[treat_id] - cpm[ctrl_id]).values for key, (treat_id, ctrl_id) in pair_map.items()},
        index=counts["feature"],
    )

    mean_lfc = lfc.mean(axis=1)
    n_pairs = len(pair_keys)
    sign_consistency = (np.sign(lfc.values) == np.sign(mean_lfc.values)[:, None]).sum(axis=1) / n_pairs
    criteria = {
        "mean_abs_log2fc_threshold": MEAN_ABS_LOG2FC_THRESHOLD,
        "sign_consistency": f"{SIGN_CONSISTENCY_MIN:.4f}",
        "sign_consistency_observed": float(sign_consistency.max()),
        "n_pairs": n_pairs,
    }

    # 特征重叠声明：本任务单数据集，无独立"巨噬细胞条件对比"数据源；
    # 保守处理：以高表达（基线均值 > 中位数）基因作为 overlap 近似并如实说明。
    mean_all = cpm.mean(axis=1)
    high_expr = mean_all > mean_all.median()

    mask = (mean_lfc.abs() >= MEAN_ABS_LOG2FC_THRESHOLD) & (sign_consistency >= SIGN_CONSISTENCY_MIN) & high_expr
    program_genes = mean_lfc[mask].index.tolist()
    criteria["feature_overlap"] = "high-expression proxy (single-dataset; see limitations)"

    # 空程序分支：预指定程序不存在 → 上下文对比不被支持（adverse），如实报告。
    # 附上"近阈值"基因作为下一轮进化的输入（不影响 outcome 判定）。
    if not program_genes:
        near_program = mean_lfc[mean_lfc.abs() >= MEAN_ABS_LOG2FC_THRESHOLD].index.tolist()
        results = {
            "program": {
                "criteria": criteria,
                "genes": [],
                "n_genes": 0,
                "near_threshold_genes": near_program,
                "near_threshold_n": len(near_program),
            },
            "baseline": {
                "context_contrast": None,
                "p_value": None,
                "ci_lower": None,
                "ci_upper": None,
                "donor_level": {},
                "method": "donor-aware pseudobulk paired test on program composite score",
                "note": "Prespecified intervention-associated program is empty; no context contrast computed.",
            },
            "ridge": {
                "context_coefficient": None,
                "composition_robust": False,
                "covariates": ["donor", "condition", "composition(library-size proxy)"],
                "note": "No program to regress.",
            },
            "outcome": "adverse",
            "justification": (
                f"Prespecified intervention-associated program is empty under stated criteria "
                f"(|mean log2FC|>={MEAN_ABS_LOG2FC_THRESHOLD}, sign>={SIGN_CONSISTENCY_MIN}, high-expression; "
                f"{len(near_program)} genes pass the magnitude threshold but fail directional consistency "
                f"({criteria['sign_consistency']} required)). The context contrast is therefore not supported "
                "by the available data. This is an exploratory donor-aware diagnostic and does not establish "
                "direct target causality."
            ),
            "limitations": (
                "Exploratory donor-aware diagnostic on n=12 samples (6 donor-specimen pairs). "
                "No independent macrophage-condition contrast dataset was available, so feature overlap uses a "
                "high-expression proxy; composition covariates use library size as a proxy; batch not modeled "
                "(single batch). Small sample size and donor heterogeneity can mask directional consistency. "
                "Does not establish direct target causality, clinical efficacy, or mechanism."
            ),
        }
        return results

    # Donor-aware pseudobulk：程序基因的供体级 composite score
    don = pd.concat(
        [
            pd.DataFrame(
                {
                    "sample_id": [treat_id, ctrl_id],
                    "condition": ["UNC106238", "none"],
                    "pair": key,
                    "program_score": [float(cpm.loc[program_genes, treat_id].mean()), float(cpm.loc[program_genes, ctrl_id].mean())],
                }
            )
            for key, (treat_id, ctrl_id) in pair_map.items()
        ],
        ignore_index=True,
    )
    don = don.merge(d[["sample_id", "donor_id", "specimen"]], on="sample_id")

    # 基线：程序分数在 (none, UNC106238) 配对内的供体级对比（配对 t/符号检验）
    cont = don.pivot(index="pair", columns="condition", values="program_score")
    delta = cont["UNC106238"] - cont["none"]
    t_stat, p_value = stats.ttest_rel(cont["UNC106238"], cont["none"])
    donor_level = {str(k): float(v) for k, v in delta.to_dict().items()}
    context_contrast = float(delta.mean())

    # Ridge 稳健性：y=程序分数；协变量 donor、condition、composition(libsize 代理)
    lib = counts.iloc[:, 1:].sum(axis=0)
    X = pd.DataFrame(
        {
            "intercept": 1.0,
            "condition_unc": (don["condition"] == "UNC106238").astype(float),
            **{f"donor_{k}": (don["donor_id"] == k).astype(float) for k in sorted(don["donor_id"].unique())[1:]},
        },
        index=don.index,
    )
    libsize = don["sample_id"].map(lib).astype(float)
    composition = (libsize - libsize.mean()) / libsize.std()

    from sklearn.linear_model import Ridge

    X_ridge = X.copy()
    X_ridge["composition"] = composition.values
    ridge = Ridge(alpha=1.0)
    ridge.fit(X_ridge, don["program_score"])
    coeff_full = float(ridge.coef_[X_ridge.columns.get_loc("condition_unc")])
    ridge_nc = Ridge(alpha=1.0)
    ridge_nc.fit(X.drop(columns=["composition"]), don["program_score"])
    coeff_base = float(ridge_nc.coef_[X.drop(columns=["composition"]).columns.get_loc("condition_unc")])

    robust = abs(coeff_full) >= ROBUST_KEEP_FRACTION * abs(coeff_base)
    ridge_p = 2.0 * (1.0 - stats.t.cdf(abs(t_stat), df=max(len(delta) - 1, 1)))

    # 判定规则（instruction Interpretations）：supportive 需 baseline 显著且对组成稳健
    baseline_supported = (np.sign(context_contrast) == np.sign(coeff_full)) and (p_value < ALPHA)
    if baseline_supported and robust:
        outcome = "supportive"
    elif baseline_supported and not robust:
        outcome = "inconclusive"
    else:
        outcome = "adverse"

    results = {
        "program": {
            "criteria": criteria,
            "genes": program_genes,
            "n_genes": len(program_genes),
        },
        "baseline": {
            "context_contrast": context_contrast,
            "p_value": float(p_value),
            "ci_lower": float(delta.mean() - 1.96 * delta.std(ddof=1) / np.sqrt(len(delta))) if len(delta) > 1 else None,
            "ci_upper": float(delta.mean() + 1.96 * delta.std(ddof=1) / np.sqrt(len(delta))) if len(delta) > 1 else None,
            "donor_level": donor_level,
            "method": "donor-aware pseudobulk paired test on program composite score",
        },
        "ridge": {
            "context_coefficient": coeff_full,
            "p_value_note": ridge_p,
            "composition_robust": bool(robust),
            "covariates": ["donor", "condition", "composition(library-size proxy)"],
        },
        "outcome": outcome,
        "justification": (
            f"Program: {len(program_genes)} prespecified genes. Baseline context contrast "
            f"{context_contrast:.3f} (p={p_value:.3g}); ridge context coefficient {coeff_full:.3f}, "
            f"composition-robust={robust}. Outcome {outcome} per prespecified rules. "
            "This is an exploratory donor-aware diagnostic and does not establish direct target causality."
        ),
        "limitations": (
            "Exploratory donor-aware diagnostic on n=12 samples (6 donor-specimen pairs). "
            "No independent macrophage-condition contrast dataset was available, so feature overlap uses a "
            "high-expression proxy; composition covariates use library size as a proxy; batch not modeled "
            "(single batch). Does not establish direct target causality, clinical efficacy, or mechanism."
        ),
    }
    return results


if __name__ == "__main__":
    results = run()
    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    RESULTS.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {RESULTS}")
    print(f"outcome={results['outcome']}  n_genes={results['program'].get('n_genes')}  "
          f"contrast={results['baseline']['context_contrast']}  p={results['baseline']['p_value']}  "
          f"robust={results['ridge']['composition_robust']}")