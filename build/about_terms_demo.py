# Demos: /magazine/test/about/ (about page proposals) and /magazine/test/terms/ (terms cleanup).
# Built inside the policy-page shell so header, footer and fonts match. Every fact is from the print issue or the edition data.
import os, re, json, html
import data
D = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(D, "site", "magazine")
I = "../../img/"
R = "../../"
ISSUE = data.ISSUE
A = {a["slug"]: a for a in data.ARTICLES}
TINT = {"gregory": "#e8532a", "newyorkers": "#f05a7e", "twoartists": "#b07a4a", "abs": "#c9462c", "endeavor": "#1b5e6b", "comic": "#5b4a8a"}
NSA = "National Spiritual Assembly of the Bahá’ís of the United States"
PLACES = len(json.load(open(os.path.join(D, "usmap.json")))["places"])
def t(s): return s.replace("'", "’")
def shell(src_slug, title, body, css, js=""):
    h = open(os.path.join(SITE, src_slug, "index.html")).read()
    h = re.sub(r"<main>.*</main>", lambda m: "<main>" + body + "</main>", h, count=1, flags=re.S)
    h = h.replace('href="../favicon.svg"', 'href="../../favicon.svg"').replace("<head>", '<head>\n<meta name="robots" content="noindex">', 1)
    h = re.sub(r"<title>[^<]*</title>", f"<title>{title}</title>", h, count=1)
    return h.replace("</style>", css + "</style>", 1).replace("</body>", (f"<script>{js}</script>" if js else "") + "</body>", 1)

SWITCH_CSS = (".bar0{position:sticky;top:0;z-index:5;display:flex;gap:6px;align-items:center;overflow-x:auto;scrollbar-width:none;padding:8px 16px;background:var(--card);border-bottom:1px solid var(--rule)}"
    ".bar0 b{font:700 11px var(--ui);letter-spacing:.12em;text-transform:uppercase;color:var(--mute);white-space:nowrap;margin-right:6px}"
    ".bar0 button{font:600 13px var(--ui);border:1px solid var(--rule);background:none;color:var(--ink);border-radius:999px;padding:6px 12px;cursor:pointer;white-space:nowrap}.bar0 button[aria-pressed=true]{background:var(--ink);color:var(--paper);border-color:var(--ink)}"
    ".vv[hidden]{display:none}")
SWITCH_JS = ("(function(){var V=[].slice.call(document.querySelectorAll('.vv')),B=[].slice.call(document.querySelectorAll('.bar0 button'));"
    "function go(k){V.forEach(function(v,i){v.hidden=i!==k});B.forEach(function(b,i){b.setAttribute('aria-pressed',i===k)});history.replaceState(null,'','#v'+(k+1))}"
    "B.forEach(function(b,i){b.onclick=function(){go(i);scrollTo(0,0)}});var m=/^#v(\\d)$/.exec(location.hash);go(m?Math.min(+m[1]-1,V.length-1):0)})();")
def switch(label, variants):
    bar = f'<nav class="bar0" aria-label="Variants"><b>{label}</b>' + "".join(f'<button type="button">{k+1} · {n}</button>' for k, (n, _) in enumerate(variants)) + "</nav>"
    return bar, "".join(f'<div class="vv"{"" if k == 0 else " hidden"}>{h}</div>' for k, (_, h) in enumerate(variants))

# ------------------------------------------------------------------ ABOUT
FEAT = sorted([a for a in data.ARTICLES], key=lambda a: int(a["pages"].split("–")[0]))
DEPTS = [("Ḥuqúqu’lláh", 30), ("Abiding in God’s Law: Artistic expressions of the human spirit", 32), ("Bahá’í Bookstore", 36), ("Rhythm of Bahá’í Life", 39),
         ("National Bahá’í Fund", 42), ("Brilliant Star Treasure Box", 47), ("Chinese (Simplified)", 49), ("Español (Spanish)", 58), ("بخش فارسی (Persian)", 69),
         ("Classified", 79), ("Education", 80), ("In Memoriam", 81), ("Contact Information", 84)]
