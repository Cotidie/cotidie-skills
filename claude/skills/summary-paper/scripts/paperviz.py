#!/usr/bin/env python3
"""Deterministic figure generation for /summary-paper.

Subcommands
  card     paces.json  -o figures/paces-card.svg
  chart    results.json -o figures/results.svg [--kind auto|bar|dot]
  crop     paper.pdf --page N --bbox x0 y0 x1 y1 -o figures/fig-N.png [--dpi 200]
  preview  paper.pdf --page N -o /tmp/p.png      (page with a 0.1 grid for bbox reading)
  preview  figure.svg -o /tmp/f.png              (rasterize an SVG: rsvg/inkscape/chrome, MuPDF fallback)
  toc      paper.pdf                               (likely section headings per page, by font size)

Palette matches textbook-notes (light theme).
"""
import argparse
import json
import sys
from pathlib import Path
from xml.sax.saxutils import escape

INK, INK2, INK3 = "#141A1D", "#4C575C", "#76838A"
LINE, LINE2, SURFACE, GROUND = "#D2D9DC", "#B4BFC3", "#FFFFFF", "#EDEFF0"
ACCENT, ACCENT_SOFT = "#0A6C77", "#DCEDEF"
WARM, WARM_SOFT = "#8F5D0D", "#F5E8CF"
FLAG, FLAG_SOFT = "#9C2A24", "#F3DDDB"
FONT = "'IBM Plex Sans KR','Apple SD Gothic Neo','NanumGothic',system-ui,sans-serif"
MONO = "'IBM Plex Mono','SF Mono',Menlo,monospace"


# ---------------------------------------------------------------- text utils
def char_w(ch: str, px: float) -> float:
    o = ord(ch)
    if 0x1100 <= o <= 0x11FF or 0x3000 <= o <= 0x9FFF or 0xAC00 <= o <= 0xD7AF or 0xFF00 <= o <= 0xFFEF:
        return px * 0.98          # CJK: roughly one em
    if ch in "iljtfI.,:;'|!":
        return px * 0.30
    if ch.isupper() or ch in "mwMW@":
        return px * 0.66
    return px * 0.52


def text_w(s: str, px: float) -> float:
    return sum(char_w(c, px) for c in s)


def wrap(text: str, max_px: float, px: float, max_lines: int = 0) -> list[str]:
    """Greedy word wrap by estimated width. A single word wider than the line
    (long CJK run, URL) is split per character."""
    lines, cur = [], ""
    for word in text.replace("\n", " ").split():
        cand = f"{cur} {word}" if cur else word
        if text_w(cand, px) <= max_px:
            cur = cand
            continue
        if cur:
            lines.append(cur)
            cur = ""
        if text_w(word, px) <= max_px:
            cur = word
            continue
        for ch in word:  # oversize word: hard-split
            if text_w(cur + ch, px) <= max_px or not cur:
                cur += ch
            else:
                lines.append(cur)
                cur = ch
    if cur:
        lines.append(cur)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(" .,") + "…"
    return lines


def tspans(lines, x, y, lh) -> str:
    return "".join(
        f'<tspan x="{x}" y="{y + i * lh:.1f}">{escape(l)}</tspan>' for i, l in enumerate(lines)
    )


# ---------------------------------------------------------------- card
ROWS = [
    ("P", "Problem", "problem"),
    ("A", "Approach", "approach"),
    ("C", "Claim", "claim"),
    ("E", "Evaluation", "evaluation"),
    ("S", "Substantiation", "substantiation"),
]
VERDICT_STYLE = {
    "yes": (ACCENT, ACCENT_SOFT),
    "partial": (WARM, WARM_SOFT),
    "no": (FLAG, FLAG_SOFT),
}


