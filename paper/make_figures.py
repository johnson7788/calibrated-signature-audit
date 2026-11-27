"""make_figures.py — 论文图（校准主线）。

图：
  fig1_fpr_calibration.png   名义 vs 置换校准的误判率（α=0.05，三队列）
  fig2_null_distribution.png 随机签名零分布 + 真实签名位置（两个队列）
  fig3_replication_heatmap.png 复现矩阵（应用示例）
  fig4_threshold_sensitivity.png 阈值敏感性

数据来源：paper/null_calibration.csv、paper/calibration_perm.csv、paper/realcal.csv、
          pilot/results/replication_matrix.md、pilot/results/alpha_sensitivity.md
"""
from __future__ import annotations

import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
RESULTS = ROOT / "pilot" / "results"
OUT = PAPER / "figures"
OUT.mkdir(parents=True, exist_ok=True)

COHORTS = ["GSE50760", "GSE95132", "GSE110224"]
VERDICT_COLOR = {"robust": "#2a9d8f", "fragile": "#e9c46a", "not_reproduced": "#e76f51"}


def fig_fpr():
    null = pd.read_csv(PAPER / "null_calibration.csv")
    perm = pd.read_csv(PAPER / "calibration_perm.csv")
    nominal = []
    calibrated = []
    for c in COHORTS:
        n = null[(null.cohort == c) & (null.alpha == 0.05) & (null.min_stable == 0.8)].fpr.iloc[0]
        p = perm[perm.cohort == c].fpr_perm_005.iloc[0]
        nominal.append(n * 100)
        calibrated.append(p * 100)

    x = np.arange(len(COHORTS))
    w = 0.34
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    ax.bar(x - w / 2, nominal, w, label="Nominal test (alpha = 0.05)", color="#e76f51")
    ax.bar(x + w / 2, calibrated, w, label="Permutation calibration", color="#2a9d8f")
    ax.axhline(5, color="#333", ls="--", lw=1, label="Nominal 5%")
    for i, (n, p) in enumerate(zip(nominal, calibrated)):
        ax.text(i - w / 2, n + 1.2, f"{n:.1f}%", ha="center", fontsize=8,
                bbox=dict(facecolor="white", edgecolor="none", pad=0.5, alpha=0.85))
        ax.text(i + w / 2, p + 1.2, f"{p:.1f}%", ha="center", fontsize=8,
                bbox=dict(facecolor="white", edgecolor="none", pad=0.5, alpha=0.85))
    ax.set_xticks(x, COHORTS)
    ax.set_ylabel("False-positive rate (%)")
    ax.set_title("Random signatures declared 'robust' (size 100)", fontsize=10)
    ax.legend(fontsize=7, frameon=False)
    ax.set_ylim(0, max(nominal) * 1.25)
    fig.tight_layout()
    fig.savefig(OUT / "fig1_fpr_calibration.png", dpi=300)
    plt.close(fig)


