"""result_bridge.py — 实测结果 → 候选假设的证据回流（M3）。

把执行产出的 results.json 转成：
  1) 追加到选中候选的 evidence 列表（可审计的"实测记录"）；
  2) 一段结构化摘要文本，供下一轮 proposer 上下文携带（闭环的关键信息传递）。
"""
from __future__ import annotations

from typing import Any


def build_evidence_entry(candidate_id: str, results: dict[str, Any], reward: int) -> str:
    """把 results.json 压缩成一条证据记录（文本行，附于候选 evidence）。"""
    outcome = results.get("outcome", "unknown")
    program = results.get("program", {})
    baseline = results.get("baseline", {})
    ridge = results.get("ridge", {})
    parts = [
        f"[exec-record] candidate={candidate_id}",
        f"  verifier_reward={reward}",
        f"  outcome={outcome}",
        f"  program_genes={program.get('n_genes', program.get('n_genes'))}",
        f"  near_threshold_genes={program.get('near_threshold_n')}",
        f"  context_contrast={baseline.get('context_contrast')}",
        f"  p_value={baseline.get('p_value')}",
        f"  composition_robust={ridge.get('composition_robust')}",
        f"  justification={str(results.get('justification', ''))[:300]}",
    ]
    return "\n".join(parts)


def build_next_round_context(results: dict[str, Any]) -> str:
    """生成下一轮 proposer 可以消费的实测证据摘要。"""
    outcome = results.get("outcome", "unknown")
    n = results.get("program", {}).get("n_genes", 0)
    near = results.get("program", {}).get("near_threshold_n", 0)
    if outcome == "adverse" and n == 0:
        return (
            f"EXECUTION RESULT (adverse): the prespecified intervention-associated transcript "
            f"program is EMPTY under the stated criteria ({near} genes passed the |log2FC|>=1.0 "
            "magnitude threshold but failed the >=5/6 directional-consistency requirement). "
            "The context contrast is not supported by the available data. "
            "Revise the hypothesis: e.g. relax/modify the program definition, change the contrast, "
            "or address donor heterogeneity explicitly."
        )
    if outcome == "supportive":
        return (
            f"EXECUTION RESULT (supportive): program of {n} genes detected; context contrast "
            "robust to composition differences."
        )
    return f"EXECUTION RESULT ({outcome}): program of {n} genes; see evidence for details."