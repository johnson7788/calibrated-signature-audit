# 术语表（Glossary）

> 配合 `pilot/` 复现审计引擎与 `closed_loop/` 可执行闭环使用。
> 每条尽量给出"一句话定义 + 本项目中的实例"，便于读报告时对照。

---

## 一、数据库与编号

| 术语 | 定义 | 本项目实例 |
|---|---|---|
| **GEO** | Gene Expression Omnibus，NCBI 的公共基因表达数据库（芯片/测序），论文常被要求在此存档 | 本次数据源头 GSE50760 |
| **GSE** | GEO Series：一个研究/数据集的编号 | GSE50760（18 患者 × 3 部位） |
| **GSM** | GEO Sample：单个样本编号 | GSM1228184 等 54 个 |
| **ArrayExpress** | EBI 的表达数据库，编号形如 `E-MTAB-xxxx` | E-MTAB-8316（已接入闭环项目） |
| **BioStudies** | EBI 统一数据平台，存放 ArrayExpress 迁移数据及 GEO 镜像（`E-GEOD-xxxx`） | 54 个 FPKM 文件的实际下载源 |
| **Expression Atlas** | EBI 的"策划版"表达数据库：人工筛选实验、统一重算差异表达、提供标准下载 | `atlas_de.txt`（论文声称）来源 |
| **SRA / ENA** | 原始测序读段存档（美国 NCBI / 欧洲 EBI），存 fastq | 本次未用（用了作者上传的 processed 文件） |
| **PRIDE** | 蛋白组数据存档，编号形如 `PXDxxxxxx` | 待扩展 |
| **MetaboLights** | 代谢组数据存档，编号形如 `MTBLSxxxx` | 待扩展 |

## 二、文件与格式

| 术语 | 定义 | 本项目实例 |
|---|---|---|
| **series matrix** | GEO 每系列的汇总文件：上半是样本元数据，下半是表达矩阵 | GSE50760 的该文件**表达值部分为空**，只用于解析元数据 |
| **SDRF** | Sample and Data Relationship Format，样本↔数据对应表（MAGE-TAB 标准），一行一样本 | E-MTAB-8316 的 design 由其转换 |
| **IDF** | Investigation Design Format，实验设计描述文件 | 出处凭证，未直接解析 |
| **processed data** | 作者或数据库加工后的数据（表达矩阵、FPKM 表等），相对"原始 fastq" | 54 个 `*_FPKM.txt` |
| **raw data** | 未加工的原始测序读段（fastq） | 本次不使用 |

## 三、表达值尺度

| 术语 | 定义 | 适用场景 |
|---|---|---|
| **counts** | 原始读数（整数），未归一化 | 差异分析（DESeq2/edgeR），本项目引擎自动转 log2 CPM |
| **CPM** | Counts Per Million：仅按测序深度归一化 | 快速比较，不校正基因长度 |
| **FPKM** | Fragments Per Kilobase per Million：按基因长度+深度归一化 | 同基因跨样本可比；**不可直接跨基因比** |
| **TPM** | Transcripts Per Million：长度校正后总和归一 | 跨基因、跨样本可比 |
| **log2(x+1)** | 表达值取 log2 加 1，压缩偏态、稳定方差 | 几乎所有下游统计的前提 |

## 四、统计概念