def fig_null():
    """从 pilot 数据重算两个队列的随机签名零分布（种子固定）。"""
    from pilot.audit import load_matrix, load_metadata, to_log2x

    cfg = {
        "GSE95132": dict(matrix="pilot/data/gse95132/GSE95132_counts.tsv.gz",
                         meta="pilot/data/gse95132/design.json", value_type="counts",
                         col="tissue", a="tumor", b="adjacent", pair="patient"),
        "GSE110224": dict(matrix="pilot/data/gse110224/matrix.tsv.gz",
                          meta="pilot/data/gse110224/design.json", value_type="log",
                          col="condition", a="cancer", b="normal", pair="patient"),
    }
    rng = np.random.default_rng(7)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.2))
    real_effect = {"GSE95132": 0.40, "GSE110224": 1.97}  # realcal.csv 中的自验证效应（示例）
    for ax, name in zip(axes, ["GSE95132", "GSE110224"]):
        c = cfg[name]
        expr = to_log2x(load_matrix(Path(c["matrix"])), c["value_type"])
        meta = load_metadata(Path(c["meta"]))
        meta["sample_id"] = meta["sample_id"].astype(str)
        ds = []
        for key, grp in meta.groupby(c["pair"]):
            a = grp[grp[c["col"]] == c["a"]]["sample_id"]
            b = grp[grp[c["col"]] == c["b"]]["sample_id"]
            if len(a) == 1 and len(b) == 1:
                ds.append(expr[a.iloc[0]] - expr[b.iloc[0]])
        deltas = pd.DataFrame(ds)
        G = deltas.shape[1]
        null = np.array([deltas.iloc[:, rng.choice(G, 100, replace=False)].mean(axis=1).values.mean()
                         for _ in range(2000)])
        ax.hist(null, bins=40, color="#8ecae6", edgecolor="white", alpha=0.9)
        ax.axvline(0, color="#333", ls=":", lw=1)
        ax.axvline(real_effect[name], color="#e76f51", lw=2, label="real signature")
        ax.set_title(f"{name}: random 100-gene signatures", fontsize=9)
        ax.set_xlabel("signature effect (paired delta)")
        ax.legend(fontsize=7, frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "fig2_null_distribution.png", dpi=300)
    plt.close(fig)


def fig_matrix():
    text = (RESULTS / "replication_matrix.md").read_text(encoding="utf-8")
    data = {"up": {}, "down": {}}
    section = None
    for line in text.splitlines():
        if line.startswith("## 上调签名"):
            section = "up"
            continue
        if line.startswith("## 下调签名"):
            section = "down"
            continue
        if section and line.startswith("| top-"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            size = int(cells[0].replace("top-", ""))
            data[section][size] = {}
            for cohort, cell in zip(COHORTS, cells[1:]):
                m = re.match(r"(\w+) \(([+-]?[\d.]+)\)", cell)
                if m:
                    data[section][size][cohort] = (m.group(1), float(m.group(2)))
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6))
    for ax, direction, label in zip(axes, ("up", "down"), ("Up-regulated", "Down-regulated")):
        sizes = sorted(data[direction])
        mat = np.array([[data[direction][s][c][1] for c in COHORTS] for s in sizes])
        im = ax.imshow(mat, cmap="RdBu_r", vmin=-3, vmax=3, aspect="auto")
        ax.set_xticks(range(len(COHORTS)), COHORTS, rotation=20, fontsize=8)
        ax.set_yticks(range(len(sizes)), [f"top-{s}" for s in sizes], fontsize=8)
        for i, s in enumerate(sizes):
            for j, c in enumerate(COHORTS):
                v, e = data[direction][s][c]
                ax.text(j, i, f"{v}\n{e:+.2f}", ha="center", va="center", fontsize=7)
        ax.set_title(label, fontsize=10)
        fig.colorbar(im, ax=ax, shrink=0.8, label="effect")
    fig.suptitle("Replication matrix (application under calibration)", fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT / "fig3_replication_heatmap.png", dpi=300)
    plt.close(fig)


def fig_threshold():
    rows = []
    for line in (RESULTS / "alpha_sensitivity.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("| splitdown-a"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            m = re.search(r"alpha=([\d.]+)", cells[0])
            rows.append((float(m.group(1)), cells[-1].strip("*")))
    rows.sort()
    fig, ax = plt.subplots(figsize=(5.4, 2.6))
    alphas = [f"alpha={r[0]}" for r in rows]
    colors = [VERDICT_COLOR.get(r[1], "#adb5bd") for r in rows]
    ax.bar(alphas, [1] * len(rows), color=colors, edgecolor="#333")
    for i, (a, v) in enumerate(rows):
        ax.text(i, 0.5, v, ha="center", va="center", fontsize=9)
    ax.set_yticks([])
    ax.set_title("Same claim, different alpha -> different verdict", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / "fig4_threshold_sensitivity.png", dpi=300)
    plt.close(fig)


def main():
    fig_fpr()
    fig_null()
    fig_matrix()
    fig_threshold()
    for p in sorted(OUT.glob("*.png")):
        print(f"wrote {p} ({p.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()