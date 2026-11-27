#!/usr/bin/env bash
# upload_hf.sh — 把 dist/hf_upload 上传到 Hugging Face 数据集仓库。
# 用法：
#   export HF_TOKEN=hf_xxx          # 写权限 token
#   export PROXY=http://127.0.0.1:7890   # 可选，默认此值
#   bash scripts/upload_hf.sh
set -euo pipefail
cd "$(dirname "$0")/.."

: "${HF_TOKEN:?请先 export HF_TOKEN（写权限 token）}"
PROXY="${PROXY:-http://127.0.0.1:7890}"
HF_USER="${HF_USER:-johnson7788}"
REPO="${REPO:-calibrated-signature-audit}"
SRC="dist/hf_upload"

[ -d "$SRC" ] || { echo "缺少 $SRC，请先运行打包步骤"; exit 1; }

echo "== 1. 创建仓库（若不存在）=="
curl -s --max-time 60 -x "$PROXY" -X POST "https://huggingface.co/api/repos/create" \
  -H "Authorization: Bearer $HF_TOKEN" -H "Content-Type: application/json" \
  -d "{\"type\":\"dataset\",\"name\":\"$REPO\",\"private\":false}" >/dev/null || true

echo "== 2. 克隆（走代理，token 认证）=="
TMP="$(mktemp -d)"
git -c http.proxy="$PROXY" -c https.proxy="$PROXY" clone \
  "https://${HF_USER}:${HF_TOKEN}@huggingface.co/datasets/${HF_USER}/${REPO}" "$TMP/repo" 2>/dev/null \
  || { echo "克隆失败：检查代理与 token"; exit 1; }

echo "== 3. 复制并推送 =="
cp -R "$SRC"/. "$TMP/repo"/
cd "$TMP/repo"
git config user.name "Zhicai Guo"
git config user.email "363800649@qq.com"
git add -A
git -c http.proxy="$PROXY" -c https.proxy="$PROXY" commit -m "Add manuscript PDF, figures, processed data and calibration tables" || true
git -c http.proxy="$PROXY" -c https.proxy="$PROXY" push

echo "== 完成 =="
echo "https://huggingface.co/datasets/${HF_USER}/${REPO}"
