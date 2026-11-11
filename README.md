# Rust Book Slides

Unofficial study slides for *[The Rust Programming Language](https://doc.rust-lang.org/book/)*: every chapter and the appendix, in 23 decks and 1,556 slides. The slides keep the book's explanations, code listings and compiler output instead of summarizing them.

- Site: `docs/`, served by GitHub Pages. There is one page per chapter, and printing a page gives one slide per PDF page.
- Source: `src/chNN/`, which holds each deck's `deck.json` (slide order) and one HTML file per slide.
- Build: `python3 tools/build.py` regenerates `docs/` from `src/` and needs no dependencies.
- Layout check: `tools/layout-check.js` is a function to evaluate on a chapter page. It reports content that runs into the footer and code lines wider than their box.

## License

The source book is © The Rust Project Developers, by Steve Klabnik, Carol Nichols, and Chris Krycho, with contributions from the Rust Community. It is licensed under [MIT](LICENSE-MIT) or [Apache-2.0](LICENSE-APACHE). This adaptation is available under the same terms. [COPYRIGHT](COPYRIGHT) lists the attribution, the changes made and the third-party material.

This project is not affiliated with or endorsed by the Rust Project or the Rust Foundation.