def cmd_card(args):
    d = json.loads(Path(args.input).read_text(encoding="utf-8"))
    W, PAD = 960, 36
    label_w, gap = 150, 22
    text_x = PAD + label_w + gap
    text_w_px = W - text_x - PAD
    body_px, body_lh = 16.5, 25
    out = []
    y = PAD + 4

    title_lines = wrap(d["title"], W - 2 * PAD, 26, max_lines=2)
    out.append(
        f'<text font-family="{FONT}" font-size="26" font-weight="600" fill="{INK}" '
        f'letter-spacing="-0.01em">{tspans(title_lines, PAD, y + 26, 33)}</text>'
    )
    y += 26 + 33 * (len(title_lines) - 1) + 14
    meta = " · ".join(str(d[k]) for k in ("authors", "venue", "year") if d.get(k))
    if meta:
        out.append(
            f'<text x="{PAD}" y="{y + 12}" font-family="{MONO}" font-size="12.5" '
            f'letter-spacing="0.06em" fill="{INK3}">{escape(meta)}</text>'
        )
        y += 30
    y += 10
    out.append(f'<line x1="{PAD}" y1="{y}" x2="{W - PAD}" y2="{y}" stroke="{LINE2}" stroke-width="1"/>')
    y += 22

    for letter, word, key in ROWS:
        val = d.get(key, "")
        verdict = None
        if key == "substantiation" and isinstance(val, dict):
            verdict = str(val.get("verdict", "")).strip()
            val = val.get("text", "")
        lines = wrap(str(val), text_w_px, body_px, max_lines=4)
        row_h = max(len(lines) * body_lh, 44)
        # label column
        out.append(
            f'<text x="{PAD}" y="{y + 30}" font-family="{MONO}" font-size="30" font-weight="600" '
            f'fill="{ACCENT}">{letter}</text>'
        )
        out.append(
            f'<text x="{PAD + 30}" y="{y + 28}" font-family="{MONO}" font-size="11.5" '
            f'letter-spacing="0.12em" fill="{INK3}">{word.upper()}</text>'
        )
        ty = y + 20
        if verdict:
            col, soft = VERDICT_STYLE.get(verdict.lower(), (INK2, GROUND))
            pill_w = text_w(verdict, 13) + 26
            out.append(
                f'<rect x="{text_x}" y="{y + 4}" width="{pill_w:.0f}" height="24" rx="12" fill="{soft}"/>'
                f'<text x="{text_x + pill_w / 2:.1f}" y="{y + 20.5}" text-anchor="middle" font-family="{MONO}" '
                f'font-size="13" font-weight="600" letter-spacing="0.08em" fill="{col}">{escape(verdict)}</text>'
            )
            ty = y + 4 + 24 + 20
            row_h = max(row_h, 24 + 8 + len(lines) * body_lh)
        out.append(
            f'<text font-family="{FONT}" font-size="{body_px}" fill="{INK}">'
            f'{tspans(lines, text_x, ty, body_lh)}</text>'
        )
        y += row_h + 18
        if key != "substantiation":
            out.append(f'<line x1="{text_x}" y1="{y - 8}" x2="{W - PAD}" y2="{y - 8}" stroke="{LINE}" stroke-width="1"/>')
    H = y + PAD - 10
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        f'role="img" aria-label="PACES summary card">'
        f'<rect width="{W}" height="{H}" fill="{SURFACE}" stroke="{LINE2}"/>'
        + "".join(out)
        + "</svg>\n"
    )
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(svg, encoding="utf-8")
    print(args.output)


