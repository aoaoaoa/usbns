"""Animations for the calls to action, shown in the labs gallery under Animations.
M1 and M2 are live on the site (the Send a story popup); M3 and M4 are proposals in the same manner as M1:
a passage from the Writings, set small, with an image that enacts its metaphor."""
import math
STATUS = {"live": "Live on the site", "proposed": "Proposed"}
def panel(svg, q, cite, cls=""):
    return (f'<div class="pn {cls}"><figure class="pq"><blockquote><p>{q}</p></blockquote><figcaption><b>{cite[0]}</b><span>{cite[1]}</span></figcaption></figure>{svg}</div>')

# M1 Gems revealed (live)
G = [(70,182),(170,226),(260,172),(350,236),(430,192),(510,222),(120,250),(300,206)]
m1 = panel('<svg class="art" viewBox="0 0 560 300" preserveAspectRatio="xMidYMax slice" aria-hidden="true"><path fill="#2a3150" d="M0 150C120 130 220 165 330 145S500 130 560 150V300H0z"/><path fill="#323a5e" d="M0 200C140 186 260 214 380 196S520 188 560 200V300H0z"/><path fill="#3b446b" d="M0 244C130 236 280 256 400 240S520 236 560 244V300H0z"/>'
           + "".join(f'<polygon class="gm" style="--i:{i}" points="{x},{y-9} {x+7},{y} {x},{y+9} {x-7},{y}"/>' for i,(x,y) in enumerate(G)) + '</svg>',
           "Regard man as a mine rich in gems of inestimable value. Education can, alone, cause it to reveal its treasures, and enable mankind to benefit therefrom.",
           ("Bahá’u’lláh", "Gleanings from the Writings of Bahá’u’lláh, CXXII"), "big")
# M2 Prompts (live)
m2 = ('<div class="pn light"><div class="tw"><p class="tl">What happened <small>A few paragraphs is plenty.</small></p><div class="fld"><span class="twt"></span><b class="caret"></b></div>'
      '<p class="th">The four step headings of the form, typed in turn while the field is empty. It stops the moment the reader clicks in.</p></div></div>')
# M3 Light of unity
import random
rnd = random.Random(7)
pts = []
def _inq(x, y): return ((x-150)/178)**2 + ((y-36)/86)**2 < 1  # the quotation's dark core
for gx in range(0, 560, 28):
    for gy in range(0, 300, 24):
        x, y = gx + 14 + rnd.uniform(-11, 11), gy + 12 + rnd.uniform(-9, 9)
        if _inq(x, y) or rnd.random() < .18: continue
        pts.append((round(x), round(y)))
ring = []
for k in range(64):
    t = k / 64 * 2 * math.pi
    x, y = 150 + (196 + rnd.uniform(-6, 6)) * math.cos(t), 36 + (96 + rnd.uniform(-4, 4)) * math.sin(t)
    if 4 < x < 556 and 4 < y < 296: ring.append((round(x), round(y)))
pts = [p for p in pts if min([math.hypot(p[0]-q[0], p[1]-q[1]) for q in ring] + [99]) > 14] + ring
sky = [(rnd.randint(4, 556), rnd.randint(4, 296), rnd.choice((.6, .8, 1.0))) for _ in range(170)]
ox, oy = 280, 320
def dist(p): return math.hypot(p[0]-ox, p[1]-oy)
lines = []
for i, a in enumerate(pts):
    if rnd.random() < .35: continue
    near = sorted(pts, key=lambda b: math.hypot(a[0]-b[0], a[1]-b[1]))[1:2]
    for b in near:
        if math.hypot(a[0]-b[0], a[1]-b[1]) < 40: lines.append((a, b, max(dist(a), dist(b))))
