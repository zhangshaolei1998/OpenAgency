"""Evolution under a fixed topology versus the full evolution space (OfficeQA Pro).

Both arms start from the same initialization. The fixed arm can only edit the
shared context on a single-node graph; the full arm may also edit the topology.
"""
import json
from pathlib import Path
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
D = json.load(open(ROOT / "data" / "fixed_topology.json"))

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif", "Times New Roman"],
    "font.size": 9,
    "axes.linewidth": 0.7,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

C_FIX = "#8c8c8c"
C_FULL = "#c1272d"
C_INIT = "#333333"

fig, ax = plt.subplots(figsize=(8.0, 1.95))

init = D["init"]
fx = [0] + D["fixed"]["rounds"]
fy = [init] + D["fixed"]["scores"]
gx = [0] + D["full"]["rounds"]
gy = [init] + D["full"]["scores"]

ceiling = D["fixed"]["ceiling"]
ax.axhline(ceiling, color=C_FIX, linestyle=":", linewidth=0.9, zorder=1)
ax.text(3.35, ceiling + 1.6, f"previous-protocol ceiling {ceiling}", fontsize=7,
        color=C_FIX, va="bottom", ha="center")

ax.plot(fx, fy, linestyle="--", color=C_FIX, linewidth=1.4, zorder=2,
        marker="o", markersize=5, markerfacecolor="white",
        markeredgecolor=C_FIX, markeredgewidth=1.2,
        label=D["fixed"]["label"])
ax.plot(gx, gy, linestyle="-", color=C_FULL, linewidth=1.6, zorder=3,
        marker="s", markersize=5.5, markerfacecolor=C_FULL,
        markeredgecolor="black", markeredgewidth=0.4,
        label=D["full"]["label"])

ax.plot([0], [init], marker="D", markersize=6, markerfacecolor=C_INIT,
        markeredgecolor="black", markeredgewidth=0.4, zorder=4)
ax.annotate(f"init {init}\n1 node", xy=(0, init), xytext=(2, -19),
            textcoords="offset points", fontsize=7, color=C_INIT, ha="center")

for x, y in zip(D["fixed"]["rounds"], D["fixed"]["scores"]):
    ax.annotate(f"{y}", xy=(x, y), xytext=(0, -12), textcoords="offset points",
                fontsize=7, color=C_FIX, ha="center")

notes = ["+reader (2)", "+verifier (3)", "division edit (3)", "+solver (4)"]
for x, y, note in zip(D["full"]["rounds"], D["full"]["scores"], notes):
    ax.annotate(f"{y}", xy=(x, y), xytext=(0, 8), textcoords="offset points",
                fontsize=7.5, color=C_FULL, ha="center", weight="bold")
    dx = 20 if x == 1 else 0
    ax.annotate(note, xy=(x, y), xytext=(dx, -14), textcoords="offset points",
                fontsize=6.5, color=C_FULL, ha="center")

ax.set_xlabel("Evolution round")
ax.set_ylabel("Accuracy (Acc@1%)")
ax.set_xlim(-0.45, 6.45)
ax.set_ylim(0, 80)
ax.set_xticks(range(0, 7))
ax.set_yticks([0, 20, 40, 60, 80])
ax.grid(True, axis="y", linestyle=":", color="gray", linewidth=0.5, alpha=0.6)
ax.legend(loc="upper right", frameon=False, fontsize=7.5, handlelength=2.0,
          bbox_to_anchor=(1.005, 1.06))

plt.tight_layout()
out = ROOT / "figures" / "fixed_topology.pdf"
plt.savefig(out, bbox_inches="tight")
print(f"saved {out}")
