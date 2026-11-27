# 预印本提交清单（bioRxiv / medRxiv）

> 状态：稿件完成（`paper/manuscript.md`，约 3,300 词），图 4 张（300 dpi），代码可复现。
> 作者信息已填入。剩余：GitHub 仓库地址（代码可用性声明）。

## 0. 服务器选择

| 服务器 | 定位 | 本文适配度 |
|---|---|---|
| **bioRxiv** | 生命科学预印本（含生物信息学/方法学） | **推荐**：分类选 *Bioinformatics* |
| **medRxiv** | 健康/临床研究预印本 | 可选：分类 *Health Informatics*；方法学工具可能被建议转投 bioRxiv |

> 两者同属 CSHL，流程一致；建议一次选对，避免撤稿冷却期。

## 1. 稿件信息（已填）

| 项 | 内容 |
|---|---|
| 标题 | *Calibrating signature audits: nominal tests understate false-positive rates by up to five-fold* |
| 作者 | Zhicai Guo（郭志才） |
| 单位 | Yifu Knowledge (Beijing) Technology Co., Ltd., Room 08A05, 7th Floor, No. Bing 2, North East Third Ring Road, Chaoyang District, Beijing, China |
| 通讯邮箱 | 363800649@qq.com |
| 摘要 | 结构化（Background/Methods/Results/Conclusions），约 300 词 |
| 关键词 | signature audit; gene-set permutation; false-positive rate; reproducibility; omics |
| 资金 | 无特定资助（This research received no specific grant from any funding agency.） |
| 作者贡献 | Zhicai Guo: Conceptualization, Software, Formal analysis, Writing – original draft. |
| 利益冲突 | 无 |
| 伦理 | 仅公开去标识数据，无需伦理审批 |
| AI 声明 | 已写（AI 辅助编码/分析/起草，作者复核并负责） |

## 2. 仍需你提供

| 项 | 说明 |
|---|---|
| **GitHub 仓库 URL** | 代码可用性声明需要；仓库内容我已备好（`pilot/`、`closed_loop/`、`tests/`、`paper/`） |
| ORCID（可选） | 建议提供，便于关联 |
| 核准日期与版本 | 提交时填 |

## 3. 提交前 24 小时检查表

- [ ] 全文通读（重点：数字与图一致）
- [ ] 摘要 ≤300 词
- [ ] 4 张图 300 dpi，图注完整（`paper/figures/`）
- [ ] 数据可用性：GEO 编号可访问（GSE50760 / GSE95132 / GSE110224）
- [ ] 代码可用性：GitHub 链接（待填）+ Zenodo DOI（可后补）
- [ ] 伦理、资金、利益冲突、AI 声明齐全
- [ ] 许可：CC-BY 4.0
- [ ] 分类：bioRxiv — Bioinformatics
- [ ] 备份：稿件 + 图 + 补充材料打包

## 4. 提交步骤（bioRxiv）

1. 注册（可用 ORCID 登录）；
2. New submission：标题、摘要、作者、单位、分类；
3. 上传 PDF（由 `paper/manuscript.html` 打印）与图文件；
4. 声明项：伦理、利益冲突、资金、AI 使用、数据/代码可用性、作者同意；
5. 选择许可 CC-BY 4.0；
6. 提交 → screening（1–3 个工作日）→ 发布获得 DOI；
7. 发布后把 DOI 填回 GitHub README 与 Zenodo。

## 5. 常见退回原因

1. 作者同意未确认；2. 伦理声明缺失；3. 利益冲突/资金为空；4. AI 声明缺失；5. 数据不可得；6. 图片分辨率不足。

## 6. 转 PDF

- 浏览器打开 `paper/manuscript.html` → 打印 → 另存为 PDF（图已内嵌）；
- 或安装 pandoc 后：`pandoc manuscript.md -o manuscript.pdf --pdf-engine=xelatex`。

## 7. 发布之后

1. 期刊投稿时在 cover letter 引用预印本 DOI；
2. 多数期刊允许预印本（Nature 系列、PLOS、BMC、GigaScience 等）；
3. 审稿修改后用 "new version" 更新，保留旧版本 DOI。