m3 = panel('<svg class="art" viewBox="0 0 560 300" preserveAspectRatio="xMinYMax slice" aria-hidden="true"><defs><radialGradient id="hl"><stop offset="0" stop-color="#fff" stop-opacity="1"/><stop offset=".28" stop-color="#fff0d9" stop-opacity=".9"/><stop offset=".6" stop-color="#f6d09a" stop-opacity=".34"/><stop offset="1" stop-color="#e2b072" stop-opacity="0"/></radialGradient><radialGradient id="qg"><stop offset="0" stop-color="#1d2236" stop-opacity=".55"/><stop offset=".5" stop-color="#1d2236" stop-opacity="0"/><stop offset=".64" stop-color="#ffe2b8" stop-opacity=".5"/><stop offset=".74" stop-color="#ffd59c" stop-opacity=".62"/><stop offset=".86" stop-color="#f3c07e" stop-opacity=".25"/><stop offset="1" stop-color="#e2b072" stop-opacity="0"/></radialGradient><radialGradient id="lu" cx="50%" cy="100%" r="60%"><stop offset="0" stop-color="#fff6ee" stop-opacity="1"/><stop offset=".5" stop-color="#f0c88f" stop-opacity=".6"/><stop offset="1" stop-color="#e2b072" stop-opacity="0"/></radialGradient></defs>'
           '<circle class="dawn" cx="280" cy="320" r="430" fill="url(#lu)"/><ellipse class="qh" cx="150" cy="36" rx="270" ry="134" fill="url(#qg)"/>' + "".join(f'<circle class="sk" style="--t:{(i%9)*.4:.1f}s" cx="{x}" cy="{y}" r="{r}"/>' for i,(x,y,r) in enumerate(sky))
           + "".join(f'<line class="lk" style="--d:{d/240:.2f}" x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}"/>' for a,b,d in lines)
           + "".join(f'<g class="sr" style="--d:{dist(p)/240 + rnd.random()*.25:.2f}"><circle cx="{p[0]}" cy="{p[1]}" r="{(1.5 + (i%4)*.55)*6.5:.1f}" fill="url(#hl)"/><circle cx="{p[0]}" cy="{p[1]}" r="{1.8 + (i%4)*.6:.2f}" fill="#fffcf8"/></g>' for i,p in enumerate(pts)) + '</svg>',
           "Thou art My lamp and My light is in thee.", ("Bahá’u’lláh", "The Hidden Words, Arabic 11"), "lu")
# M4 One tree
LEAF = ["#e2b072", "#f2cfc6", "#86c6d1", "#c9953f", "#d8c3a5", "#b8d4a8", "#e8a48f"]
lv = []
br = [("M40 300 C120 250 200 240 300 226 S470 190 540 150", 0), ("M200 241 C220 210 250 196 280 186", .5), ("M330 220 C350 250 380 262 420 266", .8), ("M420 205 C440 176 470 166 500 164", 1.0), ("M120 268 C130 240 150 226 172 220", .3)]
spots = [(170,240),(230,236),(262,192),(286,186),(300,224),(352,240),(392,262),(420,268),(440,190),(470,170),(498,162),(520,158),(130,252),(160,222),(250,206),(372,214),(456,196),(540,150),(330,214),(210,244)]
for i,(x,y) in enumerate(spots):
    lv.append(f'<ellipse class="lf" style="--i:{i};--c:{LEAF[i%len(LEAF)]}" cx="{x}" cy="{y-9}" rx="6" ry="11" transform="rotate({(i*47)%120-60} {x} {y})"/>')
m4 = panel('<svg class="art" viewBox="0 0 560 300" preserveAspectRatio="xMidYMax slice" aria-hidden="true">'
           + "".join(f'<path class="br" style="--d:{d}" d="{p}"/>' for p,d in br) + "".join(lv) + '</svg>',
           "Ye are the fruits of one tree, and the leaves of one branch.", ("Bahá’u’lláh", "Gleanings from the Writings of Bahá’u’lláh, CXXXII"))
