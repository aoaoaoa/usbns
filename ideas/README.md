# Ideas bank

Treatments set aside for possible later use.

- **badi-ring/** The Badí‘ calendar drawn as a ring of 19 months in a year-long colour gradient, with each month's Feast and Holy Days in its popup. Briefly replaced by a flat year ribbon, then restored in the Two artists story (November 2026). The ribbon renderer (kind="ribbon", with Ayyám-i-Há as four gold dots) stays in build.py for later use. `badi-ring.png` is the rendered figure, `badi-ring.svg` its markup (styles not included), `ring_renderer.py` the generator branch. The renderer is still used for the full edition's "The year 183 B.E." chart.
- **life-in-years/** Louis Gregory's life as a grid of years: one filled square for each year he lived, outlined squares for each year since, events colored by kind (life, teaching journeys, service and institutions, writings, legacy) with popups. Shown briefly as No. 2 under the Gregory timeline (November 2026), alongside a two-column ledger of the same entries. `life-in-years.png` is the rendered figure; `renderer.py` holds both generator branches and their CSS. The data (GREGORY_EVENTS, GREGORY_KINDS) stays in data.py.
