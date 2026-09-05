#!/usr/bin/env python3
"""Mechanical checks for a PACES summary.

  check_summary.py <dir>/summary.md --pdf paper.pdf

Checks
  1. Shape caps per section. A "unit" is one prose sentence or one bullet.
       Problem        <=2 units, no bullets, <=250 chars
       Approach       <=4 units (lead + <=3 bullets), <=450 chars
       Claim          1 unit, no bullets, <=200 chars
       Evaluation     <=6 units (lead + 3~5 bullets), <=750 chars
       Substantiation <=3 units (verdict line + sentence + <=2 bullets), <=300 chars
     Every sentence <=140 non-space chars. A bullet holds one sentence.
     Chars are non-space; figure lines and captions are not counted.
  2. Verbatim copying: any run of 8+ consecutive Latin words also present in the paper text
  3. Numbers in the summary that do not appear anywhere in the paper text
     (matches against the whole PDF including references; a computed value can pass by coincidence,
      so label computed values as such in the body)
  4. Every referenced figure file exists
Exit 1 on any FAIL. Warnings do not fail.
"""
import argparse
import re
import sys
from pathlib import Path

CAPS = {"problem": 2, "approach": 4, "claim": 1, "evaluation": 6, "substantiation": 3}
CHAR_CAPS = {"problem": 250, "approach": 450, "claim": 200, "evaluation": 750, "substantiation": 300}
BULLETS_ALLOWED = {"problem": False, "approach": True, "claim": False, "evaluation": True, "substantiation": True}
SENTENCE_CHARS = 140
SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.M)


def sections(md: str) -> dict:
    parts = SECTION_RE.split(md)
    out = {}
    for i in range(1, len(parts), 2):
        key = parts[i].strip().lower()
        key = re.sub(r"^[pacesPACES]\s*[·.\-]\s*", "", key)  # allow "P · Problem"
        out[key] = parts[i + 1]
    return out


def strip_markup(t: str) -> str:
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", t)          # images
    t = re.sub(r"^\*.*\*\s*$", " ", t, flags=re.M)      # italic caption lines
    t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
    t = re.sub(r"\*\*Verdict:[^*]*\*\*", " ", t)
    t = re.sub(r"[*_`>#|]", " ", t)
    return t


def sentences(t: str) -> list:
    t = strip_markup(t)
    t = re.sub(r"\b(e\.g|i\.e|et al|vs|Fig|Eq|Tab|approx|cf|p)\.", lambda m: m.group(0).replace(".", "§"), t)
    t = re.sub(r"(\d)\.(\d)", r"\1§\2", t)               # decimals
    t = re.sub(r"\b([A-Z])\.", r"\1§", t)                # initials
    return [p.strip() for p in re.split(r"[.!?。]+(?:\s|$)", t) if p.strip()]


def count_sentences(t: str) -> int:
    return len(sentences(t))


def split_bullets(section: str):
    """Return (prose_text, [bullet_text, ...]). A bullet line starts with -, * or 1."""
    prose, bullets = [], []
    for line in section.splitlines():
        m = re.match(r"^\s*(?:[-*]|\d+[.)])\s+(.*)$", line)
        if m:
            bullets.append(re.sub(r"^\*\*[^*]+\*\*\s*[:：]?\s*", "", m.group(1)))  # drop bold lead label
        else:
            prose.append(line)
    return "\n".join(prose), bullets


def nsc(t: str) -> int:
    return len(re.sub(r"\s", "", strip_markup(t)))


def norm_words(t: str) -> list:
    return re.findall(r"[a-z][a-z\-]+", t.lower())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("markdown_file")
    ap.add_argument("--pdf", help="source paper; enables verbatim and number checks")
    ap.add_argument("--ngram", type=int, default=8)
    a = ap.parse_args()
    src = Path(a.markdown_file)
    md = src.read_text(encoding="utf-8")
    secs = sections(md)
    fails, warns = [], []

    # 1. caps
    for key, cap in CAPS.items():
        if key not in secs:
            fails.append(f"missing section: ## {key.title()}")
            continue
        prose, bullets = split_bullets(secs[key])
        prose_sents = sentences(prose)
        units = len(prose_sents) + len(bullets)
        chars = nsc(secs[key])
        ccap = CHAR_CAPS[key]
        problems = []
        if units > cap:
            problems.append(f"{units} units > cap {cap}")
        if chars > ccap:
            problems.append(f"{chars} non-space chars > cap {ccap}")
        if bullets and not BULLETS_ALLOWED[key]:
            problems.append("bullets not allowed here")
        for b in bullets:
            if len(sentences(b)) > 1:
                problems.append(f"bullet has {len(sentences(b))} sentences: \"{b[:40]}…\"")
        for snt in prose_sents + [x for b in bullets for x in sentences(b)]:
            if nsc(snt) > SENTENCE_CHARS:
                problems.append(f"sentence {nsc(snt)} chars > {SENTENCE_CHARS}: \"{snt[:40]}…\"")
        status = "ok" if not problems else "FAIL"
        print(f"[shape] {key:<14} {len(prose_sents)} sentence(s) + {len(bullets)} bullet(s) = {units} units (cap {cap}), "
              f"{chars} chars (cap {ccap})  {status}")
        for pr in problems:
            fails.append(f"{key}: {pr}")
    if "substantiation" in secs and not re.search(r"\*\*Verdict:\s*(Yes|Partial|No)\*\*", secs["substantiation"]):
        fails.append("substantiation: missing `**Verdict: Yes|Partial|No**` line")

    # 4. figures
    for m in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", md):
        p = src.parent / m.group(1)
        if not p.exists():
            fails.append(f"figure missing: {m.group(1)}")
    figdir = src.parent / "figures"
    if figdir.exists():
        referenced = set(re.findall(r"!\[[^\]]*\]\(([^)]+)\)", md))
        for f in figdir.iterdir():
            if f"figures/{f.name}" not in referenced:
                warns.append(f"unreferenced figure: figures/{f.name}")

    # 2 + 3. against the paper
    if a.pdf:
        try:
            import fitz
        except ImportError:
            sys.exit("PyMuPDF missing: python3 -m pip install pymupdf")
        paper = " ".join(p.get_text() for p in fitz.open(a.pdf))
        paper_norm = " ".join(norm_words(paper))
        body = strip_markup("\n".join(secs.get(k, "") for k in CAPS))
        words = norm_words(body)
        starts = [i for i in range(len(words) - a.ngram + 1)
                  if " ".join(words[i:i + a.ngram]) in paper_norm]
        runs, run = [], []
        for i in starts:  # merge overlapping windows into one copied span
            if run and i != run[-1] + 1:
                runs.append(run)
                run = []
            run.append(i)
        if run:
            runs.append(run)
        for r in runs:
            span = " ".join(words[r[0]:r[-1] + a.ngram])
            fails.append(f"verbatim ({len(r) + a.ngram - 1} words): \"{span}\"")
        nums = set(re.findall(r"(?<![\w.\-])\d+(?:\.\d+)?(?![\w.])", body))  # skips LLaVA-1.5, GPT-4
        paper_nums = set(re.findall(r"\d+(?:\.\d+)?", paper))
        for n in sorted(nums, key=lambda s: float(s)):
            if n not in paper_nums and n.rstrip("0").rstrip(".") not in paper_nums:
                warns.append(f"number not found in paper text: {n}")

    for w in warns:
        print(f"[warn] {w}")
    for f in fails:
        print(f"[FAIL] {f}")
    print("RESULT:", "FAIL" if fails else "PASS", f"({len(fails)} fail, {len(warns)} warn)")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