# M5 One country
grat = "".join(f'<path class="gr" d="M0 {y} Q280 {y-26} 560 {y}"/>' for y in range(150, 300, 30)) + "".join(f'<path class="gr" d="M{x} 130 Q{x + (x-280)*.12} 220 {x + (x-280)*.2} 300"/>' for x in range(40, 560, 60))
borders = ["M60 170 L120 200 L110 250 L160 280", "M200 160 L230 210 L210 260", "M300 150 L280 200 L320 240 L300 290", "M390 170 L420 220 L400 270", "M470 160 L500 210 L480 260 L520 290"]
cities = [(90,220),(170,190),(150,262),(250,230),(330,190),(360,262),(440,200),(470,250),(520,210),(220,280)]
arcs = []
for i in range(len(cities)-1):
    a, b = cities[i], cities[i+1]; mx, my = (a[0]+b[0])/2, min(a[1], b[1]) - 34
    arcs.append(f'<path class="ac" style="--i:{i}" d="M{a[0]} {a[1]} Q{mx} {my} {b[0]} {b[1]}"/>')
m5 = panel('<svg class="art" viewBox="0 0 560 300" preserveAspectRatio="xMidYMax slice" aria-hidden="true">' + grat
           + "".join(f'<path class="bd" style="--i:{i}" d="{d}"/>' for i,d in enumerate(borders)) + "".join(arcs)
           + "".join(f'<circle class="ct" cx="{x}" cy="{y}" r="3.2"/>' for x,y in cities) + '</svg>',
           "The earth is but one country, and mankind its citizens.", ("Bahá’u’lláh", "Gleanings from the Writings of Bahá’u’lláh, CXVII"))
# M6 Perfect chord: voices arrive from both sides, meet in the middle, light blooms where they meet, and the chord opens outward inside it
WC = ["#e2b072", "#f2cfc6", "#86c6d1", "#c9953f", "#b8d4a8"]
F0 = [1.6 + i*.55 for i in range(5)]
def wave(f, a, ph, rev=False):
    xs = list(range(-10, 571, 5)); xs = xs[::-1] if rev else xs
    return " ".join(f'{x},{200 + a*math.sin(x/560*2*math.pi*f + ph):.1f}' for x in xs)
def _cy(x): return 200 + sum(24*math.sin(x/560*2*math.pi*f + i*.9) for i,f in enumerate(F0))/2.3
chord = " ".join(f'{x},{_cy(x):.1f}' for x in range(-10, 571, 4))
half_l = " ".join(f'{x},{_cy(x):.1f}' for x in range(280, -11, -4)); half_r = " ".join(f'{x},{_cy(x):.1f}' for x in range(280, 571, 4))
ws = "".join(f'<polyline class="wv6" style="--i:{i};--c:{WC[i]};--o:{(i-2)*30}px" points="{wave(F0[i], 24, i*.9, rev=(i%2==1))}"/>' for i in range(5))
m6 = panel(f'<svg class="art" viewBox="0 0 560 300" preserveAspectRatio="xMidYMax slice" aria-hidden="true"><defs><radialGradient id="bl6"><stop offset="0" stop-color="#fff6ea" stop-opacity=".8"/><stop offset=".5" stop-color="#f3c98e" stop-opacity=".28"/><stop offset="1" stop-color="#f3c98e" stop-opacity="0"/></radialGradient></defs>'
           f'{ws}<ellipse class="bl6" cx="280" cy="200" rx="300" ry="92" fill="url(#bl6)"/><polyline class="cg6" points="{chord}"/><polyline class="cd6" points="{half_l}"/><polyline class="cd6" points="{half_r}"/></svg>',
           "…the diversity in the human family should be the cause of love and harmony, as it is in music where many different notes blend together in the making of a perfect chord.",
           ("‘Abdu’l-Bahá", "Paris Talks, “Beauty and Harmony in Diversity”"), "lu ch")
