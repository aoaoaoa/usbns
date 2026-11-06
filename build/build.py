import html, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import ISSUE, VOICES, ARTICLES
SUB = "A U.S. Bah\u00e1\u2019\u00ed News Service"

def esc(s): return html.escape(s, quote=False) if s else ""
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
SIDES = '<meta name="claude:viewport-fit-sides" content="cover">'
GUT = "padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));"

def body_html(blocks, qa_style="dl"):
    out = []
    for b in blocks:
        k = b[0]
        if k == "p": out.append(f"<p>{esc(b[1])}</p>")
        elif k == "h": out.append(f"<h3>{esc(b[1])}</h3>")
        elif k == "q": out.append(f'<blockquote class="pull"><p>{esc(b[1])}</p><cite>{esc(b[2])}</cite></blockquote>')
        elif k == "note": out.append(f'<p class="note">{esc(b[1])}</p>')
        elif k == "qa": out.append(f'<p class="qa">{esc(b[1])}</p>')
        elif k == "a": out.append(f'<p class="ans"><b>{esc(b[1])}</b> {esc(b[2])}</p>')
        elif k == "pair": out.append('<figure class="photo pair">' + "".join(f'<div><img src="img/{f}" alt="{esc(c)}" loading="lazy"><figcaption>{esc(c)}</figcaption></div>' for f,c in b[1:]) + '</figure>')
        elif k == "img": out.append(f'<figure class="photo"><img src="img/{b[1]}" alt="{esc(b[2])}" loading="lazy"><figcaption>{esc(b[2])}</figcaption></figure>')
    return "\n".join(out)

def first_para_dropcap(h):
    return h.replace("<p>", '<p class="first">', 1)

