"""CLI 冒烟测试。"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "pilot.cli", *args],
        cwd=ROOT, capture_output=True, text=True, timeout=120,
    )


def test_help_lists_commands():
    r = _run("--help")
    assert r.returncode == 0
    for cmd in ("audit", "split-half", "matrix", "cross", "prepare-microarray"):
        assert cmd in r.stdout


def test_datasets_lists_registered_cohorts():
    r = _run("datasets")
    assert r.returncode == 0
    assert "GSE50760" in r.stdout
    assert "GSE48684" in r.stdout


def test_unknown_command_exits_nonzero():
    r = _run("nope")
    assert r.returncode == 1