| 术语 | 定义 | 本项目实例 |
|---|---|---|
| **DE（differential expression）** | 两组间表达有显著差异 | 审计核心 |
| **fold change（FC）** | 倍数变化 = 组 A 均值 / 组 B 均值 | Atlas 表 1.4、-2.0 等 |
| **log2FC** | log2(FC)，正=上调、负=下调；±1 = 2 倍/一半 | 预设阈值 `|log2FC| ≥ 1.0` |
| **p 值** | 若真实无差异，观察到当前或更极端结果的概率 | 签名检验 p=1.5e-5 |
| **FDR / BH 校正** | 多重检验下"显著结果中预计假阳性比例"；BH 为常用算法 | 半样本扫描 9 对时最小 FDR≈46（理论不可能显著） |
| **效应量（effect size）** | 差异幅度本身（与显著性无关） | +1.72 / -2.42 |
| **CI（置信区间）** | 效应量的不确定范围 | results.json 的 ci_lower/ci_upper |
| **配对设计（paired）** | 同一患者/供体内比较，消除个体差异 | GSE50760 同患者三部位；E-MTAB-8316 同 donor-specimen |
| **非配对设计（unpaired）** | 两组独立样本比较 | 引擎同样支持 |
| **pseudobulk** | 把单细胞数据按样本聚合为"伪批量"再检验 | E-MTAB-8316 审计用 |
| **ridge 回归** | 带 L2 正则的线性回归，用于协变量调整/稳健性分析 | E-MTAB-8316 的组成稳健性检查 |
| **LOO（leave-one-out）** | 每次剔除一个样本/患者重算，观察结论稳定性 | 留一患者通过率 1.0 |
| **split-half（半样本）** | 一部分数据选假设，另一部分只做检验 | 前 9 患者选签名 → 后 9 患者验证 |
| **out-of-sample** | 未参与假设/模型选择的数据 | 半样本验证的测试集 |
| **robust / fragile / not_reproduced / inconclusive** | 本引擎的四档判定 | 见 `pilot/README.md` 第 2 节 |

## 五、流程与系统名词

| 术语 | 定义 | 对应代码/文件 |
|---|---|---|
| **claim（主张）** | 一条可检验的研究结论（含方向与特征集） | `claims.*.json` |
| **signature（签名）** | 一组特征（基因/蛋白）的集合，整体打分 | `signature_up_top100.txt` 等 |
| **signature score** | 签名内所有特征表达的均值（每个样本一个数） | `audit.py: signature_score()` |
| **audit（审计）** | 用数据重跑主张并判定稳健性 | `pilot/audit.py` |
| **job / episode** | 闭环项目中的一轮交互（提出→批判→选择→执行） | `closed_loop/run.py` |
| **verifier（验证器）** | 检查输出格式与自洽性的程序（10 项规则） | `closed_loop/verifier.py` |
| **compiler（编译器）** | 把任务规格转成可执行分析脚本 | `closed_loop/compiler.py` |
| **executor（执行器）** | 在子进程中运行生成脚本（超时/内存限制） | `closed_loop/executor.py` |
| **result_bridge（结果回流）** | 把实测结论写回假设证据并传给下一轮 | `closed_loop/result_bridge.py` |
| **evidence 回流** | 上述机制的动作描述 | 同上 |
| **grounding（接地）** | 让假设与真实证据（文献/数据）挂钩，而非凭空生成 | 当前实现的短板之一 |
| **Harbor 任务** | DiscoveryRSI 的"可执行任务"格式（instruction + verifier + fixtures） | 任务包 `datasets/.../task-packages/` |
| **manifest（研究清单）** | 一次战役的配置（问题、领域、角色、工具） | `configs/research_manifest.json` |

## 六、四组最易混淆概念

| 对比 | 要点 |
|---|---|
| **counts vs FPKM vs TPM** | counts 是原始读数；FPKM/TPM 已归一化；FPKM 不可跨基因比较，TPM 可以。尺度混用会改变结论，必须记录 |
| **p 值 vs FDR** | 单次检验看 p；成千上万基因同时检验看 FDR。scan 用 FDR，signature 用 p |
| **配对 vs 非配对** | 配对消除个体差异、功效更高；设计判断错误会使结论方向相反 |
| **显著 vs 有效应** | p 小≠效应大；样本大时微小差异也显著。报告必须同时给效应量与 p |

## 七、读报告速查：先看哪几个数

拿到一份审计结果（如 `pilot/results/gse50760_audit.md`），按这个顺序读：

1. **判定（verdict）**：robust / fragile / not_reproduced / inconclusive——先看结论；
2. **效应量（effect）**：方向对不对、幅度是否合理（±1 以上通常算强）；
3. **p 值**：显著性（配对样本 <5 对时 p 值基本无信息）；
4. **LOO 通过率**：换个患者/样本还成立吗；
5. **特征数（n_features）**：签名里有多少个在矩阵中真的找得到（缺失多说明 ID 映射有问题）。

## 八、最小工作流（术语视角）

```
GSE/GSM（数据库编号）
  → processed 文件（FPKM/counts）
  → 矩阵（feature × sample）+ 元数据（design）
  → log2 变换
  → claim（signature + 方向 + 阈值）
  → audit（配对检验 + LOO + 判定）
  → verdict（robust/fragile/...）
```