m7 = ('<div class="pn lu ch" data-k="staff"><figure class="pq"><blockquote><p>…the diversity in the human family should be the cause of love and harmony, as it is in music where many different notes blend together in the making of a perfect chord.</p></blockquote>'
      '<figcaption><b>‘Abdu’l-Bahá</b><span>Paris Talks, “Beauty and Harmony in Diversity”</span></figcaption></figure>'
      '<svg class="art helix" viewBox="0 0 560 300" preserveAspectRatio="xMidYMax slice" aria-hidden="true"></svg></div>')

A = [("M1", "anim-gems", "Gems revealed", "live", "The Send a story popup, when opened from Coming next: the Education call and its quotation.",
      "Gems surface from layers of earth while the passage is read. The call’s own text becomes the image.", m1),
     ("M2", "anim-prompts", "Prompts in the empty field", "live", "The Send a story popup: the What happened field.",
      "While the field is empty, the form’s four step headings type in turn, so the blank box always suggests a first line.", m2),
     ("M3", "anim-light", "My light is in thee", "proposed", "The Send a story popup, for a call in a later issue, in the same place as M1; or the receipt after sending.",
      "A dawn rises from below and, one by one, lights a sky of stars that draw toward their neighbors: each person a lamp, each light joining the others.", m3),
     ("M4", "anim-chord", "A perfect chord", "proposed", "The end of the arts stories in this issue (New Yorkers, Two artists), or the Race Unity call.",
      "Five voices arrive from both sides and meet in the middle; light blooms where they meet, and the chord opens outward from that center.", m6),
     ("M5", "anim-small", "Smaller sizes", "proposed", "A column, a popup, a sidebar or a card: wherever the full stage is too large.",
      "M1, M3, M4 and M6 at two smaller sizes, the composition kept whole. Type scales with the panel but never below 12 px; the small size is 4:3 so the art keeps clear of the citation.", None)]
def _sm(name, html):
    return (f'<section class="smb"><h2>{name}</h2><div class="smr">'
            f'<div class="sm m"><p class="lbl">Medium · 600 px <button type="button" class="rp">Replay</button></p>{html}</div>'
            f'<div class="sm s"><p class="lbl">Small · 380 px, 4:3 <button type="button" class="rp">Replay</button></p>{html}</div></div></section>')
A.append(("M6", "anim-strand", "From staff to strand", "proposed", "The end of the arts stories in this issue (New Yorkers, Two artists), or the Race Unity call: an alternative to M4.",
          "Five staff lines enter flat at the left and twist, as they cross, into a double helix; the notes on the staff become its rungs. Many notes, one chord; many people, one human family.", m7))
A[4] = A[4][:6] + ("".join(_sm(nm, h) for nm, h in (("Gems revealed", m1), ("My light is in thee", m3), ("A perfect chord", m6), ("From staff to strand", m7))),)

