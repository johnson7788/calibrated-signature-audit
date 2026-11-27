"""run.py — M3 闭环编排：DiscoveryLoop 风格的 propose→critique→select，
选中后接入 compiler→executor→verifier→result_bridge，证据随轮次回流。

不修改原仓库 src/discovery_rsi 的任何代码——闭环逻辑全部在 closed_loop 内。

用法：
  export DISCOVERY_RSI_API_KEY=...
  python -m closed_loop.run --iterations 3 --replay closed_loop/data/campaign.jsonl
"""
from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict
from pathlib import Path
from typing import Any

from discovery_rsi.core import Candidate, Episode, ReplayBuffer

from . import LLMClient
from .compiler import INSTRUCTION, compile_task
from .executor import run_script
from .result_bridge import build_evidence_entry, build_next_round_context
from .verifier import verify_file

ROOT = Path(__file__).resolve().parent
RESULTS_PATH = ROOT / "data" / "prepared" / "results_closed_loop.json"

QUESTION = (
    "In fibroblast-macrophage coculture (E-MTAB-8316), does the magnitude or direction of "
    "the prespecified intervention-associated (UNC106238) transcript response differ between "
    "macrophage-present and macrophage-absent fibroblast contexts in a way not explained by "
    "donor, condition, batch, or sample-composition differences?"
)

_TASK_CTX = ("Target dataset: E-MTAB-8316, 12 samples, 6 donor-specimen pairs, "
             "conditions 'none' (n=6) and 'UNC106238' (n=6).")


def _parse_candidates(ep: int, raw: str, parent: str | None) -> list[Candidate]:
    text = raw.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
    try:
        data = json.loads(text)
        items = data["candidates"]
    except (json.JSONDecodeError, KeyError, TypeError):
        items = [{"claim": text[:400], "plan": "Specify comparator, measurement and falsification criterion.",
                  "alternatives": [], "evidence": []}]
    out: list[Candidate] = []
    for i, x in enumerate(items[:2], 1):
        if not isinstance(x, dict) or not x.get("claim"):
            continue
        out.append(Candidate(
            id=f"episode-{ep}-{i}",
            claim=str(x["claim"])[:1200],
            plan=str(x.get("plan", ""))[:1200],
            alternatives=[str(a)[:300] for a in x.get("alternatives", []) if str(a).strip()],
            evidence=[str(e)[:300] for e in x.get("evidence", []) if str(e).strip()],
            parents=[parent] if parent else [],
        ))
    return out


def _propose(llm: LLMClient, ep: int, history: list[Candidate]) -> list[Candidate]:
    parent = history[-1].id if history else None
    ctx_parts = [QUESTION, _TASK_CTX]
    if history:
        ctx_parts.append(
            "Previous round selected hypothesis and its execution evidence:\n"
            + history[-1].evidence[-1] if history[-1].evidence else "no execution yet"
        )
    prompt = (
        "You are a scientific hypothesis lead. Return ONLY a JSON object:\n"
        '{"candidates": [{"claim": "...", "plan": "...", "alternatives": ["..."], "evidence": ["..."]}, ...]}\n'
        "Each candidate must be a falsifiable research hypothesis with a concrete comparator, "
        "measurable outcome, alternative explanations, and evidence basis. At most 2 candidates.\n\n"
        f"CONTEXT:\n{chr(10).join(ctx_parts)}\nEpisode {ep}; parent={parent}."
    )
    return _parse_candidates(ep, llm.complete(prompt), parent)


def _critique(llm: LLMClient, c: Candidate) -> tuple[float, str]:
    prompt = (
        "Score this research hypothesis 0-10. Return ONLY JSON {\"score\": <0-10 float>, "
        "\"critique\": \"<string>\"}. Require: concrete comparator, measurable outcome, "
        "alternative explanation, evidence provenance, falsification rule.\n"
        + json.dumps({"claim": c.claim[:800], "plan": c.plan[:800], "alternatives": c.alternatives}, ensure_ascii=False)
    )
    text = llm.complete(prompt).strip()
    try:
        data = json.loads(text)
        return float(data["score"]), str(data["critique"])[:500]
    except (json.JSONDecodeError, KeyError, TypeError):
        return 0.0, text[:500]


def _execute_and_bridge(c: Candidate) -> dict[str, Any]:
    """编译(LLM 提取参数) → 执行 → 验证 → 回流。返回 results dict。"""
    compile_task(Path(INSTRUCTION).read_text(encoding="utf-8"), RESULTS_PATH, llm=None,
                 out_name="analysis_closed_loop.py")
    res = run_script(ROOT / "generated" / "analysis_closed_loop.py", timeout=180.0, max_mem_mb=4096)
    if res["returncode"] != 0:
        c.evidence.append(f"[exec-record] execution failed: {res['stderr'][-300:]}")
        return {"outcome": "exec_failed", "program": {}, "baseline": {}, "ridge": {},
                "justification": "execution failed"}
    results = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    reward, errors = verify_file(RESULTS_PATH)
    if reward == 0:
        c.evidence.append(f"[exec-record] verifier REJECTED output: {errors[:3]}")
    c.evidence.append(build_evidence_entry(c.id, results, reward))
    c.critique += f" [executed reward={reward}]"
    return results


def run_campaign(iterations: int, replay_path: str) -> list[Episode]:
    llm = LLMClient()
    replay = ReplayBuffer(replay_path)
    episodes: list[Episode] = []
    history: list[Candidate] = []

    for ep in range(1, iterations + 1):
        candidates = _propose(llm, ep, history)
        if not candidates:
            episodes.append(Episode(ep, [], None, "no_candidates"))
            continue
        for c in candidates:
            c.score, c.critique = _critique(llm, c)
        selected = max(candidates, key=lambda c: (c.score, c.id))
        _execute_and_bridge(selected)
        history.append(selected)
        episodes.append(Episode(ep, candidates, selected.id))
        replay.append(Episode(ep, candidates, selected.id))

    return episodes


def main() -> None:
    ap = argparse.ArgumentParser(description="closed_loop campaign")
    ap.add_argument("--iterations", type=int, default=2)
    ap.add_argument("--replay", default=str(ROOT / "data" / "campaign.jsonl"))
    args = ap.parse_args()
    if not os.environ.get("DISCOVERY_RSI_API_KEY"):
        raise SystemExit("set DISCOVERY_RSI_API_KEY first")
    episodes = run_campaign(args.iterations, args.replay)
    print(json.dumps(
        [{"number": e.number, "selected_id": e.selected_id, "status": e.status,
          "candidate_count": len(e.candidates)} for e in episodes],
        ensure_ascii=False, indent=2))
    last = episodes[-1].candidates
    sel = {e.selected_id: e for e in episodes}
    for e in episodes:
        for c in e.candidates:
            if c.id == e.selected_id and c.evidence:
                print(f"\n--- episode {e.number} selected {c.id} evidence ---")
                print("\n".join(c.evidence[-3:])[:800])


if __name__ == "__main__":
    main()