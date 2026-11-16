"""Abstract placeholders for TAB guides and demos: colour fields and simple forms in the magazine's palette, one composition per key, stable across builds."""
import itertools, random, hashlib

LABELS = {
 "wide": "Wide shot", "xwide": "Extreme wide shot", "mid": "Mid-shot", "mcu": "Medium close-up", "cu": "Close-up", "ecu": "Extreme close-up",
 "audview": "Audience perspective", "thirds": "Grid of thirds", "vanish": "Vanishing point", "depth": "Depth and focus", "shoulder": "Over the shoulder",
 "reaction": "Audience reaction", "audwide": "Audience wide shot", "stage": "Stage shot", "light": "Dynamic lighting", "engage": "Engagement with the audience",
 "circle": "A circle seen from within", "group": "Group photo", "phone": "A phone", "quiet": "Conversation, not interrupted", "action": "Action",
 "focus1": "One face in focus", "joy": "Joy", "devotion": "Devotion", "posed": "Posed", "candid": "Candid", "hands": "Hands at work",
 "sign": "The sign at the door", "home": "A home that hosts a class", "words": "A few lines in someone's own words", "video": "A short horizontal video",
 "service": "Young people serving together", "mic": "Faces clear of the microphone"}

# grounds and inks: lapis, teal, saffron, vermilion, blush, sage, plum, sky, gilt
GROUNDS = [("#2448c8", "#1a2f86"), ("#1b5e6b", "#123f49"), ("#e9a21f", "#d07a17"), ("#c9462c", "#9c3121"), ("#f2cfc6", "#e3a99b"),
           ("#8fae8b", "#5f8a62"), ("#6b3a6e", "#45244a"), ("#8fb8de", "#5d8fc2"), ("#d9b562", "#b8903c")]
INKS = ["#2448c8", "#1b5e6b", "#e9a21f", "#c9462c", "#f2cfc6", "#8fae8b", "#6b3a6e", "#8fb8de", "#f6e7c1", "#fdfcf9"]

def _rng(key): return random.Random(int(hashlib.md5(key.encode()).hexdigest()[:8], 16))

def _shapes(r, ground):
    inks = [c for c in INKS if c not in ground]
    r.shuffle(inks)
    out = []
    kind = r.choice(["sun", "arcs", "bands", "tiles", "orbit", "hill"])
    a, b, c = inks[:3]
    if kind == "sun":
        cx, cy, rad = r.choice([48, 80, 112]), r.choice([44, 56, 70]), r.randint(26, 40)
        out += [f'<circle cx="{cx}" cy="{cy}" r="{rad + 14}" fill="{a}" opacity=".35"/>', f'<circle cx="{cx}" cy="{cy}" r="{rad}" fill="{a}"/>',
                f'<rect x="0" y="{r.randint(84, 96)}" width="160" height="40" fill="{b}" opacity=".9"/>']
    elif kind == "arcs":
        cx = r.choice([0, 160]); cy = 120
        out += [f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="none" stroke="{col}" stroke-width="13"/>' for rr, col in ((112, a), (88, b), (64, c))]
        out.append(f'<circle cx="{160 - cx if cx else 128}" cy="28" r="10" fill="{c}"/>')
    elif kind == "bands":
        ang = r.choice([-18, -10, 12, 20])
        out.append(f'<g transform="rotate({ang} 80 60)">' + "".join(f'<rect x="-40" y="{y}" width="240" height="{h}" fill="{col}" opacity="{o}"/>' for y, h, col, o in ((18, 22, a, .95), (48, 12, b, .9), (68, 30, c, .85))) + '</g>')
    elif kind == "tiles":
        cols = [a, b, c, inks[3]]
        for i in range(4):
            for j in range(3):
                if r.random() < .55:
                    out.append(f'<rect x="{14 + i * 34}" y="{12 + j * 34}" width="28" height="28" rx="{r.choice([0, 14])}" fill="{r.choice(cols)}" opacity="{r.choice([.7, .9, 1])}"/>')
    elif kind == "orbit":
        cx, cy = r.randint(60, 100), r.randint(50, 70)
        out += [f'<ellipse cx="{cx}" cy="{cy}" rx="62" ry="24" fill="none" stroke="{a}" stroke-width="2.5" transform="rotate({r.randint(-25, 25)} {cx} {cy})"/>',
                f'<circle cx="{cx}" cy="{cy}" r="22" fill="{b}"/>', f'<circle cx="{cx + r.choice([-48, 46])}" cy="{cy + r.randint(-14, 14)}" r="8" fill="{c}"/>']
    else:  # hill
        y0 = r.randint(66, 82)
        out += [f'<circle cx="{r.randint(96, 132)}" cy="{r.randint(26, 40)}" r="14" fill="{c}"/>',
                f'<path d="M0 {y0}C40 {y0 - 26} 80 {y0 - 18} 160 {y0 - 34}V120H0Z" fill="{a}"/>',
                f'<path d="M0 {y0 + 22}C50 {y0 + 4} 110 {y0 + 30} 160 {y0 + 10}V120H0Z" fill="{b}"/>']
    return "".join(out)

def _make(key):
    r = _rng(key)
    g1, g2 = r.choice(GROUNDS)
    u = key + "@@"
    defs = (f'<defs><linearGradient id="g{u}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{g1}"/><stop offset="1" stop-color="{g2}"/></linearGradient>'
            f'<clipPath id="c{u}"><rect width="160" height="120" rx="4"/></clipPath></defs>')
    return (f'<svg class="fig" viewBox="0 0 160 120" role="img" aria-label="{LABELS.get(key, key)}">{defs}<g clip-path="url(#c{u})">'
            f'<rect width="160" height="120" fill="url(#g{u})"/>{_shapes(r, (g1, g2))}</g></svg>')

_n = itertools.count(1)
class _Fig(dict):
    """Each read returns the drawing with ids made unique, so one figure can appear many times on a page."""
    def __getitem__(self, k): return dict.__getitem__(self, k).replace("@@", "-" + str(next(_n)))
FIG = _Fig()
for _k in LABELS: dict.__setitem__(FIG, _k, _make(_k))