# ------------------------------------------------------------------ V1 FOLIO
def build_folio():
    secs = []
    bands = ["#1b5e6b", "#8a3a1e", "#3b3f7a", "#5c2a4e", "#2f5d3a", "#8b6a1a"]
    for i, a in enumerate(ARTICLES):
        art = ""
        if a.get("art"):
            if a["slug"] == "comic":
                art = f'''<figure class="plate comic"><img src="img/{a["art"]}" alt="{esc(a["art_alt"])}"><img src="img/{a["art2"]}" alt="{esc(a["art2_alt"])}"><figcaption>{esc(a["art_credit"])}</figcaption></figure>'''
            else:
                cls = "plate bare" if a.get("art_transparent") else "plate"
                art = f'''<figure class="{cls}"><img src="img/{a["art"]}" alt="{esc(a["art_alt"])}"><figcaption>{esc(a["art_credit"])}</figcaption></figure>'''
        else:
            art = '<div class="numeral" aria-hidden="true">50</div>'
        dek = f'<p class="dek">{esc(a["dek"])}</p>' if a.get("dek") else ""
        by = f'<p class="by">{esc(a["byline"])}</p>' if a.get("byline") else ""
        secs.append(f'''<article class="story" id="{a["slug"]}">
  {art}
  <header class="shead">
    <p class="kicker"><span>{esc(a["kicker"])}</span><span>pp. {a["pages"]}</span></p>
    <h2>{esc(a["title"])}</h2>
    {dek}{by}
  </header>
  <div class="prose">{first_para_dropcap(body_html(a["body"]))}</div>
</article>''')
        if i < len(VOICES):
            v = VOICES[i]
            secs.append(f'''</div><aside class="voice" style="--band:{bands[i % len(bands)]}"><div class="vin"><p>{esc(v[0])}</p><cite>{esc(v[1])}</cite></div></aside><div class="wrap">''')
    index = "".join(f'<li><a href="#{a["slug"]}"><span class="t">{esc(a["title"])}</span><span class="pg">{a["pages"].split("–")[0]}</span></a></li>' for a in ARTICLES)
    return f'''<title>{esc(ISSUE["title"])} Folio</title>
{SIDES}
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Libre+Caslon+Display&family=Libre+Caslon+Text:ital,wght@0,400;0,700;1,400&family=Public+Sans:ital,wght@0,400;0,600;1,400&display=swap">
<style>
/* Layout: one long folio. The cover painting carries a set masthead; an index follows; each feature opens on its art plate and runs in a single measure with a margin column for pull quotes; between features, a colored band carries one passage from the issue's pages on the arts. */
:root{{
  --paper:#f5f1e8; --ink:#1d1a16; --mute:#6a635a; --rule:#d9d2c4; --accent:#1b5e6b; --cream:#f7f2ea;
  --disp:"Libre Caslon Display",Georgia,serif; --text:"Libre Caslon Text",Georgia,serif; --ui:"Public Sans","Helvetica Neue",Arial,sans-serif;
}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--paper:#15130f;--ink:#efe9dd;--mute:#a39b8e;--rule:#2f2a22;--accent:#7fc0c9;--cream:#1c1915;color-scheme:dark}}}}
:root[data-theme="dark"]{{--paper:#15130f;--ink:#efe9dd;--mute:#a39b8e;--rule:#2f2a22;--accent:#7fc0c9;--cream:#1c1915;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--paper);color:var(--ink);font-family:var(--text);font-size:18px;line-height:1.55}}
.wrap{{max-width:1180px;margin:0 auto;{GUT}}}
.ui{{font-family:var(--ui);font-size:12px;letter-spacing:.12em;text-transform:uppercase}}
/* cover */
.cover{{padding-block:clamp(28px,5vw,64px) 0}}
.cover .mast .the{{font-family:var(--disp);font-size:clamp(18px,2.2vw,26px);margin:0 0 -.2em .1em}}
.cover h1{{font-family:var(--disp);font-size:clamp(56px,11vw,150px);line-height:.95;margin:0;letter-spacing:-.015em;font-weight:400}}
.cover .sub{{font-family:var(--disp);font-size:clamp(18px,2.2vw,28px);margin:14px 0 0 .1em;font-style:italic}}
.cover .line{{display:flex;flex-wrap:wrap;gap:8px 32px;margin-top:24px;font-family:var(--ui);font-size:13px;letter-spacing:.06em;color:var(--mute)}}
.painting{{margin:clamp(28px,4vw,48px) auto 0;width:fit-content;max-width:100%;border:1px solid var(--rule);background:var(--cream);padding:clamp(10px,1.4vw,18px)}}
.painting .mat{{border:1px solid var(--rule)}}
.painting img{{display:block;width:auto;max-width:100%;height:auto;max-height:96vh}}
.painting figcaption{{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;font-family:var(--ui);font-size:12px;letter-spacing:.06em;color:var(--mute);padding:12px 2px 0}}
/* front matter */
.front{{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:48px clamp(32px,6vw,96px);padding-block:clamp(40px,7vw,96px);border-bottom:1px solid var(--rule)}}
.front h2{{font-family:var(--disp);font-size:clamp(32px,4vw,52px);font-weight:400;margin:0 0 20px;letter-spacing:-.01em}}
.index{{list-style:none;margin:0;padding:0;border-top:1px solid var(--rule)}}
.index a{{display:flex;justify-content:space-between;gap:16px;align-items:baseline;padding:14px 0;border-bottom:1px solid var(--rule);color:inherit;text-decoration:none;font-size:19px;line-height:1.3}}
.index a:hover .t,.index a:focus-visible .t{{color:var(--accent)}}
.index .pg{{font-family:var(--ui);font-size:13px;color:var(--mute);font-variant-numeric:tabular-nums}}
.epi p{{font-family:var(--disp);font-size:clamp(22px,2.4vw,30px);line-height:1.3;margin:0 0 12px;text-wrap:pretty}}
.epi cite{{font-style:normal;font-family:var(--ui);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--mute)}}
.about{{margin-top:36px;color:var(--mute);font-size:16px}}
.about b{{color:var(--ink);font-weight:700}}
/* stories */
.story{{padding-block:clamp(48px,8vw,112px) 0}}
.plate{{margin:0 0 clamp(28px,4vw,48px);background:var(--cream);border:1px solid var(--rule)}}
.plate img{{display:block;width:100%;height:auto;max-height:78vh;object-fit:cover}}
.plate.bare{{background:transparent;border:0}}
.plate.bare img{{max-height:none;object-fit:contain;max-width:1000px}}
.plate.bare figcaption{{padding-left:0}}
.plate.comic{{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--rule)}}
.plate.comic img{{max-height:none;background:#fff}}
.plate.comic figcaption{{grid-column:1/-1;background:var(--cream)}}
.plate figcaption{{font-family:var(--ui);font-size:12px;letter-spacing:.06em;color:var(--mute);padding:10px 14px}}
.numeral{{font-family:var(--disp);font-size:clamp(160px,28vw,360px);line-height:.8;color:var(--accent);margin:0 0 .05em -.03em;letter-spacing:-.04em}}
.shead{{max-width:30ch}}
.kicker{{display:flex;justify-content:space-between;font-family:var(--ui);font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin:0 0 20px;max-width:62ch}}
.shead h2{{font-family:var(--disp);font-size:clamp(38px,5.6vw,76px);line-height:1;font-weight:400;letter-spacing:-.02em;margin:0 0 18px;text-wrap:balance}}
.dek{{font-size:clamp(20px,2vw,26px);font-style:italic;margin:0 0 12px;color:var(--mute)}}
.by{{font-family:var(--ui);font-size:13px;letter-spacing:.04em;margin:0 0 36px;color:var(--mute)}}
.by::before{{content:"By ";}}
.prose{{max-width:66ch;font-size:19px;line-height:1.6}}
.prose p{{margin:0 0 1.2em;text-wrap:pretty}}
.prose p.first::first-letter{{font-family:var(--disp);font-size:4.4em;float:left;line-height:.78;padding:.08em .1em 0 0;color:var(--accent)}}
.prose h3{{font-family:var(--ui);font-weight:600;font-size:14px;letter-spacing:.1em;text-transform:uppercase;margin:2.2em 0 .8em;color:var(--accent)}}
.prose .pull{{margin:2em 0 2em clamp(-120px,-10vw,0px);padding:0 0 0 20px;border-left:3px solid var(--accent);max-width:34ch}}
.prose .pull p{{font-family:var(--disp);font-size:clamp(22px,2.2vw,30px);line-height:1.25;margin:0 0 10px}}
.prose .pull cite{{font-style:normal;font-family:var(--ui);font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--mute)}}
.prose .photo{{margin:2em 0;max-width:none}}
.prose .photo.pair{{display:grid;grid-template-columns:1fr 1fr;gap:16px;max-width:none}}
.prose .photo.pair>div{{min-width:0}}
@media (max-width:640px){{.prose .photo.pair{{grid-template-columns:1fr}}}}
.prose .photo img{{display:block;width:100%;height:auto;border:1px solid var(--rule)}}
.prose .photo figcaption{{font-family:var(--ui);font-size:12.5px;letter-spacing:.02em;color:var(--mute);margin-top:8px;line-height:1.5}}
.prose .note{{font-family:var(--ui);font-size:15px;color:var(--mute);border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:14px 0;margin:2em 0}}
.prose .qa{{font-weight:700;margin-top:1.8em}}
.prose .ans b{{font-family:var(--ui);font-weight:600;font-size:14px;letter-spacing:.06em;text-transform:uppercase;color:var(--accent);margin-right:.4em}}
/* voices */
.voice{{background:var(--band);color:#f7f2ea;margin-top:clamp(48px,8vw,112px)}}
.voice+.wrap .story{{padding-top:clamp(48px,8vw,112px)}}
.vin{{max-width:1180px;margin:0 auto;{GUT}padding-block:clamp(40px,6vw,80px)}}
.voice p{{font-family:var(--disp);font-size:clamp(22px,2.6vw,34px);line-height:1.3;max-width:34ch;margin:0 0 18px;text-wrap:pretty}}
.voice cite{{font-style:normal;font-family:var(--ui);font-size:12px;letter-spacing:.12em;text-transform:uppercase;opacity:.8}}
.colophon{{padding-block:clamp(48px,8vw,96px);font-family:var(--ui);font-size:13px;color:var(--mute);max-width:60ch;line-height:1.6;border-top:1px solid var(--rule);margin-top:clamp(48px,8vw,112px)}}
a:focus-visible{{outline:2px solid var(--accent);outline-offset:3px}}
@media (max-width:820px){{
  .front{{grid-template-columns:1fr}}
  .prose .pull{{margin-left:0}}
  .plate.comic{{grid-template-columns:1fr}}
}}
</style>
<header class="cover wrap">
  <div class="mast">
    <p class="the">The</p>
    <h1>American Bahá'í</h1>
    <p class="sub">{SUB}</p>
    <div class="line"><span>{esc(ISSUE["date"])}</span><span>{esc(ISSUE["url"])}</span></div>
  </div>
  <figure class="painting"><div class="mat"><img src="img/cover-paint.jpg" alt="Oil painting by Juliet Bogan: two figures in a flowering meadow look toward terraced green farmland and ochre mountains under a pale sky"></div><figcaption><span>Cover painting by {esc(ISSUE["cover_artist"])}</span><span>Oil on canvas</span></figcaption></figure>
</header>
<main>
<div class="wrap">
<section class="front">
  <div>
    <h2>Features</h2>
    <ol class="index">{index}</ol>
    <p class="about"><b>About this issue.</b> {esc(ISSUE["about"])}</p>
  </div>
  <div class="epi">
    <p>“{esc(ISSUE["epigraph"])}”</p>
    <cite>{esc(ISSUE["epigraph_src"])}</cite>
    <p class="about"><b>About the cover.</b> {esc(ISSUE["cover_note"])} <i>Juliet Bogan</i></p>
  </div>
</section>
{"".join(secs)}
<footer class="colophon">{esc(ISSUE["publisher"])} Feature texts transcribed from the printed issue; passages between features are drawn from “Abiding in God's Law: Artistic expressions of the human spirit,” pp. 32–33.</footer>
</div>
</main>
'''

