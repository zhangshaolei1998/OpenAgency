"""Token budget vs primary metric across evolution rounds.
- All lines dashed
- Markers v1..v4 colored light-to-dark (evolution stage)
- Benchmark distinguished by line color + endpoint label
- No baseline points
"""
import json
from pathlib import Path
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
TOKEN = json.load(open(ROOT / "data" / "token_budget.json"))
TOKEN = {k: v for k, v in TOKEN.items() if isinstance(v, dict) and "v1" in v}

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif", "Times New Roman"],
    "font.size": 10,
    "axes.linewidth": 0.7,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

fig, ax = plt.subplots(figsize=(8.0, 4.2))

general_qa = ["HumanEval", "MBPP", "GSM8K", "MATH", "HotpotQA"]
qa_colors = ["#a6cee3", "#6baed6", "#3182bd", "#08519c", "#54278f", "#3f007d"]

other_line = {
    "SWE-bench":       "#c0392b",
    "DevEval":         "#e67300",
    "DDR-Bench":       "#2e8b57",
    "TheAgentCompany": "#7b3f9d",
    "DeepPlanning":    "#c9a86a",
    "MARBLE":          "#1f77b4",
    "AutomationBench": "#17becf",
    "HLE":             "#8c564b",
    "OfficeQA":        "#e377c2",
}

version_shades = ["#fee0b6", "#fdae61", "#f46d43", "#c1272d"]

MARKER = "o"


def plot_line(bench, line_color):
    series = TOKEN[bench]
    xs = [series[v]["tokens_k"] for v in ["v1", "v2", "v3", "v4"]]
    ys = [series[v]["metric"] for v in ["v1", "v2", "v3", "v4"]]
    # dashed line connecting v1..v4 in benchmark color
    ax.plot(xs, ys, linestyle="--", color=line_color, linewidth=1.2, alpha=0.75, zorder=2)
    # markers colored by evolution stage
    for i in range(4):
        ax.plot(xs[i], ys[i], marker=MARKER, markersize=6,
                markerfacecolor=version_shades[i],
                markeredgecolor="black", markeredgewidth=0.4, zorder=3)
    # benchmark label at v4 endpoint
    ax.annotate(bench, xy=(xs[-1], ys[-1]), xytext=(6, 0),
                textcoords="offset points", fontsize=7, color=line_color, va="center")


for i, bench in enumerate(general_qa):
    plot_line(bench, qa_colors[i])

for bench, color in other_line.items():
    plot_line(bench, color)

ax.set_xlabel("Avg model tokens per instance (K)")
ax.set_ylabel("Primary metric (%)")
ax.set_xlim(6, 76)
ax.grid(True, linestyle=":", color="gray", linewidth=0.5, alpha=0.6)

# legend for version stages
legend_handles = [
    plt.Line2D([0], [0], marker=MARKER, color="gray", markerfacecolor=version_shades[i],
               markeredgecolor="black", markeredgewidth=0.4, linestyle="none",
               markersize=6, label=f"v{i+1}")
    for i in range(4)
]
ax.legend(handles=legend_handles, loc="lower right", frameon=False, fontsize=8,
          ncol=4, handlelength=0.8, columnspacing=0.8)

plt.tight_layout()
out = ROOT / "figures" / "token_vs_score.pdf"
plt.savefig(out, bbox_inches="tight")
print(f"saved {out}")
