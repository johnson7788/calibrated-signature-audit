"""pilot 引擎测试：半样本切分、签名推导、阈值扫描渲染。"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd
import pytest

from pilot.audit import render_markdown
from pilot.split_half import derive_signature, split_pairs


def _meta(n_patients: int = 6) -> pd.DataFrame:
    recs = []
    for i in range(1, n_patients + 1):
        pid = f"P{i}"
        recs.append({"sample_id": f"{pid}_t", "patient": pid, "condition": "tumor"})
        recs.append({"sample_id": f"{pid}_n", "patient": pid, "condition": "normal"})
    return pd.DataFrame(recs)


class TestSplitPairs:
    def test_even_split(self):
        train, test = split_pairs(_meta(6), "patient", "condition", "tumor", "normal", 0.5)
        assert len(train) == 3 and len(test) == 3
        assert set(train).isdisjoint(test)

    def test_incomplete_pairs_excluded(self):
        meta = _meta(4)
        meta = meta[~((meta.patient == "P1") & (meta.condition == "normal"))]  # P1 缺 normal
        train, test = split_pairs(meta, "patient", "condition", "tumor", "normal", 0.5)
        assert "P1" not in train + test
        assert len(train) + len(test) == 3

    def test_train_frac_bounds(self):
        train, test = split_pairs(_meta(4), "patient", "condition", "tumor", "normal", 0.9)
        assert len(test) >= 1 and len(train) >= 1


class TestDeriveSignature:
    def test_up_and_down_selected_by_delta(self):
        rng = np.random.default_rng(0)
        genes = [f"G{i}" for i in range(10)]
        meta = _meta(4)
        train = ["P1", "P2"]
        cols = {}
        for pid in train:
            t = pd.Series(rng.normal(5, 0.1, len(genes)), index=genes)
            # 前 3 个基因 tumor 高 2 个 log 单位，后 3 个低 2 个
            t.iloc[:3] += 2.0
            t.iloc[-3:] -= 2.0
            cols[f"{pid}_t"] = t
            cols[f"{pid}_n"] = pd.Series(rng.normal(5, 0.1, len(genes)), index=genes)
        expr = pd.DataFrame(cols)
        up, down, _ = derive_signature(expr, meta, train, "condition", "tumor", "normal", "patient", 5, 1.5)
        assert len(up) == 3 and len(down) == 3
        assert all(g.startswith("G") for g in up + down)

    def test_threshold_filters_weak_effects(self):
        genes = ["A", "B"]
        meta = _meta(2)
        expr = pd.DataFrame({"P1_t": [2.0, 5.0], "P1_n": [0.0, 5.0],
                             "P2_t": [2.0, 5.0], "P2_n": [0.0, 5.0]}, index=genes)
        up, down, _ = derive_signature(expr, meta, ["P1", "P2"], "condition", "tumor", "normal",
                                       "patient", 10, 1.5)
        assert up == ["A"] and down == []


class TestRender:
    def test_methods_block_present(self):
        from pilot.audit import AuditResult

        r = AuditResult("c1", "claim", "signature", n_features=10, effect=0.5, p_value=0.01,
                        verdict="robust",
                        details={"test": "wilcoxon_signed_rank", "alpha": 0.05,
                                 "min_effect": 0.5, "min_stable_fraction": 0.8})
        md = render_markdown([r])
        assert "方法学元数据" in md
        assert "wilcoxon_signed_rank" in md
        assert "robust" in md