# ---------------------------------------------------------------- chart
def cmd_chart(args):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import rcParams

    import logging
    from matplotlib import font_manager

    logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
    rcParams["svg.fonttype"] = "none"  # keep text as text; the viewer's fonts apply
    installed = {f.name for f in font_manager.fontManager.ttflist}
    preferred = ["IBM Plex Sans KR", "Pretendard", "NanumGothic", "Noto Sans CJK KR",
                 "Apple SD Gothic Neo", "Malgun Gothic", "DejaVu Sans"]
    rcParams["font.family"] = [f for f in preferred if f in installed] or ["sans-serif"]
    d = json.loads(Path(args.input).read_text(encoding="utf-8"))
    groups = d["groups"]
    methods = []
    for g in groups:
        for m in g["values"]:
            if m not in methods:
                methods.append(m)
    highlight = d.get("highlight")
    vals = [v for g in groups for v in g["values"].values() if v is not None]
    kind = args.kind
    if kind == "auto":
        # Decide per group: a SOTA table has groups on different baselines
        # (ImageNet 88 vs VTAB 77) but 1-3 point gaps inside each group. Bars
        # from zero hide those gaps, so use dots unless some group spreads wide.
        def spread(g):
            gv = [v for v in g["values"].values() if v is not None]
            return (max(gv) - min(gv)) / max(abs(max(gv)), 1e-9) if len(gv) > 1 else 0
        kind = "bar" if any(spread(g) >= 0.15 for g in groups) else "dot"

    n_g, n_m = len(groups), len(methods)
    fig_w = max(6.4, 1.6 * n_g * max(n_m, 2) * 0.55 + 2)
    fig, ax = plt.subplots(figsize=(min(fig_w, 11), 4.2 if kind == "bar" else 1.0 + 0.55 * n_g * n_m))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    greys = [INK3, LINE2, INK2, "#9AA5AA", "#5F6B70", "#C3CCD0"]

    def color(m, i):
        return ACCENT if m == highlight else greys[i % len(greys)]

    if kind == "bar":
        width = 0.8 / n_m
        for i, m in enumerate(methods):
            xs = [gi + (i - (n_m - 1) / 2) * width for gi in range(n_g)]
            ys = [g["values"].get(m) for g in groups]
            ys_plot = [y if y is not None else 0 for y in ys]
            bars = ax.bar(xs, ys_plot, width * 0.92, color=color(m, i), label=m, zorder=3)
            for b, y in zip(bars, ys):
                if y is None:
                    continue
                ax.annotate(
                    f"{y:g}", (b.get_x() + b.get_width() / 2, b.get_height()),
                    xytext=(0, 3), textcoords="offset points", ha="center", va="bottom",
                    fontsize=8.5, color=INK2,
                )
        ax.set_xticks(range(n_g))
        ax.set_xticklabels([g["name"] for g in groups], fontsize=10, color=INK)
        ax.set_ylabel(d.get("metric", ""), fontsize=10, color=INK2)
        ax.yaxis.grid(True, color=LINE, linewidth=0.8, zorder=0)
        ax.set_axisbelow(True)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for s in ("left", "bottom"):
            ax.spines[s].set_color(LINE2)
        ax.tick_params(colors=INK2, length=0)
        if n_m > 1:
            ax.legend(frameon=False, fontsize=9, ncol=min(n_m, 4), loc="upper center",
                      bbox_to_anchor=(0.5, -0.14))
    else:  # dot plot, narrow range, axis does not start at zero
        rows, labels, ys_pos = [], [], []
        pos = 0
        for g in groups:
            for i, m in enumerate(methods):
                v = g["values"].get(m)
                if v is None:
                    continue
                rows.append((pos, v, color(m, i), m == highlight))
                labels.append(f"{g['name']} · {m}" if n_g > 1 else m)
                ys_pos.append(pos)
                pos += 1
            pos += 0.6
        lo, hi = min(vals), max(vals)
        pad = (hi - lo) * 0.25 or abs(hi) * 0.02 or 1
        for p, v, c, hl in rows:
            ax.hlines(p, lo - pad, v, color=LINE, linewidth=1.2, zorder=2)
            ax.plot(v, p, "o", color=c, markersize=9 if hl else 7, zorder=3)
            ax.annotate(f"{v:g}", (v, p), xytext=(7, 0), textcoords="offset points",
                        va="center", fontsize=9, color=INK if hl else INK2,
                        fontweight="bold" if hl else "normal")
        ax.set_yticks(ys_pos)
        ax.set_yticklabels(labels, fontsize=9.5, color=INK)
        ax.invert_yaxis()
        ax.set_xlim(lo - pad, hi + pad * 1.6)
        ax.set_xlabel(d.get("metric", "") + "   (축은 0에서 시작하지 않음)", fontsize=9.5, color=INK2)
        ax.xaxis.grid(True, color=LINE, linewidth=0.8, zorder=0)
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)
        ax.spines["bottom"].set_color(LINE2)
        ax.tick_params(colors=INK2, length=0)

    title = d.get("title", "")
    if d.get("higher_is_better") is False:
        title += "  (↓ lower is better)"
    if title:
        ax.set_title(title, loc="left", fontsize=11.5, color=INK, fontweight="bold", pad=12)
    if d.get("source"):
        fig.text(0.99, 0.01, f"출처: {d['source']}", ha="right", va="bottom", fontsize=8, color=INK3)
    fig.tight_layout()
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, format="svg", transparent=True, bbox_inches="tight")
    print(args.output)


# ---------------------------------------------------------------- crop / preview
def _fitz():
    try:
        import fitz  # PyMuPDF
    except ImportError:
        sys.exit("PyMuPDF missing: python3 -m pip install pymupdf")
    return fitz


def cmd_crop(args):
    fitz = _fitz()
    doc = fitz.open(args.input)
    page = doc[args.page - 1]
    r = page.rect
    x0, y0, x1, y1 = args.bbox
    clip = fitz.Rect(r.x0 + x0 * r.width, r.y0 + y0 * r.height, r.x0 + x1 * r.width, r.y0 + y1 * r.height)
    pix = page.get_pixmap(dpi=args.dpi, clip=clip)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    pix.save(args.output)
    print(f"{args.output} {pix.width}x{pix.height}")


def _render_svg(src: Path, out: Path, dpi: int) -> str:
    """Rasterize an SVG with the most faithful renderer installed.
    MuPDF (the fallback) drops <marker> arrowheads and substitutes fonts."""
    import shutil
    import subprocess

    out.parent.mkdir(parents=True, exist_ok=True)
    if shutil.which("rsvg-convert"):
        subprocess.run(["rsvg-convert", "-d", str(dpi), "-p", str(dpi), "-o", str(out), str(src)], check=True)
        return "rsvg-convert"
    if shutil.which("inkscape"):
        subprocess.run(["inkscape", str(src), "--export-type=png", f"--export-filename={out}",
                        f"--export-dpi={dpi}"], check=True, capture_output=True, timeout=120)
        return "inkscape"
    for chrome in ("google-chrome", "chromium", "chromium-browser"):
        if shutil.which(chrome):
            subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                            f"--window-size=1000,{int(1000 * 0.75)}", f"--screenshot={out}",
                            src.resolve().as_uri()], check=True, capture_output=True, timeout=120)
            return chrome
    fitz = _fitz()
    fitz.open(str(src))[0].get_pixmap(dpi=dpi).save(str(out))
    return "mupdf (approximate: no arrow markers, substituted fonts)"


