#!/usr/bin/env python3
"""Build the static site: src/chNN/{deck.json,slides/*.html} -> docs/chNN.html + docs/index.html.

Usage: python3 tools/build.py
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC, OUT = ROOT / "src", ROOT / "docs"

FONTS = ("https://fonts.googleapis.com/css2?family=Libertinus+Serif:wght@400;600"
         "&family=Source+Sans+3:wght@400;600&family=IBM+Plex+Mono:wght@400;600&display=swap")
REPO = "https://github.com/wipiano/rustbook-slides"
NOTICE = (
    'Unofficial slides adapted from <a href="https://doc.rust-lang.org/book/"><i>The Rust Programming Language</i></a> '
    "by Steve Klabnik, Carol Nichols, and Chris Krycho, with contributions from the Rust Community "
    "(edition for Rust 1.97.0). Original text and code © The Rust Project Developers, licensed under "
    '<a href="https://github.com/rust-lang/book/blob/main/LICENSE-MIT">MIT</a> or '
    '<a href="https://github.com/rust-lang/book/blob/main/LICENSE-APACHE">Apache-2.0</a>; '
    f'this adaptation is available under the same terms (<a href="{REPO}/blob/main/COPYRIGHT">details</a>). '
    "Not affiliated with or endorsed by the Rust Project or the Rust Foundation. "
    "“Rust” is a trademark of the Rust Foundation."
)


def page(title, body, extra_head=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="{html.escape(FONTS)}">
<link rel="stylesheet" href="assets/site.css">
{extra_head}</head>
<body>
{body}
<footer class="notice"><p>{NOTICE}</p></footer>
</body>
</html>
"""


def main():
    decks = []
    for d in sorted(SRC.glob("ch[0-9][0-9]")):
        idx = json.loads((d / "deck.json").read_text())
        # Deck titles are "Rust Book Ch.N — Title"; the site shows the part after the dash.
        label, _, name = idx["title"].partition(" — ")
        slides = []
        for sid in idx["order"]:
            s = (d / "slides" / f"{sid}.html").read_text()
            slides.append(re.sub(r"<aside>[\s\S]*?</aside>", "", s).strip())
        decks.append({"file": f"{d.name}.html", "label": label.replace("Rust Book ", ""), "name": name, "slides": slides})

    for i, dk in enumerate(decks):
        prev = f'<a href="{decks[i-1]["file"]}">← {html.escape(decks[i-1]["label"])}</a>' if i else "<span></span>"
        nxt = f'<a href="{decks[i+1]["file"]}">{html.escape(decks[i+1]["label"])} →</a>' if i + 1 < len(decks) else "<span></span>"
        frames = "\n".join(f'<div class="frame" id="slide-{n}">\n{s}\n</div>' for n, s in enumerate(dk["slides"], 1))
        body = (f'<header class="bar"><a href="index.html">Contents</a><h1>{html.escape(dk["label"])} — {html.escape(dk["name"])}</h1>'
                f'<nav>{prev}{nxt}</nav></header>\n<main class="deck">\n{frames}\n</main>')
        (OUT / dk["file"]).write_text(page(f'{dk["label"]} — {dk["name"]} · Rust Book Slides', body,
                                           '<script src="assets/slides.js" defer></script>\n'))

    rows = "\n".join(f'<li><a href="{dk["file"]}"><span>{html.escape(dk["label"])}</span> {html.escape(dk["name"])}</a>'
                     f'<small>{len(dk["slides"])} slides</small></li>' for dk in decks)
    total = sum(len(dk["slides"]) for dk in decks)
    body = f"""<main class="toc">
<h1>The Rust Programming Language — Slides</h1>
<p>A slide-by-slide study companion covering every chapter of the book without summarizing it away:
the explanations, every listing and the compiler output it discusses. {len(decks)} decks, {total} slides.
Each page scrolls through one chapter; print a page to get one slide per PDF page.</p>
<ol>
{rows}
</ol>
<p><a href="{REPO}">Source on GitHub</a></p>
</main>"""
    (OUT / "index.html").write_text(page("The Rust Programming Language — Slides", body))
    print(f"built {len(decks)} decks, {total} slides -> {OUT}")


if __name__ == "__main__":
    main()
