# 复现审计 SOP（标准操作流程）

> 目标：给定一个"论文结论 + 原始数据"，产出**可审计、可复现、结论分级**的稳健性报告。
> 适用：两组比较类结论（肿瘤/正常、处理/对照、配对/非配对），转录组、芯片、甲基化等矩阵型数据。
> 版本：v1.0（2026-11-27）

---

## 0. 适用与不适用

| 适合 | 不适合 |
|---|---|
| 组学矩阵 + 明确分组（≥5 样本/组） | 只有汇总数据（均值/柱状图） |
| 结论可写成"X 在 A 组高于 B 组" | 生存分析、交互效应、单细胞聚类（需新模板） |
| 有配对或可调整的协变量 | 受控数据（dbGaP 等） |

---

## 1. 环境（一次性）

```bash
cd /Users/admin/Documents/DiscoveryRSI
/usr/local/bin/python3.12 -m venv .venv
.venv/bin/pip install -e ".[test]" numpy==2.2.6 pandas==2.2.3 scipy==1.15.3 \
    scikit-learn==1.6.1 statsmodels==0.14.4
.venv/bin/pytest -q          # 应显示 23 passed
```

## 2. 数据准备

### 2.1 转录组 / 计数矩阵

```
feature   S1    S2    S3
GENE1     120   98    143
GENE2     45    52    38
```

- 第一列特征 ID（基因符号或 Ensembl），其余列名=样本 ID；
- 支持 `.tsv/.csv` 及 `.gz`；
- `value_type`：`counts`（自动 log2 CPM）或 `log`（已归一化）。

### 2.2 样本元数据（design.json）

```json
[{"sample_id": "S1", "condition": "tumor", "patient": "P1", "batch": "b1"}]
```

必需：`sample_id` + 分组列；配对设计加配对列；可选协变量（batch/age/sex）。

### 2.3 芯片原始数据

```bash
python -m pilot.cli prepare-microarray \
  --series-matrix pilot/data/gseXXXXX/series_matrix.txt.gz \
  --platform-annot /tmp/gpl570.soft \
  --title-pattern 'Patient_(\d+)_(normal|cancer)' --title-groups patient,condition \
  --out-matrix pilot/data/gseXXXXX/matrix.tsv.gz \
  --out-design pilot/data/gseXXXXX/design.json
```

- 平台注释：`https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GPL570&targ=self&form=text&view=data`
- 探针→符号：同符号保留平均表达最高的探针。

### 2.4 甲基化

矩阵同 2.1（行=探针，值=beta）；缺失值按行中位数填补（本仓库脚本已内置）。

### 2.5 注册数据集（可选）

编辑 `pilot/datasets.json`，`python -m pilot.cli datasets` 可查。

---

## 3. 写 claims（**审计前锁定阈值**）

```json
{
  "claims": [{
    "id": "paper-2024-a",
    "name": "论文 A：signature X 在治疗组上调",
    "type": "signature",
    "dataset": {"matrix": "pilot/data/xxx/matrix.tsv.gz",
                 "metadata": "pilot/data/xxx/design.json",
                 "value_type": "counts"},
    "group": {"column": "condition", "a": "treated", "b": "control", "paired_by": ["patient"]},
    "signature": {"features_file": "pilot/data/xxx/signature.txt"},
    "alpha": 0.05,
    "min_effect": 0.5,
    "claimed_direction": "a_gt_b",
    "robustness": {"covariates": [], "min_stable_fraction": 0.8}
  }]
}
```

**规则**：
- `type: signature`（审计）或 `scan`（探索，不能证明结论真假）；
- `claimed_direction` 必须来自论文原文（`a_gt_b`/`a_lt_b`/`any`）；
- `alpha`/`min_effect`/`min_stable_fraction` **先定后跑**，跑完不许改，否则结论可被操纵；
- 签名来源必须写明（文献列表 / 数据集 DE / 训练集），不同来源不可比。

## 4. 运行

