"""Paper figures with the current author-adjusted architecture layout."""

from pathlib import Path
import argparse
import base64
import json
import shutil

ROOT = Path(__file__).resolve().parents[2]
from . import style as v
from ..reference import DATA

EDGE = "#000000"
BLUE = "#EAF4FB"
GREEN = "#F0F8EC"
CREAM = "#FFF8DF"
GOLD = INNER = "#000000"
TEXT_CHECKS = []
LAYOUT_CHECKS = []


def panel(ax, x, y, w, h, fill="white", edge="#000000", lw=0.75, radius=1.6):
    patch = v.FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=fill,
        edgecolor="#000000",
        linewidth=lw,
    )
    ax.add_patch(patch)
    if not hasattr(ax, "_node_regions"):
        ax._node_regions = []
    ax._node_regions.append((x, y, w, h))


def t(ax, x, y, label, fs=8.5, bold=False, ha="center", va="center", linespacing=1.18):
    return ax.text(
        x,
        y,
        label,
        fontsize=fs,
        fontweight="bold" if bold else "normal",
        ha=ha,
        va=va,
        color="#000000",
        linespacing=linespacing,
    )


def document(ax, x, y, w, h):
    from matplotlib.patches import Polygon

    fold = 2.0
    ax.add_patch(
        Polygon(
            [(x, y), (x + w, y), (x + w, y + h - fold), (x + w - fold, y + h), (x, y + h)],
            closed=True,
            facecolor="white",
            edgecolor="#000000",
            linewidth=0.6,
        )
    )
    ax.plot(
        [x + w - fold, x + w - fold, x + w],
        [y + h, y + h - fold, y + h - fold],
        color="#000000",
        lw=0.6,
    )
    t(ax, x + w / 2, y + h * 0.48, "C", fs=11.0, bold=True)


def line(ax, points, lw=0.75):
    ax.plot(
        [p[0] for p in points],
        [p[1] for p in points],
        color="#000000",
        lw=lw,
        solid_capstyle="butt",
        solid_joinstyle="miter",
    )
    if not hasattr(ax, "_routes"):
        ax._routes = []
    ax._routes.append({"points": points, "arrow": False})


def arrow(ax, points):
    from matplotlib.path import Path as MplPath
    import numpy as np

    assert len(points) >= 2
    assert all((a[0] == b[0]) != (a[1] == b[1]) for a, b in zip(points, points[1:])), (
        "Orthogonal nonzero segments"
    )
    display = ax.transData.transform(points)
    terminal = np.linalg.norm(display[-1] - display[-2]) * 72 / ax.figure.dpi
    assert terminal >= 5.0, ("Arrow terminal must fit its head", terminal, points)
    # Leave a one-point clearance before the node border; draw one continuous path.
    unit = (display[-1] - display[-2]) / np.linalg.norm(display[-1] - display[-2])
    display[-1] -= unit * (0.9 * ax.figure.dpi / 72)
    adjusted = ax.transData.inverted().transform(display)
    path = MplPath(adjusted, [MplPath.MOVETO] + [MplPath.LINETO] * (len(points) - 1))
    ax.add_patch(
        v.FancyArrowPatch(
            path=path,
            arrowstyle="-|>",
            mutation_scale=7.0,
            linewidth=0.75,
            facecolor="#000000",
            edgecolor="#000000",
            capstyle="butt",
            joinstyle="miter",
        )
    )
    if not hasattr(ax, "_routes"):
        ax._routes = []
    ax._routes.append(
        {"points": adjusted.tolist(), "arrow": True, "terminal_points": float(terminal)}
    )


