#!/usr/bin/env bash
# run_all.sh — 一键重跑全部已发布结果（约 30 秒）+ 全量测试。
set -euo pipefail
cd "$(dirname "$0")/.."
PY=.venv/bin/python

echo "== 1. 示例审计（E-MTAB-8316）=="
$PY -m pilot.cli audit --claims pilot/claims.example.json --out pilot/results/audit.md >/dev/null

echo "== 2. GSE50760 审计（含阈值敏感性）=="
$PY -m pilot.cli audit --claims pilot/claims.gse50760.json --out pilot/results/gse50760_audit.md >/dev/null
$PY -m pilot.cli audit --claims pilot/claims.gse50760.split.json --out pilot/results/gse50760_split_audit.md >/dev/null

echo "== 3. 半样本协议 =="
$PY -m pilot.cli split-half --matrix pilot/data/gse50760/GSE50760_log2fpkm.tsv.gz \
  --metadata pilot/data/gse50760/design.json --group-col condition --a primary --b normal \
  --pair-col patient --top 100 --min-delta 1.5 --out pilot/results/gse50760_split_half.md >/dev/null

echo "== 4. 多队列复现矩阵 =="
$PY -m pilot.cli matrix --de-file pilot/data/gse50760/atlas_de.txt --cohorts pilot/cohorts.json \
  --sizes 50,100,200 --out pilot/results/replication_matrix.md >/dev/null

echo "== 5. 交叉签名矩阵 =="
$PY -m pilot.cli cross --cohorts pilot/cohorts.json --size 100 --out pilot/results/cross_signature.md >/dev/null

echo "== 6. 跨组学：甲基化扫描 =="
$PY -m pilot.cli audit --claims pilot/claims.methylation.json --out pilot/results/methylation_audit.md >/dev/null

echo "== 7. 全量测试 =="
$PY -m pytest -q

echo "== 完成：报告在 pilot/results/ =="
$PY -m pilot.cli datasets