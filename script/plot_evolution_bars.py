"""Evolution bars grouped by 3 benchmark categories.
- General reasoning: HumanEval, MBPP, GSM8K, MATH, HotpotQA
- Long-horizon complex: SWE-bench, DeepPlanning, HLE
- Production-oriented: DevEval, DDR-Bench, TheAgentCompany, MARBLE, AutomationBench, OfficeQA
"""
import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = json.load(open(ROOT / "data" / "benchmark_results.json"))["benchmarks"]

# (label, evolution_dict, Prev. SOTA, category)
GROUPS = []

def series(benchmark):
    return {"v0": benchmark["multi_v0"], **benchmark["evolution"]}

metric_label = {"HumanEval": "pass@1", "MBPP": "pass@1", "GSM8K": "EM", "MATH": "EM", "HotpotQA": "F1"}
for k in ["HumanEval", "MBPP", "GSM8K", "MATH", "HotpotQA"]:
    b = DATA[k]
    GROUPS.append((f"{k}\n({metric_label[k]})", series(b), b["prev_sota"], "general"))

GROUPS.append(("SWE-bench\n(FM)", series(DATA["SWE-bench"]), DATA["SWE-bench"]["prev_sota"], "longhorizon"))
GROUPS.append(("DeepPlanning\n(Avg Acc)", series(DATA["DeepPlanning"]), DATA["DeepPlanning"]["prev_sota"], "longhorizon"))
GROUPS.append(("HLE\n(Acc)", series(DATA["HLE"]), DATA["HLE"]["prev_sota"], "longhorizon"))

GROUPS.append(("DevEval\n(AT)", series(DATA["DevEval"]), DATA["DevEval"]["prev_sota"], "production"))
GROUPS.append(("DDR-Bench\n(Overall)", series(DATA["DDR-Bench"]), DATA["DDR-Bench"]["prev_sota"], "production"))
GROUPS.append(("TheAgentCompany\n(Score)", series(DATA["TheAgentCompany"]), DATA["TheAgentCompany"]["prev_sota"], "production"))
GROUPS.append(("MARBLE\n(Overall)", series(DATA["MARBLE"]), DATA["MARBLE"]["prev_sota"], "production"))
GROUPS.append(("AutomationBench\n(Acc)", series(DATA["AutomationBench"]), DATA["AutomationBench"]["prev_sota"], "production"))
GROUPS.append(("OfficeQA Pro\n(Acc@1\\%)", series(DATA["OfficeQA"]), DATA["OfficeQA"]["prev_sota"], "production"))

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 9,
    "axes.labelsize": 10,
    "axes.linewidth": 0.7,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

fig, ax = plt.subplots(figsize=(16.5, 3.6))

n_group = len(GROUPS)
bar_w = 0.16
gap = 0.10
group_w = 5 * bar_w
centers = np.arange(n_group) * (group_w + gap + bar_w)

shades = ["#f2f2f2", "#fee0b6", "#fdae61", "#f46d43", "#c1272d"]

YMIN = 0
for i, (label, ev, baseline, cat) in enumerate(GROUPS):
    for j, v in enumerate(["v0", "v1", "v2", "v3", "v4"]):
        x = centers[i] - group_w / 2 + j * bar_w + bar_w / 2
        val = ev[v]
        height = max(0, val - YMIN)
        ax.bar(x, height, bottom=YMIN, width=bar_w * 0.95, color=shades[j],
               edgecolor="black", linewidth=0.35, zorder=3)
    xleft = centers[i] - group_w / 2 - bar_w * 0.15
    xright = centers[i] + group_w / 2 + bar_w * 0.15
    ax.plot([xleft, xright], [baseline, baseline],
            linestyle="--", color="dimgray", linewidth=1.05, zorder=4)

ax.set_xticks(centers)
ax.set_xticklabels([g[0] for g in GROUPS], fontsize=7.2)
ax.set_ylabel("Primary metric (%)", fontsize=10)
ax.set_ylim(YMIN, 118)
ax.set_yticks([0, 20, 40, 60, 80, 100])
ax.tick_params(axis="y", labelsize=8)
ax.grid(axis="y", linestyle=":", color="gray", linewidth=0.5, alpha=0.6, zorder=1)

# Category separators + top labels
def cat_span(idxs, label):
    left = centers[idxs[0]] - group_w / 2 - 0.05
    right = centers[idxs[-1]] + group_w / 2 + 0.05
    ax.annotate("", xy=(left, 111), xytext=(right, 111),
                xycoords="data", textcoords="data",
                arrowprops=dict(arrowstyle="-", color="dimgray", linewidth=0.7))
    ax.text((left + right) / 2, 113, label,
            ha="center", va="bottom", fontsize=9, style="italic", color="#404040")

general_idx = [i for i, g in enumerate(GROUPS) if g[3] == "general"]
long_idx    = [i for i, g in enumerate(GROUPS) if g[3] == "longhorizon"]
prod_idx    = [i for i, g in enumerate(GROUPS) if g[3] == "production"]
cat_span(general_idx, "General QA Tasks")
cat_span(long_idx,    "Long-horizon Tasks")
cat_span(prod_idx,    "Production-oriented Tasks")

def sep_between(a, b):
    x = (centers[a] + centers[b]) / 2
    ax.axvline(x, color="lightgray", linestyle=":", linewidth=0.9, zorder=0)
sep_between(general_idx[-1], long_idx[0])
sep_between(long_idx[-1], prod_idx[0])

handles = [plt.Rectangle((0, 0), 1, 1, facecolor=shades[i], edgecolor="black", linewidth=0.4)
           for i in range(5)]
handles.append(plt.Line2D([0], [0], linestyle="--", color="dimgray", linewidth=1.05))
labels = ["Multi-agent (init)", "v1", "v2", "v3", "v4", "Prev. SOTA"]
ax.legend(handles, labels, loc="upper center", ncol=6, frameon=False, fontsize=8.5,
          bbox_to_anchor=(0.5, 1.20))

plt.tight_layout()
out = ROOT / "figures" / "evolution_bars.pdf"
plt.savefig(out, bbox_inches="tight")
print(f"saved {out}")
