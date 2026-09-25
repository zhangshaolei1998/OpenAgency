"""Ablation over the factorized evolving space. Three arms x four benchmarks."""
import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
D = json.load(open(ROOT / "data" / "evolution_space.json"))

BENCH = D["benchmarks"]
arms = ["init", "division_only", "full"]
labels = [
    "Initialization",
    "Division only",
    "Full space",
]
colors = ["#bdbdbd", "#fdae61", "#c1272d"]

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif", "Times New Roman"],
    "font.size": 9,
    "axes.linewidth": 0.7,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

fig, ax = plt.subplots(figsize=(4.9, 2.9))
n = len(BENCH)
x = np.arange(n)
w = 0.26

for j, a in enumerate(arms):
    ys = D["arms"][a]
    offset = (j - 1) * w
    ax.bar(x + offset, ys, width=w * 0.92, color=colors[j],
           edgecolor="black", linewidth=0.4, label=labels[j], zorder=3)
    for i, y in enumerate(ys):
        ax.text(x[i] + offset, y + 1.2, f"{y:.1f}", ha="center", va="bottom", fontsize=6.4)

# mark the one benchmark where the optimizer left the division level
i = D["graph_edited"].index(True)
ax.annotate("", xy=(x[i] + w, D["arms"]["full"][i] - 1.5),
            xytext=(x[i], D["arms"]["division_only"][i] + 1.5),
            arrowprops=dict(arrowstyle="-|>", color="#c1272d", lw=0.9,
                            connectionstyle="arc3,rad=-0.25"), zorder=4)
ax.text(x[i] - 0.10, (D["arms"]["division_only"][i] + D["arms"]["full"][i]) / 2 + 4,
        "+34.6", fontsize=7, color="#c1272d", ha="right", va="center")

ax.set_xticks(x)
ax.set_xticklabels(BENCH, fontsize=8)
ax.set_ylabel("Primary metric (%)")
ax.set_ylim(0, 118)
ax.grid(axis="y", linestyle=":", color="gray", linewidth=0.5, alpha=0.6, zorder=1)
ax.legend(loc="upper center", ncol=3, frameon=False, fontsize=7.4,
          bbox_to_anchor=(0.5, 1.14), handlelength=1.1, columnspacing=1.0)

plt.tight_layout()
out = ROOT / "figures" / "evolution_space.pdf"
plt.savefig(out, bbox_inches="tight")
print(f"saved {out}")
