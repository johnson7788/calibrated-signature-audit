"""make_html.py — 把 manuscript.md 转成可打印的 HTML（含图）。"""
from pathlib import Path
import markdown

root = Path(__file__).resolve().parent
md = (root / "manuscript.md").read_text(encoding="utf-8")
body = markdown.markdown(md, extensions=["tables", "fenced_code"])

css = """
body { max-width: 860px; margin: 2rem auto; padding: 0 1rem;
       font-family: -apple-system, "Helvetica Neue", Arial, sans-serif;
       line-height: 1.6; color: #111; }
h1 { font-size: 1.6rem; line-height: 1.3; }
h2 { border-bottom: 2px solid #333; padding-bottom: .2rem; margin-top: 2rem; }
h3 { margin-top: 1.5rem; }
table { border-collapse: collapse; width: 100%; margin: 1rem 0; font-size: .9rem; }
th, td { border: 1px solid #ccc; padding: .4rem .6rem; text-align: left; }
code { background: #f4f4f4; padding: .1rem .3rem; border-radius: 3px; }
blockquote { border-left: 3px solid #999; margin-left: 0; padding-left: 1rem; color: #444; }
hr { border: none; border-top: 1px solid #ddd; margin: 2rem 0; }
@media print { body { max-width: none; } a { color: inherit; text-decoration: none; } }
"""
figs = """
<h2>Figures</h2>
""" + "".join(
    f"<figure style='margin:1.5rem 0'><img src='figures/{name}' style='max-width:100%'>"
    f"<figcaption style='color:#444;font-size:.9rem'>{cap}</figcaption></figure>"
    for name, cap in [
        ("fig1_fpr_calibration.png", "Figure 1. Nominal versus calibrated false-positive rates."),
        ("fig2_null_distribution.png", "Figure 2. Gene-set null distributions and a real signature."),
        ("fig3_replication_heatmap.png", "Figure 3. Replication matrix under calibration."),
        ("fig4_threshold_sensitivity.png", "Figure 4. Threshold sensitivity of the verdict."),
    ]
)
html = f"<!doctype html><html><head><meta charset='utf-8'><title>Manuscript</title><style>{css}</style></head><body>{body}{figs}</body></html>"
(root / "manuscript.html").write_text(html, encoding="utf-8")
print("wrote", root / "manuscript.html")