PUB = ("The American Bahá’í (ISSN 1062-1113) is published once every 2 months for a total of 5 issues per year by the " + NSA + ", 1233 Central St., Evanston, IL 60201-1611.")
ABOUT_ISSUE = t(ISSUE["about"])
COVER_NOTE = t(ISSUE["cover_note"]).replace("Natural beauty merges", "Natural, vernal beauty merges")  # print reads "Natural, vernal beauty"
EPI = t(ISSUE["epigraph"])
LANGS = "The issue also includes the National Spiritual Assembly’s mid-year reflections, presented in English and Persian, alongside the magazine’s first publication in Simplified Chinese."
STAFF = ('<dl class="st"><dt>Editor</dt><dd>Neena Rouhani</dd><dt>Designer</dt><dd>Luthando Mazibuko</dd><dt>Photography</dt><dd>By license or by permission of community members</dd></dl>')
def feats(link=True):
    return "".join(f'<li style="--c:{TINT[a["slug"]]}"><a href="{R}{a["slug"]}/"><span class="k">{t(a["kicker"])}</span><span class="tt">{t(a["title"])}</span><span class="pg">{a["pages"].split("–")[0]}</span></a></li>' for a in FEAT)

v1 = f'''<article class="a1"><p class="nm"><small>The</small>American Bahá’í</p><p class="iss">{ISSUE["vol"]} · {ISSUE["date"].replace(" / ", "/")}</p><p class="th">{ISSUE["theme"]}</p>
<div class="rule"></div><p class="pub">{PUB}</p>{STAFF}
<p class="ty">This edition is set in Literata, Bricolage Grotesque and Barlow Condensed.</p>
<div class="rule"></div><p class="cp">Entire contents Copyright ©2026 by the {NSA}. World rights reserved. Printed in the U.S.A.</p></article>'''

v2 = f'''<article class="a2"><figure><img src="{I}cover-paint-v2.jpg" alt="The cover painting of this issue by Juliet Bogan"><figcaption>Cover · Juliet Bogan</figcaption></figure>
<div class="a2b"><p class="k">About the cover from artist Juliet Bogan</p><blockquote>{COVER_NOTE}</blockquote>
<p class="k">About this issue</p><p class="lead">{ABOUT_ISSUE}</p><p>{LANGS}</p>
<div class="facts"><span>{ISSUE["vol"]}</span><span>{ISSUE["date"].replace(" / ", "/")}</span><span>5 issues a year</span></div><p class="pub">{PUB}</p>{STAFF}</div></article>'''

v3 = f'''<article class="a3"><div class="ep"><p>“{EPI}”</p><span>The Universal House of Justice</span></div>
<div class="ct3"><p class="dt">{ISSUE["date"]}</p><h2 class="cn">Contents</h2><ol class="fe">{feats()}</ol>
<p class="k">Features</p><ul class="dp">{"".join(f"<li><span>{n}</span><i></i><b>{p}</b></li>" for n, p in DEPTS)}</ul></div>
<div class="ab3"><p class="k">About this issue</p><p>{ABOUT_ISSUE}</p><p>{LANGS}</p><p class="pub">{PUB}</p></div></article>'''

N = [("57", "volumes", "Volume 57, Number 5 is this issue."), ("5", "issues a year", "Published once every 2 months."), ("4", "languages", "English, with sections in Simplified Chinese, Spanish and Persian."),
     ("6", "stories online", "From race amity in South Carolina to a comic from Indianapolis."), (str(PLACES), "places named", "From Bellingham, Washington, to Edinburg, Texas.")]
v4 = f'''<article class="a4"><p class="nm"><small>The</small>American Bahá’í</p><p class="lead">{ABOUT_ISSUE}</p>
<ul class="nums">{"".join(f'<li><b>{n}</b><span class="u">{u}</span><span class="d">{d}</span></li>' for n, u, d in N)}</ul>
<p class="pub">{PUB}</p>{STAFF}</article>'''

SHELF = [("cover-v56n1.jpg", "Volume 56, Number 1"), ("cover-v57n1.jpg", "Volume 57, Number 1"), ("cover-v57n2.jpg", "Volume 57, Number 2"), ("cover-v57n4.jpg", "Volume 57, Number 4"), ("cover-full-v2.jpg", "Volume 57, Number 5")]
v5 = f'''<article class="a5"><p class="nm"><small>The</small>American Bahá’í</p><p class="lead">{ABOUT_ISSUE}</p>
<div class="shelf">{"".join(f'<figure{" class=now" if k == len(SHELF)-1 else ""}><img src="{I}{f}" alt="Cover, {c}" loading="lazy"><figcaption>{c}</figcaption></figure>' for k, (f, c) in enumerate(SHELF))}</div>
<div class="a5b"><div><p class="k">This issue · {ISSUE["theme"]}</p><p>{LANGS}</p><p><a href="{R}">Read the issue →</a></p></div><div><p class="pub">{PUB}</p>{STAFF}</div></div></article>'''