# ------------------------------------------------------------------ V2 PLATES
def build_plates():
    chapters = []
    for i, a in enumerate(ARTICLES):
        n = i + 1
        if a.get("art"):
            if a["slug"] == "comic":
                plate = f'<div class="img two"><img src="img/{a["art"]}" alt="{esc(a["art_alt"])}"><img src="img/{a["art2"]}" alt="{esc(a["art2_alt"])}"></div>'
            else:
                plate = f'<div class="img{" bare" if a.get("art_transparent") else ""}"><img src="img/{a["art"]}" alt="{esc(a["art_alt"])}"></div>'
        else:
            plate = '<div class="img type"><span>50</span></div>'
        dek = f'<p class="dek">{esc(a["dek"])}</p>' if a.get("dek") else ""
        by = f'<p class="by">{esc(a["byline"])}</p>' if a.get("byline") else ""
        chapters.append(f'''<section class="chapter" id="{a["slug"]}">
  <div class="plate">
    {plate}
    <div class="cap"><span class="n">Plate {n}</span><span>{esc(a["art_credit"] or "Set in type")}</span><span>pp. {a["pages"]}</span></div>
  </div>
  <header class="chead">
    <p class="kicker">{esc(a["kicker"])}</p>
    <h2>{esc(a["title"])}</h2>
    {dek}{by}
  </header>
  <div class="prose">{body_html(a["body"])}</div>
</section>''')
    nav = "".join(f'<a href="#{a["slug"]}">{esc(a["short"])}</a>' for a in ARTICLES)
    return f'''<title>{esc(ISSUE["title"])} Plates</title>
{SIDES}
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..700;1,6..96,400..700&family=Source+Serif+4:ital,opsz,wght@0,8..60,300..600;1,8..60,300..600&family=DM+Mono:wght@400;500&display=swap">
<style>
/* Layout: a dark gallery. Each feature is hung as a plate on a charcoal wall, its illustration at full width with a caption strip in mono; the headline follows in Bodoni italic, and the text runs in one lit column. One deliberate theme. */
:root{{
  --wall:#141312; --card:#1c1a18; --fg:#f1ebe0; --dim:#a69d8e; --rule:#2c2926; --gold:#d6b25e; --rose:#e8a3a3;
  --disp:"Bodoni Moda","Didot","Bodoni 72",Georgia,serif; --text:"Source Serif 4",Georgia,serif; --mono:"DM Mono","SF Mono",Menlo,monospace;
  color-scheme:dark;
}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{margin:0;background:var(--wall);color:var(--fg);font-family:var(--text);font-size:19px;line-height:1.55}}
.bar{{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:color-mix(in oklab,var(--wall) 88%,transparent);backdrop-filter:blur(10px);border-bottom:1px solid var(--rule)}}
body::before{{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--wall)}}
.bar .in{{max-width:1280px;margin:0 auto;{GUT}display:flex;gap:24px;align-items:center;min-height:52px;overflow-x:auto;scrollbar-width:none}}
.bar .brand{{font-family:var(--disp);font-size:18px;white-space:nowrap;color:var(--fg);text-decoration:none;flex:none}}
.bar nav{{display:flex;gap:18px;margin-left:auto}}
.bar nav a{{font-family:var(--mono);font-size:12px;letter-spacing:.04em;color:var(--dim);text-decoration:none;white-space:nowrap;padding:6px 0}}
.bar nav a:hover,.bar nav a:focus-visible{{color:var(--gold)}}
.wrap{{max-width:1280px;margin:0 auto;{GUT}}}
/* cover */
.cover{{padding-block:clamp(40px,7vw,96px) clamp(32px,5vw,64px);display:grid;grid-template-columns:minmax(0,1fr);gap:clamp(32px,5vw,64px)}}
.cover .img{{background:var(--card);border:1px solid var(--rule);padding:clamp(12px,1.6vw,22px);width:fit-content;max-width:100%;margin:0 auto}}
.cover .img .mat{{border:1px solid color-mix(in oklab,var(--gold) 45%,transparent);padding:1px}}
.cover .img img{{display:block;width:auto;max-width:100%;height:auto;max-height:94vh}}
.cover .img figcaption{{display:flex;justify-content:space-between;font-family:var(--mono);font-size:12px;color:var(--dim);padding:12px 2px 0}}
.cover .img figcaption b{{color:var(--gold);font-weight:500}}
.cover h1{{font-family:var(--disp);font-weight:400;font-size:clamp(52px,8vw,120px);line-height:.92;letter-spacing:-.02em;margin:0 0 20px;font-variation-settings:"opsz" 96}}
.cover h1 em{{font-style:italic;font-weight:500}}
.cover .meta{{font-family:var(--mono);font-size:12px;letter-spacing:.04em;color:var(--dim);display:grid;gap:4px;margin-bottom:28px}}
.cover .epi{{font-family:var(--disp);font-style:italic;font-size:clamp(20px,2vw,26px);line-height:1.35;max-width:36ch;margin:0 0 10px;color:var(--fg)}}
.cover cite{{font-style:normal;font-family:var(--mono);font-size:12px;color:var(--dim)}}
.cover .about{{font-size:16px;color:var(--dim);max-width:52ch;margin:28px 0 0}}
.cover .about b{{color:var(--fg);font-weight:500}}
/* chapters */
.chapter{{padding-block:clamp(56px,9vw,128px) 0;border-top:1px solid var(--rule);margin-top:clamp(56px,9vw,128px)}}
.plate{{background:var(--card);border:1px solid var(--rule);padding:clamp(10px,1.5vw,20px)}}
.plate .img{{background:#000;display:grid;place-items:center}}
.plate .img img{{display:block;width:100%;height:auto;max-height:80vh;object-fit:contain}}
.plate .img.bare{{background:var(--card);padding:clamp(16px,3vw,48px)}}
.plate .img.bare img{{max-width:1100px}}
.plate .img.two{{grid-template-columns:1fr 1fr;gap:2px;background:var(--rule)}}
.plate .img.two img{{max-height:none;background:#fff}}
.plate .img.type{{min-height:40vh}}
.plate .img.type span{{font-family:var(--disp);font-style:italic;font-size:clamp(180px,32vw,440px);line-height:.8;color:var(--gold);font-variation-settings:"opsz" 96}}
.cap{{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;font-family:var(--mono);font-size:12px;color:var(--dim);padding:12px 2px 0}}
.cap .n{{color:var(--gold)}}
.chead{{max-width:1000px;margin:clamp(32px,5vw,64px) auto 0}}
.kicker{{font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--gold);margin:0 0 18px}}
.chead h2{{font-family:var(--disp);font-style:italic;font-weight:400;font-size:clamp(40px,6.4vw,92px);line-height:.98;letter-spacing:-.02em;margin:0 0 20px;text-wrap:balance;font-variation-settings:"opsz" 96}}
.dek{{font-size:clamp(20px,2vw,26px);font-weight:300;margin:0 0 10px;color:var(--dim)}}
.by{{font-family:var(--mono);font-size:12px;color:var(--dim);margin:0}}
.prose{{max-width:66ch;margin:clamp(32px,5vw,56px) auto 0;font-size:19px;line-height:1.62;font-weight:300}}
.prose p{{margin:0 0 1.2em;text-wrap:pretty}}
.prose h3{{font-family:var(--disp);font-style:italic;font-weight:500;font-size:28px;margin:2em 0 .6em;color:var(--fg)}}
.prose .pull{{margin:2em 0;padding:28px 0;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)}}
.prose .pull p{{font-family:var(--disp);font-style:italic;font-size:clamp(24px,2.6vw,34px);line-height:1.25;margin:0 0 12px;color:var(--rose)}}
.prose .pull cite{{font-style:normal;font-family:var(--mono);font-size:12px;color:var(--dim)}}
.prose .note{{font-family:var(--mono);font-size:13px;color:var(--dim);line-height:1.6;margin:2.4em 0}}
.prose .photo{{margin:2.2em 0;background:var(--card);border:1px solid var(--rule);padding:10px}}
.prose .photo.pair{{display:grid;grid-template-columns:1fr 1fr;gap:16px;max-width:none}}
.prose .photo.pair>div{{min-width:0}}
@media (max-width:640px){{.prose .photo.pair{{grid-template-columns:1fr}}}}
.prose .photo img{{display:block;width:100%;height:auto}}
.prose .photo figcaption{{font-family:var(--mono);font-size:12px;color:var(--dim);padding:10px 2px 0;line-height:1.5}}
.prose .qa{{font-family:var(--disp);font-style:italic;font-size:24px;line-height:1.3;color:var(--gold);margin:2em 0 .8em}}
.prose .ans b{{font-family:var(--mono);font-weight:500;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--dim);margin-right:.5em}}
.colophon{{max-width:1280px;margin:clamp(56px,9vw,128px) auto 0;{GUT}padding-block:40px 64px;border-top:1px solid var(--rule);font-family:var(--mono);font-size:12px;line-height:1.7;color:var(--dim)}}
a:focus-visible{{outline:2px solid var(--gold);outline-offset:3px}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
@media (max-width:860px){{.plate .img.two{{grid-template-columns:1fr}}}}
</style>
<div class="bar"><div class="in"><a class="brand" href="#top">The American Bahá'í</a><nav>{nav}</nav></div></div>
<main id="top">
<header class="cover wrap">
  <div>
    <h1>Plates from <em>the arts issue</em></h1>
    <div class="meta"><span>{esc(ISSUE["title"])}</span><span>{SUB}</span><span>{esc(ISSUE["date"])}</span><span>Cover painting by {esc(ISSUE["cover_artist"])}</span></div>
    <p class="epi">“{esc(ISSUE["epigraph"])}”</p>
    <cite>{esc(ISSUE["epigraph_src"])}</cite>
    <p class="about"><b>About this issue.</b> {esc(ISSUE["about"])}</p>
  </div>
  <figure class="img"><div class="mat"><img src="img/cover-paint.jpg" alt="Oil painting by Juliet Bogan: two figures in a flowering meadow look toward terraced green farmland and ochre mountains under a pale sky"></div><figcaption><b>Cover</b><span>Painting by {esc(ISSUE["cover_artist"])}</span><span>Oil on canvas</span></figcaption></figure>
</header>
<div class="wrap">{"".join(chapters)}</div>
<footer class="colophon">{esc(ISSUE["publisher"])}<br>Feature texts transcribed from the printed issue. Plate 3 reproduces the printed opener with its title as set in the magazine.</footer>
</main>
'''

