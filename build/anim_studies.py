"""Animations for the calls to action, shown in the story-ctas gallery under Animations.
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
           ("Bahá’u’lláh", "Gleanings from the Writings of Bahá’u’lláh, CXXII"))
# M2 Prompts (live)
m2 = ('<div class="pn light"><div class="tw"><p class="tl">What happened <small>A few paragraphs is plenty.</small></p><div class="fld"><span class="twt"></span><b class="caret"></b></div>'
      '<p class="th">The four step headings of the form, typed in turn while the field is empty. It stops the moment the reader clicks in.</p></div></div>')
# M3 Light of unity
import random
rnd = random.Random(7)
pts = [(rnd.randint(14, 546), rnd.randint(118, 292)) for _ in range(150)]
pts += [(rnd.randint(440, 548), rnd.randint(14, 120)) for _ in range(30)] + [(rnd.randint(330, 548), rnd.randint(84, 128)) for _ in range(18)]
sky = [(rnd.randint(4, 556), rnd.randint(4, 296), rnd.choice((.6, .8, 1.0))) for _ in range(170)]
ox, oy = 280, 320
def dist(p): return math.hypot(p[0]-ox, p[1]-oy)
lines = []
for i, a in enumerate(pts):
    near = sorted(pts, key=lambda b: math.hypot(a[0]-b[0], a[1]-b[1]))[1:2]
    for b in near:
        if math.hypot(a[0]-b[0], a[1]-b[1]) < 48: lines.append((a, b, max(dist(a), dist(b))))
m3 = panel('<svg class="art" viewBox="0 0 560 300" preserveAspectRatio="xMidYMax slice" aria-hidden="true"><defs><radialGradient id="lu" cx="50%" cy="100%" r="60%"><stop offset="0" stop-color="#fff1e8" stop-opacity="1"/><stop offset=".5" stop-color="#e9bf86" stop-opacity=".5"/><stop offset="1" stop-color="#e2b072" stop-opacity="0"/></radialGradient></defs>'
           '<circle class="dawn" cx="280" cy="320" r="430" fill="url(#lu)"/>' + "".join(f'<circle class="sk" style="--t:{(i%9)*.4:.1f}s" cx="{x}" cy="{y}" r="{r}"/>' for i,(x,y,r) in enumerate(sky))
           + "".join(f'<line class="lk" style="--d:{d/240:.2f}" x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}"/>' for a,b,d in lines)
           + "".join(f'<circle class="pt" style="--d:{dist(p)/240:.2f}" cx="{p[0]}" cy="{p[1]}" r="{1.4 + (i%4)*.6:.2f}"/>' for i,p in enumerate(pts)) + '</svg>',
           "So powerful is the light of unity that it can illuminate the whole earth.", ("Bahá’u’lláh", "Gleanings from the Writings of Bahá’u’lláh, CXXXII"), "lu")
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
# M6 Perfect chord
def wave(f, a, ph, y0=0):
    pts = " ".join(f'{x},{220 + y0 + a*math.sin(x/560*2*math.pi*f + ph):.1f}' for x in range(0, 561, 8))
    return pts
WC = ["#e2b072", "#f2cfc6", "#86c6d1", "#c9953f", "#b8d4a8"]
ws = "".join(f'<polyline class="wv" style="--i:{i};--c:{WC[i]};--o:{(i-2)*24}px" points="{wave(2+i*.5, 14, i*.9)}"/>' for i in range(5))
chord = " ".join(f'{x},{220 + sum(14*math.sin(x/560*2*math.pi*(2+i*.5) + i*.9) for i in range(5))/2.6:.1f}' for x in range(0, 561, 6))
m6 = panel(f'<svg class="art" viewBox="0 0 560 300" preserveAspectRatio="xMidYMax slice" aria-hidden="true">{ws}<polyline class="cd" points="{chord}"/></svg>',
           "…the diversity in the human family should be the cause of love and harmony, as it is in music where many different notes blend together in the making of a perfect chord.",
           ("‘Abdu’l-Bahá", "Paris Talks, “Beauty and Harmony in Diversity”"))

A = [("M1", "anim-gems", "Gems revealed", "live", "The Send a story popup, when opened from Coming next: the Education call and its quotation.",
      "Gems surface from layers of earth while the passage is read. The call’s own text becomes the image.", m1),
     ("M2", "anim-prompts", "The prompts write themselves", "live", "The Send a story popup: the What happened field.",
      "While the field is empty, the form’s four step headings type in turn, so the blank box always suggests a first line.", m2),
     ("M3", "anim-light", "The light of unity", "proposed", "The Race Unity call (Summer 2027), in the same place as M1.",
      "A dawn rises from below; scattered points brighten as the light reaches them, then draw toward their neighbors.", m3),
     ("M4", "anim-chord", "A perfect chord", "proposed", "The end of the arts stories in this issue (New Yorkers, Two artists), or the Race Unity call.",
      "Five waves in five colors move toward one another and resolve into a single chord.", m6)]

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
/* M3 */.dawn{transform-origin:280px 320px;transform:scale(.05);animation:dawn 9s cubic-bezier(.25,.5,.3,1) .4s forwards}@keyframes dawn{to{transform:scale(1)}}
.sk{fill:#f4f0fb;opacity:.6;animation:tw 3.6s ease-in-out var(--t) infinite}@keyframes tw{50%{opacity:1}}.pt{fill:#6b75a0;animation:ptl 1.1s ease calc(.6s + var(--d) * 3.6s) forwards}@keyframes ptl{to{fill:#fffaf5;filter:drop-shadow(0 0 3px #fff) drop-shadow(0 0 10px #f3c98e) drop-shadow(0 0 18px #e2b072)}}
.lk{stroke:#f3c98e;stroke-width:.8;opacity:0;animation:lk 1.4s ease calc(1.6s + var(--d) * 3.6s) forwards}@keyframes lk{to{opacity:.85}}
/* M4 */.br{fill:none;stroke:#8a7356;stroke-width:3;stroke-linecap:round;stroke-dasharray:600;stroke-dashoffset:600;animation:grow 2.2s ease calc(.3s + var(--d) * 1s) forwards}.br:first-child{stroke-width:5}@keyframes grow{to{stroke-dashoffset:0}}
.lf{fill:var(--c);opacity:0;transform-box:fill-box;transform-origin:50% 100%;animation:leaf .7s cubic-bezier(.2,.9,.3,1.3) calc(1.4s + var(--i) * .16s) forwards}@keyframes leaf{from{opacity:0;transform:scale(0)}to{opacity:.92;transform:scale(1)}}
/* M5 */.gr{fill:none;stroke:#3b446b;stroke-width:1}.bd{fill:none;stroke:#86c6d1;stroke-width:1.2;stroke-dasharray:5 4;opacity:.8;animation:bd 1.6s ease calc(.6s + var(--i) * .25s) forwards}@keyframes bd{to{opacity:0}}
.ac{fill:none;stroke:#e2b072;stroke-width:1.4;stroke-dasharray:200;stroke-dashoffset:200;animation:grow 1s ease calc(2.2s + var(--i) * .3s) forwards}.ct{fill:#f2cfc6}
/* M6 */.wv{fill:none;stroke:var(--c);stroke-width:1.6;opacity:.9;transform:translateY(var(--o));animation:join 2.6s cubic-bezier(.5,0,.3,1) calc(.6s + var(--i) * .12s) forwards}@keyframes join{70%{opacity:.9}to{transform:none;opacity:.12}}
.cd{fill:none;stroke:#fbf7ef;stroke-width:2.4;stroke-dasharray:1200;stroke-dashoffset:1200;animation:grow 1.8s ease 3s forwards}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;animation-delay:0s!important;animation-iteration-count:1!important}}
"""
JS = r"""
(function(){var t=document.querySelector('.twt');if(!t)return;var P=['What happened, and where…','Who was there…','A photograph or two…','What you learned…'],pi=0,ci=0,del=0,rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
function run(){var p=P[pi];if(rm){t.textContent=p;pi=(pi+1)%4;return setTimeout(run,3000)}if(!del){ci++;t.textContent=p.slice(0,ci);if(ci>=p.length){del=1;return setTimeout(run,1900)}return setTimeout(run,48)}ci--;t.textContent=p.slice(0,ci);if(ci<=0){del=0;pi=(pi+1)%4;return setTimeout(run,380)}setTimeout(run,16)}run()})();
var rp=document.querySelector('.rpl');if(rp)rp.onclick=function(){var p=document.querySelector('.pn');if(p.classList.contains('light'))return;var h=p.innerHTML;p.innerHTML='';void p.offsetWidth;p.innerHTML=h};
"""
def body(x):
    code, slug, name, st, where, why, html = x
    return (f'<main class="an-w"><header class="an-h"><p class="kk">Animation · {code}</p><h1>{name}</h1></header><span class="st {st}">{STATUS[st]}</span>{html}'
            f'<div class="ab"><div><h2>Where it goes</h2><p>{where}</p></div><div><h2>What it does</h2><p>{why}</p></div></div>'
            + ('' if st == "live" and slug == "anim-prompts" else '<button type="button" class="rpl">Replay</button>') + '</main>')

CSS += ".pn.lu{background:radial-gradient(ellipse at 50% 120%,#4a5a92 0%,#2a3460 45%,#1d2236 85%)}.pn.lu .pq{max-width:720px}.pn.lu .pq p{font-size:clamp(18px,2.2vw,22px);line-height:1.45}.pn.lu .pq::before{font-size:56px;top:12px}.lk{stroke-width:1}"
