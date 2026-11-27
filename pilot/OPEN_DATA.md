# 开源组学数据检索目录（试点用）

> 目标：为"复现审计"试点找到**数据可获取 + 结论可检验**的公开数据集。
> 所有端点均于 2026-11-25 实测（经本机 Clash 代理）。

## 0. 先说结论（避坑指南）

公开数据"能下载"和"能审计"是两回事。实测下来分三档：

| 档位 | 特征 | 处理 |
|---|---|---|
| **A. 可直接跑** | 有 processed 矩阵（counts/FPKM/TMP） + 元数据 | 立即可接入审计引擎 |
| **B. claims 易得、矩阵需拼** | Atlas 有策划好的 DE 结果表；数据在 BioStudies 逐样本文件里 | 需写拼接脚本（54 个文件 → 一个矩阵） |
| **C. 不可用/避坑** | 镜像只有 IDF+SDRF（无数据）；series matrix 只有表头；只有 1GB 级 RAW 对齐文件 | 跳过或改路线 |

## 1. 数据源目录（实测状态）

| 数据源 | 用途 | 端点模式 | 实测 |
|---|---|---|---|
| **Expression Atlas** | 找实验、拿"论文声称的差异基因" | 列表：`/gxa/json/experiments`（4562 个实验，1528 个人类差异表达）；DE 表：`/gxa/experiments-content/<acc>/download/RNASEQ_MRNA_DIFFERENTIAL?...` | ✅ 200，TSV 约 300KB |
| **BioStudies**（EBI，ArrayExpress/GEO 镜像） | 下载作者上传的 processed 文件 | 文件列表：`/biostudies/api/v1/files/<acc>`；下载：`/biostudies/files/<acc>/<file>`（**需 -L 跟随 302**） | ✅ 实测成功 |
| **ArrayExpress 旧路径** | E-MTAB 类文件 | `/arrayexpress/files/<acc>/<file>` | ✅ 实测（E-MTAB-8316） |
| **GEO FTP** | 补充文件、series matrix | `ftp.ncbi.nlm.nih.gov/geo/series/GSE<前缀>nnn/<GSE>/suppl/`（RAW.tar / 作者矩阵）；`matrix/`（series matrix，**经常只有表头**） | ✅ 可达；matrix 可能为空 |
| **PRIDE**（蛋白组） | 蛋白组原始/processed | `/pride/ws/archive/v2/projects` | ✅ 200 |
| **MetaboLights**（代谢组） | 代谢组研究 | `/metabolights/ws/studies` | ✅ 200 |
| **Zenodo / Figshare** | 论文配套数据（补遗） | 按 DOI/标题搜 | 未测 |

## 2. 候选数据集（人类，两组设计优先）

| 数据集 | 设计 | 样本 | 可审计的主张（claims 来源） | 数据状态 |
|---|---|---|---|---|
| **E-MTAB-8316** ✅ | RA 滑膜成纤维细胞 × 巨噬细胞共培养，配对 | 12（6 对） | UNC106238 转录响应是否依赖巨噬细胞环境 | **已接入**（counts + design） |
| **GSE50760** ✅ | 结直肠癌：正常/原发/肝转移，同患者配对 | 54（18 患者 × 3 部位） | 肿瘤 vs 正常的差异基因（论文的预后 signature） | **已跑通**：54 个 FPKM 文件已下载拼装（23,503 基因 × 54 样本），审计结果见 `pilot/results/gse50760_summary.md` |
| **GSE95132** ✅ | 结直肠癌：肿瘤 vs 癌旁，配对 | 31（12 患者） | 肿瘤 vs 癌旁 DE | **已用于跨队列复现**：read counts 矩阵（GEO FTP），见 `pilot/results/crossstudy_summary.md` |
| **GSE110224** ✅ | 结直肠癌：肿瘤 vs 癌旁，配对，芯片 GPL570 | 34（17 对） | 肿瘤 vs 癌旁 DE | **已用于第三队列**：series matrix + GPL570 注释映射（45,782 符号），见 `pilot/results/replication_matrix.md` |
| **GSE48684** ✅ | 结直肠癌/腺瘤：450K 甲基化 | 147 | 甲基化差异 | **跨组学案例**：series matrix 296MB，485,578 CpG，见 `pilot/results/methylation_summary.md` |
| **GSE54456** ⚠️ | 银屑病 皮肤病变 vs 正常，配对 | 179 | 病变 vs 正常的 DE 基因 | 镜像仅 IDF+SDRF；矩阵需查 GEO suppl |
| **GSE36761** ⚠️ | 法洛四联症 右心室 vs 健康 | 29 | 疾病相关转录改变 | 镜像仅元数据；查 GEO suppl |
| **GSE51403** ⚠️ | MCF7 细胞 + E2 处理 | 38 | E2 响应基因 | 镜像仅元数据 |
| **GSE47718** ⚠️ | 吸烟者 vs 非吸烟者 气道基底细胞 | 52 | 吸烟相关转录改变 | 镜像仅元数据 |
| **GSE49155** ⚠️ | 肺鳞癌 vs 正常 | 24 | 肿瘤 vs 正常 | 镜像仅元数据 |
| **GSE101794** ⚠️ | 儿童克罗恩病 回肠活检 | 304 | 疾病 vs 对照 | BioStudies 无文件；查 GEO |
| **GSE112057** ⚠️ | JIA/IBD 全血 | 202 | 疾病 vs 对照 | BioStudies 无文件；查 GEO |
| **GSE22260** ❌ | 前列腺癌 vs 正常 | 30 | 肿瘤 DE | 只有 1GB 级 RAW 对齐文件，不可用 |
| **GSE37211** ⚠️ | 甲状旁腺腺瘤细胞 + 化合物 | 27 | 化合物响应 | 查 GEO |

