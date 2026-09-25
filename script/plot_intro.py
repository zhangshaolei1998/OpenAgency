"""Intro illustration: Blueprint-driven vs Agent-driven vs OpenAgency
Three panels showing how the collaboration structure differs, with a small
evolution loop on the right panel to emphasize the self-evolving property."""
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

ROOT = Path(__file__).resolve().parent.parent

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 9,
})

fig, axes = plt.subplots(1, 3, figsize=(11.5, 2.8))

# =============================================================
# Panel 1: Blueprint-driven — rigid fixed chain
# =============================================================
ax = axes[0]
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values(): s.set_edgecolor("lightgray")

nodes = {"A": (0.12, 0.55), "B": (0.36, 0.55), "C": (0.60, 0.55), "D": (0.84, 0.55)}
node_color = "#c8c8c8"
for name, (x, y) in nodes.items():
    box = mpatches.FancyBboxPatch((x - 0.07, y - 0.09), 0.14, 0.18,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        facecolor=node_color, edgecolor="black", linewidth=0.6)
    ax.add_patch(box)
    ax.text(x, y, name, ha="center", va="center", fontsize=10, fontweight="bold")

# fixed forward arrows
for a, b in [("A", "B"), ("B", "C"), ("C", "D")]:
    xs, ys = nodes[a]; xd, yd = nodes[b]
    arr = mpatches.FancyArrowPatch((xs + 0.07, ys), (xd - 0.07, yd),
        arrowstyle="-|>", mutation_scale=12, linewidth=1.4, color="#404040")
    ax.add_patch(arr)

ax.set_title("Blueprint-driven", fontsize=10, fontweight="bold", pad=6)
ax.text(0.5, 0.15, "fixed workflow;\nno runtime adaptation", ha="center", va="center",
        fontsize=8, color="#666", style="italic")

# =============================================================
# Panel 2: Agent-driven — dense mesh, no rules
# =============================================================
ax = axes[1]
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values(): s.set_edgecolor("lightgray")

nodes = {"A": (0.24, 0.75), "B": (0.76, 0.75), "C": (0.24, 0.35), "D": (0.76, 0.35)}
node_color = "#fbb4ae"
for name, (x, y) in nodes.items():
    circ = mpatches.FancyBboxPatch((x - 0.07, y - 0.09), 0.14, 0.18,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        facecolor=node_color, edgecolor="black", linewidth=0.6)
    ax.add_patch(circ)
    ax.text(x, y, name, ha="center", va="center", fontsize=10, fontweight="bold")

# all-to-all bidirectional edges
import itertools
pairs = list(itertools.combinations(nodes.keys(), 2))
for a, b in pairs:
    xs, ys = nodes[a]; xd, yd = nodes[b]
    arr = mpatches.FancyArrowPatch((xs, ys), (xd, yd),
        connectionstyle="arc3,rad=0.1",
        arrowstyle="<->", mutation_scale=8, linewidth=0.9,
        color="#c0392b", alpha=0.55)
    ax.add_patch(arr)

ax.set_title("Agent-driven (Free-form)", fontsize=10, fontweight="bold", pad=6)
ax.text(0.5, 0.08, "any-to-any communication;\nhard to inspect or improve", ha="center", va="center",
        fontsize=8, color="#666", style="italic")

# =============================================================
# Panel 3: OpenAgency — admissible boundary + agent choice + evolution
# =============================================================
ax = axes[2]
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values(): s.set_edgecolor("lightgray")

nodes = {"A": (0.16, 0.72), "B": (0.44, 0.72), "C": (0.44, 0.36), "D": (0.72, 0.54)}
node_color = "#fdae61"
for name, (x, y) in nodes.items():
    box = mpatches.FancyBboxPatch((x - 0.07, y - 0.09), 0.14, 0.18,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        facecolor=node_color, edgecolor="#c1272d", linewidth=1.0)
    ax.add_patch(box)
    ax.text(x, y, name, ha="center", va="center", fontsize=10, fontweight="bold")

# admissible edges only (subset)
admissible = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("C", "B")]
for a, b in admissible:
    xs, ys = nodes[a]; xd, yd = nodes[b]
    arr = mpatches.FancyArrowPatch((xs, ys), (xd, yd),
        connectionstyle="arc3,rad=0.1",
        arrowstyle="-|>", mutation_scale=10, linewidth=1.2,
        color="#c1272d", alpha=0.85)
    ax.add_patch(arr)

# dashed admissibility boundary (a wide ellipse around A/B/C/D)
boundary = mpatches.FancyBboxPatch((0.06, 0.22), 0.78, 0.62,
    boxstyle="round,pad=0.01,rounding_size=0.08",
    facecolor="none", edgecolor="#c1272d", linewidth=1.0, linestyle="--", alpha=0.6)
ax.add_patch(boundary)
ax.text(0.09, 0.85, "$\\Gamma$", fontsize=11, color="#c1272d", fontweight="bold")

# evolution loop annotation at bottom
ax.annotate("", xy=(0.90, 0.35), xytext=(0.85, 0.5),
    arrowprops=dict(arrowstyle="->", color="#404040", lw=0.9,
                    connectionstyle="arc3,rad=0.5"))
ax.text(0.98, 0.42, "trace", fontsize=7, color="#404040", rotation=270)
ax.text(0.90, 0.15, "$\\mathcal{P}^{(v)} \\to \\mathcal{P}^{(v+1)}$",
        fontsize=8, color="#c1272d", ha="center")

ax.set_title("OpenAgency (Ours)", fontsize=10, fontweight="bold", pad=6, color="#c1272d")
ax.text(0.44, 0.06, "governed protocol; agent chooses in $\\Gamma$;\nprotocol evolves across runs",
        ha="center", va="center", fontsize=8, color="#666", style="italic")

plt.tight_layout()
out = ROOT / "figures" / "intro.pdf"
plt.savefig(out, bbox_inches="tight")
print(f"saved {out}")