def cmd_preview(args):
    src = Path(args.input)
    if src.suffix.lower() == ".svg":
        used = _render_svg(src, Path(args.output), args.dpi)
        print(f"{args.output} via {used}")
        return
    fitz = _fitz()
    doc = fitz.open(str(src))
    page = doc[(args.page or 1) - 1]
    if src.suffix.lower() == ".pdf":
        # draw a 0.1 grid with labels so bbox fractions can be read off the image
        shape = page.new_shape()
        r = page.rect
        for i in range(1, 10):
            x = r.x0 + r.width * i / 10
            y = r.y0 + r.height * i / 10
            shape.draw_line((x, r.y0), (x, r.y1))
            shape.draw_line((r.x0, y), (r.x1, y))
        shape.finish(color=(0.05, 0.42, 0.47), width=0.6, dashes="[3 3] 0")
        shape.commit()
        for i in range(1, 10):
            x = r.x0 + r.width * i / 10
            y = r.y0 + r.height * i / 10
            page.insert_text((x + 2, r.y0 + 10), f"{i/10:.1f}", fontsize=7, color=(0.05, 0.42, 0.47))
            page.insert_text((r.x0 + 2, y - 2), f"{i/10:.1f}", fontsize=7, color=(0.05, 0.42, 0.47))
    pix = page.get_pixmap(dpi=args.dpi)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    pix.save(args.output)
    print(f"{args.output} {pix.width}x{pix.height}")


# ---------------------------------------------------------------- toc
def cmd_toc(args):
    """Print likely section headings per page: short lines set larger or bolder than body text."""
    import statistics

    fitz = _fitz()
    doc = fitz.open(args.input)
    sizes = []
    pages = []
    for page in doc:
        d = page.get_text("dict")
        lines = []
        for b in d["blocks"]:
            for l in b.get("lines", []):
                spans = [sp for sp in l["spans"] if sp["text"].strip()]
                if not spans:
                    continue
                text = "".join(sp["text"] for sp in spans).strip()
                size = max(sp["size"] for sp in spans)
                bold = any("Bold" in sp["font"] or sp["flags"] & 16 for sp in spans)
                lines.append((text, size, bold))
                sizes.append(size)
        pages.append(lines)
    import re

    body = statistics.median(sizes) if sizes else 10
    numbered = re.compile(r"^(?:[IVX]+|[0-9]+(?:\.[0-9]+)*|[A-H])[.)]?\s+[A-Z]")  # "III. METHOD", "4.1 Setup", "A. Data"
    for i, lines in enumerate(pages, 1):
        for text, size, bold in lines:
            if len(text) > 90 or len(text) < 3:
                continue
            letters = [c for c in text if c.isalpha()]
            caps = letters and sum(c.isupper() for c in letters) / len(letters) > 0.8 and len(text) < 60
            if size >= body * 1.12 or (bold and size >= body * 0.98 and len(text) < 60) \
                    or (numbered.match(text) and len(text) < 60) or caps:
                print(f"p.{i:<3} {size:5.1f}  {text}")


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("card"); p.add_argument("input"); p.add_argument("-o", "--output", required=True)
    p.set_defaults(fn=cmd_card)
    p = sub.add_parser("chart"); p.add_argument("input"); p.add_argument("-o", "--output", required=True)
    p.add_argument("--kind", choices=["auto", "bar", "dot"], default="auto"); p.set_defaults(fn=cmd_chart)
    p = sub.add_parser("crop"); p.add_argument("input"); p.add_argument("--page", type=int, required=True)
    p.add_argument("--bbox", type=float, nargs=4, metavar=("X0", "Y0", "X1", "Y1"), required=True)
    p.add_argument("--dpi", type=int, default=200); p.add_argument("-o", "--output", required=True)
    p.set_defaults(fn=cmd_crop)
    p = sub.add_parser("toc"); p.add_argument("input"); p.set_defaults(fn=cmd_toc)
    p = sub.add_parser("preview"); p.add_argument("input"); p.add_argument("--page", type=int)
    p.add_argument("--dpi", type=int, default=72); p.add_argument("-o", "--output", required=True)
    p.set_defaults(fn=cmd_preview)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
