"""Portable figure primitives from the recorded plotting implementation."""

from collections import Counter
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Patch

INK = MUTED = EDGE = "#000000"
TEAL = "#C3DFDB"
RUST = "#E7C6AA"
GRAY = "#D7DCE2"


def setup_fonts():
    plt.rcParams.update(
        {
            "font.family": "STIXGeneral",
            "font.size": 8.5,
            "mathtext.fontset": "stix",
            "text.color": INK,
            "axes.labelcolor": INK,
            "xtick.color": INK,
            "ytick.color": INK,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "svg.hashsalt": "icpc-visual-v17",
            "hatch.linewidth": 0.35,
            "axes.linewidth": 0.65,
            "savefig.facecolor": "white",
        }
    )


def canvas(w, h, xmax=100, ymax=45):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set(xlim=(0, xmax), ylim=(0, ymax))
    ax.axis("off")
    return fig, ax


def coverage(a, prior, save):
    fig, ax = plt.subplots(figsize=(3.35, 2.28))
    fig.subplots_adjust(left=0.31, right=0.97, bottom=0.27, top=0.86)
    stages = [
        ("Frozen first\napplication", [0, 0, 12]),
        (
            "Intermediate\nfield gate",
            [
                prior["full_contract_tasks"],
                prior["field_gate_qualified_partial_contracts"],
                a["API_version_tasks"]
                - prior["full_contract_tasks"]
                - prior["field_gate_qualified_partial_contracts"],
            ],
        ),
        (
            "Qualified\ncompletion",
            [
                a["full_observation_contracts"],
                a["partial_contracts"],
                a["current_unqualified_tasks"],
            ],
        ),
    ]
    colors = [TEAL, RUST, GRAY]
    hatches = ["", "..", "///"]
    labels = ["Full", "Partial", "Unknown"]
    for i, (label, counts) in enumerate(stages):
        left = 0
        for n, c, h in zip(counts, colors, hatches):
            if n:
                ax.barh(
                    2 - i,
                    n,
                    left=left,
                    height=0.56,
                    color=c,
                    edgecolor=EDGE,
                    linewidth=0.55,
                    hatch=h,
                    zorder=3,
                )
                ax.text(
                    left + n / 2,
                    2 - i,
                    str(n),
                    ha="center",
                    va="center",
                    fontsize=9.5,
                    fontweight="bold",
                )
            left += n
        assert left == 12
    ax.set_yticks([2, 1, 0], [s[0] for s in stages], fontsize=8.5)
    ax.set_xticks([0, 3, 6, 9, 12])
    ax.set_xlim(0, 12)
    ax.set_ylim(-0.55, 2.55)
    ax.set_xlabel("API/version tasks", fontsize=8.5, labelpad=3)
    ax.set_title("Same fixed queue: 12 tasks", fontsize=9.5, pad=9)
    ax.grid(axis="x", lw=0.4, color="#CED5DC", zorder=0)
    ax.tick_params(axis="y", length=0, pad=5)
    for side in ["top", "right", "left"]:
        ax.spines[side].set_visible(False)
    fig.legend(
        [
            Patch(facecolor=c, edgecolor=EDGE, hatch=h, linewidth=0.5)
            for c, h in zip(colors, hatches)
        ],
        labels,
        loc="lower center",
        bbox_to_anchor=(0.54, -0.005),
        ncol=3,
        frameon=False,
        fontsize=8.2,
        handlelength=1.4,
        columnspacing=1.3,
    )
    save(fig, "fig03_contract_completion")


def outcomes(groups, save):
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.70), sharey=True)
    fig.subplots_adjust(left=0.17, right=0.97, bottom=0.20, top=0.73, wspace=0.18)
    color = [TEAL, RUST, GRAY]
    hatches = ["", "..", "///"]
    keys = ["SUPPORT", "REFUTE", "UNKNOWN"]
    totals = [Counter(), Counter()]
    for phase, ax in enumerate(axes):
        for i, g in enumerate(groups):
            counts = g["intermediate" if phase == 0 else "qualified"]
            start = 0
            for key, c, h in zip(keys, color, hatches):
                n = counts[key]
                totals[phase][key] += n
                w = n / g["requests"] * 100
                if n:
                    ax.barh(
                        3 - i,
                        w,
                        left=start,
                        height=0.56,
                        color=c,
                        hatch=h,
                        edgecolor=EDGE,
                        lw=0.55,
                        zorder=3,
                    )
                    ax.text(
                        start + w / 2,
                        3 - i,
                        f"{n:,}",
                        ha="center",
                        va="center",
                        fontsize=8.1,
                        bbox={"facecolor": c, "edgecolor": "none", "pad": 0.35},
                    )
                start += w
            assert abs(start - 100) < 1e-9
        ax.set_xlim(0, 100)
        ax.set_ylim(-0.55, 3.55)
        ax.set_xticks([0, 25, 50, 75, 100])
        ax.tick_params(axis="x", labelsize=8)
        ax.get_xticklabels()[-1].set_ha("right")
        ax.grid(axis="x", color="#D3D9DF", lw=0.4, zorder=0)
        ax.tick_params(axis="y", length=0, pad=7)
        for side in ["top", "right", "left"]:
            ax.spines[side].set_visible(False)
        t = totals[phase]
        name = "(a) Intermediate admission" if phase == 0 else "(b) Qualified completion"
        ax.set_title(
            name + "\n" + f"S {t['SUPPORT']:,}   R {t['REFUTE']:,}   U {t['UNKNOWN']:,}",
            fontsize=9.1,
            pad=10,
        )
    axes[0].set_yticks(
        [3, 2, 1, 0], [g["label"] + "\n" + f"N = {g['requests']:,}" for g in groups], fontsize=8.4
    )
    fig.legend(
        [Patch(facecolor=c, edgecolor=EDGE, hatch=h, lw=0.5) for c, h in zip(color, hatches)],
        ["SUPPORT: equal", "REFUTE: unequal", "UNKNOWN: abstain"],
        ncol=3,
        frameon=False,
        loc="upper center",
        bbox_to_anchor=(0.57, 1.025),
        fontsize=8.7,
        handlelength=1.5,
        columnspacing=2.0,
    )
    fig.text(
        0.58, 0.045, "Share of the same valid request catalogue (%)", ha="center", fontsize=8.7
    )
    save(fig, "fig04_request_outcomes")


def table_preview(name, headers, rows, widths, w, h, save):
    fig, ax = canvas(w, h)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    y = 0.88
    dy = 0.66 / len(rows)
    xs = [0.01]
    for v in widths[:-1]:
        xs.append(xs[-1] + v)
    ax.plot([0.01, 0.99], [0.98, 0.98], color=INK, lw=1)
    for x, header in zip(xs, headers):
        ax.text(x, y, header, ha="left", va="center", fontsize=8.8, fontweight="bold")
    ax.plot([0.01, 0.99], [0.78, 0.78], color=INK, lw=0.6)
    for i, row in enumerate(rows):
        for j, (x, value) in enumerate(zip(xs, row)):
            ax.text(
                x,
                0.78 - (i + 0.5) * dy,
                value,
                ha="left",
                va="center",
                fontsize=8.2,
                linespacing=1.1,
            )
    ax.plot([0.01, 0.99], [0.12, 0.12], color=INK, lw=0.8)
    save(fig, name, pdf=False)
