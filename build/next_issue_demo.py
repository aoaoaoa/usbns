# /magazine/test/next/: next issue preview studies. Theme: Education (from the editors).
# Quotation verified against the Bahá’í Reference Library: Gleanings CXXII. Threads quote this issue's own text.
import os
from about_terms_demo import shell, switch, SWITCH_CSS, SWITCH_JS, SITE, TINT
I = "../../img/"; R = "../../"
SUBMIT = "https://link.bahai.us/TAB_submit"; SUBS = "/usbns/magazine/landing/#subscribe"
Q = "Regard man as a mine rich in gems of inestimable value. Education can, alone, cause it to reveal its treasures, and enable mankind to benefit therefrom."
QS = "Bahá’u’lláh, Gleanings from the Writings of Bahá’u’lláh, CXXII"
ARR = '<span aria-hidden="true">→</span>'
DOORS = (f'<div class="dr"><a class="door" href="{SUBMIT}"><span class="dk">Online</span><b>Submit a story or photographs</b><span class="ds">Log in with your Bahá’í Online Services account (BOSA).</span><span class="go">Submit {ARR}</span></a>'
         f'<a class="door" href="mailto:TAB@usbnc.org?subject=Education%20issue"><span class="dk">By email</span><b>Write to the editors</b><span class="ds">A lead or a story idea in a few lines.</span><span class="go">TAB@usbnc.org {ARR}</span></a></div>')
SUBL = f'<p class="sub"><a href="{SUBS}">Get the next issue when it’s out {ARR}</a></p>'
ACTS = ["Children’s classes", "Junior youth groups", "Study circles", "Tutor training", "Seasonal Bahá’í schools"]

v1 = f'''<section class="n1"><p class="kk">Next issue</p><h2 class="big">Education</h2>
<blockquote><p>“{Q}”</p><cite>{QS}</cite></blockquote>
<p class="ask">Every story in this issue began as a report from a community. If learning is changing lives where you are, tell us.</p>{DOORS}{SUBL}</section>'''

TH = [("gregory", "gregory-group-hd.jpg", "Race amity", "In recent years, LGBI continues to contribute to the training and empowerment of young people centered on the principle of the oneness of humanity."),
      ("abs", "abs-stage-duo.jpg", "Scholarship", "…every person can contribute to the generation of knowledge…"),
      ("newyorkers", "ny-park.jpg", "Community", "Aware that children might ask to join, she also brought along washable children’s paints, a pad of paper and extra brushes."),
      ("endeavor", "az-ace.jpg", "Across America · San Francisco cluster", "…a group of Nepali parents whose children participate in children’s classes and the junior youth spiritual empowerment program."),
      ("comic", "comic-1.jpg", "Adventures in pioneering", "Two years ago, pioneers in the Westlake neighborhood of Indianapolis helped their young neighbors raise $1,500 towards transportation so they could attend Midwest Region camps for youth and junior youth.")]
v2 = (f'<section class="n2"><p class="kk">Next issue · Education</p><h2 class="h">Learning already runs through this issue.</h2><p class="ld">Next issue, it’s the theme.</p><ul class="th">'
      + "".join(f'<li style="--c:{TINT[s]}"><a href="{R}{s}/"><img src="{I}{im}" alt="" loading="lazy"><span><small>{k}</small>{x}</span></a></li>' for s, im, k, x in TH)
      + f'</ul><p class="ask">Have a story like these? Send it for the Education issue.</p>{DOORS}</section>')

v3 = f'''<section class="n3"><div class="nb"><p class="nbh"><span>Next issue</span><span>Education</span></p><p class="nbq">“{Q}”<br><small>{QS}</small></p>
<p class="nbl">We’re looking for stories from</p><ul>{"".join(f"<li>{a}</li>" for a in ACTS)}<li>and wherever else learning happens where you live</li></ul></div>
<div class="side"><p class="ask">Send us your notes, photographs and what you’re learning.</p>{DOORS}{SUBL}</div></section>'''

v4 = f'''<section class="n4"><div class="cv"><p class="nm"><small>The</small>American Bahá’í</p><p class="cvt">Education</p><p class="cq">“{Q}”</p><p class="cs">{QS}</p><p class="cn">Next issue</p></div>
<div class="side"><p class="kk">Coming next</p><h2 class="h">The Education issue</h2><p class="ld">The cover is still to come. The stories can come from you.</p>{DOORS}{SUBL}</div></section>'''

