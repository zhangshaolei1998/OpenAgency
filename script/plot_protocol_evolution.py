"""Protocol evolution case study: one row per benchmark, four columns for v1..v4.
Nodes are roles, edges are handoffs (solid = handoff, dashed = retry/validity).
Newly added structure per round highlighted in red."""
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parent.parent

def N(x, y): return (x, y)

# LAYOUTS[bench][version] = {nodes, edges, new_nodes, new_edges, title}
LAYOUTS = {
    "SWE-bench": {
        "v1": {"nodes": {"Locator": N(0.20, 0.65), "Editor": N(0.55, 0.65), "Verifier": N(0.55, 0.30)},
               "edges": [("Locator","Editor","solid"),("Editor","Verifier","solid")],
               "new_nodes": [], "new_edges": [], "title": "v1: locate$\\to$edit$\\to$verify"},
        "v2": {"nodes": {"Locator": N(0.20, 0.65), "Editor": N(0.55, 0.65), "Verifier": N(0.55, 0.30)},
               "edges": [("Locator","Editor","solid"),("Editor","Verifier","solid"),
                         ("Verifier","Editor","dashed")],
               "new_nodes": [], "new_edges": [("Verifier","Editor","dashed")],
               "title": "v2: + edit retry"},
        "v3": {"nodes": {"Locator": N(0.20, 0.65), "Editor": N(0.55, 0.65), "Verifier": N(0.55, 0.30)},
               "edges": [("Locator","Editor","solid"),("Editor","Verifier","solid"),
                         ("Verifier","Editor","dashed"),("Verifier","Locator","dashed")],
               "new_nodes": [], "new_edges": [("Verifier","Locator","dashed")],
               "title": "v3: + re-locate on fail"},
        "v4": {"nodes": {"Locator": N(0.15, 0.65), "Editor": N(0.48, 0.65),
                          "StructVal": N(0.82, 0.85), "SemVal": N(0.82, 0.45)},
               "edges": [("Locator","Editor","solid"),("Editor","StructVal","solid"),
                         ("Editor","SemVal","solid"),
                         ("StructVal","Locator","dashed"),("SemVal","Editor","dashed")],
               "new_nodes": ["StructVal","SemVal"],
               "new_edges": [("Editor","StructVal","solid"),("Editor","SemVal","solid"),
                             ("StructVal","Locator","dashed"),("SemVal","Editor","dashed")],
               "title": "v4: split verifier"},
    },
    "DevEval": {
        "v1": {"nodes": {"Coder": N(0.25, 0.65), "Reviewer": N(0.70, 0.65)},
               "edges": [("Coder","Reviewer","solid"),("Reviewer","Coder","dashed")],
               "new_nodes": [], "new_edges": [], "title": "v1: coder$\\leftrightarrow$reviewer"},
        "v2": {"nodes": {"Coder": N(0.25, 0.65), "Reviewer": N(0.70, 0.65)},
               "edges": [("Coder","Reviewer","solid"),("Reviewer","Coder","dashed")],
               "new_nodes": [], "new_edges": [], "title": "v2: + test injection"},
        "v3": {"nodes": {"Coder": N(0.25, 0.65), "Reviewer": N(0.70, 0.65)},
               "edges": [("Coder","Reviewer","solid"),("Reviewer","Coder","dashed")],
               "new_nodes": [], "new_edges": [], "title": "v3: 5-round + error patterns"},
        "v4": {"nodes": {"Coder": N(0.15, 0.65), "SelfTest": N(0.48, 0.65),
                          "Reviewer": N(0.82, 0.65)},
               "edges": [("Coder","SelfTest","solid"),("SelfTest","Reviewer","solid"),
                         ("Reviewer","Coder","dashed"),("SelfTest","Coder","dashed")],
               "new_nodes": ["SelfTest"],
               "new_edges": [("Coder","SelfTest","solid"),("SelfTest","Reviewer","solid"),
                             ("SelfTest","Coder","dashed")],
               "title": "v4: + self-test node"},
    },
    "DDR-Bench": {
        "v1": {"nodes": {"Researcher": N(0.30, 0.65), "Reporter": N(0.75, 0.65)},
               "edges": [("Researcher","Reporter","solid")],
               "new_nodes": [], "new_edges": [], "title": "v1: research$\\to$report"},
        "v2": {"nodes": {"Researcher": N(0.30, 0.65), "Reporter": N(0.75, 0.65)},
               "edges": [("Researcher","Reporter","solid")],
               "new_nodes": [], "new_edges": [], "title": "v2: enriched handoff"},
        "v3": {"nodes": {"Researcher": N(0.15, 0.65), "OpsPhase": N(0.48, 0.65),
                          "Reporter": N(0.82, 0.65)},
               "edges": [("Researcher","OpsPhase","solid"),("OpsPhase","Reporter","solid")],
               "new_nodes": ["OpsPhase"],
               "new_edges": [("Researcher","OpsPhase","solid"),("OpsPhase","Reporter","solid")],
               "title": "v3: + ops phase"},
        "v4": {"nodes": {"Researcher": N(0.13, 0.80), "OpsPhase": N(0.42, 0.80),
                          "Reporter": N(0.72, 0.80), "Auditor": N(0.42, 0.30)},
               "edges": [("Researcher","OpsPhase","solid"),
                         ("OpsPhase","Reporter","solid"),
                         ("Reporter","Auditor","dashed"),("Auditor","Reporter","dashed")],
               "new_nodes": ["Auditor"],
               "new_edges": [("Reporter","Auditor","dashed"),("Auditor","Reporter","dashed")],
               "title": "v4: + quant auditor"},
    },
    "HumanEval": {
        "v1": {"nodes": {"Solver": N(0.30, 0.65), "Verifier": N(0.75, 0.65)},
               "edges": [("Solver","Verifier","solid")],
               "new_nodes": [], "new_edges": [], "title": "v1: solve$\\to$verify"},
        "v2": {"nodes": {"Solver": N(0.30, 0.65), "Verifier": N(0.75, 0.65)},
               "edges": [("Solver","Verifier","solid"),("Verifier","Solver","dashed")],
               "new_nodes": [], "new_edges": [("Verifier","Solver","dashed")],
               "title": "v2: + per-dataset prompt"},
        "v3": {"nodes": {"Solver": N(0.30, 0.65), "Verifier": N(0.75, 0.65)},
               "edges": [("Solver","Verifier","solid"),("Verifier","Solver","dashed")],
               "new_nodes": [], "new_edges": [], "title": "v3: conservative verifier"},
        "v4": {"nodes": {"Solver": N(0.20, 0.65), "EdgeCase": N(0.55, 0.85),
                          "Verifier": N(0.55, 0.45)},
               "edges": [("Solver","EdgeCase","solid"),("EdgeCase","Verifier","solid"),
                         ("Verifier","Solver","dashed")],
               "new_nodes": ["EdgeCase"],
               "new_edges": [("Solver","EdgeCase","solid"),("EdgeCase","Verifier","solid")],
               "title": "v4: + edge-case check"},
    },
    "TheAgentCompany": {
        "v1": {"nodes": {"Planner": N(0.15, 0.65), "Executor": N(0.50, 0.65),
                          "Reviewer": N(0.85, 0.65)},
               "edges": [("Planner","Executor","solid"),("Executor","Reviewer","solid")],
               "new_nodes": [], "new_edges": [], "title": "v1: plan$\\to$exec$\\to$review"},
        "v2": {"nodes": {"Planner": N(0.15, 0.65), "Executor": N(0.50, 0.65),
                          "Reviewer": N(0.85, 0.65)},
               "edges": [("Planner","Executor","solid"),("Executor","Reviewer","solid"),
                         ("Reviewer","Executor","dashed")],
               "new_nodes": [], "new_edges": [("Reviewer","Executor","dashed")],
               "title": "v2: + auth + pagination"},
        "v3": {"nodes": {"Planner": N(0.15, 0.65), "Executor": N(0.50, 0.65),
                          "Reviewer": N(0.85, 0.65)},
               "edges": [("Planner","Executor","solid"),("Executor","Reviewer","solid"),
                         ("Reviewer","Executor","dashed"),("Reviewer","Planner","dashed")],
               "new_nodes": [], "new_edges": [("Reviewer","Planner","dashed")],
               "title": "v3: + re-plan on zero-result"},
        "v4": {"nodes": {"Planner": N(0.13, 0.65), "Executor": N(0.42, 0.65),
                          "PyRunner": N(0.72, 0.85), "Reviewer": N(0.72, 0.45)},
               "edges": [("Planner","Executor","solid"),("Executor","PyRunner","solid"),
                         ("Executor","Reviewer","solid"),
                         ("Reviewer","Executor","dashed"),("PyRunner","Executor","dashed")],
               "new_nodes": ["PyRunner"],
               "new_edges": [("Executor","PyRunner","solid"),("PyRunner","Executor","dashed")],
               "title": "v4: + python runner"},
    },
    "DeepPlanning": {
        "v1": {"nodes": {"Solver": N(0.50, 0.65)},
               "edges": [], "new_nodes": [], "new_edges": [],
               "title": "v1: monolithic solver"},
        "v2": {"nodes": {"Researcher": N(0.30, 0.65), "Solver": N(0.75, 0.65)},
               "edges": [("Researcher","Solver","solid")],
               "new_nodes": ["Researcher"],
               "new_edges": [("Researcher","Solver","solid")],
               "title": "v2: + researcher"},
        "v3": {"nodes": {"Researcher": N(0.15, 0.65), "Solver": N(0.50, 0.65),
                          "Verifier": N(0.85, 0.65)},
               "edges": [("Researcher","Solver","solid"),("Solver","Verifier","solid"),
                         ("Verifier","Solver","dashed")],
               "new_nodes": ["Verifier"],
               "new_edges": [("Solver","Verifier","solid"),("Verifier","Solver","dashed")],
               "title": "v3: + verifier"},
        "v4": {"nodes": {"Researcher": N(0.13, 0.65), "Solver": N(0.42, 0.65),
                          "Checklist": N(0.72, 0.85), "Verifier": N(0.72, 0.45)},
               "edges": [("Researcher","Solver","solid"),("Solver","Checklist","solid"),
                         ("Checklist","Verifier","solid"),("Verifier","Solver","dashed")],
               "new_nodes": ["Checklist"],
               "new_edges": [("Solver","Checklist","solid"),("Checklist","Verifier","solid")],
               "title": "v4: + constraint checklist"},
    },
    "MARBLE": {
        "v1": {"nodes": {"Reviewer": N(0.15, 0.65), "Brainstormer": N(0.50, 0.65),
                          "Writer": N(0.85, 0.65)},
               "edges": [("Reviewer","Brainstormer","solid"),("Brainstormer","Writer","solid")],
               "new_nodes": [], "new_edges": [],
               "title": "v1: rev$\\to$brain$\\to$write"},
        "v2": {"nodes": {"Generator": N(0.15, 0.65), "Critic": N(0.50, 0.65),
                          "Reviser": N(0.85, 0.65)},
               "edges": [("Generator","Critic","solid"),("Critic","Reviser","solid")],
               "new_nodes": ["Generator","Critic","Reviser"],
               "new_edges": [("Generator","Critic","solid"),("Critic","Reviser","solid")],
               "title": "v2: G$\\to$C$\\to$R pipeline"},
        "v3": {"nodes": {"Generator": N(0.15, 0.65), "Critic": N(0.50, 0.65),
                          "Reviser": N(0.85, 0.65)},
               "edges": [("Generator","Critic","solid"),("Critic","Reviser","solid"),
                         ("Critic","Generator","dashed")],
               "new_nodes": [], "new_edges": [("Critic","Generator","dashed")],
               "title": "v3: + feasibility retry"},
        "v4": {"nodes": {"Generator": N(0.13, 0.65), "Critic": N(0.42, 0.65),
                          "Expander": N(0.72, 0.85), "Reviser": N(0.72, 0.45)},
               "edges": [("Generator","Critic","solid"),("Critic","Expander","solid"),
                         ("Expander","Reviser","solid"),("Critic","Generator","dashed")],
               "new_nodes": ["Expander"],
               "new_edges": [("Critic","Expander","solid"),("Expander","Reviser","solid")],
               "title": "v4: + idea expander"},
    },
    "AutomationBench": {
        "v1": {"nodes": {"Executor": N(0.30, 0.65), "Verifier": N(0.75, 0.65)},
               "edges": [("Executor","Verifier","solid"),("Verifier","Executor","dashed")],
               "new_nodes": [], "new_edges": [],
               "title": "v1: execute$\\to$verify"},
        "v2": {"nodes": {"Solver": N(0.50, 0.65)},
               "edges": [("Solver","Solver","dashed")],
               "new_nodes": ["Solver"],
               "new_edges": [("Solver","Solver","dashed")],
               "phases": ["Execute", "Self-Verify"],
               "new_phases": ["Execute", "Self-Verify"],
               "title": "v2: solver + self-verify"},
        "v3": {"nodes": {"Solver": N(0.50, 0.65)},
               "edges": [("Solver","Solver","dashed")],
               "new_nodes": [], "new_edges": [],
               "phases": ["Execute", "Coverage", "Verify"],
               "new_phases": ["Coverage"],
               "title": "v3: + requirement coverage"},
        "v4": {"nodes": {"Solver": N(0.50, 0.65)},
               "edges": [("Solver","Solver","dashed")],
               "new_nodes": [], "new_edges": [],
               "phases": ["Execute", "Coverage", "WordMatch"],
               "new_phases": ["WordMatch"],
               "title": "v4: + word-for-word check"},
    },
    "HLE": {
        "v1": {"nodes": {"Solver": N(0.30, 0.65), "Verifier": N(0.75, 0.65)},
               "edges": [("Solver","Verifier","solid")],
               "new_nodes": [], "new_edges": [],
               "title": "v1: solve$\\to$verify"},
        "v2": {"nodes": {"Solver": N(0.30, 0.65), "Verifier": N(0.75, 0.65)},
               "edges": [("Solver","Verifier","solid")],
               "new_nodes": [], "new_edges": [],
               "title": "v2: + write-first"},
        "v3": {"nodes": {"Solver": N(0.20, 0.80), "Done": N(0.75, 0.85),
                          "Verifier": N(0.75, 0.45)},
               "edges": [("Solver","Done","solid"),("Solver","Verifier","solid")],
               "new_nodes": ["Done"],
               "new_edges": [("Solver","Done","solid")],
               "title": "v3: + confidence route"},
        "v4": {"nodes": {"Solver": N(0.20, 0.80), "Done": N(0.75, 0.85),
                          "Verifier": N(0.75, 0.45)},
               "edges": [("Solver","Done","solid"),("Solver","Verifier","solid"),
                         ("Verifier","Solver","dashed")],
               "new_nodes": [], "new_edges": [("Verifier","Solver","dashed")],
               "title": "v4: + conditional retry"},
    },
    "OfficeQA": {
        "v1": {"nodes": {"Solver": N(0.50, 0.65)},
               "edges": [], "new_nodes": [], "new_edges": [],
               "title": "v1: prompt-tuned solver"},
        "v2": {"nodes": {"Reader": N(0.25, 0.65), "Solver": N(0.75, 0.65)},
               "edges": [("Reader","Solver","solid")],
               "new_nodes": ["Reader"],
               "new_edges": [("Reader","Solver","solid")],
               "title": "v2: + reader (file-based)"},
        "v3": {"nodes": {"Reader": N(0.15, 0.65), "Solver": N(0.50, 0.65),
                          "Verifier": N(0.85, 0.65)},
               "edges": [("Reader","Solver","solid"),("Solver","Verifier","solid"),
                         ("Verifier","Solver","dashed")],
               "new_nodes": ["Verifier"],
               "new_edges": [("Solver","Verifier","solid"),("Verifier","Solver","dashed")],
               "title": "v3: + verifier"},
        "v4": {"nodes": {"Reader": N(0.15, 0.65), "Solver": N(0.50, 0.65),
                          "Verifier": N(0.85, 0.65)},
               "edges": [("Reader","Solver","solid"),("Solver","Verifier","solid"),
                         ("Verifier","Solver","dashed"),("Reader","Reader","dashed")],
               "new_nodes": [],
               "new_edges": [("Reader","Reader","dashed")],
               "title": "v4: + completeness check"},
    },
}