CSS = r"""
.an-w{max-width:980px;margin:0 auto;padding:clamp(28px,5vw,56px) 16px 72px}
.an-h .kk{margin-bottom:12px}.an-h h1{font:700 clamp(30px,4.4vw,46px)/1.08 var(--text);margin:0 0 10px}
.st{display:inline-block;font:700 11px var(--ui);letter-spacing:.14em;text-transform:uppercase;border-radius:999px;padding:4px 10px;margin:0 0 14px;border:1px solid var(--rule);color:var(--mute)}.st.live{background:var(--teal);color:var(--card);border-color:var(--teal)}
.pn{position:relative;overflow:hidden;background:#1d2236;border-radius:10px;aspect-ratio:16/9;min-height:300px;margin:18px 0 22px;color:#fbf7ef}
.pn .art{position:absolute;inset:0;width:100%;height:100%}
.pq{position:relative;z-index:1;margin:0;padding:24px 28px 0 56px;max-width:640px}.pq::before{content:"“";position:absolute;left:24px;top:14px;font:400 44px/1 var(--text);color:#e2b072}
.pq blockquote{margin:0}.pq p{margin:0;font:italic 400 14px/1.6 var(--text);color:#fbf7ef;text-wrap:pretty}
.pq figcaption{display:grid;gap:1px;margin-top:18px;padding-top:12px;position:relative;font:12px/1.4 var(--ui);color:#ddd3c4}.pq figcaption::before{content:"";position:absolute;top:0;left:0;width:28px;height:1px;background:#e2b072}
.pq figcaption b{font:700 11px/1.4 var(--ui);letter-spacing:.14em;text-transform:uppercase;color:#fbf7ef}.pq figcaption span{font-style:italic}
.ab{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:28px}.ab h2{font:600 12px var(--ui);letter-spacing:.14em;text-transform:uppercase;color:var(--mute);margin:0 0 6px}.ab p{margin:0;font:17px/1.55 var(--text)}
.rpl{margin-top:22px;font:600 13px var(--ui);background:none;border:1px solid var(--rule);color:var(--ink);border-radius:999px;padding:6px 16px;cursor:pointer}
@media(max-width:700px){.ab{grid-template-columns:1fr;gap:16px}.pn{aspect-ratio:auto;min-height:360px}.pq{padding:20px 20px 0 46px}.pq::before{left:16px}}
/* M1 */.gm{fill:#e2b072;transform-box:fill-box;transform-origin:center;opacity:0;animation:gmin 2.2s ease calc(.4s + var(--i) * .38s) forwards}
@keyframes gmin{0%{opacity:0;transform:scale(.3)}40%{opacity:1;transform:scale(1.25)}60%{filter:brightness(1.7)}100%{opacity:1;transform:scale(1)}}
/* M2 */.pn.light{background:var(--card);border:1px solid var(--rule);color:var(--ink);display:grid;place-items:center}.tw{width:min(86%,560px);display:grid;gap:10px}
.tl{margin:0;font:700 11px var(--ui);letter-spacing:.16em;text-transform:uppercase;color:var(--mute)}.tl small{font:500 12px var(--ui);letter-spacing:0;text-transform:none;margin-left:8px}
.fld{min-height:120px;background:repeating-linear-gradient(transparent 0 31px,var(--rule) 31px 32px);font:16px/32px var(--ui);color:var(--mute);padding:0 2px}
.caret{display:inline-block;width:2px;height:1.1em;background:var(--teal);vertical-align:-3px;margin-left:1px;animation:cr 1s steps(1) infinite}@keyframes cr{50%{opacity:0}}.th{margin:6px 0 0;font:14px/1.5 var(--ui);color:var(--mute)}
/* M3 */.dawn{transform-origin:280px 320px;transform:scale(.05);opacity:.4;will-change:transform,opacity;animation:dawn 10s cubic-bezier(.33,0,.2,1) .3s forwards}@keyframes dawn{to{transform:scale(1);opacity:1}}
.sk{fill:#fbf8ff;opacity:.7;animation:tw 4.8s ease-in-out var(--t) infinite}@keyframes tw{50%{opacity:1}}.qh{opacity:0;transform-box:fill-box;transform-origin:center;transform:scale(.7);will-change:transform,opacity;animation:qh 5s cubic-bezier(.33,0,.2,1) 4.2s forwards}@keyframes qh{to{opacity:1;transform:scale(1)}}.sr{opacity:0;will-change:opacity;animation:srl 2.2s cubic-bezier(.4,0,.2,1) calc(.6s + var(--d) * 3.8s) forwards}@keyframes srl{to{opacity:1}}
.lk{stroke:#ffe6c4;stroke-width:.6;opacity:0;animation:lk 2.4s cubic-bezier(.4,0,.2,1) calc(1.8s + var(--d) * 3.8s) forwards}@keyframes lk{to{opacity:.22}}
/* M6 */.wv6{fill:none;stroke:var(--c);stroke-width:6;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:900;stroke-dashoffset:900;transform:translateY(var(--o));will-change:transform,opacity;animation:in6 1.6s ease calc(.4s + var(--i) * .25s) forwards,j6 2.6s cubic-bezier(.45,0,.2,1) calc(2.2s + var(--i) * .1s) forwards}@keyframes in6{to{stroke-dashoffset:0}}@keyframes j6{to{transform:none;opacity:.34}}
.bl6{transform-box:fill-box;transform-origin:center;opacity:0;transform:scale(.1);will-change:transform,opacity;animation:bl6 2.8s cubic-bezier(.2,.7,.2,1) 4.3s forwards}@keyframes bl6{40%{opacity:1}to{opacity:.55;transform:scale(1)}}
.cg6{fill:none;stroke:#fff1dc;stroke-width:32;stroke-linecap:round;stroke-linejoin:round;opacity:0;animation:cg6 2.2s ease 4.6s forwards}@keyframes cg6{to{opacity:.26}}
.cd6{fill:none;stroke:#fffdf9;stroke-width:8.5;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:800;stroke-dashoffset:800;animation:grow 2.1s cubic-bezier(.4,0,.2,1) 4.5s forwards}@keyframes grow{to{stroke-dashoffset:0}}
.nt{fill:var(--c);transform:translateY(var(--o));will-change:transform,opacity;animation:join 3.4s cubic-bezier(.45,0,.2,1) calc(.8s + var(--i) * .15s) forwards}.sf{stroke:#fbf7ef;stroke-width:.6;opacity:.08}
.cdg{fill:none;stroke:#f3c98e;stroke-width:16;stroke-linecap:round;stroke-linejoin:round;opacity:0;animation:cg 2.4s ease 4s forwards}@keyframes cg{to{opacity:.16}}
.cd{fill:none;stroke:#fffaf5;stroke-width:4.4;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1400;stroke-dashoffset:1400;animation:grow 2.4s cubic-bezier(.4,0,.2,1) 3.9s forwards}
.pn.ch{background:radial-gradient(ellipse at 50% 80%,#4b4f8a 0%,#2c3466 45%,#1d2236 90%)}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;animation-delay:0s!important;animation-iteration-count:1!important}}
"""
JS = r"""
[].forEach.call(document.querySelectorAll('.rp'),function(b){b.onclick=function(){var p=b.closest('.sm').querySelector('.pn'),h=p.innerHTML;p.innerHTML='';void p.offsetWidth;p.innerHTML=h}});
(function(){var t=document.querySelector('.twt');if(!t)return;var P=['What happened, and where…','Who was there…','A photograph or two…','What you learned…'],pi=0,ci=0,del=0,rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
function run(){var p=P[pi];if(rm){t.textContent=p;pi=(pi+1)%4;return setTimeout(run,3000)}if(!del){ci++;t.textContent=p.slice(0,ci);if(ci>=p.length){del=1;return setTimeout(run,1900)}return setTimeout(run,48)}ci--;t.textContent=p.slice(0,ci);if(ci<=0){del=0;pi=(pi+1)%4;return setTimeout(run,380)}setTimeout(run,16)}run()})();
var rp=document.querySelector('.rpl');if(rp)rp.onclick=function(){var p=document.querySelector('.pn');if(p.classList.contains('light'))return;var h=p.innerHTML;p.innerHTML='';void p.offsetWidth;p.innerHTML=h};
"""
def body(x):
    code, slug, name, st, where, why, html = x
    return (f'<main class="an-w"><header class="an-h"><p class="kk">Animation · {code}</p><h1>{name}</h1></header><span class="st {st}">{STATUS[st]}</span>{html}'
            f'<div class="ab"><div><h2>Where it goes</h2><p>{where}</p></div><div><h2>What it does</h2><p>{why}</p></div></div>'
            + ('' if slug in ("anim-prompts", "anim-small") else '<button type="button" class="rpl">Replay</button>') + '</main>')

