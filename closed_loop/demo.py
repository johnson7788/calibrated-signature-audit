"""demo.py — 一键演示入口（M4）。

两种模式：
  python -m closed_loop.demo --offline             # 用已有 campaign.jsonl 生成假设树（无需 API key）
  python -m closed_loop.demo --iterations 2        # 跑一轮新闭环战役 + 生成假设树（需要 DISCOVERY_RSI_API_KEY）
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from .run import run_campaign
from .visualize import visualize

ROOT = Path(__file__).resolve().parent
REPLAY = ROOT / "data" / "campaign.jsonl"
TREE = ROOT / "data" / "hypothesis_tree.md"


def main() -> None:
    ap = argparse.ArgumentParser(description="DiscoveryRSI closed-loop demo")
    ap.add_argument("--offline", action="store_true", help="只可视化已有回放，不调用 LLM")
    ap.add_argument("--iterations", type=int, default=2)
    ap.add_argument("--replay", default=str(REPLAY))
    args = ap.parse_args()

    if not args.offline:
        key = os.environ.get("DISCOVERY_RSI_API_KEY")
        if not key:
            raise SystemExit("offline 模式需要 --offline；在线模式需要 DISCOVERY_RSI_API_KEY")
        print(f"== 运行闭环战役（{args.iterations} 轮）==")
        run_campaign(args.iterations, args.replay)

    episodes = [
        json.loads(line)
        for line in Path(args.replay).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not episodes:
        raise SystemExit(f"回放文件为空：{args.replay}")
    tree = visualize(episodes)
    TREE.write_text(tree, encoding="utf-8")
    print(f"\n== 假设树已写入 {TREE} ==")


if __name__ == "__main__":
    main()