ABOUT_CSS = '''main{max-width:1080px!important}main h1{display:none}
.nm{font:400 clamp(40px,6vw,68px)/1 var(--text);letter-spacing:-.015em;margin:0}.nm small{display:block;font:italic 400 .34em var(--text);color:#b8782e;margin:0 0 .1em .05em}
.k{font:700 12px var(--ui)!important;letter-spacing:.16em;text-transform:uppercase;color:#b8782e;margin:28px 0 10px!important}
.lead{font:400 clamp(19px,2vw,23px)/1.5 var(--text)!important;text-wrap:pretty}
.pub{font:14px/1.6 var(--ui)!important;color:var(--mute)}
.st{display:grid;grid-template-columns:auto 1fr;gap:6px 18px;margin:16px 0 0;font:15px/1.45 var(--ui)}.st dt{font-weight:700;color:var(--mute)}.st dd{margin:0}
/* 1 colophon */
.a1{max-width:560px;margin:20px auto 0;text-align:center}.a1 .iss{font:italic 17px var(--text)!important;margin:16px 0 4px!important;color:var(--mute)}.a1 .th{font:700 15px var(--ui)!important;letter-spacing:.2em;text-transform:uppercase;margin:0!important}
.a1 .rule{width:60px;height:5px;border:1px solid var(--ink);border-width:1px 0;margin:30px auto}.a1 .st{justify-content:center;text-align:left;max-width:420px;margin:18px auto 0}
.a1 .ty{font:italic 16px var(--text)!important;color:var(--mute);margin-top:22px!important}.a1 .cp{font:13px/1.6 var(--ui)!important;color:var(--mute)}
/* 2 the cover */
.a2{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(24px,4vw,56px);align-items:start}.a2 figure{margin:0;position:sticky;top:16px}.a2 img{width:100%;display:block;box-shadow:0 20px 40px rgba(29,26,22,.2)}
.a2 figcaption{font:13px var(--ui);color:var(--mute);margin-top:8px}.a2 blockquote{margin:0;font:italic 18px/1.6 var(--text);border-left:3px solid #b8782e;padding-left:18px}
.a2 .k:first-child{margin-top:0!important}.facts{display:flex;flex-wrap:wrap;gap:8px;margin:20px 0}.facts span{font:600 13px var(--ui);border:1px solid var(--rule);border-radius:999px;padding:6px 12px;background:var(--card)}
/* 3 contents */
.a3{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:clamp(24px,4vw,56px);align-items:start}
.ep{aspect-ratio:1;border-radius:50%;background:var(--card);border:1px solid var(--rule);display:grid;place-content:center;padding:14%;text-align:left}.ep p{font:400 clamp(17px,1.9vw,22px)/1.4 var(--ui)!important;margin:0 0 14px!important}.ep span{font:700 14px var(--ui)}
.ct3 .dt{font:15px var(--ui)!important;letter-spacing:.06em;margin:0!important}.cn{font:300 clamp(40px,5vw,56px)/1 var(--ui)!important;letter-spacing:-.01em!important;text-transform:none!important;color:var(--ink)!important;border:0!important;padding:0!important;margin:4px 0 18px!important}
.fe{list-style:none;margin:0;padding:0}.fe a{display:grid;grid-template-columns:1fr auto;gap:2px 14px;padding:10px 0 10px 12px;border-left:4px solid var(--c);text-decoration:none;color:var(--ink);margin-bottom:8px}.fe a:hover{background:var(--card)}
.fe .k{grid-column:1;margin:0!important;font-size:11px!important;color:var(--mute)}.fe .tt{grid-column:1;font:700 17px/1.3 var(--text)}.fe .pg{grid-column:2;grid-row:1/3;align-self:center;font:700 17px var(--ui)}
.dp{list-style:none;margin:0;padding:0;font:15px/1.4 var(--ui)}.dp li{display:flex;align-items:baseline;gap:6px;padding:4px 0}.dp i{flex:1;border-bottom:1px dotted var(--mute);transform:translateY(-4px)}.dp b{font-weight:700}
.ab3{grid-column:1/-1;border-top:1px solid var(--rule);padding-top:8px;max-width:720px}
/* 4 numbers */
.a4 .nm{margin-bottom:18px}.a4 .lead{max-width:40ch}.nums{list-style:none;margin:34px 0;padding:0;display:grid;grid-template-columns:repeat(5,1fr);gap:0;border-top:1px solid var(--rule)}
.nums li{padding:22px 20px 22px 0;border-bottom:1px solid var(--rule);display:grid;gap:2px}.nums b{font:400 clamp(48px,6vw,72px)/1 var(--text);color:#b8782e}.nums .u{font:700 13px var(--ui);letter-spacing:.14em;text-transform:uppercase}.nums .d{font:15px/1.5 var(--ui);color:var(--mute)}
/* 5 shelf */
.a5 .lead{max-width:36ch}.shelf{display:flex;gap:clamp(10px,2vw,22px);align-items:flex-end;margin:34px 0;overflow-x:auto;padding:0 0 12px;border-bottom:10px solid #c9b9a0;box-shadow:0 8px 0 -4px rgba(0,0,0,.08)}
.shelf figure{margin:0;flex:0 0 clamp(120px,17%,190px)}.shelf img{width:100%;aspect-ratio:4/5.15;object-fit:cover;display:block;box-shadow:0 10px 18px rgba(29,26,22,.2)}.shelf .now{flex-basis:clamp(150px,22%,240px)}
.shelf figcaption{font:12px var(--ui);color:var(--mute);margin-top:8px}.shelf .now figcaption{color:var(--ink);font-weight:700}
.a5b{display:grid;grid-template-columns:1.2fr 1fr;gap:40px}.a5b .k{margin-top:0!important}
@media (max-width:760px){.a2,.a3,.a5b{grid-template-columns:1fr}.a2 figure{position:static}.nums{grid-template-columns:1fr 1fr}.ep{max-width:420px}}'''

