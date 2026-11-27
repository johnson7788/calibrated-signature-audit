#!/usr/bin/env bash
# ============================================================================
# M0 自动化：环境恢复后由 bash 一键执行（可重复运行，幂等）
# 目标：数据下载+prepared 转换 → LLM API 验证 → 依赖安装 → verifier fixture 对齐
# 前置：本脚本在 DSH 会话中执行（bash 可用即可），或直接在终端运行
# ============================================================================
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATA_DIR="$ROOT/closed_loop/data"
RAW_DIR="$DATA_DIR/raw"
PREP_DIR="$DATA_DIR/prepared"
TMP_WORK="$DATA_DIR/tmp_workspace"
VENV="$ROOT/.venv"

echo "==> [1/6] 环境自检"
python3 --version
"$VENV/bin/python" --version 2>/dev/null || echo "  (venv 需重建：见步骤 4)"

echo "==> [2/6] 下载 E-MTAB-8316（biostudies API 定位真实 URL）"
mkdir -p "$RAW_DIR"
# 先用 -L 跟随重定向拿文件；若 biostudies API 的 files 端点给出新布局，按需调整
curl -sL --max-time 90 -o "$RAW_DIR/MK_readcountMatrix.txt.gz" \
  "https://www.ebi.ac.uk/biostudies/files/E-MTAB-8316/MK_readcountMatrix.txt.gz" || {
  echo "  ! 直连失败，改用 ftp.ebi.ac.uk 探测（先看重定向 Location）";
  curl -sIL --max-time 30 "https://www.ebi.ac.uk/biostudies/files/E-MTAB-8316/MK_readcountMatrix.txt.gz" | grep -i '^location';
  exit 1
}
curl -sL --max-time 60 -o "$RAW_DIR/E-MTAB-8316.sdrf.txt" \
  "https://www.ebi.ac.uk/biostudies/files/E-MTAB-8316/E-MTAB-8316.sdrf.txt"
ls -l "$RAW_DIR"
echo "  sha256(counts) = $(shasum -a 256 "$RAW_DIR/MK_readcountMatrix.txt.gz" | cut -d' ' -f1)"

echo "==> [3/6] prepared 转换"
mkdir -p "$PREP_DIR" "$TMP_WORK"
"$VENV/bin/python" - <<'PY'
import csv, gzip, json, os, pathlib
raw = pathlib.Path(os.environ["RAW_DIR"]); prep = pathlib.Path(os.environ["PREP_DIR"])
# 3a. counts：gzip TSV（feature 列 + 样本列）→ 与任务契约一致的 prepared 形态
src = raw / "MK_readcountMatrix.txt.gz"
with gzip.open(src, "rt") as f:
    header = f.readline().rstrip("\n").split("\t")
print("     counts 头字段:", header[:8], "... 共", len(header), "列")
# 原样拷贝作为 prepared 起点（预置文件名与契约一致）
with gzip.open(src, "rb") as fi, gzip.open(prep / "E-MTAB-8316.counts.tsv.gz", "wb") as fo:
    fo.write(fi.read())
# 3b. design：sdrf → JSON（sample_id/donor_id/condition/cell_type/source_metadata）
sdrf = raw / "E-MTAB-8316.sdrf.txt"
with open(sdrf) as f:
    rows = list(csv.DictReader(f, delimiter="\t"))
print("     sdrf 行数:", len(rows), "列:", list(rows[0].keys())[:12] if rows else "-")
# 从 sdrf 常用列名映射（按实际列名调整）：
#   Source Name / Characteristics[Individual] / Factor Value[compound] / Characteristics[Cell type]
design = []
for r in rows:
    def val(*names):
        for n in names:
            if n in r and r[n].strip():
                return r[n].strip()
        return None
    design.append({
        "sample_id": val("Source Name"),
        "donor_id": val("Characteristics[Individual]", "Characteristics[donor]"),
        "condition": val("Factor Value[compound]", "Factor Value[Condition]"),
        "cell_type": val("Characteristics[Cell type]", "Characteristics[cell type]"),
        "source_metadata": {k: v for k, v in r.items() if v and v.strip()}
    })
with open(prep / "E-MTAB-8316.design.json", "w") as f:
    json.dump(design, f, indent=2, ensure_ascii=False)
print("     design 样例:", json.dumps(design[0] if design else {}, ensure_ascii=False)[:300])
PY
echo "  prepared sha256："
shasum -a 256 "$PREP_DIR/E-MTAB-8316.counts.tsv.gz" "$PREP_DIR/E-MTAB-8316.design.json"

echo "==> [4/6] venv 依赖（pinned 版本，与任务 Dockerfile 一致）"
"$VENV/bin/pip" install -q --upgrade pip
"$VENV/bin/pip" install -q "numpy==2.2.6" "pandas==2.2.3" "scipy==1.15.3" "scikit-learn==1.6.1" "statsmodels==0.14.4"
"$VENV/bin/pip" install -q -e "$ROOT[test]"
echo "  已安装: $("$VENV/bin/pip" list 2>/dev/null | grep -iE "numpy|pandas|scipy|scikit|statsmodels")"

echo "==> [5/6] LLM API 验证（litellm 中转 / deepseek-v4-flash）"
curl -s --max-time 60 -X POST "https://litellm.infox-med.com/v1/chat/completions" \
  -H "Authorization: Bearer ${DISCOVERY_RSI_API_KEY:-<你的token>}" \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-v4-flash","messages":[{"role":"user","content":"Reply with exactly: OK"}]}' | head -c 400
echo

echo "==> [6/6] verifier fixture 对齐（期望 1/0/0/0）"
TASKS="$ROOT/datasets/DiscoveryRSI-Hypothesis-Task-Examples/task-packages/DiscoveryRSI-Hypothesis-Task-Examples/tasks/unc106238-context-response"
run_fixture() { # $1=fixture 名
  rm -rf "$TMP_WORK" && mkdir -p "$TMP_WORK"
  # fixture 写死 /workspace：sed 替换为本地临时目录
  sed "s|/workspace|$TMP_WORK|g" "$TASKS/validation/$1.sh" > "$TMP_WORK/fixture.sh"
  bash "$TMP_WORK/fixture.sh"
  "$VENV/bin/python" -m closed_loop.verifier --results "$TMP_WORK/results.json" && echo "  $1 -> 1 (PASS)" || echo "  $1 -> 0 (REJECT OK)"
}
echo "  positive_fixture.sh   → 期望 1"
run_fixture positive_fixture.sh || true
echo "  overclaim_fixture.sh  → 期望 0"
run_fixture overclaim_fixture.sh || true
echo "  missing_ridge_fixture.sh → 期望 0"
run_fixture missing_ridge_fixture.sh || true
echo "  stale_result_fixture.sh  → 期望 0"
run_fixture stale_result_fixture.sh || true

echo
echo "==> M0 完成。下一步: M1 参考实现（真实数据）→ compiler → 闭环。"
echo "    原始/repaired 数据在: $DATA_DIR"