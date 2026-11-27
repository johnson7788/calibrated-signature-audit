# 复现审计试点工具箱

> 目的：拿你自己的组学矩阵（转录组/蛋白组/代谢组），批量复核"论文结论在我的数据上是否稳健"。
> 当前状态：引擎已可在示例数据上运行；你提供数据后即可接入。
> 📖 名词看不懂？先读 **[GLOSSARY.md](GLOSSARY.md)**（GEO/FPKM/signature/FDR/配对设计等）。


## 快速开始（5 分钟）

```bash
# 0) 环境自检
.venv/bin/pytest -q                     # 23 passed

# 1) 看已注册数据集
python -m pilot.cli datasets

# 2) 审计一组主张（示例：GSE50760 上下调签名）
python -m pilot.cli audit --claims pilot/claims.gse50760.json --out /tmp/report.md

# 3) 一键重跑全部已发布结果（约 30 秒）
bash pilot/run_all.sh
```

- 完整操作手册：**[SOP.md](SOP.md)**
- 报告输出：`pilot/results/`
- 术语不懂：**[GLOSSARY.md](GLOSSARY.md)**

## 1. 你需要准备什么

每个"主张"（论文里的一条主结论）对应三样东西：

### ① 表达矩阵（`matrix`）

```
feature     S1      S2      S3   ...
ENSG0001    120     98      143  ...
ENSG0002    45      52      38   ...
```

- 第一列为特征 ID（基因/蛋白 ID），其余列名为样本 ID；
- 支持 `.tsv` / `.csv` / `.tsv.gz` / `.csv.gz`；
- `value_type`：`counts`（引擎自动做 log2 CPM）或 `log`（已归一化则原样使用）。

### ② 样本元数据（`metadata`）

JSON 数组或 CSV，至少包含：

| 列 | 必需 | 说明 |
|---|---|---|
| `sample_id` | ✅ | 与矩阵列名一一对应 |
| `condition`（或你的分组列名） | ✅ | 两组比较的分组变量 |
| `donor_id` / `specimen`（或配对键列） | 配对设计时 ✅ | 配对比较用 |
| 协变量（batch、age、sex…） | 可选 | 稳健性检查用 |

示例：

```json
[
  {"sample_id": "S1", "condition": "treated", "donor_id": "D1", "batch": "b1", "age": 68},
  {"sample_id": "S2", "condition": "control", "donor_id": "D1", "batch": "b1", "age": 68}
]
```

### ③ 主张规格（`claims.json`）

```json
{
  "claims": [
    {
      "id": "paper-2024-a",
      "name": "论文 A 主结论：signature X 在治疗组上调",
      "type": "signature",
      "dataset": {
        "matrix": "my_data/counts.tsv.gz",
        "metadata": "my_data/design.json",
        "value_type": "counts"
      },
      "group": {
        "column": "condition",
        "a": "treated",
        "b": "control",
        "paired_by": ["donor_id"]
      },
      "signature": {
        "features_file": "my_data/signature_X.txt"
      },
      "alpha": 0.05,
      "min_effect": 0.2,
      "claimed_direction": "a_gt_b",
      "robustness": {
        "covariates": ["batch"],
        "min_stable_fraction": 0.8
      }
    }
  ]
}
```

- `type: "signature"`：**审计模式**，检验给定特征集合的组间差异（论文结论复核用）；
- `type: "scan"`：**探索模式**，全特征扫描（看看数据里有没有信号，不能证明结论真假）；
- `claimed_direction`：`a_gt_b` / `a_lt_b` / `any`（论文声称的方向，用于检验方向是否复现）；
- `robustness.covariates`：加入回归的协变量（如 `batch`）；
- `min_stable_fraction`：留一法（逐个剔配对）检验中，通过比例的下限。

## 2. 运行

```bash
cd /Users/admin/Documents/DiscoveryRSI
.venv/bin/python -m pilot.audit --claims pilot/claims.example.json --out pilot/results/audit.md
```

输出（`audit.md`）：

| 判定 | 含义 |
|---|---|
| **robust** | 主检验通过 + 稳健性达标（换一个配对、加协变量都还成立） |
| **fragile** | 主检验通过，但稳健性不达标（结论依赖特定样本/未调整的协变量） |
| **not_reproduced** | 主检验未通过（方向不对、不显著或效应太小） |
| **inconclusive** | 数据不足（配对不够、特征缺失） |