CSS += ".pn.lu{background:radial-gradient(ellipse at 50% 112%,#8a9be0 0%,#5263a8 34%,#33407a 66%,#252d5a 100%)}.pn.lu .pq{max-width:720px}.pn.lu .pq p{font-size:clamp(18px,2.2vw,22px);line-height:1.45}.pn.lu .pq::before{font-size:56px;top:12px}"

CSS += ".pn.lu .pq p{text-shadow:0 1px 12px rgba(29,34,54,.85)}"

CSS += ".pn.big .pq{max-width:720px}.pn.big .pq p{font-size:clamp(18px,2.2vw,22px);line-height:1.45;text-shadow:0 1px 12px rgba(29,34,54,.85)}.pn.big .pq::before{font-size:56px;top:12px}"

CSS += (".smb{border-top:1px solid var(--rule);padding:24px 0 6px}.smb:first-of-type{border-top:0}.smb h2{font:700 20px/1.2 var(--text);margin:0 0 14px}"
 ".smr{display:flex;flex-wrap:wrap;gap:24px;align-items:flex-start}.sm.m{width:min(100%,560px)}.sm.s{width:min(100%,360px)}"
 ".lbl{font:700 11px var(--ui);letter-spacing:.14em;text-transform:uppercase;color:var(--mute);margin:0 0 8px;display:flex;justify-content:space-between;align-items:center}"
 ".lbl button{font:600 12px var(--ui);background:none;border:1px solid var(--rule);color:var(--ink);border-radius:999px;padding:4px 12px;cursor:pointer;letter-spacing:0;text-transform:none}"
 ".sm .pn{aspect-ratio:16/9!important;min-height:0!important;margin:0!important;border-radius:8px;container-type:inline-size}.sm.s .pn{aspect-ratio:4/3!important}"
 ".sm .pq{padding:3.4cqw 4cqw 0 7.6cqw!important;max-width:74cqw!important}.sm .pq::before{left:3.2cqw!important;top:2cqw!important;font-size:max(26px,6.4cqw)!important}"
 ".sm .pq p{font-size:max(12px,2.15cqw)!important;line-height:1.45!important}.sm .pq figcaption{margin-top:max(8px,1.8cqw)!important;padding-top:max(6px,1.2cqw)!important;font-size:max(10px,1.5cqw)!important}.sm .pq figcaption b{font-size:max(9.5px,1.4cqw)!important}"
 "@media (max-width:420px){.sm .pn{aspect-ratio:4/3!important}}")

