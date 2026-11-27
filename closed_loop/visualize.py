"""visualize.py — 从 campaign 回放生成假设树（含实测结果标注）。

输入：replay JSONL（每行一个 Episode：candidates 含 evidence 与 score、selected_id）
输出：stdout 文本树 + closed_loop/data/hypothesis_tree.md（文本树 + Mermaid 图）
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT_MD = ROOT / "data" / "hypothesis_tree.md"


def _outcome_from_evidence(evidence: list[str]) -> str:
    for line in evidence:
        m = re.search(r"outcome=(\w+)", line)
        if m:
            return m.group(1)
    return "not_run"


def _short(text: str, n: int = 90) -> str:
    text = " ".join(str(text).split())
    return text if len(text) <= n else text[: n - 1] + "…"


def visualize(episodes: list[dict]) -> str:
    lines: list[str] = []
    lines.append("# 假设树与实测结果标注")
    lines.append("")
    mermaid: list[str] = ["```mermaid", "graph TD"]

    selected_ids: set[str] = set()
    sel_outcome: dict[str, str] = {}
    for ep in episodes:
        if ep.get("selected_id"):
            selected_ids.add(ep["selected_id"])

    # 先收集选中候选的 outcome（供父节点标注）
    for ep in episodes:
        for c in ep.get("candidates", []):
            if c["id"] in selected_ids:
                sel_outcome[c["id"]] = _outcome_from_evidence(c.get("evidence", []))

    # 文本树
    for ep in episodes:
        num = ep["number"]
        lines.append(f"## Episode {num}（status={ep.get('status', 'completed')}）")
        lines.append("")
        for c in ep.get("candidates", []):
            mark = "⭐" if c["id"] == ep.get("selected_id") else "  "
            parents = c.get("parents") or []
            label = f"{mark} {c['id']}"
            if parents:
                label += f"  ^ parents={parents}"
            lines.append(f"- **{label}**  score={c.get('score', 0.0):.1f}")
            lines.append(f"  - claim: {_short(c['claim'], 110)}")
            if c["id"] in sel_outcome:
                lines.append(f"  - **exec outcome: {sel_outcome[c['id']]}**")
        lines.append("")

    # Mermaid 节点行（每个候选定义一次，避免重复定义覆盖）
    node_ids = set()
    for ep in episodes:
        for c in ep.get("candidates", []):
            mid = _mid(c["id"])
            if mid in node_ids:
                continue
            node_ids.add(mid)
            mermaid.append(f'    {mid}["{_short(c["id"], 24)} {sel_outcome.get(c["id"], "")}"]')
    # Mermaid 边行（血缘）
    for ep in episodes:
        for c in ep.get("candidates", []):
            for p in c.get("parents") or []:
                mermaid.append(f'    {_mid(p)} --> {_mid(c["id"])}')

    lines.append("## Mermaid（可渲染树）")
    lines.append("")
    lines.append("\n".join(dict.fromkeys(mermaid)) + "\n```")
    return "\n".join(lines)


def _mid(node_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "_", node_id)[:40] or "node"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--replay", default=str(ROOT / "data" / "campaign.jsonl"))
    ap.add_argument("--out", default=str(OUT_MD))
    args = ap.parse_args()

    episodes = [json.loads(line) for line in Path(args.replay).read_text(encoding="utf-8").splitlines() if line.strip()]
    if not episodes:
        raise SystemExit(f"no episodes in {args.replay}")
    text = visualize(episodes)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()