def overview():
    fig, ax = v.canvas(7, 3.40, xmax=200, ymax=100)
    panel(ax, 1, 18, 34, 67, BLUE)
    t(ax, 18, 81, "Bound evidence", 9.6, True)
    document(ax, 6, 62, 10, 14)
    document(ax, 21, 62, 10, 14)
    t(ax, 11, 58, "old", 8.2)
    t(ax, 26, 58, "new", 8.2)
    t(ax, 18, 49, "Source / build identity\nAuthored call interface", 8.3)
    t(ax, 18, 39.5, r"Entry object $d$", 8.4)
    for i in range(8):
        x = 3.3 + 3.75 * i
        ax.add_patch(
            v.Rectangle((x, 32), 3.3, 4.8, facecolor="white", edgecolor="#000000", linewidth=0.5)
        )
    panel(ax, 3.5, 20.5, 29, 8.2, "#FFFDFA", lw=0.6, radius=1.3)
    t(ax, 18, 24.6, r"$z=(x,c,d)$", 9.8)

    panel(ax, 43, 56, 75, 41, GREEN)
    t(ax, 80.5, 92.5, "Restricted summary proposal", 9.8, True)
    panel(ax, 46, 65, 30, 22, "white", lw=0.55, radius=1.4)
    t(ax, 61, 83, "Native queries", 8.8, True)
    t(ax, 61, 76.5, r"$0,\ e_i,\ldots$", 10.0)
    t(ax, 61, 70, "membership / basis", 8.0)
    panel(ax, 83, 65, 32, 22, "white", lw=0.55, radius=1.4)
    t(ax, 99, 83, r"Candidate $S_v$", 8.8, True)
    t(ax, 99, 74.9, "bit / affine\ninteger / ordered", 8.4)
    arrow(ax, [(76, 77), (83, 77)])
    t(ax, 80.5, 60.4, "Finite observations propose candidates", 8.2)

    panel(ax, 43, 7, 75, 43, GREEN)
    t(ax, 80.5, 46.4, "Field-sensitive qualification", 9.6, True)
    panel(ax, 46, 21, 31, 20, "white", lw=0.55, radius=1.4)
    t(ax, 61.5, 38.1, "Source route", 8.7, True)
    t(ax, 61.5, 29.2, "Targets + safety\nComplete unwinding\nListed rule premises", 8.1)
    panel(ax, 82, 21, 33, 20, "white", lw=0.55, radius=1.4)
    t(ax, 98.5, 38.1, "Emission check", 8.7, True)
    t(ax, 98.5, 29.2, "Model / emitted C\nRanges + coefficients\nIndependent replay", 8.1)
    t(ax, 79.5, 30, "+", 9.6, True)
    panel(ax, 46, 9.5, 69, 8.4, "#FFFDFA", lw=0.6, radius=1.3)
    t(ax, 80.5, 13.7, r"$\forall z\in D_v:\ \pi_PF_v(z)=\pi_PS_v(z)$", 9.3)

    panel(ax, 126, 22, 45, 61, CREAM)
    t(ax, 148.5, 78.1, "Relational guard", 9.8, True)
    panel(ax, 129, 66.5, 39, 8.5, "white", lw=0.55, radius=1.3)
    t(ax, 148.5, 70.7, "Admitted old/new pair", 8.4)
    panel(ax, 129, 46.5, 39, 15.5, "#FFFDFA", lw=0.6, radius=1.3)
    t(ax, 148.5, 54.2, r"$G_P=[\pi_PS_o(z_o)$" + "\n" + r"$=\pi_PS_n(z_n)]$", 9.8)
    t(
        ax,
        148.5,
        34.7,
        "Call premises must hold\nAffine: checked kernel\nOthers: typed predicates",
        8.1,
    )
    for y, title, body in [
        (68, "SUPPORT", "Equal on P"),
        (45, "REFUTE", "Unequal on P"),
        (22, "UNKNOWN", "Abstain"),
    ]:
        panel(ax, 176, y, 23, 14, BLUE)
        t(ax, 187.5, y + 10.2, title, 8.7, True)
        t(ax, 187.5, y + 4.1, body, 8.1)
    arrow(ax, [(35, 74), (43, 74)])
    arrow(ax, [(35, 34), (43, 34)])
    arrow(ax, [(98, 56), (98, 50)])
    arrow(ax, [(118, 43), (126, 43)])
    for y in [75, 52, 29]:
        arrow(ax, [(171, y), (176, y)])
    t(ax, 80.5, 2.5, "Incomplete checks yield UNKNOWN", 8.0)
    save(fig, "fig01_system_overview")


