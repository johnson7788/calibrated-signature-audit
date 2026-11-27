# calibrated-signature-audit

**组学签名审计——带校准的零假设。**

[English](README.md) | **简体中文**

本仓库是以下预印本的配套代码与数据：

> 郭志才（Zhicai Guo）. *Calibrating signature audits: nominal tests understate false-positive rates by up to five-fold.*（签名审计的校准：名义检验将假阳性率低估达五倍）
> 预印本：bioRxiv（待提交）· PDF：[paper/manuscript.pdf](paper/manuscript.pdf) · 数据：[Hugging Face](https://huggingface.co/datasets/johnson/calibrated-signature-audit)

**核心发现。** 在名义 5% 水平下，常规签名审计把 **12.4%** 和 **24.6%** 的随机 100 基因签名判为"robust"（两个结直肠癌队列，超出名义水平 2.5–4.9 倍）。使用**同规模基因集置换校准**后，假阳性率回到 **4.0–6.4%**，而全部 36 个真实签名仍然显著。

---

## 一句话理解

签名审计通常这样算：把签名里所有基因的表达平均成一个分数，再做样本级检验（如配对 Wilcoxon），按名义 α 判定"复现/不复现"。但签名是**一组相关基因**，不是独立样本；随机基因集也能继承全局偏移，于是名义 5% 实际可能是 12–25%。这本仓库给出问题诊断与修复方法。

## 仓库结构

```
pilot/                  # 审计工具箱（主要交付物）
├── cli.py              # 命令行入口
├── audit.py            # 审计引擎（signature/scan、留一法、协变量、阈值扫描）
├── permutation.py      # 基因集置换校准（论文核心方法）
├── split_half.py       # 半样本协议（训练集选签名 → 留出集检验）
├── replication_matrix.py / cross_signature.py
├── prepare_microarray.py
├── SOP.md              # 标准操作流程
├── datasets.json       # 已注册数据集
├── data/               # processed 矩阵（小文件入库）
└── results/            # 生成的审计报告

paper/                  # 论文、图与支撑实验
├── manuscript.md / .pdf
├── figures/            # 4 张 300 dpi 图
├── exp_null.py         # 名义假阳性率实验
├── exp_calibrated.py   # 置换校准实验
├── exp_realcal.py      # 真实签名存活检验
└── SUBMISSION_CHECKLIST.md

closed_loop/            # DiscoveryRSI 风格的可执行研究闭环（支撑工作）
src/, tests/            # 上游 harness 与测试
datasets/               # 第三方任务包（见 THIRD_PARTY_NOTICES.md）
docs/                   # 上游 README 备份
```

## 快速开始

```bash
python3.12 -m venv .venv
.venv/bin/pip install -e ".[test]" numpy pandas scipy scikit-learn statsmodels matplotlib
.venv/bin/pytest -q                         # 26 passed

# 列出已注册数据集
.venv/bin/python -m pilot.cli datasets

# 审计一组主张（示例：GSE50760 签名）
.venv/bin/python -m pilot.cli audit --claims pilot/claims.gse50760.json --out /tmp/report.md

# 重跑本仓库全部报告（约 20 秒）
bash pilot/run_all.sh
```

复现论文的校准数字：

```bash
PYTHONPATH=. .venv/bin/python paper/exp_null.py        # 名义 FPR（表 1 左）
PYTHONPATH=. .venv/bin/python paper/exp_calibrated.py  # 置换 FPR（表 1 右）
PYTHONPATH=. .venv/bin/python paper/exp_realcal.py     # 真实签名存活
MPLCONFIGDIR=/tmp/mpl .venv/bin/python paper/make_figures.py
```

## 数据

处理后的矩阵、主张规格、图与 PDF 归档于
**Hugging Face：https://huggingface.co/datasets/johnson/calibrated-signature-audit**

原始数据：NCBI GEO
[GSE50760](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE50760)、
[GSE95132](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE95132)、
[GSE110224](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE110224)。
仓库不再分发原始文件；处理脚本见 `pilot/prepare_*.py` 与数据集卡片。

## 许可

本项目自有代码（`pilot/`、`paper/`、`closed_loop/`）采用 MIT 许可（见 [LICENSE](LICENSE)）。
上游组件（`src/discovery_rsi/`、`datasets/`）源自
[Gen-Verse/DiscoveryRSI](https://github.com/Gen-Verse/DiscoveryRSI)，采用 Apache-2.0；
详见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。公开数据集保留其原始条款。

## 引用

```bibtex
@article{guo2026calibrating,
  title   = {Calibrating signature audits: nominal tests understate false-positive rates by up to five-fold},
  author  = {Guo, Zhicai},
  year    = {2026},
  note    = {Preprint},
  url     = {https://github.com/johnson7788/calibrated-signature-audit}
}
```

机器可读元数据见 [CITATION.cff](CITATION.cff)。

## 致谢

本工作建立在 DiscoveryRSI harness 与任务包（Gen-Verse/DiscoveryRSI）之上，并使用 NCBI GEO 与 Expression Atlas 的公开数据。

## 联系方式

郭志才（Zhicai Guo）· 363800649@qq.com
医赋知识（北京）科技股份有限公司