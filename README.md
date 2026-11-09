# The American Bahá'í, the arts issue

TAB online: the October/November/December 2026 issue of The American Bahá'í, a U.S. Bahá'í News publication, as a one-page site. Six features with their illustrations and photographs.

- `magazine/` the curated magazine.
  - `magazine/index.html` the curated edition.
  - `magazine/members/` the full edition: the curated features plus the National Spiritual Assembly's mid-year letter and the departments.
  - `magazine/landing/` the landing page (the newsstand): current cover, In this issue with Read / Listen, earlier issues, the reader survey. `magazine/landing/alt/` is its motif-wall variant.
  - `magazine/alt/` and `magazine/members/alt/` the editions with the colour-index phone menu; `magazine/alt/plates/` and `magazine/alt/reader/` earlier presentations kept for reference.
  - `magazine/img/`, `magazine/audio/` art, photographs and story readings.
- `ideas/` treatments set aside for later use.
- `build/data.py` the six features; `build/member_data.py` the letter and departments. The next issue is a new pair of data files.
- `build/build.py` the generator. Run `python3 build.py` beside `data.py`, `member_data.py`, `usmap.json`, `favicon.svg` and an `out/img/` folder of images; it writes `out/` (artifact pages) and `site/magazine/`. Copy `site/magazine/` over `magazine/`, then run `build/newsstand.py` to rebuild the landing page.

Published with GitHub Pages from `main` via `.github/workflows/pages.yml`. Contents © 2026 National Spiritual Assembly of the Bahá'ís of the United States.
