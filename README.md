# The American Bahá'í, the arts issue

TAB online: the October/November/December 2026 issue of The American Bahá'í, a U.S. Bahá'í News publication, as a one-page site. Six features with their illustrations and photographs.

- `index.html` the curated edition: six features.
- `member/` the full edition: the same six features plus the National Spiritual Assembly's mid-year letter and the departments (Ḥuqúqu'lláh, Abiding in God's Law, the Fund, Rhythm of Bahá'í Life, the Bookstore, notices).
- `alt/` the curated edition with the colour-index phone menu; `member/alt/` the same for the full edition. Both are written by the same build as the main pages, so they stay in step.
- `alt/plates/`, `alt/reader/` two earlier presentations, kept for reference.
- `ideas/` treatments set aside for later use.
- `audio/` story readings, as they are added.
- `img/` art and photographs.
- `build/data.py` the six features; `build/member_data.py` the letter and departments. The next issue is a new pair of data files.
- `build/build.py` the generator. Run `python3 build.py` beside `data.py`, `member_data.py`, `usmap.json`, `favicon.svg` and an `out/img/` folder of images; it writes `out/` (artifact pages) and `site/` (this tree). Copy `site/` over the repository root to publish.

Published with GitHub Pages from `main` via `.github/workflows/pages.yml`. Contents © 2026 National Spiritual Assembly of the Bahá'ís of the United States.