# ------------------------------------------------------------------ TERMS
CC = '<a href="https://creativecommons.org/licenses/by-nc-nd/4.0/" rel="license noopener" target="_blank">Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License</a>'
ML = '<a href="mailto:termsofuse@bahai.us">termsofuse@bahai.us</a>'
CLAUSES = [
 ("meaning", "Meaning", "The Content may not be used in a way that misrepresents the intent of the original source."),
 ("notice", "Notice and credit", f"Any use of the Content must be accompanied by the notice “Copyright © {NSA}” together with attribution to bahai.us, where appropriate, and the name of the individual author, where one is named."),
 ("media", "Photographs, audio, video and maps", "Audio-visual content may be cropped and edited for size. No other editing is permitted. You may use, reproduce, distribute, link to and display it under a limited, non-exclusive license, provided its intent, character, nature and meaning remain unaltered and the individual author is credited where named."),
 ("commercial", "Commercial and other uses", f"Any use for a commercial purpose, or any use not covered by this license, requires permission before use. Write to {ML}."),
 ("withdrawal", "Withdrawal", "The National Assembly may withdraw permission to use the Content at any time and for any use. Use of the Content must then cease immediately."),
 ("liability", "Liability", "The National Assembly does not endorse or take responsibility for third-party uses of the Content, and will not be responsible or liable to any person or organization for any direct, incidental, consequential, indirect, or punitive damages that may result from access to or use of the Content."),
]
GLANCE = [("You may", ["Share, link to and display the Content", "Crop or resize photographs and media"]),
          ("Always", ["Include “Copyright © National Spiritual Assembly of the Bahá’ís of the United States”", "Credit bahai.us and the named author", "Keep the original meaning"]),
          ("Ask first", ["Commercial use", "Any edit beyond cropping or resizing", f"Write to {ML}"])]
PROPOSED = (f'<p class="lede">Everything on this site is protected by copyright and shared under a {CC}, on the terms below.</p>'
    '<div class="gl" aria-label="At a glance">' + "".join(f'<section><h3>{h}</h3><ul>{"".join(f"<li>{x}</li>" for x in L)}</ul></section>' for h, L in GLANCE) + '</div>'
    '</div>'
    '<h2 id="copyright">Copyright</h2>'
    f'<p>All material on this website, including but not limited to text, photographs, images, illustrations, maps, audio clips and video clips (“Content”), is protected by copyrights, trademarks and other intellectual property rights. The {NSA} (“the National Assembly”) retains full legal protection for its Content under all applicable United States and international laws, and grants use of it under the terms of the {CC}.</p>'
    '<h2 id="terms">Terms of use</h2><p>You are welcome to access and use the Content subject to these conditions:</p><ol class="cl">'
    + "".join(f'<li id="{i}"><b>{h}.</b> {x}</li>' for i, h, x in CLAUSES) + '</ol>'
    '')

