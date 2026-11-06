import html, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import ISSUE, VOICES, ARTICLES
SUB = "A U.S. Bah\u00e1\u2019\u00ed News Service publication"

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
        elif k == "img":
            w = b[3] if len(b) > 3 else None
            cls = "photo small" if w else "photo"
            st = f' style="--w:{w}px"' if w else ""
            out.append(f'<figure class="{cls}"{st}><img src="img/{b[1]}" alt="{esc(b[2])}" loading="lazy"><figcaption>{esc(b[2])}</figcaption></figure>')
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
                if a.get("art_width"): cls += " capped"
                art = f'''<figure class="{cls}" style="--aw:{a.get("art_width",0)}px"><img src="img/{a["art"]}" alt="{esc(a["art_alt"])}"><figcaption>{esc(a["art_credit"])}</figcaption></figure>'''
        else:
            art = '<div class="numeral" aria-hidden="true">50</div>'
        dek = f'<p class="dek">{esc(a["dek"])}</p>' if a.get("dek") else ""
        by = f'<p class="by">{esc(a["byline"])}</p>' if a.get("byline") else ""
        blooms = '<div class="blooms" aria-hidden="true"><i></i><i></i><i></i></div>' if a["slug"] == "newyorkers" else ""
        secs.append(f'''<article class="story" id="{a["slug"]}">{blooms}
  {art}
  <header class="shead">
    <h2>{esc(a["title"])}</h2>
    {dek}
  </header>
  <aside class="margin">
    <p class="kicker">{esc(a["kicker"])}</p>
    {by}
    <p class="pp">Pages {a["pages"]}</p>
  </aside>
  <div class="prose">{first_para_dropcap(body_html(a["body"]))}</div>
</article>''')
        if i < len(VOICES):
            v = VOICES[i]
            secs.append(f'''</div><aside class="voice" style="--band:{bands[i % len(bands)]}"><div class="vin"><p>{esc(v[0])}</p><cite>{esc(v[1])}</cite></div></aside><div class="wrap">''')
    head = "".join(f'<a href="#{a["slug"]}">{esc(a["short"])}<span class="pg">{a["pages"].split("–")[0]}</span></a>' for a in ARTICLES)
    index = "".join(f'<li><a href="#{a["slug"]}"><span class="t">{esc(a["title"])}</span><span class="pg">{a["pages"].split("–")[0]}</span></a></li>' for a in ARTICLES)
    return f'''<title>{esc(ISSUE["title"])} Folio</title>
{SIDES}
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,300..800&family=Literata:ital,opsz,wght@0,7..72,300..700;1,7..72,300..700&display=swap">
<style>
/* Layout: one long folio. The cover painting carries a set masthead; an index follows; each feature opens on its art plate and runs in a single measure with a margin column for pull quotes; between features, a colored band carries one passage from the issue's pages on the arts. */
:root{{
  --paper:#f5f1e8; --ink:#1d1a16; --mute:#6a635a; --rule:#d9d2c4; --accent:#1b5e6b; --cream:#f7f2ea;
  --disp:"Bricolage Grotesque","Helvetica Neue",Arial,sans-serif; --text:"Literata",Georgia,serif; --ui:"Bricolage Grotesque","Helvetica Neue",Arial,sans-serif;
}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--paper:#15130f;--ink:#efe9dd;--mute:#a39b8e;--rule:#2f2a22;--accent:#7fc0c9;--cream:#1c1915;color-scheme:dark}}}}
:root[data-theme="dark"]{{--paper:#15130f;--ink:#efe9dd;--mute:#a39b8e;--rule:#2f2a22;--accent:#7fc0c9;--cream:#1c1915;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--paper);color:var(--ink);font-family:var(--text);font-size:18px;line-height:1.55}}
.wrap{{max-width:1180px;margin:0 auto;{GUT}}}
.ui{{font-family:var(--ui);font-size:12px;letter-spacing:.12em;text-transform:uppercase}}
/* motion: terraces behind the open right third; brush strokes under the masthead on load; watercolor blooms in the New Yorkers margin. All off under reduced motion. */
.terraces{{position:fixed;top:0;right:0;bottom:0;width:30%;z-index:0;pointer-events:none;opacity:.32;filter:blur(44px) saturate(.85)}}
.terraces i{{position:absolute;left:-20%;right:-20%;height:34%;border-radius:50% 50% 40% 40%/60% 60% 40% 40%;animation:drift 28s ease-in-out infinite alternate}}
.terraces i:nth-child(1){{top:-12%;background:linear-gradient(90deg,#d9742a,#e9a21f);animation-duration:32s}}
.terraces i:nth-child(2){{top:22%;background:#5f8f3a;animation-delay:-8s}}
.terraces i:nth-child(3){{top:50%;background:#2f6a4a;animation-delay:-16s;animation-duration:36s}}
.terraces i:nth-child(4){{top:78%;background:#b7d35a;animation-delay:-4s}}
@keyframes drift{{from{{transform:translate(-3%,0) rotate(-1.2deg)}}to{{transform:translate(3%,-2%) rotate(1.2deg)}}}}
main,.head{{position:relative;z-index:1}}
.mast{{position:relative}}
.stroke{{position:absolute;left:-2%;top:38%;width:min(760px,80%);height:90px;z-index:-1;pointer-events:none}}
.stroke path{{fill:none;stroke:#b7d35a;stroke-width:34;stroke-linecap:round;opacity:.5;stroke-dasharray:900;stroke-dashoffset:900;animation:paint 2.6s cubic-bezier(.5,0,.2,1) .4s forwards}}
.stroke path+path{{stroke:#e9a21f;stroke-width:22;animation-delay:1.1s;opacity:.45}}
@keyframes paint{{to{{stroke-dashoffset:0}}}}
.story{{position:relative}}
.blooms{{position:absolute;left:0;top:34%;width:22%;height:46%;z-index:0;pointer-events:none;filter:blur(30px);opacity:.42}}
.blooms i{{position:absolute;width:70%;aspect-ratio:1;border-radius:50%;mix-blend-mode:multiply;animation:bloom 22s ease-in-out infinite alternate}}
.blooms i:nth-child(1){{left:0;top:0;background:#f05a7e}}
.blooms i:nth-child(2){{left:30%;top:32%;background:#2448c8;animation-delay:-7s;animation-duration:27s}}
.blooms i:nth-child(3){{left:5%;top:60%;background:#f3c623;animation-delay:-13s}}
@keyframes bloom{{from{{transform:scale(.9)}}to{{transform:scale(1.15) translate(6%,-6%)}}}}
.story>*{{position:relative;z-index:1}}
@media (prefers-reduced-motion:reduce){{.terraces i,.blooms i{{animation:none}}.stroke path{{animation:none;stroke-dashoffset:0}}}}
@media (max-width:980px){{.terraces,.blooms{{display:none}}}}
/* running head */
body::before{{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--paper)}}
.head{{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:color-mix(in oklab,var(--paper) 92%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--rule)}}
.head .in{{max-width:1180px;margin:0 auto;{GUT}display:flex;align-items:baseline;gap:32px;min-height:48px;font-family:var(--disp)}}
.head .brand{{font-size:18px;font-weight:700;letter-spacing:-.02em;color:var(--ink);text-decoration:none;white-space:nowrap;margin-right:auto}}
.head nav{{display:flex;gap:26px;overflow-x:auto;scrollbar-width:none;padding:10px 0}}
.head nav a{{font-family:var(--text);font-style:italic;font-size:18px;color:var(--ink);text-decoration:none;white-space:nowrap;border-bottom:1px solid transparent;padding-bottom:2px}}
.head nav a.on{{border-bottom-color:var(--ink)}}
.head nav a:hover,.head nav a:focus-visible{{color:var(--accent)}}
.head .pg{{font-family:var(--ui);font-size:11px;letter-spacing:.1em;color:var(--mute);margin-left:6px;font-style:normal}}
@media (max-width:700px){{.head .brand{{display:none}} .head nav{{gap:18px}} .head .pg{{display:none}}}}
/* cover */
.cover{{padding-block:clamp(28px,5vw,64px) 0}}
.cover .mast .the{{font-family:var(--disp);font-weight:500;font-size:clamp(18px,2.2vw,26px);margin:0 0 -.1em .05em}}
.cover h1{{font-family:var(--disp);font-size:clamp(56px,11vw,150px);line-height:.9;margin:0;letter-spacing:-.04em;font-weight:800;font-variation-settings:"opsz" 96}}
.cover .sub{{font-family:var(--text);font-size:clamp(18px,2.2vw,28px);margin:14px 0 0 .05em;font-style:italic;font-weight:300}}
.cover .line{{display:flex;flex-wrap:wrap;gap:8px 32px;margin-top:24px;font-family:var(--ui);font-size:13px;letter-spacing:.06em;color:var(--mute)}}
.painting{{margin:clamp(28px,4vw,48px) auto 0;width:fit-content;max-width:100%;border:1px solid var(--rule);background:var(--cream);padding:clamp(10px,1.4vw,18px)}}
.painting .mat{{border:1px solid var(--rule)}}
.painting img{{display:block;width:auto;max-width:100%;height:auto;max-height:96vh}}
.painting figcaption{{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;font-family:var(--ui);font-size:12px;letter-spacing:.06em;color:var(--mute);padding:12px 2px 0}}
/* front matter */
.front{{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:48px clamp(32px,6vw,96px);padding-block:clamp(40px,7vw,96px);border-bottom:1px solid var(--rule)}}
.front h2{{font-family:var(--disp);font-size:clamp(32px,4vw,52px);font-weight:800;margin:0 0 20px;letter-spacing:-.03em}}
.index{{list-style:none;margin:0;padding:0;border-top:1px solid var(--rule)}}
.index a{{display:flex;justify-content:space-between;gap:16px;align-items:baseline;padding:14px 0;border-bottom:1px solid var(--rule);color:inherit;text-decoration:none;font-family:var(--text);font-style:italic;font-size:22px;line-height:1.25;font-weight:300}}
.index a:hover .t,.index a:focus-visible .t{{color:var(--accent)}}
.index .pg{{font-family:var(--ui);font-size:13px;color:var(--mute);font-variant-numeric:tabular-nums}}
.epi p{{font-family:var(--text);font-style:italic;font-weight:300;font-size:clamp(22px,2.4vw,30px);line-height:1.3;margin:0 0 12px;text-wrap:pretty}}
.epi cite{{font-style:normal;font-family:var(--ui);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--mute)}}
.about{{margin-top:36px;color:var(--mute);font-size:16px}}
.about b{{color:var(--ink);font-weight:700}}
/* stories */
.story{{padding-block:clamp(48px,8vw,112px) 0}}
.plate{{margin:0 0 clamp(28px,4vw,48px);background:var(--cream);border:1px solid var(--rule)}}
.plate img{{display:block;width:100%;height:auto;max-height:78vh;object-fit:cover}}
.plate.capped{{max-width:var(--aw);margin-left:auto;margin-right:auto}}
.plate.bare{{background:transparent;border:0}}
.plate.bare img{{max-height:none;object-fit:contain;max-width:1000px}}
.plate.bare figcaption{{padding-left:0}}
.plate.comic{{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--rule)}}
.plate.comic img{{max-height:none;background:#fff}}
.plate.comic figcaption{{grid-column:1/-1;background:var(--cream)}}
.plate figcaption{{font-family:var(--ui);font-size:12px;letter-spacing:.06em;color:var(--mute);padding:10px 14px}}
.numeral{{font-family:var(--disp);font-weight:800;font-size:clamp(160px,28vw,360px);line-height:.8;color:var(--accent);margin:0 0 .05em -.03em;letter-spacing:-.06em}}
/* article grid: a 3-column field. Margin column at left holds kicker, byline, pages; the headline spans the field; prose sits in the middle column with air on both sides; pull quotes hang into the left margin, photographs span margin and text. */
.story{{display:grid;grid-template-columns:minmax(140px,1fr) minmax(0,66ch) minmax(0,1fr);column-gap:clamp(24px,4vw,64px)}}
.story>.plate,.story>.numeral{{grid-column:1/-1}}
.shead{{grid-column:1/-1;margin:0 0 clamp(40px,6vw,88px)}}
.shead h2{{font-family:var(--disp);font-size:clamp(44px,7vw,104px);line-height:.92;font-weight:700;letter-spacing:-.035em;font-variation-settings:"opsz" 96;margin:0 0 22px;text-wrap:balance;max-width:14ch}}
.dek{{font-family:var(--disp);font-weight:300;font-size:clamp(20px,2vw,28px);margin:0;color:var(--mute);max-width:34ch}}
.margin{{grid-column:1;grid-row:3;font-family:var(--ui);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--mute);line-height:1.6;align-self:start}}
.margin p{{margin:0}}
.kicker{{color:var(--accent);font-weight:600;margin-bottom:10px!important}}
.by::before{{content:"By ";}}
.pp{{margin-top:10px!important;font-variant-numeric:tabular-nums}}
.prose{{grid-column:1/-1;display:grid;grid-template-columns:subgrid;column-gap:inherit;font-size:18.5px;line-height:1.62;font-variation-settings:"opsz" 18}}
.prose>*{{grid-column:2;min-width:0}}
.prose p{{margin:0 0 1.25em;text-wrap:pretty}}
.prose p.first{{font-size:1.14em;line-height:1.5}}
.prose p.first::first-letter{{font-family:var(--disp);font-weight:700;font-size:4.2em;float:left;line-height:.8;padding:.06em .1em 0 0;color:var(--accent)}}
.prose h3{{font-family:var(--ui);font-weight:600;font-size:13px;letter-spacing:.14em;text-transform:uppercase;margin:3.2em 0 1em;color:var(--accent);padding-top:1.2em;border-top:1px solid var(--rule)}}
.prose .pull{{grid-column:1;grid-row:span 2;margin:.4em 0 2em;padding:0 0 0 18px;border-left:3px solid var(--accent);align-self:start}}
.prose .pull p{{font-family:var(--disp);font-weight:500;font-size:clamp(20px,1.9vw,26px);line-height:1.22;letter-spacing:-.015em;margin:0 0 10px}}
.prose .pull cite{{font-style:normal;font-family:var(--ui);font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--mute)}}
.prose .photo{{grid-column:1/-1;margin:2.4em 0;display:grid;grid-template-columns:subgrid;column-gap:inherit;align-items:end}}
.prose .photo>img{{grid-column:1/-1}}
.prose .photo>figcaption{{grid-column:1;grid-row:2;margin-top:10px}}
.prose .photo.small{{grid-column:2;display:block;max-width:var(--w)}}
.prose .photo.small>figcaption{{margin-top:10px}}
.prose .photo.pair{{grid-column:1/-1;grid-template-columns:1fr 1fr;gap:20px;align-items:start}}
.prose .photo.pair>div{{grid-column:auto}}
.prose .photo.pair>div{{min-width:0}}
@media (max-width:640px){{.prose .photo.pair{{grid-template-columns:1fr}}}}
.prose .photo img{{display:block;width:100%;height:auto;border:1px solid var(--rule)}}
.prose .photo figcaption{{font-family:var(--ui);font-size:12.5px;letter-spacing:.02em;color:var(--mute);margin-top:8px;line-height:1.5}}
.prose .note{{font-family:var(--ui);font-size:15px;color:var(--mute);border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:14px 0;margin:2em 0}}
.prose .qa{{font-family:var(--disp);font-weight:700;font-size:20px;letter-spacing:-.01em;margin-top:1.8em}}
.prose .ans b{{font-family:var(--ui);font-weight:600;font-size:14px;letter-spacing:.06em;text-transform:uppercase;color:var(--accent);margin-right:.4em}}
/* voices */
.voice{{background:var(--band);color:#f7f2ea;margin-top:clamp(48px,8vw,112px)}}
.voice+.wrap .story{{padding-top:clamp(48px,8vw,112px)}}
.vin{{max-width:1180px;margin:0 auto;{GUT}padding-block:clamp(40px,6vw,80px)}}
.voice p{{font-family:var(--text);font-style:italic;font-weight:300;font-size:clamp(22px,2.6vw,34px);line-height:1.3;max-width:34ch;margin:0 0 18px;text-wrap:pretty}}
.voice cite{{font-style:normal;font-family:var(--ui);font-size:12px;letter-spacing:.12em;text-transform:uppercase;opacity:.8}}
.colophon{{padding-block:clamp(48px,8vw,96px);font-family:var(--ui);font-size:13px;color:var(--mute);max-width:60ch;line-height:1.6;border-top:1px solid var(--rule);margin-top:clamp(48px,8vw,112px)}}
a:focus-visible{{outline:2px solid var(--accent);outline-offset:3px}}
@media (max-width:980px){{
  .story{{grid-template-columns:minmax(0,1fr)}}
  .shead,.margin,.prose{{grid-column:1}}
  .margin{{grid-row:auto;position:static;display:flex;gap:18px;flex-wrap:wrap;margin-bottom:28px}}
  .margin .kicker,.margin .pp{{margin:0!important}}
  .prose{{display:block}}
  .prose .pull{{margin:1.6em 0}}
  .prose .photo{{display:block}}
  .prose .photo.pair{{display:grid;grid-template-columns:1fr 1fr}}

  .front{{grid-template-columns:1fr}}
  .prose .pull{{margin-left:0}}
  .plate.comic{{grid-template-columns:1fr}}
}}
</style>
<div class="head"><div class="in"><a class="brand" href="#top">The American Bahá'í</a><nav aria-label="Features">{head}</nav></div></div>
<div class="terraces" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
<header class="cover wrap" id="top">
  <div class="mast">
    <svg class="stroke" viewBox="0 0 720 90" preserveAspectRatio="none" aria-hidden="true"><path d="M20 55 C 160 20, 300 80, 440 45 S 640 30, 700 50"/><path d="M40 70 C 200 40, 380 90, 560 55 S 660 50, 690 62"/></svg>
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
<script>
(function(){{
  var links=[].slice.call(document.querySelectorAll('.head nav a'));
  var secs=[].slice.call(document.querySelectorAll('article.story'));
  if(!('IntersectionObserver' in window))return;
  var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(!e.isIntersecting)return;
    links.forEach(function(a){{a.classList.toggle('on',a.getAttribute('href')==='#'+e.target.id)}});}});}},{{rootMargin:'-30% 0px -60% 0px'}});
  secs.forEach(function(x){{io.observe(x)}});
}})();
</script>
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
                plate = f'<div class="img{" bare" if a.get("art_transparent") else ""}{" capped" if a.get("art_width") else ""}" style="--aw:{a.get("art_width",0)}px"><img src="img/{a["art"]}" alt="{esc(a["art_alt"])}"></div>'
        else:
            plate = '<div class="img type"><span>50</span></div>'
        dek = f'<p class="dek">{esc(a["dek"])}</p>' if a.get("dek") else ""
        by = f'<p class="by">{esc(a["byline"])}</p>' if a.get("byline") else ""
        pal = {"gregory":("#f26b2b","#2448c8","#f05a7e","#f3c623"),"newyorkers":("#2448c8","#f05a7e","#f3c623","#5f8f3a"),"twoartists":("#b07a4a","#e9a21f","#2f6a4a","#f26b2b"),"abs":("#c9462c","#1b5e6b","#e9a21f","#2448c8"),"endeavor":("#e9a21f","#1b5e6b","#9ec3cc","#f26b2b"),"comic":("#f3c623","#2448c8","#f26b2b","#5f8f3a")}[a["slug"]]
        torn = f'<div class="torn" aria-hidden="true" style="--a:{pal[0]};--b:{pal[1]};--c:{pal[2]};--d:{pal[3]}"><i></i><i></i><i></i><i></i></div>'
        chapters.append(f'''<section class="chapter" id="{a["slug"]}">
  <div class="plate">
    {plate}
    <div class="cap"><span class="n">Plate {n}</span><span>{esc(a["art_credit"] or "Set in type")}</span><span>pp. {a["pages"]}</span></div>
  </div>
  <header class="chead">{torn}
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
.bar nav{{display:flex;gap:26px;margin-left:auto}}
.bar nav a{{font-family:var(--disp);font-style:italic;font-size:17px;letter-spacing:.01em;color:var(--dim);text-decoration:none;white-space:nowrap;padding:6px 0;font-variation-settings:"opsz" 24}}
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
.plate .img.capped{{padding:clamp(16px,3vw,48px) 0}}
.plate .img.capped img{{max-width:var(--aw)}}
.plate .img.bare{{background:var(--card);padding:clamp(16px,3vw,48px)}}
.plate .img.bare img{{max-width:1100px}}
.plate .img.two{{grid-template-columns:1fr 1fr;gap:2px;background:var(--rule)}}
.plate .img.two img{{max-height:none;background:#fff}}
.plate .img.type{{min-height:40vh}}
.plate .img.type span{{font-family:var(--disp);font-style:italic;font-size:clamp(180px,32vw,440px);line-height:.8;color:var(--gold);font-variation-settings:"opsz" 96}}
.cap{{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;font-family:var(--mono);font-size:12px;color:var(--dim);padding:12px 2px 0}}
.cap .n{{color:var(--gold)}}
/* motion: torn paper behind each headline, in the story's palette, settling slowly; cover letters lean from the cursor. */
.chead{{max-width:1000px;margin:clamp(32px,5vw,64px) auto 0;position:relative}}
.chead>*{{position:relative;z-index:1}}
.torn{{position:absolute;inset:-10% -4% -10% 40%;z-index:0!important;pointer-events:none;opacity:.22}}
.torn i{{position:absolute;animation:settle 20s ease-in-out infinite alternate}}
.torn i:nth-child(1){{right:6%;top:-6%;width:44%;height:70%;background:var(--a);clip-path:polygon(4% 0,96% 6%,100% 60%,88% 100%,10% 94%,0 40%);animation-delay:-3s}}
.torn i:nth-child(2){{right:30%;top:30%;width:38%;height:60%;background:var(--b);clip-path:polygon(0 12%,80% 0,100% 50%,92% 100%,18% 96%,4% 60%);animation-delay:-9s;animation-duration:24s}}
.torn i:nth-child(3){{right:0;bottom:-4%;width:26%;height:46%;background:var(--c);clip-path:polygon(10% 0,100% 10%,90% 100%,0 86%);animation-delay:-14s}}
.torn i:nth-child(4){{right:48%;top:0;width:16%;aspect-ratio:1;height:auto;background:var(--d);border-radius:50%;animation-duration:16s}}
@keyframes settle{{from{{transform:translate(0,0) rotate(0)}}to{{transform:translate(-1.5%,1.5%) rotate(1.5deg)}}}}
.cover h1 span{{display:inline-block;transition:transform .5s cubic-bezier(.2,.8,.2,1)}}
.cover h1 span.sp{{width:.22em}}
@media (prefers-reduced-motion:reduce){{.torn i{{animation:none}}.cover h1 span{{transition:none}}}}
@media (max-width:860px){{.torn{{display:none}}}}
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
@media (min-width:1000px){{.prose .photo.pair{{width:calc(100% + 14rem);margin-left:-7rem}}}}
@media (max-width:640px){{.prose .photo.pair{{grid-template-columns:1fr}}}}
.prose .photo.small{{max-width:calc(var(--w) + 20px)}}
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
<script>
(function(){{
  if(matchMedia('(prefers-reduced-motion: reduce)').matches||!matchMedia('(hover: hover)').matches)return;
  var h=document.querySelector('.cover h1'); if(!h)return;
  var out=[]; h.childNodes.forEach(function(n){{
    var tag=n.nodeType===1?n.tagName.toLowerCase():null; var txt=n.textContent;
    txt.split('').forEach(function(ch){{var s=document.createElement('span');if(ch===' '){{s.className='sp';s.innerHTML='&nbsp;'}}else s.textContent=ch; if(tag){{var w=document.createElement(tag);w.appendChild(s);out.push(w)}}else out.push(s);}});
  }});
  h.textContent=''; out.forEach(function(x){{h.appendChild(x)}});
  var spans=[].slice.call(h.querySelectorAll('span'));
  h.addEventListener('mousemove',function(e){{spans.forEach(function(s){{var r=s.getBoundingClientRect();var dx=(r.left+r.width/2)-e.clientX;var k=Math.max(-1,Math.min(1,dx/180));s.style.transform='rotate('+(k*-5)+'deg) translateY('+(Math.abs(k)*-4)+'px)';}});}});
  h.addEventListener('mouseleave',function(){{spans.forEach(function(s){{s.style.transform=''}});}});
}})();
</script>
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
                art = f'<figure class="inset{" bare" if a.get("art_transparent") else ""}" style="max-width:{a.get("art_width") or 860}px"><img src="img/{a["art"]}" alt="{esc(a["art_alt"])}"><figcaption>{esc(a["art_credit"])}</figcaption></figure>'
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
    rail = "".join(f'<a href="#{a["slug"]}" style="--tint:{tints[a["slug"]]}"><span>{esc(a["short"])}</span><i class="fill"></i></a>' for a in ARTICLES)
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
body::before{{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--rail)}}
.tabs{{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--rail);border-bottom:1px solid var(--rule)}}
.tabs .in{{max-width:1100px;margin:0 auto;{GUT}display:flex;align-items:stretch;gap:0;overflow-x:auto;scrollbar-width:none}}
.tabs .brand{{font-family:var(--disp);font-weight:700;font-size:17px;letter-spacing:-.02em;color:var(--fg);text-decoration:none;white-space:nowrap;align-self:center;margin-right:28px}}
.tabs .brand small{{display:block;font-weight:400;font-size:11px;color:var(--mute);letter-spacing:.02em}}
.tabs nav{{display:flex;margin-left:auto}}
.tabs nav a{{display:flex;align-items:flex-end;padding:18px 16px 0;border-bottom:4px solid var(--tint);color:var(--fg);text-decoration:none;font-family:var(--disp);font-weight:600;font-size:15px;letter-spacing:-.01em;white-space:nowrap}}
.tabs nav a span{{padding-bottom:12px}}
/* motion: the current tab's underline fills as the story is read; a thin dark line slides between tabs. */
.tabs nav a .fill{{position:absolute;left:0;bottom:-4px;height:4px;width:0;background:var(--fg);opacity:.9;transition:width .4s cubic-bezier(.2,.8,.2,1)}}
.tabs nav a{{position:relative}}
.tabs nav a.on .fill{{width:var(--p,0%)}}
.tabs .ind{{position:absolute;bottom:-1px;height:2px;background:var(--fg);transition:left .5s cubic-bezier(.2,.8,.2,1),width .5s cubic-bezier(.2,.8,.2,1)}}
.tabs .in{{position:relative}}
@media (prefers-reduced-motion:reduce){{.tabs nav a .fill,.tabs .ind{{transition:none}}}}
.tabs nav a.on{{background:var(--bg)}}
.tabs nav a:hover,.tabs nav a:focus-visible{{background:var(--bg)}}
.pages{{{GUT}}}
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
.prose .photo{{margin:2.4em 0;display:grid;grid-template-columns:minmax(0,1fr) 15ch;gap:14px 24px;align-items:end;max-width:none;width:min(58rem,calc(100vw - 32px))}}
.prose .photo>img{{display:block;width:100%;height:auto;border-radius:4px;grid-row:1;grid-column:1}}
.prose .photo.small{{grid-template-columns:minmax(0,var(--w)) 15ch;width:auto}}
.prose .photo>figcaption{{grid-column:2;grid-row:1;font-family:var(--disp);font-size:13px;line-height:1.5;color:var(--mute);padding-top:10px;border-top:3px solid var(--tint);align-self:end}}
.prose .photo>figcaption::before{{content:"Photograph";display:block;font-size:11px;letter-spacing:.12em;text-transform:uppercase;font-weight:700;color:var(--tint);margin-bottom:6px}}
.prose .photo.pair{{grid-template-columns:1fr 1fr;gap:22px;align-items:start;width:min(66rem,calc(100vw - 32px))}}
.prose .photo.pair>div{{min-width:0}}
.prose .photo.pair>div img{{display:block;width:100%;height:auto;border-radius:4px}}
.prose .photo.pair>div figcaption{{font-family:var(--disp);font-size:13px;line-height:1.5;color:var(--mute);margin-top:10px;padding-top:10px;border-top:3px solid var(--tint)}}
@media (max-width:640px){{.prose .photo,.prose .photo.pair{{grid-template-columns:1fr}} .prose .photo>figcaption{{grid-column:1;grid-row:2}}}}
.prose .note{{font-family:var(--disp);font-size:14px;color:var(--mute);background:var(--rail);padding:14px 16px;border-radius:4px;margin:2em 0}}
.prose .qa{{font-family:var(--disp);font-weight:700;font-size:20px;letter-spacing:-.01em;margin:1.8em 0 .6em}}
.prose .ans b{{font-family:var(--disp);font-weight:700;font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--tint);margin-right:.4em}}
.colophon{{max-width:1100px;margin:clamp(56px,8vw,112px) auto 0;padding-block:32px 64px;border-top:1px solid var(--rule);font-family:var(--disp);font-size:13px;line-height:1.6;color:var(--mute)}}
a:focus-visible{{outline:2px solid var(--fg);outline-offset:3px}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
@media (max-width:900px){{
  .tabs .brand small{{display:none}}
  .tabs nav{{margin-left:0}}
  .tabs nav a{{padding:14px 12px 0;font-size:14px}}
  .inset.two{{grid-template-columns:1fr}}
}}
</style>
<div class="tabs"><div class="in"><a class="brand" href="#top">The American Bahá'í<small>{SUB}</small></a><nav aria-label="Features">{rail}</nav><span class="ind" aria-hidden="true"></span></div></div>
<main class="pages" id="top">
<header class="cover">
  <div>
    <h1>Six features from the arts issue</h1>
    <p class="about"><b>About this issue.</b> {esc(ISSUE["about"])}</p>
  </div>
  <figure><div class="mat"><img src="img/cover-paint.jpg" alt="Oil painting by Juliet Bogan: two figures in a flowering meadow look toward terraced green farmland and ochre mountains under a pale sky"></div><figcaption>Cover painting by {esc(ISSUE["cover_artist"])} · Oil on canvas</figcaption></figure>
</header>
{"".join(arts)}
<footer class="colophon">{esc(ISSUE["publisher"])}<br>Feature texts transcribed from the printed issue.<br>“{esc(ISSUE["epigraph"])}” {esc(ISSUE["epigraph_src"])}</footer>
</main>
<script>
(function(){{
  var links=[].slice.call(document.querySelectorAll('.tabs nav a'));
  var secs=[].slice.call(document.querySelectorAll('article.story'));
  var ind=document.querySelector('.tabs .ind'), inn=document.querySelector('.tabs .in');
  var cur=null;
  function place(a){{if(!a||!ind)return;var r=a.getBoundingClientRect(),b=inn.getBoundingClientRect();ind.style.left=(r.left-b.left+inn.scrollLeft)+'px';ind.style.width=r.width+'px';}}
  function progress(){{if(!cur)return;var a=links.filter(function(l){{return l.getAttribute('href')==='#'+cur.id}})[0];if(!a)return;
    var r=cur.getBoundingClientRect();var top=r.top+scrollY, h=r.height;var p=(scrollY+innerHeight*0.4-top)/h;p=Math.max(0,Math.min(1,p));a.style.setProperty('--p',(p*100).toFixed(1)+'%');}}
  if('IntersectionObserver' in window){{
    var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(!e.isIntersecting)return;cur=e.target;
      links.forEach(function(a){{var on=a.getAttribute('href')==='#'+e.target.id;a.classList.toggle('on',on);if(on)place(a);}});progress();}});}},{{rootMargin:'-30% 0px -60% 0px'}});
    secs.forEach(function(x){{io.observe(x)}});
  }}
  addEventListener('scroll',progress,{{passive:true}}); addEventListener('resize',function(){{place(document.querySelector('.tabs nav a.on'))}});
}})();
</script>
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
