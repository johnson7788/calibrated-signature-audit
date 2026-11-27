# DiscoveryRSI 可执行闭环——技术报告

> 项目：把 DiscoveryRSI 的"假设 → 执行 → 验证 → 回流"断环接上，在本机跑通可演示的最小闭环。
> 日期：2026-11-23 ｜ 状态：M0–M3 完成，M4 收尾 ｜ 配套：`可执行闭环-研究方案.md`、`closed_loop/specs/unc106238-context-response.md`

---

## 1. 摘要

DiscoveryRSI 的开源部分是**断环**：假设被编译成 Harbor 任务后即止步——验证器只检查输出格式、fixtures 是合成的、`scientific_result` 恒为 `not_established`，没有任何一步真正执行数据分析。本报告记录我们补上的四件套（**compiler → executor → verifier → result_bridge**）在真实数据（E-MTAB-8316，RA 滑膜成纤维细胞-巨噬细胞共培养转录组，12 样本）上的实现与验证。闭环已真实运行 2 轮：第 1 轮对"UNC106238 干预相关转录程序"的检验得到 **adverse（程序为空）**，实测证据回流后，第 2 轮假设明确引用了上一轮诊断结论（*"Context contrast...unavailable in the prior diagnostic"*）——**证据跨轮回流成立**。

## 2. 断点分析（为什么值得做）

| 断点 | 证据（源码/官方文件） |
|---|---|
| 不真正执行 | verifier（`tests/test.sh`）只检查 `results.json` 的键/值/措辞；`validation/` 下是合成 fixture 脚本，与科学计算无关 |
| 结果恒"未确立" | `provenance.json`：`scientific_result: "not_established"`、`full_scientific_execution_performed_for_release: false` |
| 镜像缺失 | `task.toml` 引用 `discoveryrsi-task-examples:local`，公开仓库无此镜像（公开 Dockerfile 是通用 python 示例） |
| 无学习回流 | 开源 harness 的 ReplayBuffer 只记录文本，`Doctorate 的"信用优化/回放/再发现"训练在闭源侧 |

**我们验证的机制**：闭环真执行后，下一轮假设携带实测证据——这是"从假设工厂到可实证研究循环"的关键一步。

## 3. 系统设计

```
DiscoveryLoop 风格循环（closed_loop/run.py，不改原仓库 core）
  propose(LLM) → critique(LLM, score 0-10) → select(max score)
      │
      ▼ selected candidate
  compiler.py     instruction.md + 任务 schema → 分析脚本（模板优先，LLM 补缝隙）
  executor.py     venv 子进程（timeout + 可选 RLIMIT_AS）
  verifier.py     tests/test.sh 的等价移植（10 项检查，防过度声称）
  result_bridge.py outcome/统计 → 候选 evidence 实测记录 + 下一轮上下文
      │
      ▼ 下一轮 propose 上下文 = 顶层问题 + 上一轮 exec 证据