v5 = f'''<section class="n5"><p class="kk">Placements</p><h2 class="h">Three places the preview could live</h2>
<p class="lbl">1 · At the end of the issue, after the last story</p><div class="m1"><span class="k">Next issue</span><b>Education</b><span class="q">“Education can, alone, cause it to reveal its treasures…”</span><a href="{SUBMIT}">Send a story {ARR}</a></div>
<p class="lbl">2 · On the landing, below “In this issue”</p><div class="m2"><div><span class="k">Coming next</span><b>Education</b></div><p>Children’s classes, junior youth groups, study circles, schools. Tell us what learning looks like where you live.</p><a class="btn" href="{SUBMIT}">Submit {ARR}</a></div>
<p class="lbl">3 · In the running head, beside the date</p><div class="m3"><span class="dt">Oct/Nov/Dec 2026</span><span class="chip">Next: Education</span></div></section>'''

CSS = '''main{max-width:1040px!important}main>h1{display:none}
.kk{font:700 12px var(--ui)!important;letter-spacing:.18em;text-transform:uppercase;color:#b8782e;margin:0 0 10px!important}
.big{font:400 clamp(64px,11vw,140px)/.95 var(--text)!important;letter-spacing:-.02em!important;text-transform:none!important;color:var(--ink)!important;border:0!important;padding:0!important;margin:0 0 26px!important}
.h{font:700 clamp(28px,3.6vw,42px)/1.1 var(--text)!important;letter-spacing:-.01em!important;text-transform:none!important;color:var(--ink)!important;border:0!important;padding:0!important;margin:0 0 10px!important}
.ld{font:19px/1.5 var(--text)!important;color:var(--mute)}.ask{font:19px/1.5 var(--text)!important;margin:28px 0 16px!important;max-width:44ch}
blockquote{margin:0;max-width:34ch;border-left:4px solid #b8782e;padding-left:20px}blockquote p{font:italic 400 clamp(20px,2.4vw,26px)/1.4 var(--text)!important;margin:0 0 10px!important}cite{font:normal 13px var(--ui);color:var(--mute)}
.dr{display:grid;grid-template-columns:1fr 1fr;gap:14px;max-width:720px}.door{display:grid;gap:6px;align-content:start;text-decoration:none;color:var(--ink)!important;background:var(--card);border:1px solid var(--rule);border-top:4px solid #222e4c;padding:18px}.door+.door{border-top-color:#b8782e}.door:hover{border-color:var(--ink)}
.dk{font:700 11px var(--ui);letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}.door b{font:700 19px/1.2 var(--text)}.ds{font:14px/1.5 var(--ui);color:var(--mute)}.go{font:700 15px var(--ui);color:var(--link);margin-top:6px}
.sub{font:600 15px var(--ui)!important;margin-top:16px!important}
.th{list-style:none;margin:26px 0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}.th a{display:grid;grid-template-columns:96px 1fr;gap:14px;align-items:start;text-decoration:none;color:var(--ink);background:var(--card);border:1px solid var(--rule);border-left:5px solid var(--c);padding:12px}
.th img{width:96px;height:96px;object-fit:cover}.th small{display:block;font:700 11px var(--ui);letter-spacing:.12em;text-transform:uppercase;color:var(--mute);margin-bottom:4px}.th span{font:16px/1.45 var(--text)}
.n3,.n4{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(24px,4vw,56px);align-items:start}.n3 .dr,.n4 .dr{grid-template-columns:1fr}
.nb{background:#fffdf6;color:#1d1a16;box-shadow:0 14px 34px rgba(29,26,22,.15);padding:26px 28px 26px 70px;background-image:linear-gradient(90deg,transparent 50px,#e3a69a 50px,#e3a69a 52px,transparent 52px),repeating-linear-gradient(#fffdf6 0 31px,#cfdbe6 31px 32px);transform:rotate(-.6deg)}
.nbh{display:flex;justify-content:space-between;font:700 12px var(--ui)!important;letter-spacing:.16em;text-transform:uppercase;color:#b8782e;margin:0 0 6px!important}.nbh span:last-child{font:italic 400 34px/1 var(--text);letter-spacing:0;text-transform:none;color:#1d1a16}
.nbq{font:italic 17px/32px var(--text)!important;margin:0 0 10px!important}.nbq small{font:normal 12px var(--ui);color:#6a635a}.nbl{font:700 15px/32px var(--ui)!important;margin:0!important}.nb ul{margin:0;padding-left:1.1em;font:18px/32px var(--text)}.nb li:last-child{font-style:italic;color:#6a635a}
.cv{aspect-ratio:8.5/11;background:linear-gradient(160deg,#1b5e6b,#222e4c 70%);color:#fff;padding:9% 9%;display:flex;flex-direction:column;box-shadow:0 22px 44px rgba(29,26,22,.25);position:relative;overflow:hidden}
.cv::after{content:"";position:absolute;right:-18%;bottom:-12%;width:70%;aspect-ratio:1;border-radius:50%;border:2px dashed rgba(242,207,198,.35)}
.cv .nm{font:400 clamp(30px,4.4vw,52px)/1 var(--text)!important;margin:0!important}.cv .nm small{display:block;font:italic 400 .36em var(--text);color:#f2cfc6}
.cv .cvt{font:400 clamp(40px,5.4vw,64px)/1 var(--text)!important;color:#f2cfc6;margin:auto 0 16px!important}.cv .cq{font:italic 400 clamp(18px,2.2vw,24px)/1.35 var(--text)!important;margin:0 0 10px!important;max-width:22ch}.cv .cs{font:12px var(--ui)!important;color:rgba(255,255,255,.7);margin:0 0 22px!important}.cv .cn{font:700 12px var(--ui)!important;letter-spacing:.18em;text-transform:uppercase;border-top:1px solid rgba(255,255,255,.3);padding-top:12px;margin:0!important}
.lbl{font:700 12px var(--ui)!important;letter-spacing:.12em;text-transform:uppercase;color:var(--mute);margin:30px 0 10px!important}
.m1{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 16px;border-top:3px double var(--ink);border-bottom:1px solid var(--rule);padding:16px 0;font:17px var(--text)}.m1 .k{font:700 11px var(--ui);letter-spacing:.16em;text-transform:uppercase;color:#b8782e}.m1 b{font:700 26px var(--text)}.m1 .q{font-style:italic;color:var(--mute);flex:1 1 260px}.m1 a{font:700 15px var(--ui)}
.m2{display:grid;grid-template-columns:auto 1fr auto;gap:20px;align-items:center;background:#222e4c;color:#fff;padding:22px 24px}.m2 .k{display:block;font:700 11px var(--ui);letter-spacing:.16em;text-transform:uppercase;color:#f2cfc6}.m2 b{font:400 34px/1 var(--text)}.m2 p{font:16px/1.5 var(--ui)!important;margin:0!important;color:rgba(255,255,255,.85)}
.m2 .btn{font:700 17px "Barlow Condensed",sans-serif;letter-spacing:.04em;text-transform:uppercase;background:#f2cfc6;color:#222e4c;text-decoration:none;padding:12px 18px;border-radius:3px;white-space:nowrap}
.m3{display:flex;gap:8px;align-items:center;background:var(--card);border:1px solid var(--rule);padding:10px 14px;max-width:420px}.m3 .dt{font:600 13px var(--ui);border:1px solid var(--rule);border-radius:999px;padding:5px 12px}.m3 .chip{font:700 13px var(--ui);background:#1b5e6b;color:#fff;border-radius:999px;padding:5px 12px}
@media (max-width:760px){.dr,.n3,.n4,.m2{grid-template-columns:1fr}.cv{max-width:380px}}'''

if __name__ == "__main__":
    bar, vv = switch("Next issue preview", [("Announcement", v1), ("Threads from this issue", v2), ("Notebook call", v3), ("Cover to come", v4), ("Placements", v5)])
    h = shell("terms", "Next Issue Studies", "<h1>Next issue</h1>" + vv, SWITCH_CSS + CSS, SWITCH_JS).replace('<header class="pt">', bar + '<header class="pt">', 1)
    os.makedirs(os.path.join(SITE, "test", "next"), exist_ok=True); open(os.path.join(SITE, "test", "next", "index.html"), "w").write(h)
    print("ok")
