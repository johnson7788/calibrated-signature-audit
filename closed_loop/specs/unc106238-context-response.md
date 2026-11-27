# 任务规格书：unc106238-context-response

> 来源：`datasets/DiscoveryRSI-Hypothesis-Task-Examples/task-packages/DiscoveryRSI-Hypothesis-Task-Examples/tasks/unc106238-context-response/`
> 用途：本文件是"编译器的目标 schema"（M0/M1 地基）。所有字段/规则均从任务包原始文件逐字核对。
> 科学地位提醒：**这是一个假设的探索性诊断，不是已确立的发现**；本规格只描述"怎么算、怎么判、怎么防过度声称"，不声称任何生物学结论。

---

## 1. 元信息（provenance.json）

| 项 | 值 |
|---|---|
| candidate_id | `candidate-10c868bb758e34c115eeefcf` |
| 领域 | `therapeutic_targets` |
| generation / parent | generation 3，父候选 `candidate-795608ea6a966b991c2abbcd` |
| 来源战役 | `raft-final-v2-300-20261016` |
| 任务名 | `context-dependent-unc106238-transcript-response`（task.toml schema_version 1.4） |
| 公开版调整 | 私有路径→可移植输入引用；私有镜像→公开 Python 示例镜像；**科学措辞与 verifier 逻辑保留** |
| fixture 校验状态 | 4/4 通过（positive→1；overclaim/missing_ridge/stale→0），但 `full_scientific_execution_performed_for_release: false` |
| 运行资源基线 | 2 CPU / 0 GPU / 8GB 内存 |

## 2. 科学问题与主张边界（hypothesis.md + instruction.md）

- **科学问题**：干预（UNC106238）相关的转录响应，其幅度/方向是否在"含巨噬细胞 vs 无巨噬细胞"的成纤维细胞上下文间有差异，且**不能用供体、条件、批次或样本组成的差异解释**。
- **已支持的最强主张**（仅此）：E-MTAB-8316 含 donor-aware 巨噬细胞条件对比——6 个单核细胞供体（嵌套在 4 个 FLS 供体簇内）、`none` vs `UNC106238` 两种条件、共 12 个条件样本。
- **未决主张（可证伪）**：上下文对比不被供体/条件/批次/组成差异解释。
- **明确的边界**：这是探索性 donor-aware 诊断；**不断言直接靶点因果、临床疗效或机制**。supporter 也必须带 `limitations` 声明。

## 3. 数据契约（bindings.json + input-requirements.json）

| 文件 | 绑定(target) | sha256 | 格式 |
|---|---|---|---|
| `E-MTAB-8316.counts.tsv.gz` | `/data/prepared/E-MTAB-8316.counts.tsv.gz/E-MTAB-8316.counts.tsv.gz` | `9ceb4b7c...b219645` | gzip TSV：`feature` 列 + 样本列（如 `MK11`） |
| `E-MTAB-8316.design.json` | `/data/prepared/E-MTAB-8316.design.json/E-MTAB-8316.design.json` | `ca011580...4c04c81` | JSON 样本元数据列表 |

- design 记录字段：`sample_id`、`donor_id`、`condition`、`cell_type`、`source_metadata`；counts 样本列按 `sample_id` 连接。
- 来源：ArrayExpress [E-MTAB-8316](https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-8316)（`included: false`，数据需自备）。
- 本地映射建议（本方案本机版）：实际文件放 `closed_loop/data/inputs/`，脚本内以相对绑定解析。

## 4. 分析规格（instruction.md 的要求，可直接实现）

1. **读数据**：按精确绑定读 counts + design。
2. **预指定干预相关转录程序（先于任何上下文比较，防 post-hoc 选择偏倚）**，用 UNC106238 vs none 对比：
   - 六个单核细胞供体的 `|mean log2 fold change| >= 1.0`；
   - 方向一致性 `>= 5/6` 供体；
   - 与巨噬细胞条件对比的 feature 重叠（共享基因标识符）。
3. **donor-aware pseudobulk 基线**：供体×条件内对重复上下文测量取均值，再做供体级探索性推断（巨噬细胞存在 vs 缺失对比）。
4. **组成稳健性敏感性分析**：ridge 回归，协变量含 donor、condition、batch、sample-composition（**敏感性分析，非因果模型**）。
5. **输出**：上下文对比、不确定性、供体级模式、是否对组成差异稳健；按声明标准报告 supportive / adverse / inconclusive。

