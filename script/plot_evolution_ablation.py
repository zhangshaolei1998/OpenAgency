"""Evolution component ablation bar chart. Three variants x four benchmarks."""
import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
D = json.load(open(ROOT / "data" / "evolution_ablation.json"))

BENCH = D["benchmarks"]
variants = ["full", "label_only", "shuffled_trace"]
labels = [
    "Full (trace + $q$ + $\\Pi_{\\mathcal{V}}$)",
    "Label only (no trace)",
    "Shuffled trace"
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

fig, ax = plt.subplots(figsize=(7.5, 3.3))
n = len(BENCH)
x = np.arange(n)
w = 0.24

for j, v in enumerate(variants):
    ys = D["variants"][v]
    offset = (j - 1) * w
    ax.bar(x + offset, ys, width=w * 0.95, color=colors[j],
           edgecolor="black", linewidth=0.4, label=labels[j], zorder=3)
    for i, y in enumerate(ys):
        ax.text(x[i] + offset, y + 1.0, f"{y:.1f}", ha="center", va="bottom", fontsize=7)

ax.set_xticks(x)
ax.set_xticklabels(BENCH, fontsize=8.5)
ax.set_ylabel("Primary metric (%)")
ax.set_ylim(0, 110)
ax.grid(axis="y", linestyle=":", color="gray", linewidth=0.5, alpha=0.6, zorder=1)
ax.legend(loc="upper center", ncol=3, frameon=False, fontsize=8,
          bbox_to_anchor=(0.5, 1.13))

plt.tight_layout()
out = ROOT / "figures" / "evolution_ablation.pdf"
plt.savefig(out, bbox_inches="tight")
print(f"saved {out}")