## 3. 示例运行结果（E-MTAB-8316 真实数据）

- `demo-scan`（全特征扫描）：**no_signal**——FDR<0.05 且 |效应|≥1.0 的基因数为 0，方向一致性中位数 0.5 → 这份数据在配对设计下无强信号；
- `demo-sig-neg`（随机 50 基因负向对照）：**not_reproduced**——留一法通过率 0.0，引擎正确拒绝假签名。

> 统计口径：scan 模式用**向量化配对 t 检验 / Welch t 检验**（2 万基因毫秒级）；signature 模式用 **Wilcoxon 符号秩检验**（调用次数少）。所有判定细节里的检验方法、配对键、阈值都会记录在 `details` 中——审计报告必须能复现方法。

## 4. 已验证的真实案例

| 案例 | 内容 | 结论 | 报告 |
|---|---|---|---|
| GSE50760（结直肠癌，18 患者 × 3 部位） | 从 BioStudies 抓 54 个 FPKM 文件 → 拼矩阵 → 审计 Atlas DE 签名 + 半样本验证 | 上下调签名均 robust；半样本泛化 robust | `pilot/results/gse50760_summary.md` |
| GSE95132（独立队列，12 患者配对） | 跨研究复现 GSE50760 签名 | 上调 robust（p=5e-4）；下调 not_reproduced（p=0.052，留一通过率 0） | `pilot/results/crossstudy_summary.md` |
| 阈值敏感性 | 同一签名在 alpha=0.01/0.05/0.1 下的判定 | 0.05→0.1 变 fragile，但 LOO=0 说明结构不稳定 | `pilot/results/alpha_sensitivity.md` |
| 复现矩阵（3 队列 × 3 规模） | GSE50760 签名 → GSE95132 / GSE110224 | **18/18 判定 robust**；效应量随规模增大而衰减 | `pilot/results/replication_matrix.md` |
| 交叉签名矩阵 | 每队列自选签名 → 互相验证 | 上调 6/6 复现；下调 5/6（GSE50760→GSE95132 脆弱） | `pilot/results/cross_signature.md` |
| 跨组学（甲基化） | GSE48684 450K：CRC/腺瘤 vs 正常 | 引擎可直接迁移；CRC vs 癌旁 78,552 个差异位点 | `pilot/results/methylation_summary.md` |

**核心方法论**：证据三级阶梯——L1 同数据换方法（方法敏感性）→ L2 半样本（跨患者泛化）→ L3 独立队列（跨研究复现）。跨队列复现才是"结论稳健"的强证据。

## 5. 两周试点计划

| 阶段 | 内容 | 产出 |
|---|---|---|
| 第 1–2 天 | 你提供 5–10 个"数据齐全 + 主结论明确"的论文对（矩阵+元数据+结论描述） | 数据清单 |
| 第 3–5 天 | 把结论转成 claims.json；跑审计；手动校验 1–2 个结果的合理性 | 首版审计表 |
| 第 6–9 天 | 迭代：补协变量、调判定规则、处理问题数据 | 稳定版审计表 |
| 第 10–14 天 | 汇总"哪些结论脆弱、脆弱在哪"；评估每篇耗时与瓶颈 | 试点报告 + 是否投入的结论 |

**试点成功标志**：能拿着审计表说"这 N 篇的结论在我的重跑下变脆弱，原因是 X（如：去掉一个供体就消失 / 未调整 batch）"。

**试点失败标志**（同样有价值）：数据格式清洗成本过高、或绝大多数论文没有可复现的"明确主结论"——那说明这条路暂时不值得投入，及早止损。

## 6. 边界（务必知道）

1. 审计回答的是"**在给定数据 + 给定判定规则下，主张是否成立**"，不是"主张是否为真"；
2. 规则由人定：`alpha`、`min_effect`、`min_stable_fraction` 都能改变判定，需在审计前锁定并记录；
3. scan 模式是探索不是审计——用 scan 找到的信号再去"验证"自己是循环论证；
4. n 太小的数据集（如配对 < 4 组）基本无法做稳健性判断，会返回 inconclusive；
5. 特征 ID 必须两侧一致（矩阵与签名文件）；跨平台（如芯片 vs RNA-seq）需先做 ID 映射。