## 5. 输出契约（results.json，verifier 检查的精确 schema）

```jsonc
{
  "program": {          // 必填
    "criteria": {       // 必填（预指定标准，如 mean_abs_log2fc_threshold, sign_consistency, feature_overlap）
      "mean_abs_log2fc_threshold": 1.0,
      "sign_consistency": "5/6",
      "feature_overlap": "macrophage-condition contrast"
    },
    "genes": ["GENE1", "GENE2"]        // 必填
  },
  "baseline": {         // 必填
    "context_contrast": 0.5,           // 必填
    "ci_lower": 0.1, "ci_upper": 0.9,  // 建议（positive fixture 含）
    "donor_level": {"SA114": 0.4, "SA115": 0.6}  // 建议
  },
  "ridge": {            // 必填
    "context_coefficient": 0.45,       // 必填
    "p_value": 0.03,                   // 建议
    "composition_robust": true         // 必填
  },
  "outcome": "supportive",             // 必填 ∈ {supportive, adverse, inconclusive}
  "justification": "…不与直接靶点因果相冲突的措辞…",  // 必填、非空
  "limitations": "Exploratory donor-aware diagnostic; does not establish direct target causality."  // 必填、非空
}
```

## 6. 验证契约（tests/test.sh = verifier，逐条）

| # | 检查 | 失败即 reward=0 |
|---|---|---|
| 1 | `results.json` 存在且可解析 | 缺失/解析失败 |
| 2 | 顶层键 `program, baseline, ridge, outcome, limitations` 齐全 | 缺任一 |
| 3 | `outcome ∈ {supportive, adverse, inconclusive}` | 非法值 |
| 4 | `program` 是 dict 且含 `criteria`、`genes` | 缺 |
| 5 | `baseline` 是 dict 且含 `context_contrast` | 缺 |
| 6 | `ridge` 是 dict 且含 `context_coefficient`、`composition_robust` | 缺 |
| 7 | `limitations` 为非空字符串 | 空/非字符串 |
| 8 | **防过度声称**：`outcome=supportive` 时 `ridge.composition_robust` 必须为 True | 不一致 |
| 9 | `justification` 为非空字符串 | 空 |
| 10 | **防过度声称**：justification 不含 `"causality is established"`；含 `"direct target causality"` 时必须同时含 `"does not"` | 违规 |

- verifier 输出：`/logs/verifier/reward.txt` 写 `0` 或 `1`，进程恒 exit 0。

## 7. 判定规则（instruction.md "Interpretation rules"）

- **supportive** = 上下文对比受数据支持，且对 donor/condition/batch/composition 差异稳健（ridge 结果 `composition_robust: true` 是必要条件之一）。
- **adverse** = 对比不受支持，或由 donor/condition/batch/composition 差异驱动。
- **inconclusive** = 对比对组成差异不稳健，或数据不足以区分主主张与其最强竞争解释。
- 注意：verifier 的 1/0 只验证"输出格式合规 + 自洽"，**不验证科学正确性**；`outcome` 的判定由分析代码按上述规则产生，verifier 只做一致性约束（规则 8 实际上约束了 `outcome=supportive` 必须配 `composition_robust=true`）。

## 8. 运行环境（Dockerfile 规定版本）

`python:3.11-slim-bookworm` + `numpy==2.2.6 pandas==2.2.3 scipy==1.15.3 scikit-learn==1.6.1 statsmodels==0.14.4`；工作目录 `/workspace`。
本机 venv 等效（Python 3.12 需验证与这些 pinned 版本兼容；必要时在 spec 的 venv 内锁同版本）。

## 9. fixture 对照（M1 对齐用）

| fixture | 写入的 results.json 关键特征 | 期望 reward |
|---|---|---|
| `positive_fixture.sh` | 完整 schema + `outcome=supportive` + `composition_robust=True` + 合规措辞 | 1 |
| `overclaim_fixture.sh` | justification 含 `"Direct target causality is established."` + limitations 空 | 0 |
| `missing_ridge_fixture.sh` | 缺 `ridge` 键 | 0 |
| `stale_result_fixture.sh` | `outcome=supportive` 但 `composition_robust=False` | 0 |

**M1 验收**：用本机执行的等价 verifier，4 个 fixture 必须得到 1/0/0/0；随后参考实现（真实数据计算）也必须通过。若两者之一不符，先修环境/路径问题，不许跳过。