```

### 模块清单

| 模块 | 职责 | 关键设计 |
|---|---|---|
| `prepare_data.py` | ArrayExpress 原始文件 → prepared counts/design | counts：`feature`+12 样本列；design：SDRF→JSON（sample_id/donor_id/condition/cell_type/specimen/source_metadata） |
| `analysis_reference.py` | M1 参考实现 | instruction 5 步流程：预指定程序 → donor-aware pseudobulk → ridge 稳健性 → 判定 |
| `verifier.py` | 结果判定 | 10 项检查（含两条防过度声称：supportive⇔composition_robust、justification 措辞），容器/本地双模式 |
| `compiler.py` | 假设→脚本 | 模板渲染 + LLM 提取参数（阈值/方向一致性/条件名/协变量）；**配对键等结构性参数由 data schema 决定**；静态检查（AST 语法 + 禁用危险调用） |
| `executor.py` | 脚本执行 | `sys.executable` 子进程、timeout、setrlimit 内存限额（macOS 降级） |
| `result_bridge.py` | 结果回流 | `[exec-record]` 证据条目 + 下一轮上下文摘要 |
| `run.py` / `demo.py` / `visualize.py` | 编排/演示/可视化 | 2–N 轮战役；假设树（文本 + Mermaid）标注实测结果 |

## 4. 实现与验证（里程碑证据）

**M0 环境与数据**
- counts `MK_readcountMatrix.txt.gz`（791,880 B，58,303×13）+ SDRF（18,139 B）与 BioStudies 官方记录精确一致（下载曾遇 `files/` 端点间歇 500：浏览器 UA + http1.1 + 重试解决）
- prepared：36,719 特征 × 12 样本；design 12 条（none/UNC106238 各 6，6 组 donor-specimen 配对）；依赖按任务 Dockerfile 同版本锁定

**M1 执行器**
- verifier 与 4 个官方 fixture 对齐：**1/0/0/0，7/7 测试通过**
- 参考实现 `Verifier passed`；**科学发现**：预设标准（|mean log2FC|≥1.0 且 ≥5/6 方向一致且高表达）下**干预相关程序为空**——137 个基因过幅度阈值但无一达到方向一致性 → `outcome=adverse`（如实报告，不硬凑）

**M2 编译器**
- 默认参数与 LLM 提取参数两条路径生成脚本，输出**均与参考实现 MATCH** 且 verifier 通过
- 静态防线实例：LLM 曾把 `condition` 猜进配对键 → 被"配对键由 data schema 决定"规则纠正（`pair_group_cols` 不进 LLM 输出）

**M3 闭环集成**
- 2 轮闭环真实运行（LLM propose/critique + 真执行）→ 假设树（`closed_loop/data/hypothesis_tree.md`）：
  - Episode 1：episode-1-2（score 8.0）选中 → 编译执行 → **adverse**
  - Episode 2：episode-2-1（parents=[episode-1-2]）→ 候选 evidence 含 `[exec-record] outcome=adverse`
- 全量回归 **17/17 通过**

## 5. 科学结果解读（诚实科学）

本任务的结果不是一个"好故事"，但它是**正确行为**：在 n=12、供体异质性高的数据上，干预效应方向跨供体不稳定（137 个高效应基因无一达到 5/6 同向）。闭环正确地把"假设未获支持"信号带回下一轮，驱动后续进化（如修改程序定义、显式建模供体异质性）。**我们验证的是闭环机制，不是生物学结论**——所有输出标注为探索性诊断证据（evidence-level），不声称直接靶点因果/疗效/机制。

## 6. 局限与边界

1. **verifier 是结构检查**：通过 = 输出合规自洽，≠ 科学正确（与官方 `validation_scope` 一致）。
2. **fixtures 是合成的**：M1 对齐证明的是"检查器行为等价"，不证明任何实验真实性。
3. **prepared 形态差异**：任务包 sha256 对应官方内部 prepared 变换，无法精确复现；自建流程以 verifier 为判据（方案 v0.3 第 8 节注记）。
4. **LLM 参数提取有边界**：instruction 不含完整数据 schema，LLM 只能补文本明示的参数；结构性参数由 schema 决定并静态校验。
5. **样本量与批次**：单批次、无独立巨噬细胞条件对比数据源（overlap 用高表达近似，已在 limitations 声明）。
6. **成本/复现**：在线战役依赖中转 API（`litellm.infox-med.com`）；LLM 输出不可逐字节复现，但管线确定性（脚本/参数/判定）完全可复现。

## 7. 后续工作（对本项目创新点 ④ 的延伸）

- **多假设回路**：让 `compiler` 的模板库覆盖更多假设类型（比较、富集、方向性），LLM 从候选 plan 选择模板；
- **真实"进化"**：在 adverse 分支上自动生成修订假设（修程序定义/换对比/分层建模），闭环多轮直到 outcome 不再 adverse；
- **结果置信**：把 verifier 扩展到"统计合理性"（效应量、CI、稳健性阈值），向科学验证靠近；
- **跨任务扩展**：3 个任务包全量接入，模板按任务规格书逐一验证。

## 8. 复现指南

```bash
# 环境（Python 3.12）
/usr/local/bin/python3.12 -m venv .venv
.venv/bin/pip install -e ".[test]" numpy==2.2.6 pandas==2.2.3 scipy==1.15.3 scikit-learn==1.6.1 statsmodels==0.14.4
.venv/bin/pytest                 # 17 passed（含 closed_loop 7 项）

# 离线演示（无需 API）：真实数据 prepared → 参考分析 → verifier → 假设树
.venv/bin/python -m closed_loop.prepare_data          # 已在仓库内（data/prepared）
.venv/bin/python -m closed_loop.analysis_reference    # 参考实现 → results.json
.venv/bin/python -m closed_loop.verifier --results closed_loop/data/prepared/results.json
.venv/bin/python -m closed_loop.demo --offline        # 假设树（文本+Mermaid）

# 在线闭环战役（需要 LLM key）
export DISCOVERY_RSI_API_KEY=...
.venv/bin/python -m closed_loop.run --iterations 2 --replay closed_loop/data/campaign.jsonl
.venv/bin/python -m closed_loop.demo --offline        # 重新生成带结果标注的树
```

**数据来源**：E-MTAB-8316（ArrayExpress/BioStudies，RA 滑膜成纤维细胞-巨噬细胞共培养 RNA-seq，12 样本）。counts=`MK_readcountMatrix.txt.gz`、SDRF=`E-MTAB-8316.sdrf.txt`，原始文件在 `closed_loop/data/inputs/`，使用遵守 EBI 数据使用条款。任务包（含 instruction/verifier/fixtures）来自 Gen-Verse/DiscoveryRSI-Hypothesis-Task-Examples（Apache-2.0）。