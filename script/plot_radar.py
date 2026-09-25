"""Radar chart of primary metrics across all 14 benchmarks, comparing
Prev. SOTA against OpenAgency (v4)."""
import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = json.load(open(ROOT / "data" / "benchmark_results.json"))["benchmarks"]

# Axis order: same 3 categories as Figure 2 (General QA, Long-horizon, Production-oriented)
axes_config = [
    # (label, baseline, v4, category)
    ("HumanEval",       DATA["HumanEval"]["prev_sota"],       DATA["HumanEval"]["evolution"]["v4"],       "general"),
    ("MBPP",            DATA["MBPP"]["prev_sota"],            DATA["MBPP"]["evolution"]["v4"],            "general"),
    ("GSM8K",           DATA["GSM8K"]["prev_sota"],           DATA["GSM8K"]["evolution"]["v4"],           "general"),
    ("MATH",            DATA["MATH"]["prev_sota"],            DATA["MATH"]["evolution"]["v4"],            "general"),
    ("HotpotQA",        DATA["HotpotQA"]["prev_sota"],        DATA["HotpotQA"]["evolution"]["v4"],        "general"),
    ("SWE-bench",       DATA["SWE-bench"]["prev_sota"],       DATA["SWE-bench"]["evolution"]["v4"],       "long"),
    ("DeepPlanning",    DATA["DeepPlanning"]["prev_sota"],    DATA["DeepPlanning"]["evolution"]["v4"],    "long"),
    ("HLE",             DATA["HLE"]["prev_sota"],             DATA["HLE"]["evolution"]["v4"],             "long"),
    ("DevEval",         DATA["DevEval"]["prev_sota"],         DATA["DevEval"]["evolution"]["v4"],         "prod"),
    ("DDR-Bench",       DATA["DDR-Bench"]["prev_sota"],       DATA["DDR-Bench"]["evolution"]["v4"],       "prod"),
    ("TheAgentCompany", DATA["TheAgentCompany"]["prev_sota"], DATA["TheAgentCompany"]["evolution"]["v4"], "prod"),
    ("MARBLE",          DATA["MARBLE"]["prev_sota"],          DATA["MARBLE"]["evolution"]["v4"],          "prod"),
    ("AutomationBench", DATA["AutomationBench"]["prev_sota"], DATA["AutomationBench"]["evolution"]["v4"], "prod"),
    ("OfficeQA Pro",    DATA["OfficeQA"]["prev_sota"],        DATA["OfficeQA"]["evolution"]["v4"],        "prod"),
]

labels = [a[0] for a in axes_config]
baseline = [a[1] for a in axes_config]
v4       = [a[2] for a in axes_config]

N = len(labels)
angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
# close polygon
baseline_c = baseline + baseline[:1]
v4_c       = v4 + v4[:1]
angles_c   = angles + angles[:1]

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif", "Times New Roman"],
    "font.size": 8.5,
    "axes.linewidth": 0.6,
})

fig, ax = plt.subplots(figsize=(5.0, 5.0), subplot_kw=dict(polar=True))

# baseline polygon
c_base = "#7f7f7f"
c_ours = "#c1272d"
ax.plot(angles_c, baseline_c, color=c_base, linewidth=1.4, linestyle="--", label="Prev. SOTA")
ax.fill(angles_c, baseline_c, color=c_base, alpha=0.15)
# OpenAgency v4 polygon
ax.plot(angles_c, v4_c, color=c_ours, linewidth=1.8, linestyle="-", label="OpenAgency")
ax.fill(angles_c, v4_c, color=c_ours, alpha=0.22)

ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)

# axis tick labels colored by category
cat_color = {"general": "#08519c", "long": "#c0392b", "prod": "#7b3f9d"}
ax.set_xticks(angles)
ax.set_xticklabels([""] * N)  # we'll place custom text
for ang, (lab, _, _, cat) in zip(angles, axes_config):
    r = 108  # push labels outside the axis
    ha = "center"
    ax.text(ang, r, lab, ha=ha, va="center", fontsize=8,
            color=cat_color[cat], fontweight="bold")

# radial ticks
ax.set_ylim(0, 100)
ax.set_yticks([25, 50, 75, 100])
ax.set_yticklabels(["25", "50", "75", "100"], fontsize=6.5, color="#666")
ax.set_rlabel_position(0)
ax.grid(color="lightgray", linewidth=0.5)

ax.legend(loc="upper right", bbox_to_anchor=(1.30, 1.08), frameon=False, fontsize=8.5)

# category legend at bottom
handles = [plt.Line2D([0], [0], marker="s", color="w", markerfacecolor=cat_color["general"],
                       markersize=8, label="General QA Tasks"),
           plt.Line2D([0], [0], marker="s", color="w", markerfacecolor=cat_color["long"],
                       markersize=8, label="Long-horizon Tasks"),
           plt.Line2D([0], [0], marker="s", color="w", markerfacecolor=cat_color["prod"],
                       markersize=8, label="Production-oriented Tasks")]
ax.legend(handles=[plt.Line2D([0], [0], color=c_base, ls="--", lw=1.4, label="Prev. SOTA"),
                    plt.Line2D([0], [0], color=c_ours, ls="-", lw=1.8, label="OpenAgency")]
                   + handles,
          loc="lower center", bbox_to_anchor=(0.5, -0.22), frameon=False, ncol=2, fontsize=7.5)

plt.tight_layout()
out = ROOT / "figures" / "main_radar.pdf"
plt.savefig(out, bbox_inches="tight")
print(f"saved {out}")