def decision():
    fig, ax = v.canvas(3.35, 2.65, xmax=100, ymax=100)
    panel(ax, 1, 80, 98, 18, BLUE, lw=0.75, radius=1.4)
    t(ax, 50, 93.6, "Call premises and fields valid?", 9.2, True)
    t(ax, 50, 86.4, r"Request $(z_o,z_n,P)$", 9.2)
    panel(ax, 77, 60, 22, 14, BLUE, lw=0.75, radius=1.4)
    t(ax, 88, 70.4, "UNKNOWN", 8.3, True)
    t(ax, 88, 64, "Abstain", 8.1)
    arrow(ax, [(88, 80), (88, 74)])
    t(ax, 94, 77, "no", 8.0)
    line(ax, [(50, 80), (50, 57)])
    line(ax, [(23, 57), (77, 57)])
    arrow(ax, [(23, 57), (23, 53)])
    arrow(ax, [(77, 57), (77, 53)])
    t(ax, 55.5, 68.5, "yes", 8.0)
    for x, title, model in [
        (1, "Old contract", r"$\pi_PS_o(z_o)$"),
        (55, "New contract", r"$\pi_PS_n(z_n)$"),
    ]:
        panel(ax, x, 31, 44, 22, BLUE, lw=0.75, radius=1.4)
        t(ax, x + 22, 49.2, title, 8.9, True)
        panel(ax, x + 3, 37, 38, 8, "#FFFDFA", lw=0.55, radius=1)
        t(ax, x + 22, 41, model, 9.3)
        for i in range(9):
            ax.add_patch(
                v.Rectangle(
                    (x + 4 + i * 4, 33),
                    3.3,
                    2.2,
                    facecolor="white",
                    edgecolor="#000000",
                    linewidth=0.45,
                )
            )
    panel(ax, 15, 14, 70, 9, CREAM, lw=0.7, radius=1.3)
    t(ax, 50, 18.5, r"$G_P=[\pi_PS_o=\pi_PS_n]$", 9.2)
    arrow(ax, [(23, 31), (23, 23)])
    arrow(ax, [(77, 31), (77, 23)])
    panel(ax, 1, 0.5, 43, 8, GREEN, lw=0.75, radius=1.2)
    t(ax, 22.5, 4.5, "SUPPORT: equal", 8.9, True)
    panel(ax, 56, 0.5, 43, 8, CREAM, lw=0.75, radius=1.2)
    t(ax, 77.5, 4.5, "REFUTE: unequal", 8.9, True)
    arrow(ax, [(22.5, 14), (22.5, 8.5)])
    arrow(ax, [(77.5, 14), (77.5, 8.5)])
    save(fig, "fig02_request_decision")