JS += "(function(){var NS='http://www.w3.org/2000/svg',RM=matchMedia('(prefers-reduced-motion: reduce)').matches,TAU=Math.PI*2;\nvar VC=['#e2b072','#f2cfc6','#86c6d1','#c9953f','#b8d4a8'];\nfunction mk(p,t,a){var e=document.createElementNS(NS,t);for(var k in a)e.setAttribute(k,a[k]);p.appendChild(e);return e}\nfunction clamp(v){return v<0?0:v>1?1:v}function ease(v){v=clamp(v);return v*v*(3-2*v)}\nfunction defs(svg){var d=mk(svg,'defs',{});var g=mk(d,'radialGradient',{id:svg.id+'b'});mk(g,'stop',{offset:'0','stop-color':'#fff6ea','stop-opacity':'.75'});mk(g,'stop',{offset:'.5','stop-color':'#f3c98e','stop-opacity':'.22'});mk(g,'stop',{offset:'1','stop-color':'#f3c98e','stop-opacity':'0'});\n var f=mk(d,'filter',{id:svg.id+'g',x:'-20%',y:'-50%',width:'140%',height:'200%'});mk(f,'feGaussianBlur',{stdDeviation:'3'});return d}\n// strand made of short segments, so each piece can carry its own depth\nfunction hx(c){return [parseInt(c.slice(1,3),16),parseInt(c.slice(3,5),16),parseInt(c.slice(5,7),16)]}var BG=hx('#2c3466');\nfunction strand(g,n,col){var s=[],c=hx(col);for(var i=0;i<n;i++){var e=mk(g,'line',{stroke:col,'stroke-linecap':'round'});e._c=c;s.push(e)}return s}\nfunction op(e,a){if(e._c){a=a<0?0:a>1?1:a;e.setAttribute('opacity',a>0.02?1:0);var c=e._c;e.setAttribute('stroke','rgb('+Math.round(BG[0]+(c[0]-BG[0])*a)+','+Math.round(BG[1]+(c[1]-BG[1])*a)+','+Math.round(BG[2]+(c[2]-BG[2])*a)+')')}else e.setAttribute('opacity',a)}\nvar B={};B.staff=function(svg){defs(svg);var cy=214,G=9,N=120,x0=-10,x1=570,dx=(x1-x0)/N,k=TAU/220;\n mk(svg,'ellipse',{cx:420,cy:cy,rx:220,ry:80,fill:'url(#'+svg.id+'b)',opacity:.45});\n var gr=mk(svg,'g',{}),R=[];for(var j=0;j<16;j++){var g=mk(gr,'g',{});R.push({l:mk(g,'line',{'stroke-width':2,'stroke-linecap':'round'}),h:mk(g,'ellipse',{rx:6,ry:4.4})})}\n var L=[0,1,2,3,4].map(function(v){return strand(mk(svg,'g',{}),N,v==2?'#fffaf5':VC[v])});\n function env(x,t){return ease((x-120)/300)*ease(t/3)}\n return function(t){var ph=t*.5,dr=ease(t/1.6);\n  L.forEach(function(s,v){var base=(v-2)*G;for(var i=0;i<N;i++){var xa=x0+i*dx,xb=xa+dx,on=(i/N)<dr?1:0,sg=v<2?1:v>2?-1:0;\n   function Y(x){var e=env(x,t),a=k*x+ph;return cy+base*(1-e)+e*(sg?sg*40*Math.sin(a):0)+(v==2?0:0)}\n   var z=sg?Math.cos(k*(xa+dx/2)+ph)*sg*env(xa,t):0;var w=v==2?3.6:2;\n   s[i].setAttribute('x1',xa);s[i].setAttribute('x2',xb);s[i].setAttribute('y1',Y(xa));s[i].setAttribute('y2',Y(xb));s[i].setAttribute('stroke-width',w+z*1.6);op(s[i],on*(v==2?.95:.55+.4*(z+1)/2))}});\n  for(var j=0;j<R.length;j++){var x=60+j*32,e=env(x,t),a=k*x+ph,ys=cy+((j%5)-2)*G,ya=cy+40*Math.sin(a),yb=cy-40*Math.sin(a),c=VC[j%5],vis=ease((t-.6-j*.1)/.6);\n   R[j].h.setAttribute('cx',x);R[j].h.setAttribute('cy',ys*(1-e)+cy*e);R[j].h.setAttribute('fill',c);R[j].h.setAttribute('transform','rotate(-20 '+x+' '+(ys*(1-e)+cy*e)+')');R[j].h.setAttribute('opacity',vis*(1-.75*e));\n   R[j].l.setAttribute('x1',x);R[j].l.setAttribute('x2',x);R[j].l.setAttribute('y1',ya*e+ys*(1-e));R[j].l.setAttribute('y2',yb*e+ys*(1-e));R[j].l.setAttribute('stroke',c);R[j].l.setAttribute('opacity',vis*e*.8)}}};var seen=0;function loop(n){[].forEach.call(document.querySelectorAll('.pn[data-k=staff]'),function(pn){var svg=pn.querySelector('svg.helix');if(!svg)return;if(!svg._f){while(svg.firstChild)svg.removeChild(svg.firstChild);svg.id='sx'+(++seen);svg._f=B.staff(svg);svg._t=n;svg._on=true;new IntersectionObserver(function(e){svg._on=e[0].isIntersecting}).observe(pn);if(RM)svg._f(8)}if(!RM&&svg._on)svg._f((n-svg._t)/1000)});requestAnimationFrame(loop)}requestAnimationFrame(loop)})();"