CHANGES = [("Two copyright paragraphs", "merged; both said the National Assembly retains full legal protection under all applicable laws."),
           ("The National Assembly’s full name", "written once, then “the National Assembly” (the current page already uses that short form once)."),
           ("Two permission routes", "termsofuse@bahai.us and a “contact us” link to bahai.us: now one address, in clause 4."),
           ("Six unlabeled bullets", "now numbered clauses with short headings and anchors, so the lightbox can link straight to clause 3, “Photographs, audio, video and maps”."),
           ("Clause 2", "“If you wish to use any Content, it must be accompanied by” shortened to “Any use of the Content must be accompanied by”."),
           ("Clause 3", "the license sentence rephrased in the second person; the conditions are unchanged."),
           ("At a glance", "a plain-language summary above the terms, marked as non-binding."),
           ("License link", "now https.")]
TERMS_CSS = '''main{max-width:760px!important}
.lede{font:400 21px/1.5 var(--text)!important}
.gl{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:24px 0 8px}.gl section{background:var(--card);border:1px solid var(--rule);border-top:4px solid #1b5e6b;padding:14px 16px}.gl section:nth-child(2){border-top-color:#b8782e}.gl section:nth-child(3){border-top-color:#222e4c}
.gl h3{font:700 12px var(--ui);letter-spacing:.14em;text-transform:uppercase;margin:0 0 8px}.gl ul{margin:0;padding-left:1.1em;font:15px/1.45 var(--ui)}.gl li{margin:0 0 6px}
.note{font:13px var(--ui)!important;color:var(--mute)}
ol.cl{list-style:none;counter-reset:c;margin:0 0 1.4em;padding:0}ol.cl li{counter-increment:c;position:relative;padding:14px 0 14px 46px;border-top:1px solid var(--rule);font:17px/1.6 var(--text);scroll-margin-top:60px}
ol.cl li::before{content:counter(c);position:absolute;left:0;top:12px;width:30px;height:30px;border-radius:50%;background:var(--card);border:1px solid var(--rule);display:grid;place-items:center;font:700 14px var(--ui);color:#b8782e}
ol.cl li:target{background:color-mix(in oklab,#b8782e 10%,transparent)}ol.cl b{font-family:var(--ui);font-size:15px}
.chg{margin:44px 0 0;padding:18px 20px;background:var(--card);border:1px dashed #b8782e}.chg h2{margin-top:0!important;border:0!important;padding:0!important}.chg ul{margin:0;padding-left:1.1em;font:15px/1.5 var(--ui)}.chg li{margin:0 0 8px}
@media (max-width:640px){.gl{grid-template-columns:1fr}}'''

if __name__ == "__main__":
    av = [("Colophon", v1), ("The cover", v2), ("Contents", v3), ("By the numbers", v4), ("The shelf", v5)]
    bar, vv = switch("About page", av)
    h = shell("terms", "About Page Studies", "<h1>About</h1>" + vv, SWITCH_CSS + ABOUT_CSS, SWITCH_JS)
    h = h.replace('<header class="pt">', bar + '<header class="pt">', 1)
    os.makedirs(os.path.join(SITE, "test", "about"), exist_ok=True); open(os.path.join(SITE, "test", "about", "index.html"), "w").write(h)

    cur = re.search(r"<main>(.*)</main>", open(os.path.join(SITE, "terms", "index.html")).read(), re.S).group(1)
    prop = "<h1>Terms of use</h1>" + PROPOSED + '<aside class="chg"><h2>What changed</h2><ul>' + "".join(f"<li><b>{a}:</b> {b}</li>" for a, b in CHANGES) + "</ul></aside>"
    bar, vv = switch("Terms page", [("Proposed", prop), ("Current", cur)])
    h = shell("terms", "Terms Page Study", vv, SWITCH_CSS + TERMS_CSS, SWITCH_JS).replace('<header class="pt">', bar + '<header class="pt">', 1)
    os.makedirs(os.path.join(SITE, "test", "terms"), exist_ok=True); open(os.path.join(SITE, "test", "terms", "index.html"), "w").write(h)
    print("ok")