# EDITS[bench][v] lists the edits the round applies, following the three edit
# levels of Section 3.3: S = structural, P = predicate, C = contextual.
# A predicate edit carries the element it guards, so the guard is drawn where it
# applies and stays visible in later rounds. A contextual edit carries the text
# it writes into the shared rule or culture, which accumulates down the row.
EDITS = {
    "SWE-bench": {
        "v1": [], "v2": [("S", "edit retry edge", None)],
        "v3": [("S", "re-locate on fail", None)],
        "v4": [("S", "split verifier", None)]},
    "DeepPlanning": {
        "v1": [], "v2": [("S", "researcher node", None)],
        "v3": [("S", "verifier node", None)],
        "v4": [("S", "constraint checklist", None)]},
    "HLE": {
        "v1": [], "v2": [("C", "answer before verifying", None)],
        "v3": [("S", "confidence route", None)],
        "v4": [("S", "conditional retry edge", None)]},
    "DevEval": {
        "v1": [], "v2": [("C", "inject unit tests", None)],
        "v3": [("P", "$\\leq 5$ rounds", ("edge", "Reviewer", "Coder")),
               ("C", "known error patterns", None)],
        "v4": [("S", "self-test node", None)]},
    "DDR-Bench": {
        "v1": [], "v2": [("C", "forward raw evidence", None)],
        "v3": [("S", "ops phase node", None)],
        "v4": [("S", "quant auditor node", None)]},
    "TheAgentCompany": {
        "v1": [], "v2": [("S", "retry edge", None), ("C", "auth and pagination", None)],
        "v3": [("S", "re-plan edge", None),
               ("P", "zero result", ("edge", "Reviewer", "Planner"))],
        "v4": [("S", "python runner node", None)]},
    "MARBLE": {
        "v1": [], "v2": [("S", "re-role to G$\\to$C$\\to$R", None)],
        "v3": [("S", "feasibility retry edge", None)],
        "v4": [("S", "idea expander", None)]},
    "AutomationBench": {
        "v1": [], "v2": [("S", "collapse to one solver", None)],
        "v3": [("S", "coverage phase", None)],
        "v4": [("P", "word-for-word", ("node", "Solver"))]},
    "OfficeQA": {
        "v1": [], "v2": [("S", "reader node", None)],
        "v3": [("S", "verifier node", None)],
        "v4": [("S", "completeness self-loop", None)]},
}