def check_geometry(fig, name):
    if name not in ["fig01_system_overview", "fig02_request_decision"]:
        return
    from matplotlib.transforms import Bbox

    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    scale = fig.dpi / 72
    texts = []
    inside = []
    collisions = []
    wire_hits = []
    for ax in fig.axes:
        for obj in ax.texts:
            if not obj.get_visible() or not obj.get_text():
                continue
            bbox = obj.get_window_extent(renderer)
            texts.append((obj, bbox))
            # Require every label to fit its innermost containing module, with padding.
            x, y = obj.get_position()
            regions = [
                r
                for r in getattr(ax, "_node_regions", [])
                if r[0] < x < r[0] + r[2] and r[1] < y < r[1] + r[3]
            ]
            if regions:
                rx, ry, rw, rh = min(regions, key=lambda r: r[2] * r[3])
                corners = ax.transData.transform([(rx, ry), (rx + rw, ry + rh)])
                area = Bbox(corners).padded(-1.2 * scale)
                if not (
                    area.x0 <= bbox.x0
                    and area.y0 <= bbox.y0
                    and area.x1 >= bbox.x1
                    and area.y1 >= bbox.y1
                ):
                    inside.append(obj.get_text())
            if not (
                bbox.x0 >= 0
                and bbox.y0 >= 0
                and bbox.x1 <= fig.bbox.width
                and bbox.y1 <= fig.bbox.height
            ):
                inside.append("Canvas: " + obj.get_text())
        for route in getattr(ax, "_routes", []):
            points = ax.transData.transform(route["points"])
            for a, b in zip(points, points[1:]):
                for obj, bbox in texts:
                    r = bbox.padded(1.0 * scale)
                    if abs(a[0] - b[0]) < 1e-4:
                        hit = r.x0 < a[0] < r.x1 and max(min(a[1], b[1]), r.y0) < min(
                            max(a[1], b[1]), r.y1
                        )
                    else:
                        hit = r.y0 < a[1] < r.y1 and max(min(a[0], b[0]), r.x0) < min(
                            max(a[0], b[0]), r.x1
                        )
                    if hit:
                        wire_hits.append(obj.get_text())
    for i, (a, ab) in enumerate(texts):
        for b, bb in texts[i + 1 :]:
            if ab.padded(0.5 * scale).overlaps(bb.padded(0.5 * scale)):
                collisions.append([a.get_text(), b.get_text()])
    need = {
        "asset": name,
        "labels_checked": len(texts),
        "labels_outside_module_or_canvas": inside,
        "label_overlaps": collisions,
        "wire_label_intersections": wire_hits,
        "continuous_orthogonal_routes": sum(len(getattr(ax, "_routes", [])) for ax in fig.axes),
        "required_module_text_padding_points": 1.2,
        "required_wire_text_clearance_points": 1.0,
        "required_label_gap_points": 1.0,
    }
    LAYOUT_CHECKS.append(need)
    assert not inside and not collisions and not wire_hits, json.dumps(need, ensure_ascii=False)


def save(fig, name, pdf=True):
    import matplotlib
    from matplotlib.text import Text
    from matplotlib.colors import to_rgba

    drawn = []
    for obj in fig.findobj(Text):
        obj.set_color("#000000")
        if obj.get_text():
            assert to_rgba(obj.get_color()) == (0.0, 0.0, 0.0, 1.0)
            drawn.append({"text": obj.get_text(), "rgba": [0, 0, 0, 1]})
    TEXT_CHECKS.append({"asset": name, "all_text_black": True, "text_objects": len(drawn)})
    border_count = 0
    for ax in fig.axes:
        for patch in ax.patches:
            ec = patch.get_edgecolor()
            if len(ec) == 4 and ec[3] > 0:
                assert tuple(ec[:3]) == (0.0, 0.0, 0.0), (
                    "Every visible diagram/plot border must be black"
                )
                border_count += 1
    TEXT_CHECKS[-1]["black_borders_checked"] = border_count
    check_geometry(fig, name)
    for ext in ["pdf", "svg", "png"] if pdf else ["svg", "png"]:
        metadata = (
            {"Creator": "ICPC reference-style v19", "CreationDate": None, "ModDate": None}
            if ext == "pdf"
            else {"Creator": "ICPC reference-style v19", "Date": None}
            if ext == "svg"
            else None
        )
        fig.savefig(v.FIG / (name + "." + ext), dpi=300, metadata=metadata)
        if ext == "svg":
            svg = (v.FIG / (name + ".svg")).read_text(encoding="utf-8")
            fontdir = Path(matplotlib.get_data_path()) / "fonts/ttf"
            css = []
            for fname, weight, style in [
                ("STIXGeneral.ttf", 400, "normal"),
                ("STIXGeneralBol.ttf", 700, "normal"),
                ("STIXGeneralItalic.ttf", 400, "italic"),
                ("STIXGeneralBolIta.ttf", 700, "italic"),
            ]:
                data = base64.b64encode((fontdir / fname).read_bytes()).decode("ascii")
                css.append(
                    "@font-face{font-family:'STIXGeneral';font-weight:"
                    + str(weight)
                    + ";font-style:"
                    + style
                    + ";src:url(data:font/ttf;base64,"
                    + data
                    + ") format('truetype');}"
                )
            svg = svg.replace(
                "<defs>", '<defs>\n<style type="text/css">' + "".join(css) + "</style>", 1
            )
            (v.FIG / (name + ".svg")).write_text(svg, encoding="utf-8")
    v.plt.close(fig)


