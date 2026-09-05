#!/usr/bin/env python3
"""Build a self-contained summary.html from summary.md.

  build_html.py <dir>/summary.md [-o <dir>/summary.html] [--template assets/template.html]

- Markdown -> HTML with the `markdown` package (tables, fenced code, attr_list).
- Every <img src="figures/x.svg"> is replaced by the SVG's own markup; PNG/JPG
  become base64 data URIs. The result opens offline as one file.
- `**Verdict: Yes**` inside the Substantiation section becomes a colored pill.
"""
import argparse
import base64
import html
import mimetypes
import re
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.exit("python package `markdown` missing. First run only: python3 -m pip install markdown")

HERE = Path(__file__).resolve().parent
DEFAULT_TEMPLATE = HERE.parent / "assets" / "template.html"
PACES_IDS = {"problem", "approach", "claim", "evaluation", "substantiation"}


def inline_assets(body: str, base: Path) -> str:
    def repl(m):
        attrs = m.group(1)
        src = re.search(r'src="([^"]+)"', attrs)
        if not src:
            return m.group(0)
        path = base / src.group(1)
        if not path.exists():
            return m.group(0)
        alt = re.search(r'alt="([^"]*)"', attrs)
        alt = alt.group(1) if alt else ""
        if path.suffix.lower() == ".svg":
            svg = path.read_text(encoding="utf-8")
            svg = re.sub(r"<\?xml[^>]*\?>", "", svg)
            svg = re.sub(r"<!DOCTYPE[^>]*>", "", svg)
            svg = re.sub(r"<metadata>.*?</metadata>", "", svg, flags=re.S)  # matplotlib credits carry a URL
            svg = svg.replace("<svg", f'<svg class="fig" role="img" aria-label="{html.escape(alt)}"', 1)
            return svg.strip()
        mime = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        b64 = base64.b64encode(path.read_bytes()).decode("ascii")
        return f'<img class="fig" alt="{html.escape(alt)}" src="data:{mime};base64,{b64}">'

    return re.sub(r"<img([^>]*)>", repl, body)


def wrap_figures(body: str) -> str:
    """<p><img|svg></p><p><em>caption</em></p>  or  <p><img|svg>\n<em>caption</em></p>  -> <figure>."""
    pat = re.compile(
        r"<p>((?:<img[^>]*>|<svg.*?</svg>))(?:</p>\s*<p>|\s*)(?:<em>(.*?)</em>)?</p>", re.S
    )  # caption may sit in the same <p> (no blank line in the .md) or the next one
    return pat.sub(
        lambda m: "<figure>" + m.group(1) + (f"<figcaption>{m.group(2)}</figcaption>" if m.group(2) else "") + "</figure>",
        body,
    )


def decorate(body: str) -> str:
    body = re.sub(
        r'<h2 id="(problem|approach|claim|evaluation|substantiation)">',
        lambda m: f'<h2 id="{m.group(1)}" class="paces" data-letter="{m.group(1)[0].upper()}">',
        body,
    )
    body = re.sub(
        r"<strong>Verdict:\s*(Yes|Partial|No)</strong>",
        lambda m: f'<span class="verdict verdict-{m.group(1).lower()}">{m.group(1)}</span>',
        body,
    )
    body = re.sub(r"<table>", '<div class="table-wrap"><table>', body)
    body = body.replace("</table>", "</table></div>")
    return body


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("markdown_file")
    ap.add_argument("-o", "--output")
    ap.add_argument("--template", default=str(DEFAULT_TEMPLATE))
    a = ap.parse_args()
    src = Path(a.markdown_file)
    out = Path(a.output) if a.output else src.with_suffix(".html")
    text = src.read_text(encoding="utf-8")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    title = next((l[2:].strip() for l in text.splitlines() if l.startswith("# ")), src.stem)
    md = markdown.Markdown(extensions=["tables", "fenced_code", "attr_list", "toc", "md_in_html"],
                           extension_configs={"toc": {"slugify": lambda v, s: re.sub(r"[^\w]+", "-", v.lower()).strip("-")}})
    body = md.convert(text)
    body = inline_assets(body, src.parent)
    body = wrap_figures(body)
    body = decorate(body)
    tpl = Path(a.template).read_text(encoding="utf-8")
    page = tpl.replace("{{TITLE}}", html.escape(title)).replace("{{BODY}}", body)
    out.write_text(page, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
