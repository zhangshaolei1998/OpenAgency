"""Single vs multi-agent grouped by 3 categories."""
import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = json.load(open(ROOT / "data" / "benchmark_results.json"))["benchmarks"]

GROUPS = []
metric_label = {"HumanEval": "pass@1", "MBPP": "pass@1", "GSM8K": "EM", "MATH": "EM", "HotpotQA": "F1"}
for k in ["HumanEval", "MBPP", "GSM8K", "MATH", "HotpotQA"]:
    b = DATA[k]
    GROUPS.append((f"{k}\n({metric_label[k]})", b["single"], b["evolution"]["v4"], "general"))

GROUPS.append(("SWE-bench\n(FM)", DATA["SWE-bench"]["single"], DATA["SWE-bench"]["evolution"]["v4"], "longhorizon"))
GROUPS.append(("DeepPlanning\n(Avg Acc)", DATA["DeepPlanning"]["single"], DATA["DeepPlanning"]["evolution"]["v4"], "longhorizon"))
GROUPS.append(("HLE\n(Acc)", DATA["HLE"]["single"], DATA["HLE"]["evolution"]["v4"], "longhorizon"))

GROUPS.append(("DevEval\n(AT)", DATA["DevEval"]["single"], DATA["DevEval"]["evolution"]["v4"], "production"))
# DDR shows Overall = avg of Msg-Wise and Traj-Wise
ddr_single_avg = (27.3 + 58.2) / 2
ddr_v4_avg = (76.1 + 75.9) / 2
GROUPS.append(("DDR-Bench\n(Overall)", ddr_single_avg, ddr_v4_avg, "production"))
GROUPS.append(("TheAgentCompany\n(Score)", DATA["TheAgentCompany"]["single"], DATA["TheAgentCompany"]["evolution"]["v4"], "production"))
GROUPS.append(("MARBLE\n(Overall)", DATA["MARBLE"]["single"], DATA["MARBLE"]["evolution"]["v4"], "production"))
GROUPS.append(("AutomationBench\n(Acc)", DATA["AutomationBench"]["single"], DATA["AutomationBench"]["evolution"]["v4"], "production"))
GROUPS.append(("OfficeQA Pro\n(Acc@1\\%)", DATA["OfficeQA"]["single"], DATA["OfficeQA"]["evolution"]["v4"], "production"))

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif", "Times New Roman"],
    "font.size": 9,
    "axes.linewidth": 0.7,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

fig, ax = plt.subplots(figsize=(16.5, 3.6))
n = len(GROUPS)
x = np.arange(n)
w = 0.36

single_vals = [g[1] for g in GROUPS]
multi_vals = [g[2] for g in GROUPS]

c_single = "#fdae61"
c_multi = "#c1272d"

# Y range: clip below 10 to enforce ylim(10, 118) visualization
YMIN = 10
bottoms_single = [max(YMIN, min(YMIN, s)) for s in single_vals]  # start bar at YMIN
heights_single = [max(0, s - YMIN) for s in single_vals]
heights_multi = [max(0, m - YMIN) for m in multi_vals]

ax.bar(x - w / 2, heights_single, width=w, bottom=YMIN, color=c_single, edgecolor="black",
       linewidth=0.4, label="Single-agent", zorder=3)
ax.bar(x + w / 2, heights_multi, width=w, bottom=YMIN, color=c_multi, edgecolor="black",
       linewidth=0.4, label="OpenAgency (v4)", zorder=3)

for i, (s, m) in enumerate(zip(single_vals, multi_vals)):
    if s >= YMIN:
        ax.text(i - w / 2, s + 0.9, f"{s:.1f}", ha="center", va="bottom", fontsize=7)
    else:
        # value below y-axis floor: mark with an arrow + text at the bottom
        ax.text(i - w / 2, YMIN + 0.9, f"{s:.1f}$\\downarrow$", ha="center", va="bottom",
                fontsize=7, color="#8a3b1a")
    ax.text(i + w / 2, m + 0.9, f"{m:.1f}", ha="center", va="bottom",
            fontsize=7, fontweight="bold")

ax.set_xticks(x)
ax.set_xticklabels([g[0] for g in GROUPS], fontsize=7.8)
ax.set_ylabel("Primary metric (%)")
ax.set_ylim(YMIN, 118)
ax.set_yticks([10, 30, 50, 70, 90, 100])
ax.grid(axis="y", linestyle=":", color="gray", linewidth=0.5, alpha=0.6, zorder=1)

def cat_span(idxs, label):
    left = x[idxs[0]] - w - 0.1
    right = x[idxs[-1]] + w + 0.1
    ax.annotate("", xy=(left, 112), xytext=(right, 112),
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
    xx = (x[a] + x[b]) / 2
    ax.axvline(xx, color="lightgray", linestyle=":", linewidth=0.9, zorder=0)
sep_between(general_idx[-1], long_idx[0])
sep_between(long_idx[-1], prod_idx[0])

ax.legend(loc="upper center", ncol=2, frameon=False, fontsize=9, bbox_to_anchor=(0.5, 1.18))

plt.tight_layout()
out = ROOT / "figures" / "single_vs_multi.pdf"
plt.savefig(out, bbox_inches="tight")
print(f"saved {out}")