# ------------------------------------------------------------------ V3 READER
def build_reader():
    tints = {"gregory":"#e8532a","newyorkers":"#f05a7e","twoartists":"#b07a4a","abs":"#c9462c","endeavor":"#1b5e6b","comic":"#e9a21f"}
    arts = []
    for a in ARTICLES:
        t = tints[a["slug"]]
        if a.get("art"):
            if a["slug"] == "comic":
                art = f'<figure class="inset two"><img src="img/{a["art"]}" alt="{esc(a["art_alt"])}"><img src="img/{a["art2"]}" alt="{esc(a["art2_alt"])}"><figcaption>{esc(a["art_credit"])}</figcaption></figure>'
            else:
                art = f'<figure class="inset{" bare" if a.get("art_transparent") else ""}"><img src="img/{a["art"]}" alt="{esc(a["art_alt"])}"><figcaption>{esc(a["art_credit"])}</figcaption></figure>'
        else:
            art = ""
        dek = f'<p class="dek">{esc(a["dek"])}</p>' if a.get("dek") else ""
        by = f'<span>{esc(a["byline"])}</span>' if a.get("byline") else ""
        arts.append(f'''<article class="story" id="{a["slug"]}" style="--tint:{t}">
  <header class="shead">
    <p class="kicker">{esc(a["kicker"])}</p>
    <h2>{esc(a["title"])}</h2>
    {dek}
    <p class="meta">{by}<span>Pages {a["pages"]}</span></p>
  </header>
  {art}
  <div class="prose">{body_html(a["body"])}</div>
</article>''')
    rail = "".join(f'<a href="#{a["slug"]}" style="--tint:{tints[a["slug"]]}"><span class="sw"></span><span class="t">{esc(a["short"])}</span><span class="pg">{a["pages"].split("–")[0]}</span></a>' for a in ARTICLES)
    return f'''<title>{esc(ISSUE["title"])} Reader</title>
{SIDES}
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,300..800&family=Literata:ital,opsz,wght@0,7..72,300..600;1,7..72,300..600&display=swap">
<style>
/* Layout: a reading app. A rail on the left lists the features with the issue's own color tabs; the stories run on the right in a wide grotesque headline and a book-weight serif, art set inset at the column width. The rail becomes a strip across the top on phones. */
:root{{
  --bg:#fbfaf7; --fg:#171614; --mute:#6d6962; --rule:#e2ded6; --rail:#f3f1ec; --tint:#1b5e6b;
  --disp:"Bricolage Grotesque","Helvetica Neue",Arial,sans-serif; --text:"Literata",Georgia,serif;
}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#111110;--fg:#eceae4;--mute:#9f9a91;--rule:#2a2825;--rail:#161513;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#111110;--fg:#eceae4;--mute:#9f9a91;--rule:#2a2825;--rail:#161513;color-scheme:dark}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{margin:0;background:var(--bg);color:var(--fg);font-family:var(--text);font-size:18px;line-height:1.55}}
.app{{display:grid;grid-template-columns:280px minmax(0,1fr);min-height:100vh}}
.rail{{background:var(--rail);border-right:1px solid var(--rule);position:sticky;top:0;height:100vh;overflow:auto;padding:28px 20px 28px max(20px,env(safe-area-inset-left,0px));display:flex;flex-direction:column;gap:28px}}
.rail .brand{{font-family:var(--disp);font-weight:700;font-size:22px;line-height:1.05;letter-spacing:-.02em;margin:0}}
.rail .brand small{{display:block;font-weight:400;font-size:12px;letter-spacing:.02em;color:var(--mute);margin-top:8px}}
.rail nav{{display:flex;flex-direction:column}}
.rail nav a{{display:grid;grid-template-columns:10px 1fr auto;gap:12px;align-items:center;padding:11px 0;border-top:1px solid var(--rule);color:inherit;text-decoration:none;font-family:var(--disp);font-size:15px;font-weight:500}}
.rail nav a:last-child{{border-bottom:1px solid var(--rule)}}
.rail nav a .sw{{width:10px;height:22px;background:var(--tint);border-radius:2px}}
.rail nav a .pg{{font-size:12px;color:var(--mute);font-variant-numeric:tabular-nums}}
.rail nav a:hover .t,.rail nav a:focus-visible .t{{text-decoration:underline;text-underline-offset:.2em}}
.rail .epi{{font-size:14px;line-height:1.5;color:var(--mute);font-style:italic;margin:auto 0 0}}
.rail .epi cite{{display:block;font-style:normal;font-family:var(--disp);font-size:11px;letter-spacing:.08em;text-transform:uppercase;margin-top:8px}}
.pages{{padding-right:max(16px,env(safe-area-inset-right,0px));padding-left:16px}}
.cover{{display:grid;grid-template-columns:minmax(0,1fr);gap:36px;padding-block:clamp(32px,5vw,72px) clamp(28px,4vw,56px);border-bottom:1px solid var(--rule);max-width:1100px;margin:0 auto}}
.cover h1{{font-family:var(--disp);font-weight:800;font-size:clamp(44px,6.6vw,96px);line-height:.92;letter-spacing:-.035em;margin:0 0 20px;font-variation-settings:"opsz" 96;text-wrap:balance}}
.cover .about{{max-width:50ch;font-size:16px;color:var(--mute);margin:0}}
.cover .about b{{color:var(--fg);font-weight:600}}
.cover figure{{margin:0 auto;width:fit-content;max-width:100%;border:1px solid var(--rule);padding:clamp(10px,1.4vw,18px);background:var(--rail);border-radius:6px}}
.cover figure .mat{{border:1px solid var(--rule);border-radius:3px;overflow:hidden}}
.cover img{{display:block;width:auto;max-width:100%;height:auto;max-height:92vh}}
.cover figcaption{{font-family:var(--disp);font-size:12px;color:var(--mute);margin-top:8px;letter-spacing:.02em}}
.story{{max-width:1100px;margin:0 auto;padding-block:clamp(56px,8vw,112px) 0}}
.story+.story{{border-top:1px solid var(--rule);margin-top:clamp(56px,8vw,112px)}}
.kicker{{font-family:var(--disp);font-size:12px;letter-spacing:.14em;text-transform:uppercase;font-weight:600;color:var(--tint);margin:0 0 16px}}
.shead h2{{font-family:var(--disp);font-weight:700;font-size:clamp(36px,5.4vw,72px);line-height:.98;letter-spacing:-.03em;margin:0 0 16px;max-width:20ch;text-wrap:balance;font-variation-settings:"opsz" 96}}
.dek{{font-family:var(--disp);font-weight:300;font-size:clamp(20px,2.2vw,28px);margin:0 0 14px;max-width:34ch}}
.meta{{display:flex;gap:20px;flex-wrap:wrap;font-family:var(--disp);font-size:13px;color:var(--mute);margin:0 0 32px}}
.inset{{margin:0 0 clamp(28px,4vw,48px);max-width:860px}}
.inset img{{display:block;width:100%;height:auto;border-radius:4px;border:1px solid var(--rule)}}
.inset.bare img{{border:0;border-radius:0}}
.inset.two{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.inset figcaption{{grid-column:1/-1;font-family:var(--disp);font-size:12px;color:var(--mute);margin-top:8px}}
.prose{{max-width:64ch;font-size:18.5px;line-height:1.62;font-variation-settings:"opsz" 18}}
.prose p{{margin:0 0 1.15em;text-wrap:pretty}}
.prose h3{{font-family:var(--disp);font-weight:700;font-size:22px;letter-spacing:-.01em;margin:2em 0 .6em}}
.prose .pull{{margin:1.8em 0;padding:4px 0 4px 20px;border-left:4px solid var(--tint)}}
.prose .pull p{{font-family:var(--disp);font-weight:500;font-size:clamp(21px,2.2vw,27px);line-height:1.25;letter-spacing:-.015em;margin:0 0 8px}}
.prose .pull cite{{font-style:normal;font-family:var(--disp);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}}
.prose .photo{{margin:2em 0}}
.prose .photo.pair{{display:grid;grid-template-columns:1fr 1fr;gap:16px;max-width:none}}
.prose .photo.pair>div{{min-width:0}}
@media (max-width:640px){{.prose .photo.pair{{grid-template-columns:1fr}}}}
.prose .photo img{{display:block;width:100%;height:auto;border-radius:4px;border:1px solid var(--rule)}}
.prose .photo figcaption{{font-family:var(--disp);font-size:12.5px;color:var(--mute);margin-top:8px;line-height:1.5}}
.prose .note{{font-family:var(--disp);font-size:14px;color:var(--mute);background:var(--rail);padding:14px 16px;border-radius:4px;margin:2em 0}}
.prose .qa{{font-family:var(--disp);font-weight:700;font-size:20px;letter-spacing:-.01em;margin:1.8em 0 .6em}}
.prose .ans b{{font-family:var(--disp);font-weight:700;font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--tint);margin-right:.4em}}
.colophon{{max-width:1100px;margin:clamp(56px,8vw,112px) auto 0;padding-block:32px 64px;border-top:1px solid var(--rule);font-family:var(--disp);font-size:13px;line-height:1.6;color:var(--mute)}}
a:focus-visible{{outline:2px solid var(--fg);outline-offset:3px}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
@media (max-width:900px){{
  .app{{grid-template-columns:1fr}}
  .rail{{position:sticky;top:env(safe-area-inset-top,0px);height:auto;border-right:0;border-bottom:1px solid var(--rule);padding:12px max(16px,env(safe-area-inset-right,0px)) 12px max(16px,env(safe-area-inset-left,0px));gap:10px;z-index:5}}
  body::before{{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--rail)}}
  .rail .brand{{font-size:16px}} .rail .brand small{{display:none}}
  .rail nav{{flex-direction:row;overflow-x:auto;gap:14px;scrollbar-width:none}}
  .rail nav a,.rail nav a:last-child{{border:0;padding:4px 0;grid-template-columns:8px auto;white-space:nowrap}}
  .rail nav a .pg{{display:none}} .rail nav a .sw{{height:14px;width:8px}}
  .rail .epi{{display:none}}
  .pages{{padding-left:max(16px,env(safe-area-inset-left,0px))}}
  .inset.two{{grid-template-columns:1fr}}
}}
</style>
<div class="app">
<aside class="rail">
  <p class="brand">The American Bahá'í<small>{SUB}<br>{esc(ISSUE["date"])}</small></p>
  <nav aria-label="Features">{rail}</nav>
  <p class="epi">“{esc(ISSUE["epigraph"])}”<cite>{esc(ISSUE["epigraph_src"])}</cite></p>
</aside>
<main class="pages">
<header class="cover">
  <div>
    <h1>Six features from the arts issue</h1>
    <p class="about"><b>About this issue.</b> {esc(ISSUE["about"])}</p>
  </div>
  <figure><div class="mat"><img src="img/cover-paint.jpg" alt="Oil painting by Juliet Bogan: two figures in a flowering meadow look toward terraced green farmland and ochre mountains under a pale sky"></div><figcaption>Cover painting by {esc(ISSUE["cover_artist"])} · Oil on canvas</figcaption></figure>
</header>
{"".join(arts)}
<footer class="colophon">{esc(ISSUE["publisher"])}<br>Feature texts transcribed from the printed issue.</footer>
</main>
</div>
'''

