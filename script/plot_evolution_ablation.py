"""Evolving-space ablation bar chart. Three nested spaces x three benchmarks."""
import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
D = json.load(open(ROOT / "data" / "evolution_ablation.json"))

BENCH = D["benchmarks"]
variants = ["full", "fixed_count", "division_only"]
labels = [
    "Full evolving space",
    "Fixed agent count",
    "Fixed graph (division only)",
]
colors = ["#c1272d", "#f46d43", "#fdae61"]

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif", "Times New Roman"],
    "font.size": 9,
    "axes.linewidth": 0.7,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

fig, ax = plt.subplots(figsize=(4.9, 3.1))
n = len(BENCH)
x = np.arange(n)
w = 0.26

for j, v in enumerate(variants):
    ys = D["variants"][v]
    offset = (j - 1) * w
    ax.bar(x + offset, ys, width=w * 0.92, color=colors[j],
           edgecolor="black", linewidth=0.4, label=labels[j], zorder=3)
    for i, y in enumerate(ys):
        ax.text(x[i] + offset, y + 1.0, f"{y:.1f}", ha="center",
                va="bottom", fontsize=6.5)

ax.set_xticks(x)
ax.set_xticklabels(BENCH, fontsize=8)
ax.set_ylabel("Primary metric (%)", fontsize=8.5)
ax.set_ylim(0, 122)
ax.tick_params(axis="y", labelsize=8)
ax.grid(axis="y", linestyle=":", color="gray", linewidth=0.5, alpha=0.6, zorder=1)
ax.legend(loc="upper center", ncol=1, frameon=False, fontsize=7.5,
          handlelength=1.4, handletextpad=0.5, labelspacing=0.28,
          borderaxespad=0.1, columnspacing=0.8)

plt.tight_layout()
out = ROOT / "figures" / "evolution_ablation.pdf"
plt.savefig(out, bbox_inches="tight")
print(f"saved {out}")
