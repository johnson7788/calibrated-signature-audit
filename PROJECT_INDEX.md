# 项目索引（从哪里开始看）

本项目包含两条工作线，共用同一批公开数据与方法论。

```
线 A：DiscoveryRSI 可执行闭环（机制验证）
  假设 → 编译 → 真执行 → 验证 → 证据回流 → 下一轮
  代码：closed_loop/    文档：closed_loop/REPORT.md

线 B：复现审计工具箱（方法产品化）
  论文结论 + 原始数据 → 稳健性审计 → 分级判定 → 报告
  代码：pilot/          文档：pilot/SOP.md
```

## 我想…… 去哪看？

| 我想 | 看这里 |
|---|---|
| 5 分钟跑一个示例 | [pilot/README.md](pilot/README.md)「快速开始」 |
| 学会独立审计一个数据集 | [pilot/SOP.md](pilot/SOP.md) |
| 看有哪些公开数据可用 | [pilot/OPEN_DATA.md](pilot/OPEN_DATA.md)，或 `python -m pilot.cli datasets` |
| 看审计结果长什么样 | [pilot/results/](pilot/results/)（7 份报告） |
| 名词看不懂 | [pilot/GLOSSARY.md](pilot/GLOSSARY.md) |
| 了解闭环系统 | [closed_loop/REPORT.md](closed_loop/REPORT.md) |
| 了解研究计划 | [研究计划.md](研究计划.md)、[可执行闭环-研究方案.md](可执行闭环-研究方案.md) |
| 看论文手稿 | [paper/manuscript.md](paper/manuscript.md)（HTML 版：[manuscript.html](paper/manuscript.html)） |
| 准备投稿 | [paper/SUBMISSION_CHECKLIST.md](paper/SUBMISSION_CHECKLIST.md) |

## 一键命令

```bash
python -m pilot.cli datasets                # 已注册数据集
python -m pilot.cli audit --claims pilot/claims.gse50760.json --out /tmp/r.md
bash pilot/run_all.sh                       # 重跑全部结果 + 全量测试（约 17 秒）
```

## 目录地图

```
.
├── closed_loop/            # 线 A：可执行闭环（M0–M4 完成）
│   ├── compiler/executor/verifier/result_bridge/run/demo
│   ├── data/               # prepared 数据 + 回放
│   └── REPORT.md
├── pilot/                  # 线 B：复现审计（A–D 完成）
│   ├── cli.py              # 统一入口
│   ├── audit.py            # 审计引擎
│   ├── split_half.py       # 半样本协议
│   ├── replication_matrix.py / cross_signature.py
│   ├── prepare_microarray.py
│   ├── datasets.json / cohorts.json
│   ├── claims.*.json       # 各实验主张（阈值锁定）
│   ├── data/               # GSE50760 / GSE95132 / GSE110224 / GSE48684
│   ├── results/            # 7 份报告
│   └── SOP.md / README.md / OPEN_DATA.md / GLOSSARY.md
├── paper/                  # 论文（校准主线，初稿完成）
│   ├── manuscript.md / .html
│   ├── figures/            # 4 张 300 dpi 图
│   ├── exp_*.py            # 支撑实验（FPR/校准/真实签名）
│   └── SUBMISSION_CHECKLIST.md
├── datasets/               # 任务包与模型卡（DiscoveryRSI 生态）
└── tests/                  # 26 个测试
```

## 当前状态

| 阶段 | 内容 | 状态 |
|---|---|---|
| A | 引擎加固（CLI/半样本/阈值扫描/方法学元数据/芯片/甲基化接入） | ✅ |
| B | 多队列复现矩阵（3 队列 × 3 规模 + 交叉签名矩阵） | ✅ |
| C | 跨组学验证（甲基化 450K） | ✅（探针级） |
| D | 产品化（CLI/SOP/注册表/一键复现/测试） | ✅ |
| E | 成文：论文初稿（校准主线） | ✅ 初稿完成，待提交预印本 |

## 关键结论（截至 2026-11-27）

- 结直肠癌"肿瘤 vs 正常"转录签名在 3 个独立队列、3 种规模、双方向共 **18/18** 判定 robust；
- 交叉签名矩阵：上调 **6/6** 复现，下调 **5/6**（唯一 fragile 指向小样本队列 GSE95132）；
- 半样本与阈值敏感性显示：**判定标准必须审计前锁定**，p=0.05 与 0.1 可能翻转结论；
- 甲基化数据可直接接入（485k 探针，CRC vs 癌旁 78,552 个差异位点），但探针相关会高估独立信号数。