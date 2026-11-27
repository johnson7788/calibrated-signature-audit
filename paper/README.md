# paper/ — 手稿与图表

## 文件

| 文件 | 内容 |
|---|---|
| `manuscript.md` | 论文全文（工具论文，约 2,800 词，英文） |
| `figures/fig1_fpr_calibration.png` | 图 1：名义 vs 置换校准的误判率（核心图） |
| `figures/fig2_null_distribution.png` | 图 2：随机签名零分布 + 真实签名位置 |
| `figures/fig3_replication_heatmap.png` | 图 3：复现矩阵（应用示例） |
| `figures/fig4_threshold_sensitivity.png` | 图 4：阈值敏感性 |
| `make_figures.py` | 从 `pilot/results/` 报告重新生成全部图 |
| `SUBMISSION_CHECKLIST.md` | 预印本提交清单 |

## 重新生成图

```bash
MPLCONFIGDIR=/tmp/mpl .venv/bin/python paper/make_figures.py
```

图的数据来自 `paper/null_calibration.csv`、`paper/calibration_perm.csv`、`paper/realcal.csv` 与 `pilot/results/` 下的报告；
若重跑分析改变了结果，图表需同步重生成（`bash pilot/run_all.sh` 后执行上面的命令）。

## 提交前要替换的占位符

- 作者 / 单位 / 通讯邮箱 / ORCID
- GitHub 仓库 URL 与 Zenodo DOI
- 资金声明、作者贡献（CRediT）
- 图分辨率：当前 200 dpi；提交前可在 `make_figures.py` 中把 `dpi=200` 改为 `dpi=300`

## 转 PDF 建议

- Pandoc：`pandoc manuscript.md -o manuscript.pdf --pdf-engine=xelatex`
- 或 Word：先转 docx，按目标期刊模板排版
- 图片需单独提供（预印本服务器支持上传图文件或含图 PDF）