LEVEL_COLOR = {"S": "#c1272d", "P": "#1f5fa8", "C": "#2e7d32"}
LEVEL_TINT = {"S": "#fdf2f2", "P": "#f1f6fc", "C": "#f2f8f2", None: "#ffffff"}
FADED = "#9a9a9a"
VERSIONS = ["v1", "v2", "v3", "v4"]

# The general question answering benchmarks converge on a two-node solve-verify
# template, so the figure covers the long-horizon and production-oriented
# benchmarks, where the protocol actually differentiates.
BENCHES = ["SWE-bench", "DeepPlanning", "HLE", "DevEval", "DDR-Bench",
           "TheAgentCompany", "MARBLE", "AutomationBench", "OfficeQA"]

# accumulate guards and shared context so each panel shows everything the
# protocol carries at that round, with only the current round highlighted
ACC = {}
for _b in BENCHES:
    _g, _c = [], []
    for _i, _v in enumerate(VERSIONS):
        for _lv, _lab, _anch in EDITS[_b][_v]:
            if _lv == "P":
                _g.append((_lab, _anch, _i))
            elif _lv == "C":
                _c.append((_lab, _i))
        ACC[(_b, _v)] = (list(_g), list(_c))


plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif", "Times New Roman"],
    "font.size": 8.5,
    "axes.linewidth": 0.7,
})