> ✅=数据路线已验证；⚠️=claims 有、数据需再查；❌=已排除。

## 3. "可审计"筛选清单（5 条，缺一不可）

1. **样本量**：两组各 ≥ 5（配对 ≥ 5 对），否则稳健性检查没意义（引擎会返回 inconclusive）；
2. **设计清晰**：分组变量唯一（如 disease vs normal），有配对键或可调整的协变量；
3. **矩阵可获取**：processed 矩阵 > 逐样本文件拼装 > 仅有原始 reads（不推荐）；
4. **论文有明确主张**：能写成"gene set X 在 A 相对 B 上调/下调"这种可检验形式；
5. **许可**：完全公开（避免 dbGaP 等受控数据）。

## 4. 搜索 playbook（自己扩展数据集时用）

### 从"论文"出发（推荐：你已经有目标论文）

- GEO 搜系列：`https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE<id>`，看 `Supplementary file` 有没有 processed 矩阵；
- BioStudies 查镜像：`https://www.ebi.ac.uk/biostudies/api/v1/files/E-GEOD-<id>`（有文件≠有数据，要看文件名和大小）；
- Atlas 查是否被策划：`https://www.ebi.ac.uk/gxa/experiments/E-GEOD-<id>`（在的话可拿 DE 表）。

### 从"数据"出发（找可审计的现成实验）

```bash
# Atlas 中筛选：人类 + 差异表达 + 样本数 >= 20
curl -s "https://www.ebi.ac.uk/gxa/json/experiments" | jq '.experiments[] | select(.species=="Homo sapiens" and .experimentType=="Differential" and .numberOfAssays>=20)'

# GEO 搜索模板（eutils）
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&term=<关键词>[Title]+AND+human[Organism]&retmax=20
```

### 蛋白组 / 代谢组

- PRIDE：`https://www.ebi.ac.uk/pride/ws/archive/v2/search/projects?keyword=<关键词>`（返回 PXD 编号）；
- MetaboLights：`https://www.ebi.ac.uk/metabolights/ws/studies`（列表）+ 研究页拿 processed 表；
- 注意：这两个库的 processed 格式差异大，接入成本高于转录组，建议第二轮再扩。

## 5. 建议的首批三例（试点起点）

1. **E-MTAB-8316**（已跑通）——验证管线与判定逻辑；
2. **GSE50760**（A 档，需拼矩阵）——验证"逐样本文件 → 矩阵 → 审计"的数据工程流程，且是**配对设计 + 同患者三部位**，很适合检验稳健性（留一患者法）；
3. **再选 1 个领域外数据集**（如 PRIDE 的蛋白组或 MetaboLights 代谢组）——验证跨组学迁移成本。

## 6. 下一步

- 我可以先写 **GSE50760 的抓取+拼装脚本**（54 个 FPKM → 矩阵 + 从 Atlas/GEO 构建 design），跑出一条真实的审计结果；
- 你如果已经有目标论文（数据在你手里或能从 GEO 找到），直接给我 accession，我按同样流程接入。