def render(output):
    output = Path(output).resolve()
    for protected in ["scguard", "provenance", "third_party", "tests", "docs", "examples"]:
        parent = ROOT / protected
        if output == parent or parent in output.parents or output == ROOT:
            raise ValueError("Choose an output directory separate from source and reference data")
    output.mkdir(parents=True, exist_ok=True)
    TEXT_CHECKS.clear()
    LAYOUT_CHECKS.clear()
    v.FIG = output
    v.setup_fonts()
    v.plt.rcParams.update(
        {
            "svg.hashsalt": "icpc-visual-v19",
            "text.color": "#000000",
            "axes.labelcolor": "#000000",
            "xtick.color": "#000000",
            "ytick.color": "#000000",
        }
    )
    overview()
    decision()
    data = json.loads((DATA / "figures/figure_data.json").read_text(encoding="utf-8"))
    stages = data["contract_stages"]
    current = {
        "API_version_tasks": 12,
        "full_observation_contracts": stages[2]["full"],
        "partial_contracts": stages[2]["partial"],
        "current_unqualified_tasks": stages[2]["unknown"],
    }
    previous = {
        "full_contract_tasks": stages[1]["full"],
        "field_gate_qualified_partial_contracts": stages[1]["partial"],
    }
    v.coverage(current, previous, save)
    v.outcomes(data["api_groups"], save)
    tables = json.loads((DATA / "figures/table_data.json").read_text(encoding="utf-8"))
    v.table_preview(
        "table01_guard_policies",
        ["Guard policy", "Support", "Refute", "Unknown", "Wrong S/R"],
        tables["writer_policy_rows"],
        [0.32, 0.16, 0.16, 0.17, 0.17],
        3.35,
        1.55,
        save,
    )
    descriptions = {
        "CRC-32": "Original step / stream + DFCC\nChecked coefficient composition",
        "Adler-32": "Original ranges + arithmetic rule\nChecked prefix emission",
        "Memory move": "Original C, complete CBMC\nand joint ESBMC results",
        "Compare sign": "Original CBMC + typed rule\nNormalized ESBMC check",
    }
    rows = [list(row[:4]) + [descriptions[row[0]]] for row in tables["source_qualification_rows"]]
    v.table_preview(
        "table02_source_qualification",
        [
            "API",
            "Frozen\nF/P/U",
            "Intermediate\nF/P/U",
            "Qualified\nF/P/U",
            "Final source connection",
        ],
        rows,
        [0.15, 0.10, 0.14, 0.12, 0.47],
        7,
        2.05,
        save,
    )
    for name in ["visual_policy_table.tex", "visual_qualification_table.tex"]:
        shutil.copy2(DATA / "figures" / name, output / name)
    result = {
        "all_checks_passed": True,
        "text_colour": "#000000",
        "border_and_arrow_colour": "#000000",
        "geometry_checks": LAYOUT_CHECKS,
        "text_checks": TEXT_CHECKS,
        "figure_sets": 4,
        "table_sets": 2,
        "source_experiments_executed": 0,
    }
    (output / "render_checks.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    return {"output": str(output), "figure_sets": 4, "table_sets": 2, "all_checks_passed": True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "build/figures")
    print(json.dumps(render(parser.parse_args().output), indent=2))


if __name__ == "__main__":
    main()