fig, axes = plt.subplots(len(BENCHES), 4, figsize=(11.0, 16.0))


def edge_point(L, src, dst):
    xs, ys = L["nodes"][src]
    xd, yd = L["nodes"][dst]
    mx, my = (xs + xd) / 2, (ys + yd) / 2
    dx, dy = xd - xs, yd - ys
    n = (dx ** 2 + dy ** 2) ** 0.5 or 1.0
    return mx - dy / n * 0.145, my + dx / n * 0.145


for row, bench in enumerate(BENCHES):
    for col, v in enumerate(VERSIONS):
        ax = axes[row, col]
        L = LAYOUTS[bench][v]
        edits = EDITS[bench][v]
        levels = [lv for lv, _, _ in edits]
        dom = "S" if "S" in levels else ("P" if "P" in levels else ("C" if "C" in levels else None))
        hi = LEVEL_COLOR.get(dom, "#404040")
        guards, ctx = ACC[(bench, v)]

        ax.set_xlim(0, 1)
        ax.set_ylim(-0.52, 1.05)
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_facecolor(LEVEL_TINT[dom])
        for spine in ax.spines.values():
            spine.set_edgecolor("lightgray")

        for src, dst, style in L["edges"]:
            xs, ys = L["nodes"][src]; xd, yd = L["nodes"][dst]
            is_new = (src, dst, style) in L["new_edges"]
            color = hi if is_new else "#404040"
            lw = 1.6 if is_new else 1.0
            if src == dst:
                arrow = mpatches.FancyArrowPatch(
                    (xs - 0.055, ys + 0.055), (xs + 0.055, ys + 0.055),
                    connectionstyle="arc3,rad=-1.6", arrowstyle="-|>",
                    mutation_scale=8, linewidth=lw, color=color,
                    linestyle="dashed" if style == "dashed" else "solid",
                    shrinkA=1, shrinkB=1)
            else:
                arrow = mpatches.FancyArrowPatch(
                    (xs, ys), (xd, yd), connectionstyle="arc3,rad=0.12",
                    arrowstyle="-|>", mutation_scale=9, linewidth=lw, color=color,
                    linestyle="dashed" if style == "dashed" else "solid",
                    shrinkA=13, shrinkB=13)
            ax.add_patch(arrow)

        for name, (x, y) in L["nodes"].items():
            is_new = name in L["new_nodes"]
            ax.add_patch(mpatches.FancyBboxPatch(
                (x - 0.11, y - 0.055), 0.22, 0.11,
                boxstyle="round,pad=0.02,rounding_size=0.03",
                linewidth=1.4 if is_new else 0.8,
                facecolor=LEVEL_TINT[dom] if is_new else "#fdefe0",
                edgecolor=hi if is_new else "black"))
            ax.text(x, y, name, ha="center", va="center",
                    fontsize=6.4 if len(name) > 8 else 7)

        phases = L.get("phases")
        if phases:
            new_phases = set(L.get("new_phases", []))
            nx, ny = next(iter(L["nodes"].values()))
            n_ph = len(phases)
            cw, ch = 0.76, 0.16
            cy = ny - 0.24
            ax.add_patch(mpatches.FancyBboxPatch(
                (nx - cw / 2, cy - ch / 2), cw, ch,
                boxstyle="round,pad=0.01,rounding_size=0.02", linewidth=0.6,
                linestyle=(0, (2, 2)), facecolor="#f8f8f8", edgecolor="#888"))
            pw = min(0.18, (cw - 0.06) / n_ph - 0.02)
            gap = (cw - n_ph * pw - 0.04) / max(n_ph - 1, 1) if n_ph > 1 else 0
            start = nx - cw / 2 + 0.02 + pw / 2
            for j, ph in enumerate(phases):
                px = start + j * (pw + gap)
                new = ph in new_phases
                pe = hi if new else "#606060"
                ax.add_patch(mpatches.FancyBboxPatch(
                    (px - pw / 2, cy - 0.03), pw, 0.06,
                    boxstyle="round,pad=0.005,rounding_size=0.015",
                    linewidth=1.1 if new else 0.6,
                    facecolor=LEVEL_TINT[dom] if new else "#ffffff", edgecolor=pe))
                ax.text(px, cy, ph, ha="center", va="center", fontsize=5.6,
                        color=pe if new else "#404040")
                if j < n_ph - 1:
                    ax.annotate("", xy=(px + pw / 2 + gap - 0.005, cy),
                                xytext=(px + pw / 2 + 0.005, cy),
                                arrowprops=dict(arrowstyle="->", color="#666",
                                                lw=0.7, shrinkA=0, shrinkB=0))

        # predicate guards sit on the element they guard and persist once added
        for lab, anch, born in guards:
            live = (born == col)
            gc = LEVEL_COLOR["P"] if live else FADED
            if anch[0] == "edge":
                gx, gy = edge_point(L, anch[1], anch[2])
            else:
                gx, gy = L["nodes"][anch[1]]
                gy += 0.135
            ax.text(gx, gy, lab, ha="center", va="center", fontsize=6, color=gc,
                    bbox=dict(boxstyle="round,pad=0.15", facecolor="white",
                              edgecolor=gc, linewidth=1.0 if live else 0.6))

        # the structural change of this round, named under the graph
        sy = 0.07
        for lv, lab, _ in edits:
            if lv != "S":
                continue
            ax.text(0.5, sy, lab, ha="center", va="top", fontsize=7,
                    color=LEVEL_COLOR["S"])
            sy -= 0.115

        # shared rule and culture, accumulating across the row
        if ctx:
            top, line = -0.12, 0.13
            h = 0.06 + line * len(ctx)
            ax.add_patch(mpatches.FancyBboxPatch(
                (0.06, top - h), 0.88, h,
                boxstyle="round,pad=0.01,rounding_size=0.02", linewidth=0.7,
                linestyle=(0, (2, 2)), facecolor="#ffffff", edgecolor="#b0b0b0"))
            ax.text(0.14, top, "shared context", ha="center", va="center",
                    fontsize=5.5, color="#888888", style="italic",
                    bbox=dict(boxstyle="square,pad=0.12", facecolor="white",
                              edgecolor="none"))
            for k, (lab, born) in enumerate(ctx):
                live = (born == col)
                ax.text(0.5, top - 0.06 - line * k,
                        ("+ " if live else "  ") + lab, ha="center", va="center",
                        fontsize=6.5,
                        color=LEVEL_COLOR["C"] if live else FADED)

        ax.set_title(f"$v_{col + 1}$", fontsize=9)

    label = "OfficeQA Pro" if bench == "OfficeQA" else bench
    axes[row, 0].text(-0.09, 0.5, label, transform=axes[row, 0].transAxes,
                      ha="right", va="center", fontsize=9.5, fontweight="bold",
                      rotation=90)

legend_elems = [
    Line2D([0], [0], color="#404040", lw=1.0, linestyle="-", label="handoff"),
    Line2D([0], [0], color="#404040", lw=1.0, linestyle="--", label="retry / validity edge"),
    mpatches.Patch(facecolor=LEVEL_COLOR["S"], edgecolor="none", label="structural edit"),
    mpatches.Patch(facecolor=LEVEL_COLOR["P"], edgecolor="none", label="predicate edit"),
    mpatches.Patch(facecolor=LEVEL_COLOR["C"], edgecolor="none", label="contextual edit"),
    mpatches.Patch(facecolor=FADED, edgecolor="none", label="carried from an earlier round"),
]
fig.legend(handles=legend_elems, loc="lower center", ncol=6, frameon=False,
           fontsize=8.5, bbox_to_anchor=(0.5, -0.006))
plt.tight_layout(rect=[0.02, 0.02, 1, 1])

out = ROOT / "figures" / "protocol_evolution.pdf"
plt.savefig(out, bbox_inches="tight")
print(f"saved {out}")