```bash
# 单个数据集审计
python -m pilot.cli audit --claims pilot/claims.xxx.json --out pilot/results/xxx_audit.md

# 阈值敏感性（同批主张三档 alpha）
python -m pilot.cli audit --claims pilot/claims.xxx.json --out pilot/results/xxx_audit.md --alpha-sweep 0.01,0.05,0.1

# 半样本协议（训练集选签名 → 留出集检验）
python -m pilot.cli split-half --matrix ... --metadata ... \
  --group-col condition --a tumor --b normal --pair-col patient \
  --top 100 --min-delta 1.5 --train-frac 0.5 --out pilot/results/xxx_split.md

# 多队列 × 多规模复现矩阵
python -m pilot.cli matrix --de-file pilot/data/gse50760/atlas_de.txt \
  --cohorts pilot/cohorts.json --sizes 50,100,200 --out pilot/results/replication_matrix.md

# 交叉签名矩阵（每队列自选签名互验）
python -m pilot.cli cross --cohorts pilot/cohorts.json --size 100 --out pilot/results/cross_signature.md
```

## 5. 读报告

报告结构：**方法学元数据**（检验/alpha/min_effect/min_stable）→ **审计结果**（判定+效应+p）→ **明细**（JSON）→（可选）**阈值敏感性**。

| 判定 | 含义 | 该怎么用 |
|---|---|---|
| `robust` | 主检验通过 + 留一/协变量稳健 | 可作为稳健结论使用 |
| `fragile` | 主检验通过但稳健性不足 | **不要**当结论；看 LOO 是否由少数样本驱动 |
| `not_reproduced` | 主检验未通过 | 结合效应量判断：方向对但 p 差一点 → 功效问题；方向反 → 真不复现 |
| `inconclusive` | 数据不足 | 补样本或换数据 |
| `signal_found` / `no_signal` | 仅 scan 模式 | 探索信号，不作结论 |

**必读**：效应量 > p 值。看 `effect` 与 LOO 通过率，再决定"复现失败"是方法问题还是现象问题。

## 6. 人工复核清单（10 项）

- [ ] 分组定义与论文一致？
- [ ] 配对键正确（同一患者/供体）？
- [ ] 样本量：每组 ≥5？配对 ≥5 对？
- [ ] 签名来源已注明（文献/DE/训练集）？
- [ ] 特征 ID 两侧一致（符号 vs Ensembl）？
- [ ] 平台一致或已说明（RNA-seq vs 芯片）？
- [ ] 阈值是否在跑之前锁定并写入报告？
- [ ] 判定是否给出效应量 + CI + p（不只标签）？
- [ ] LOO 结果是否解释（少数样本驱动？）
- [ ] 局限是否覆盖：批次、人群、样本量、平台？

## 7. 常见陷阱

1. **小 n + 多重校正**：9 对时 Wilcoxon 最小 p=2⁻⁹，BH 后不可能显著 → 换 t 检验或联合签名；
2. **签名来源**：同一数据选的签名自验证必然更高；只有留出集/独立队列才算复现；
3. **尺度**：beta（0–1）≠ log2FC；芯片 log2 ≠ counts；
4. **探针相关**：甲基化/芯片探针高度相关，FDR 命中数会高估独立信号；
5. **判定阈值**：alpha 0.05↔0.1 可能翻转结论——必须披露锁定值；
6. **"不稳健"≠"论文错"**：可能是方法/样本/定义差异，报告只陈述审计结果。

## 8. 复现全部结果

```bash
bash pilot/run_all.sh
```

重跑：示例审计、半样本、复现矩阵、交叉矩阵、甲基化扫描 + 全量测试，并覆盖 `pilot/results/`。

## 9. 目录结构

```
pilot/
├── cli.py                  统一入口（datasets/audit/split-half/matrix/cross/prepare-microarray）
├── audit.py                审计引擎（signature/scan、LOO、协变量、alpha sweep、方法学元数据）
├── split_half.py           半样本协议
├── replication_matrix.py   多队列 × 多规模矩阵
├── cross_signature.py      交叉签名矩阵
├── prepare_microarray.py   芯片预处理
├── datasets.json           数据集注册表
├── cohorts.json            矩阵实验的队列配置
├── claims.*.json           各实验的主张规格（锁定阈值）
├── data/                   数据（inputs/prepared/各队列）
├── results/                报告输出
├── README.md               使用指南
├── OPEN_DATA.md            开源数据目录（已验证通路）
└── SOP.md                  本文档
```

## 10. 变更记录

| 版本 | 日期 | 变更 |
|---|---|---|
| v1.0 | 2026-11-27 | 初始版本：CLI、SOP、注册表、一键复现 |
| — | — | 新增 claim 类型（生存/交互）时升级到 v1.1 |