for name, fn in [("folio", build_folio), ("plates", build_plates), ("reader", build_reader)]:
    with open(os.path.join(OUT, f"{name}.html"), "w") as f: f.write(fn())
print("ok")

# ---------------------------------------------------------------- GitHub Pages site
SITE = os.path.join(HERE, "site")
def standalone(body):
    body = body.replace(SIDES, "").replace('src="img/', 'src="../img/')
    body = body.replace("</style>\n", "</style>\n</head>\n<body>\n" if False else "</style>\n", 1)
    i = body.rfind("</style>")
    i = body.index("\n", i) + 1
    body = body[:i] + "</head>\n<body>\n" + body[i:]
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}</style>\n'
            + body + '\n</body>\n</html>\n')
for d, fn in [("folio", build_folio), ("plates", build_plates), ("reader", build_reader)]:
    os.makedirs(os.path.join(SITE, d), exist_ok=True)
    with open(os.path.join(SITE, d, "index.html"), "w") as f: f.write(standalone(fn()))
os.makedirs(os.path.join(SITE, "img"), exist_ok=True)
import shutil
for f in os.listdir(os.path.join(OUT, "img")): shutil.copy(os.path.join(OUT, "img", f), os.path.join(SITE, "img", f))
open(os.path.join(SITE, ".nojekyll"), "w").close()
LANDING = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>The American Bahá'í</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Libre+Caslon+Display&family=Public+Sans:wght@400;600&display=swap">
<style>
:root{{--paper:#f5f1e8;--ink:#1d1a16;--mute:#6a635a;--rule:#d9d2c4;--accent:#1b5e6b}}
@media (prefers-color-scheme:dark){{:root{{--paper:#15130f;--ink:#efe9dd;--mute:#a39b8e;--rule:#2f2a22;--accent:#7fc0c9;color-scheme:dark}}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--paper);color:var(--ink);font-family:"Libre Caslon Display",Georgia,serif;line-height:1.4}}
main{{max-width:1100px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:clamp(40px,8vw,96px)}}
.the{{font-size:clamp(18px,2.2vw,26px);margin:0 0 -.2em .1em}}
h1{{font-weight:400;font-size:clamp(52px,10vw,132px);line-height:.95;letter-spacing:-.015em;margin:0}}
.sub{{font-style:italic;font-size:clamp(18px,2.2vw,28px);margin:14px 0 0 .1em}}
.date{{font-family:"Public Sans",Arial,sans-serif;font-size:13px;letter-spacing:.06em;color:var(--mute);margin:28px 0 48px}}
ol{{list-style:none;margin:0;padding:0;border-top:1px solid var(--rule);display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));}}
li{{border-bottom:1px solid var(--rule)}}
li a{{display:block;padding:28px 0;color:inherit;text-decoration:none;padding-right:24px}}
li a:hover h2,li a:focus-visible h2{{color:var(--accent)}}
li a:focus-visible{{outline:2px solid var(--accent);outline-offset:4px}}
.v{{font-family:"Public Sans",Arial,sans-serif;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--mute)}}
h2{{font-weight:400;font-size:32px;margin:8px 0 10px;letter-spacing:-.01em}}
li p{{margin:0;font-family:"Public Sans",Arial,sans-serif;font-size:14px;line-height:1.55;color:var(--mute);max-width:40ch}}
footer{{margin-top:48px;font-family:"Public Sans",Arial,sans-serif;font-size:13px;color:var(--mute);max-width:60ch;line-height:1.6}}
</style>
</head>
<body>
<main>
<p class="the">The</p>
<h1>American Bahá'í</h1>
<p class="sub">{SUB}</p>
<p class="date">{esc(ISSUE["date"])} · Cover painting by {esc(ISSUE["cover_artist"])}</p>
<ol>
<li><a href="folio/"><span class="v">Version one</span><h2>Folio</h2><p>The issue as one long scroll: masthead over the painting, an index, six features on their art plates, quotation bands between them.</p></a></li>
<li><a href="plates/"><span class="v">Version two</span><h2>Plates</h2><p>A dark gallery: each feature's illustration hung as a numbered plate, headlines in Bodoni italic, text in one lit column.</p></a></li>
<li><a href="reader/"><span class="v">Version three</span><h2>Reader</h2><p>A reading app: a color-tabbed rail on the left, grotesque headlines and book-weight serif on the right.</p></a></li>
</ol>
<footer>{esc(ISSUE["publisher"])}</footer>
</main>
</body>
</html>
'''
with open(os.path.join(SITE, "index.html"), "w") as f: f.write(LANDING)
print("site ok")
