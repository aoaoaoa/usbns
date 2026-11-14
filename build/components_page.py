"""/magazine/components/: the design system of The American Bahá'í as a reference page, built from ds_tokens.json
(the Claude Design system synced from this repository) and the components the site actually uses."""
import json, os, html, re, shutil
D = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(D, "ds_tokens.json")))
OUT = os.path.join(D, "site", "magazine", "components")
ICONS = "/home/claude/usbns/build/icons"
e = html.escape

cols = T["color"]["tokens"]
def val(t, th): v = t["value"]; return v if isinstance(v, str) else v.get(th, v.get("light"))
light = ";".join(f"--{t['name']}:{val(t,'light')}" for t in cols)
dark = ";".join(f"--{t['name']}:{val(t,'dark')}" for t in cols if isinstance(t["value"], dict))
fam = T["type"]["families"]
fams = ";".join(f"--font-{k}:{v}" for k, v in fam.items())
sp = ";".join(f"--{t['name']}:{t['value']}" for t in T["spacing"]["tokens"])
rd = ";".join(f"--{t['name']}:{t['value']}" for t in T["radius"]["tokens"])

def lum(hx):
    hx = hx.lstrip("#"); r, g, b = (int(hx[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)
def ratio(a, b): la, lb = lum(a), lum(b); return (max(la, lb) + .05) / (min(la, lb) + .05)

TINTS = [("tint-endeavor", "Across America", "Communities engage in a common endeavor"), ("tint-gregory", "Race amity", "The Louis Gregory Bahá’í Institute"),
         ("tint-newyorkers", "Community", "New Yorkers create more unified communities"), ("tint-twoartists", "In conversation", "Two artists reimagine the role of art"),
         ("tint-abs", "Scholarship", "Association for Bahá’í Studies at 50"), ("tint-comic", "Adventures in pioneering", "Sparkling spirits in Indianapolis")]
CH = [("colour", "Colour", "tint-endeavor", "Warm paper, dark ink, and one tint per feature that does the navigating."),
      ("type", "Type", "tint-gregory", "Bricolage Grotesque points the way; Literata carries the reading."),
      ("space", "Space and shape", "tint-newyorkers", "One column, a 16px gutter, square plates and rules, round only where a finger presses."),
      ("marks", "Icons", "tint-twoartists", "Interface glyphs and single-ink social glyphs."),
      ("components", "Components", "tint-abs", "The controls readers touch: buttons, the running head, forms and dialogs."),
      ("patterns", "Patterns", "tint-comic", "How a feature is set: the opener, the reading line, the voices and the close.")]

def chap(i, key, name, tint, dek):
    return (f'<section class="ch" id="{key}" style="--accent:var(--{tint})"><div class="wrap"><header class="chap"><span class="n">{i}</span>'
            f'<span class="k">{name}</span><span class="of">{i} of {len(CH)}</span></header><h2 class="hd">{name}</h2><p class="dk">{dek}</p>')

def code(s): return f'<code>{e(s)}</code>'
def spec(name, cls, body, note, wide=False):
    return (f'<article class="spec{" wide" if wide else ""}"><div class="stage">{body}</div><div class="sm"><h4>{name}</h4>'
            f'<p class="cls">{" ".join(code(c) for c in cls.split())}</p><p>{note}</p></div></article>')

# 1 colour
NEUT = ["paper", "cream", "bar", "tabon", "tabon-white", "ink", "mute", "rule", "barrule", "accent", "mem"]
bym = {t["name"]: t for t in cols}
sw = ""
for n in NEUT:
    t = bym[n]; l, d = val(t, "light"), val(t, "dark")
    sw += (f'<div class="sw"><div class="chip"><span style="background:{l}"></span><span style="background:{d}"></span></div>'
           f'<b>{n}</b><span class="hx">{l} <i>light</i> · {d} <i>dark</i></span><p>{e(t["usage"])}</p></div>')
tints = ""
for i, (n, k, s) in enumerate(TINTS):
    v = val(bym[n], "light"); r = ratio(v, "#f5f1e8")
    tints += (f'<div class="tt" style="--c:{v}"><span class="tn">{i + 1}</span><div><b>{n}</b><span class="hx">{v}</span>'
              f'<p class="tk">{k}</p><p>{s}</p><p class="cr">{r:.2f}:1 on light paper{"" if r >= 4.5 else ": numerals, rules and fills only"}</p></div></div>')
bands = "".join(f'<div class="bd" style="background:var(--band-{i})"><b>band-{i}</b><span>{val(bym[f"band-{i}"],"light")}</span></div>' for i in range(1, 7))

# 2 type
typ = ""
for g in T["type"]["groups"]:
    typ += f'<h3 class="sub">{g["name"]} <small>{e(fam[g["family"]].split(",")[0].strip(chr(34)))} · var(--font-{g["family"]})</small></h3>'
    for s in g["styles"]:
        size = s["fontSize"]; px = float(size.rstrip("px"))
        shown = min(px, 96) if g["name"] == "Display" else px
        st = (f'font-family:var(--font-{g["family"]});font-size:{shown}px;line-height:{s["lineHeight"]};font-weight:{s["fontWeight"]};'
              f'letter-spacing:{s.get("letterSpacing","normal")};font-style:{s.get("fontStyle","normal")}')
        if s["name"] in ("label", "subhead"): st += ";text-transform:uppercase"
        if s["name"] == "subhead": st += ";color:var(--accent)"
        if s["name"] in ("dek", "caption", "label", "cover-sub"): st += ";color:var(--mute)"
        sample = {"masthead": "American Bahá’í", "chapter-numeral": "1 2 3", "story-headline": "A common endeavor", "dek": "From music and visual art to creative practices",
                  "qa": "What does the community gain from the arts?", "brand": "The American Bahá’í", "prose": "In the months since the National Spiritual Assembly shared “A Common Endeavor,” Bahá’ís across the country have been creating opportunities to introduce the message.",
                  "body": "The American Bahá’í is the national magazine of the U.S. Bahá’í community.", "voice": "Neighboring has become a verb.", "index-entry": "Communities engage in a common endeavor",
                  "pull-quote": "And they may be small, but they motivate others and they’re important.", "cover-sub": "A U.S. Bahá’í News publication", "nav-tab": "A common endeavor",
                  "popup": "Hemingway, South Carolina · Race amity", "button": "Share this story", "subhead": "Rutland, Vermont", "label": "Across America · Print pages 12–15",
                  "caption": "Quilt art by Helen Butler, from her original work"}.get(s["name"], "The American Bahá’í")
        meta = f'{size} / {s["lineHeight"]} · {s["fontWeight"]}' + (f' · {s["letterSpacing"]}' if s.get("letterSpacing") else "") + (" · italic" if s.get("fontStyle") else "")
        typ += (f'<div class="ty"><div class="tym"><b>{s["name"]}</b><span>{meta}</span><p>{e(s["usage"])}</p></div>'
                f'<p class="tys" style="{st}">{sample}</p></div>')

# 3 space and shape
spc = "".join(f'<div class="spx"><span class="bar" style="width:{t["value"]}"></span><b>{t["name"]}</b><span class="hx">{t["value"]}</span><p>{e(t["usage"])}</p></div>'
              for t in T["spacing"]["tokens"] if t["name"] != "wrap-max")
wrap = [t for t in T["spacing"]["tokens"] if t["name"] == "wrap-max"][0]
rad = "".join(f'<div class="rx"><span class="shape" style="border-radius:{t["value"]}"></span><b>{t["name"]}</b><span class="hx">{t["value"]}</span><p>{e(t["usage"])}</p></div>'
              for t in T["radius"]["tokens"])

# 4 marks
def svgfile(n):
    s = open(os.path.join(ICONS, n)).read(); s = re.sub(r"<\?xml.*?\?>", "", s)
    return re.sub(r"<svg", '<svg aria-hidden="true"', s, count=1)
soc = "".join(f'<div class="ic"><span>{svgfile(n)}</span><b>{n[:-4]}</b></div>' for n in ["facebook.svg", "instagram.svg", "linkedin.svg", "x-twitter.svg", "youtube.svg"])
GLY = {"share": '<path d="M12 3v12M7.5 7.5 12 3l4.5 4.5M5 12v7.5h14V12"/>', "play": '<path d="M8 5.5v13l11-6.5z"/>', "pause": '<path d="M8 5v14M16 5v14"/>',
       "key": '<circle cx="8" cy="12" r="4"/><path d="M12 12h9M18 12v3M21 12v2"/>', "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>', "close": '<path d="M6 6l12 12M18 6 6 18"/>'}
def g(n, sz=24): return f'<svg viewBox="0 0 24 24" width="{sz}" height="{sz}" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{GLY[n]}</svg>'
gly = "".join(f'<div class="ic"><span>{g(n)}</span><b>{n}</b></div>' for n in GLY)

# 5 components
comp = "".join([
 spec("Subscribe", "hsub", '<a class="x-hsub" href="#components">Subscribe</a>', "The one filled button in the running head. Navy on paper; on phones it shrinks to 34px tall."),
 spec("Members key", "hkey", f'<a class="x-hkey" href="#components" aria-label="Members">{g("key", 18)}</a>', "Beside Subscribe. Opens the members sign-in; its label shows on hover and to screen readers."),
 spec("Send a story", "sbtn", f'<a class="x-sbtn" href="#components">Send a story {g("arrow", 18)}</a>', "The call to contribute, the same words on every page. Condensed capitals, square corners."),
 spec("Share this story", "sharebtn", f'<button type="button" class="x-share">{g("share", 18)}<span>Share this story</span></button>', "A pill in the margin column, hairline border, ink text. radius-pill."),
 spec("Listen to this story", "listen", f'<button type="button" class="x-listen"><span class="d">{g("play", 18)}</span><span><b>Listen to this story</b><small>7 min read</small></span></button>', "A disc in the story tint with the time beneath. radius-disc."),
 spec("Add to calendar", "gcal", '<a class="x-gcal" href="#components">Add to calendar</a>', "Small outlined pill in mem, under each date of the Rhythm of Bahá’í Life."),
 spec("Text link", "fgl", '<a class="x-fgl" href="#components">Read the field guide first</a>', "A quiet underlined link beside a button, never a second button."),
 spec("Running-head tabs", "rhd tabs", '<nav class="x-tabs"><a style="--u:var(--tint-gregory)">Louis Gregory</a><a style="--u:var(--tint-newyorkers)">New Yorkers</a><a class="on" style="--u:var(--tint-endeavor)">A common endeavor</a></nav>', "Each tab underlined 4px in its story tint; the current tab sits on tabon.", True),
 spec("Kicker and byline", "kicker-top", '<div class="x-margin"><p class="x-kick">Across America</p><p class="x-lab">By Linda Ahdieh Grant</p><p class="x-lab">Print pages 12–15</p></div>', "The margin column: kicker in the tint, labels in mute, uppercase, 0.12–0.14em."),
 spec("Pace", "dv", '<div class="x-dv" role="radiogroup" aria-label="Send me"><label><input type="radio" name="dvx"><span><b>One story</b><small>as each is published</small></span></label><label><input type="radio" name="dvx" checked><span><b>A few stories</b><small>two or three at a time</small></span></label><label><input type="radio" name="dvx"><span><b>The full issue</b><small>four to six stories</small></span></label></div>', "How much arrives at a time. The middle choice is preselected.", True),
 spec("Story field and drop zone", "dfl drop", '<div class="x-form"><label class="x-f"><span>Where</span><input placeholder="Town or neighborhood, state"></label><label class="x-drop"><input type="file" class="vh"><b>Choose photographs</b><small>JPEG or PNG, as many as you like</small></label></div>', "Fields on tabon-white with radius-field; the drop zone dashed until files are chosen.", True),
 spec("Checklist line", "grl", f'<ol class="x-grl"><li class="on"><span class="ck"></span><div><b>Say where and when</b><small>Town or neighborhood, state, and the date.</small></div></li><li><span class="ck"></span><div><b>Send originals</b><small>Full-size files, not screenshots.</small></div></li></ol>', "Ticks as the form fills; tapping a line lights the field it governs."),
 spec("Members sign-in", "mg", '<div class="x-dlg"><p class="x-mk">The full issue</p><label class="x-f"><span>Bahá’í ID number</span><input placeholder="9" inputmode="numeric"></label><p class="x-clue">Not quite. Look closely at the empty field.</p><button type="button" class="x-go">Sign in</button></div>', "A dialog on tabon-white, radius-dialog. The clue appears under the field after a miss."),
])

# 6 patterns
pat = "".join([
 spec("Chapter opener", "chap", '<header class="chap x"><span class="n">5</span><span class="k">Across America</span><span class="of">5 of 5</span></header><p class="x-head">Communities engage in a common endeavor</p>', "A 6px rule in the tint, the numeral in chapter-numeral, then the headline in story-headline.", True),
 spec("Prose subhead", "prose h3", '<div class="x-prose"><h5 class="x-sub">Rutland, Vermont: sharing at the Rotary Club</h5><p>In August, Alis Headlam, a Bahá’í, shared themes from “A Common Endeavor” with the Rutland City Rotary Club at its weekly meeting.</p></div>', "Uppercase, 13px, in the accent, under a hairline.", True),
 spec("Pull quote", "pull", '<blockquote class="x-pull"><p>And they may be small, but they motivate others and they’re important.</p><cite>Paula Siegel</cite></blockquote>', "In the margin beside the text, a 3px rule in the tint."),
 spec("Figure sentence", "figsent", '<p class="x-fig">One food program in Rutland serves <b>400+</b> people each week and gives out <b>2,000+</b> meals a month.</p>', "A sentence that carries its numbers, set large, figures in the tint."),
 spec("Plate and caption", "plate", '<figure class="x-plate"><img src="../img/story-paint.webp" alt="Children’s hands at a watercolor set beside paintings" loading="lazy"><figcaption>Crown Heights, Brooklyn · this issue</figcaption></figure>', "Art on cream, a hairline frame, square corners; the caption names who, where and when.", True),
 spec("Voice band", "band-1 … band-6", '<div class="x-band"><p>Neighboring has become a verb.</p><cite>Washington County, Minnesota</cite></div>', "A quoted passage on a band ground, in #f7f2ea type; the six grounds are used in order between features.", True),
 spec("The Writings", "ext sacred", '<blockquote class="x-sacred"><p>Regard man as a mine rich in gems of inestimable value. Education can, alone, cause it to reveal its treasures, and enable mankind to benefit therefrom.</p><cite>Bahá’u’lláh</cite></blockquote>', "Passages from the Writings on a lapis tint with a gilt rule; other quotations stay plain.", True),
 spec("Contents row", "index", '<ol class="x-index"><li><span>12</span><b>Communities engage in a common endeavor</b></li><li><span>16</span><b>Association for Bahá’í Studies at 50</b></li></ol>', "Print page number, then the title in index-entry, between hairlines.", True),
 spec("Next issue", "nxl", '<div class="x-nxl"><span class="x-k">Next issue</span><b>Education</b><span class="x-k">Winter 2027</span><a href="#patterns">Send a story →</a></div>', "Closes the issue and every story: the theme, the season, the call.", True),
 spec("Glide and return", "glide", '<div class="x-gl"><div class="x-glb"><a href="#gl-abs" data-gl>ABS at 50</a><a href="#gl-endeavor" data-gl>A common endeavor</a><button type="button" class="x-glk" disabled>← Back</button></div><div class="x-glv" tabindex="0" aria-label="A sample issue"><section id="gl-gregory" class="x-gls" style="--u:var(--tint-gregory)"><b>Louis Gregory</b><span></span><span></span><span></span></section><section id="gl-newyorkers" class="x-gls" style="--u:var(--tint-newyorkers)"><b>New Yorkers</b><span></span><span></span><span></span></section><section id="gl-twoartists" class="x-gls" style="--u:var(--tint-twoartists)"><b>Two artists</b><span></span><span></span><span></span></section><section id="gl-abs" class="x-gls" style="--u:var(--tint-abs)"><b>ABS at 50</b><span></span><span></span><span></span></section><section id="gl-endeavor" class="x-gls" style="--u:var(--tint-endeavor)"><b>A common endeavor</b><span></span><span></span><span></span></section></div></div>', 'In-page links move in two phases. Out: the page steps back, scale .94 and opacity .35 over 220ms, ease-in. The position changes while the page is away. In: it comes forward at the target over 340ms, cubic-bezier(.2,.8,.2,1). The target is measured again after the move, so images loading above it cannot push it off. Each jump is added to the history, so Back returns the reader to the place they left in one step. Readers who ask for reduced motion get a plain jump. Try a link, then Back.', wide=True),
])

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,300..800&family=Literata:ital,opsz,wght@0,7..72,300..800;1,7..72,300..600&family=Barlow+Condensed:wght@700&display=swap">'
CSS = """
:root{%(light)s;%(fams)s;%(sp)s;%(rd)s;--navy:#222e4c;--gilt:#c99a3e;--lapis:#23406f;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){%(dark)s;color-scheme:dark}}
:root[data-theme=dark]{%(dark)s;color-scheme:dark}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:72px}body{margin:0;background:var(--paper);color:var(--ink);font:18px/1.55 var(--font-text)}
a{color:inherit}.vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.wrap{max-width:var(--wrap-max);margin:0 auto;padding-left:max(var(--space-gutter),env(safe-area-inset-left,0px));padding-right:max(var(--space-gutter),env(safe-area-inset-right,0px))}
code{font:500 12.5px/1 ui-monospace,SFMono-Regular,Menlo,monospace;background:var(--bar);border:1px solid var(--rule);border-radius:var(--radius-sm);padding:3px 6px;color:var(--ink)}
/* running head */
.rh{position:sticky;top:0;z-index:20;background:var(--bar);border-bottom:1px solid var(--barrule)}.rh .wrap{display:flex;align-items:center;gap:18px;min-height:58px}
.rh .br{display:flex;align-items:center;gap:8px;font:700 17px var(--font-disp);letter-spacing:-.02em;text-decoration:none;white-space:nowrap}.rh .br svg{width:22px;height:22px}.rh .br small{font:600 11px var(--font-ui);letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}
.rh nav{display:flex;gap:4px;overflow-x:auto;scrollbar-width:none;flex:1;min-width:0}.rh nav a{font:600 14px var(--font-ui);letter-spacing:-.01em;text-decoration:none;padding:18px 10px 14px;border-bottom:4px solid transparent;white-space:nowrap}
.rh nav a:hover,.rh nav a.on{border-bottom-color:var(--u)}.rh nav a.on{background:var(--tabon)}
.tg{font:600 12px var(--font-ui);letter-spacing:.1em;text-transform:uppercase;border:1px solid var(--rule);background:none;color:var(--ink);border-radius:var(--radius-pill);padding:0 12px;min-height:34px;cursor:pointer;white-space:nowrap}
/* cover */
.cv{padding:clamp(28px,5vw,56px) 0 0}.strip{display:grid;grid-template-columns:288fr 240fr 112fr 96fr 112fr 96fr 224fr;height:clamp(56px,9vw,112px);overflow:hidden}
.strip i{display:block}.strip i:last-child{background:var(--ink);position:relative}.strip i:last-child span{position:absolute;left:18%%;top:-.12em;font:800 clamp(90px,15vw,200px)/1 var(--font-disp);letter-spacing:-.05em;color:var(--paper)}
.cv h1{margin:clamp(20px,3vw,32px) 0 0;font:800 clamp(56px,11vw,150px)/.9 var(--font-disp);letter-spacing:-.04em;font-variation-settings:"opsz" 96}
.cv .csub{margin:14px 0 0;font:italic 300 clamp(15px,1.5vw,20px) var(--font-text);color:var(--mute)}
.meta{display:flex;flex-wrap:wrap;gap:6px 18px;margin:18px 0 0;font:400 12px var(--font-ui);letter-spacing:.12em;text-transform:uppercase;color:var(--mute)}.meta b{color:var(--ink);font-weight:600}
.toc{list-style:none;margin:clamp(28px,4vw,44px) 0 0;padding:0;border-top:1px solid var(--rule);display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:32px}
.toc li{border-bottom:1px solid var(--rule)}.toc a{display:grid;grid-template-columns:40px 1fr;gap:12px;align-items:baseline;padding:12px 0;text-decoration:none}.toc span{font:800 22px var(--font-disp);color:var(--c)}.toc b{font:italic 300 22px/1.25 var(--font-text)}.toc small{display:block;grid-column:2;font:400 13px/1.45 var(--font-ui);color:var(--mute)}
/* chapters */
.ch{padding:clamp(56px,8vw,112px) 0 0}.chap{display:grid;grid-template-columns:auto 1fr auto;align-items:end;gap:6px 22px;border-top:6px solid var(--accent);padding-top:16px;font:600 12px var(--font-ui);letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}
.chap .n{font:800 clamp(64px,9vw,120px)/.78 var(--font-disp);letter-spacing:-.05em;color:var(--accent);text-transform:none}.chap .k{color:var(--ink)}
.hd{margin:22px 0 0;font:700 clamp(44px,7vw,84px)/.92 var(--font-disp);letter-spacing:-.035em;max-width:14ch;text-wrap:balance}
.dk{margin:16px 0 0;font:300 clamp(19px,1.8vw,24px)/1.5 var(--font-disp);color:var(--mute);max-width:46ch}
.sub{margin:44px 0 14px;padding-top:12px;border-top:1px solid var(--rule);font:600 13px var(--font-ui);letter-spacing:.14em;text-transform:uppercase;color:var(--accent)}.sub small{margin-left:10px;color:var(--mute);letter-spacing:.06em;text-transform:none;font-weight:400}
.hx{font:500 12px ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--mute)}.hx i{font-style:normal;opacity:.7}
/* colour */
.sws{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:22px}.sw b,.tt b,.spx b,.rx b,.ic b{display:block;font:600 14px var(--font-ui)}.sw p,.tt p,.spx p,.rx p{margin:4px 0 0;font:400 13px/1.45 var(--font-ui);color:var(--mute)}
.chip{display:grid;grid-template-columns:1fr 1fr;height:84px;border:1px solid var(--rule);margin-bottom:10px}
.tts{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:18px}.tt{display:grid;grid-template-columns:96px 1fr;gap:16px;border-top:6px solid var(--c);padding-top:12px}
.tn{font:800 96px/.8 var(--font-disp);letter-spacing:-.05em;color:var(--c)}.tt .tk{font:600 12px var(--font-ui)!important;letter-spacing:.14em;text-transform:uppercase;color:var(--ink)!important}.tt .cr{font-style:italic}
.bds{display:grid;grid-template-columns:repeat(6,minmax(0,1fr))}.bd{min-height:120px;padding:14px;color:#f7f2ea;display:flex;flex-direction:column;justify-content:flex-end;font:600 13px var(--font-ui)}.bd span{font:500 11.5px ui-monospace,Menlo,monospace;opacity:.85}
/* type */
.fams{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}.fm{border:1px solid var(--rule);background:var(--bar);padding:18px}.fm .aa{font-size:84px;line-height:1}.fm b{display:block;margin-top:10px;font:600 14px var(--font-ui)}.fm span{font:400 13px var(--font-ui);color:var(--mute)}
.ty{display:grid;grid-template-columns:240px minmax(0,1fr);gap:24px;padding:18px 0;border-top:1px solid var(--rule);align-items:baseline}.tym b{display:block;font:600 14px var(--font-ui)}.tym span{font:500 12px ui-monospace,Menlo,monospace;color:var(--mute)}.tym p{margin:6px 0 0;font:400 12.5px/1.45 var(--font-ui);color:var(--mute)}
.tys{margin:0;min-width:0;overflow-wrap:anywhere;text-wrap:balance}
/* space */
.spxs{display:grid;gap:16px;max-width:760px}.spx{display:grid;grid-template-columns:120px 150px 1fr;gap:14px;align-items:center}.spx .bar{display:block;height:24px;background:var(--accent);opacity:.85}.spx p{grid-column:3}
.ruler{position:relative;margin:28px 0 0;height:44px;border:1px solid var(--rule);border-top:0;display:flex;align-items:flex-end;justify-content:center;font:500 12px ui-monospace,Menlo,monospace;color:var(--mute);padding-bottom:6px}
.rxs{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:22px}.rx .shape{display:block;width:84px;height:84px;background:var(--cream);border:2px solid var(--accent);margin-bottom:10px}
/* glide */
.x-gl{width:100%%;display:grid;gap:10px}.x-glb{display:flex;flex-wrap:wrap;gap:8px;align-items:center}.x-glb a,.x-glk{font:600 13px var(--ui);color:var(--ink);text-decoration:none;border:1px solid var(--rule);background:var(--bar);border-radius:999px;padding:0 14px;min-height:36px;display:inline-flex;align-items:center;cursor:pointer}.x-glk{margin-left:auto}.x-glk:disabled{opacity:.4;cursor:default}.x-glv{height:260px;overflow:auto;border:1px solid var(--rule);background:var(--bar);padding:14px;position:relative}.x-gls{min-height:220px;border-top:4px solid var(--u);padding:12px 0 18px;display:grid;gap:8px;align-content:start}.x-gls b{font:700 19px var(--text)}.x-gls span{display:block;height:9px;border-radius:2px;background:var(--rule)}.x-gls span:nth-of-type(2){width:80%%}.x-gls span:nth-of-type(3){width:60%%}
/* marks */
.mk{display:grid;grid-template-columns:auto 1fr;gap:32px;align-items:center}.mk .big{width:clamp(120px,18vw,200px);height:auto}.apps{display:flex;gap:18px;align-items:flex-end;flex-wrap:wrap}.apps img{border-radius:22%%;border:1px solid var(--rule)}
.ics{display:grid;grid-template-columns:repeat(auto-fill,minmax(96px,1fr));gap:14px}.ic{border:1px solid var(--rule);background:var(--bar);padding:16px 10px;text-align:center}.ic span{display:inline-flex;width:28px;height:28px;color:var(--ink)}.ic span svg{width:100%%;height:100%%;fill:currentColor}.ic span svg[fill=none]{fill:none}.ic b{margin-top:8px;font-weight:500;font-size:12.5px}
/* specs */
.specs{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px}.spec{border:1px solid var(--rule);background:var(--bar);display:grid;grid-template-rows:1fr auto;min-width:0}.spec.wide{grid-column:1/-1}
.stage{padding:clamp(20px,3vw,36px);background:var(--paper);border-bottom:1px solid var(--rule);display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:150px;min-width:0}.spec.wide .stage{align-items:flex-start}.stage>*{max-width:100%%;min-width:0}
.sm{padding:14px 18px 16px}.sm h4{margin:0;font:700 16px var(--font-disp)}.sm p{margin:6px 0 0;font:400 13.5px/1.45 var(--font-ui);color:var(--mute)}.sm .cls{display:flex;flex-wrap:wrap;gap:6px}
.x-hsub{display:inline-flex;align-items:center;min-height:40px;padding:0 18px;border-radius:6px;background:var(--navy);color:#fff;font:700 13px var(--font-ui);letter-spacing:.14em;text-transform:uppercase;text-decoration:none}
.x-hkey{display:inline-flex;width:40px;height:40px;align-items:center;justify-content:center;border:1px solid var(--rule);border-radius:50%%;color:var(--mute)}.x-hkey:hover{color:var(--ink);border-color:var(--ink)}
.x-sbtn{display:inline-flex;align-items:center;gap:10px;font:700 19px/1 "Barlow Condensed","Arial Narrow",sans-serif;letter-spacing:.04em;text-transform:uppercase;text-decoration:none;background:var(--navy);color:#f2cfc6;padding:14px 24px;border-radius:var(--radius-btn)}
.x-share{display:inline-flex;align-items:center;gap:8px;min-height:40px;padding:0 14px 0 10px;border:1px solid var(--rule);border-radius:var(--radius-pill);background:transparent;color:var(--ink);font:400 13px var(--font-ui);cursor:pointer}
.x-listen{display:grid;grid-template-columns:44px 1fr;gap:2px 12px;align-items:center;background:none;border:0;padding:0;color:var(--ink);cursor:pointer;text-align:left;font:400 14px var(--font-ui)}.x-listen .d{width:44px;height:44px;border-radius:var(--radius-disc);background:var(--accent);color:#fff;display:grid;place-items:center}.x-listen b{display:block;font-weight:600}.x-listen small{color:var(--mute);font-size:12.5px}
.x-gcal{font:600 11.5px var(--font-ui);color:var(--mem);text-decoration:none;border:1px solid currentColor;border-radius:var(--radius-pill);padding:4px 10px}
.x-fgl{font:600 14px var(--font-ui);text-decoration:underline;text-underline-offset:4px}
.x-tabs{display:flex;gap:2px;background:var(--bar);border-bottom:1px solid var(--barrule);overflow-x:auto;max-width:100%%}.x-tabs a{font:600 15px var(--font-ui);letter-spacing:-.01em;padding:16px 12px 12px;border-bottom:4px solid var(--u);white-space:nowrap}.x-tabs a.on{background:var(--tabon)}
.x-margin{font-family:var(--font-ui)}.x-kick{margin:0 0 10px;font:600 12px var(--font-ui);letter-spacing:.14em;text-transform:uppercase;color:var(--accent)}.x-lab{margin:4px 0 0;font:400 12px var(--font-ui);letter-spacing:.12em;text-transform:uppercase;color:var(--mute)}
.x-dv{display:flex;flex-wrap:wrap;gap:8px}.x-dv input{position:absolute;opacity:0}.x-dv span{display:block;border:1px solid var(--rule);background:var(--tabon-white);border-radius:var(--radius-sm);padding:10px 14px;font:400 12px/1.35 var(--font-ui);color:var(--mute);cursor:pointer;text-align:center}.x-dv b{display:block;font-size:13.5px;color:var(--ink)}.x-dv input:checked+span{border:2px solid var(--ink);padding:9px 13px}.x-dv input:focus-visible+span{outline:2px solid var(--accent);outline-offset:2px}
.x-form{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;width:100%%;max-width:720px}.x-f{display:grid;gap:6px;font:600 13px var(--font-ui);text-align:left}.x-f input{width:100%%;min-width:0;font:16px var(--font-text);padding:12px 14px;border:1px solid var(--rule);border-radius:var(--radius-field);background:var(--tabon-white);color:var(--ink);min-height:46px}
.x-drop{display:grid;place-items:center;gap:2px;border:1.5px dashed var(--rule);border-radius:var(--radius-field);padding:14px;font:400 13px var(--font-ui);color:var(--mute);cursor:pointer}.x-drop b{color:var(--ink)}
.x-grl{list-style:none;margin:0;padding:0;width:100%%;max-width:340px}.x-grl li{display:grid;grid-template-columns:22px 1fr;gap:10px;padding:9px 0;border-top:1px solid var(--rule);font:13px/1.4 var(--font-ui)}.x-grl b{display:block;font-size:14px}.x-grl small{color:var(--mute)}.x-grl .ck{width:18px;height:18px;border:1.5px solid var(--rule);border-radius:50%%;margin-top:1px}.x-grl .on .ck{background:var(--accent);border-color:var(--accent);box-shadow:inset 0 0 0 3px var(--bar)}
.x-dlg{width:min(320px,100%%);background:var(--tabon-white);border-radius:var(--radius-dialog);padding:24px 22px 20px;text-align:center;box-shadow:0 20px 50px -24px rgba(0,0,0,.45);display:grid;gap:8px}.x-star{display:block;width:30px;height:30px;margin:0 auto;color:var(--gilt)}.x-star svg{width:100%%;height:100%%}
.x-mk{margin:0;font:700 11px var(--font-ui);letter-spacing:.16em;text-transform:uppercase;color:var(--mem)}.x-mh{margin:0;font:700 26px var(--font-text)}.x-dlg .x-f input{text-align:center;font:600 22px var(--font-ui);letter-spacing:.2em}.x-dlg .x-f input::placeholder{color:var(--gilt);opacity:1}
.x-clue{margin:0;font:italic 14px var(--font-text);color:#9a5a1e}.x-go{font:700 13px var(--font-ui);letter-spacing:.12em;text-transform:uppercase;background:var(--navy);color:#fff;border:0;border-radius:6px;min-height:44px;cursor:pointer}
:root[data-theme=dark] .x-clue{color:#e2b072}@media (prefers-color-scheme:dark){:root:not([data-theme=light]) .x-clue{color:#e2b072}}
.chap.x{width:100%%}.x-head{margin:18px 0 0;font:700 clamp(40px,6vw,72px)/.92 var(--font-disp);letter-spacing:-.035em;max-width:14ch;text-wrap:balance}
.x-prose{max-width:62ch}.x-sub{margin:0 0 12px;padding-top:12px;border-top:1px solid var(--rule);font:600 13px var(--font-ui);letter-spacing:.14em;text-transform:uppercase;color:var(--accent)}.x-prose p{margin:0;font:400 19.5px/1.6 var(--font-text)}
.x-pull{margin:0;padding-left:18px;border-left:3px solid var(--accent);max-width:26ch}.x-pull p{margin:0;font:500 24px/1.24 var(--font-disp);letter-spacing:-.01em}.x-pull cite{display:block;margin-top:10px;font:400 12px var(--font-ui);letter-spacing:.12em;text-transform:uppercase;color:var(--mute);font-style:normal}
.x-fig{margin:0;font:400 24px/1.45 var(--font-text);max-width:30ch}.x-fig b{font-weight:600;font-size:1.55em;line-height:1;color:var(--accent)}
.x-plate{margin:0;width:100%%;max-width:560px;background:var(--cream);border:1px solid var(--rule)}.x-plate img{display:block;width:100%%;height:auto}.x-plate figcaption{padding:var(--space-cap) var(--space-cap-x);font:400 12px var(--font-ui);letter-spacing:.06em;color:var(--mute)}
.x-band{width:100%%;background:var(--band-1);color:#f7f2ea;padding:clamp(28px,4vw,48px);animation:band 18s steps(6) infinite}.x-band p{margin:0;font:600 clamp(24px,2.8vw,38px)/1.36 var(--font-text);letter-spacing:-.01em}.x-band cite{display:block;margin-top:12px;font:400 12px var(--font-ui);letter-spacing:.12em;text-transform:uppercase;font-style:normal;opacity:.85}
@keyframes band{0%%{background:var(--band-1)}16.6%%{background:var(--band-2)}33.3%%{background:var(--band-3)}50%%{background:var(--band-4)}66.6%%{background:var(--band-5)}83.3%%{background:var(--band-6)}}
.x-sacred{margin:0;width:100%%;max-width:720px;background:color-mix(in oklab,var(--lapis) 9%%,transparent);border-left:3px solid var(--gilt);padding:16px 22px}.x-sacred p{margin:0;font:italic 400 19.5px/1.6 var(--font-text)}.x-sacred cite{display:block;margin-top:8px;font:400 12px var(--font-ui);letter-spacing:.12em;text-transform:uppercase;font-style:normal;color:var(--mute)}
.x-index{list-style:none;margin:0;padding:0;width:100%%;max-width:720px;border-top:2px solid var(--ink)}.x-index li{display:grid;grid-template-columns:48px 1fr;gap:12px;align-items:baseline;padding:12px 0;border-bottom:1px solid var(--rule)}.x-index span{font:800 24px var(--font-disp);color:var(--accent)}.x-index b{font:italic 300 22px/1.25 var(--font-text)}
.x-nxl{display:flex;flex-wrap:wrap;align-items:baseline;gap:8px 16px;width:100%%;border-top:2px solid var(--ink);padding-top:12px;font-family:var(--font-ui)}.x-k{font:600 11px var(--font-ui);letter-spacing:.16em;text-transform:uppercase;color:var(--mute)}.x-nxl b{font:700 22px var(--font-disp)}.x-nxl a{margin-left:auto;font:600 14px var(--font-ui)}
/* footer */
.colo{margin-top:clamp(64px,9vw,120px);background:var(--navy);color:#f5f1e8;padding:36px 0 40px}.colo .wrap{display:flex;flex-wrap:wrap;gap:14px 28px;align-items:center;justify-content:space-between;font:400 13px var(--font-ui)}.colo a{color:#f5f1e8}.colo b{font:700 17px var(--font-disp)}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}.x-band{animation:none}}
@media (max-width:860px){.toc,.specs,.fams{grid-template-columns:minmax(0,1fr)}.ty{grid-template-columns:minmax(0,1fr);gap:8px}.spx{grid-template-columns:90px 1fr}.spx p{grid-column:1/-1}.bds{grid-template-columns:repeat(3,minmax(0,1fr))}.mk{grid-template-columns:minmax(0,1fr)}.x-form{grid-template-columns:minmax(0,1fr)}.rh .br span{display:none}.tt{grid-template-columns:64px 1fr}.tn{font-size:64px}}
""" % dict(light=light, dark=dark, fams=fams, sp=sp, rd=rd)

toc = "".join(f'<li><a href="#{k}" style="--c:var(--{t})"><span>{i + 1}</span><b>{n}</b><small>{d}</small></a></li>' for i, (k, n, t, d) in enumerate(CH))
navs = "".join(f'<a href="#{k}" style="--u:var(--{t})">{n}</a>' for k, n, t, d in CH)
FAMS = "".join(f'<div class="fm"><div class="aa" style="font-family:var(--font-{k});font-weight:{w}{";font-style:italic" if k == "text" else ""}">Aa</div><b>{e(v.split(",")[0].strip(chr(34)))}</b><span>var(--font-{k}) · {u}</span></div>'
               for k, v, w, u in [("disp", fam["disp"], 800, "headlines, numerals, masthead"), ("text", fam["text"], 300, "reading, deks, quotations"), ("ui", fam["ui"], 600, "labels, buttons, navigation")])
n_styles = sum(len(g["styles"]) for g in T["type"]["groups"])
page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="robots" content="noindex">
<title>Components · The American Bahá’í</title><link rel="icon" href="../favicon.svg">{FONTS}<style>{CSS}</style></head><body>
<header class="rh"><div class="wrap"><a class="br" href="../landing/"><span>The American Bahá’í</span><small>Components</small></a><nav aria-label="Sections">{navs}</nav><button type="button" class="tg" aria-pressed="false">Dark</button></div></header>
<main>
<section class="cv"><div class="wrap"><div class="strip" aria-hidden="true"><i style="background:var(--tint-endeavor)"></i><i style="background:var(--tint-gregory)"></i><i style="background:var(--tint-newyorkers)"></i><i style="background:var(--tint-twoartists)"></i><i style="background:var(--tint-abs)"></i><i style="background:var(--tint-comic)"></i><i><span>1</span></i></div>
<h1>Components</h1><p class="csub">The design system of The American Bahá’í</p>
<ol class="toc">{toc}</ol></div></section>
{chap(1, *CH[0])}<h3 class="sub">Grounds, ink and rules <small>each swatch: light theme left, dark right</small></h3><div class="sws">{sw}</div>
<h3 class="sub">Story tints <small>set as --accent on each feature; the same in both themes</small></h3><div class="tts">{tints}</div>
<h3 class="sub">Voice bands <small>band-1 to band-6, used in order in the full edition, type in #f7f2ea</small></h3><div class="bds">{bands}</div></div></section>
{chap(2, *CH[1])}<div class="fams">{FAMS}</div>{typ}</div></section>
{chap(3, *CH[2])}<h3 class="sub">Spacing</h3><div class="spxs">{spc}</div><div class="ruler">wrap-max · {wrap["value"]}: {e(wrap["usage"])}</div>
<h3 class="sub">Radius <small>plates and rules stay square</small></h3><div class="rxs">{rad}</div></div></section>
{chap(4, *CH[3])}<h3 class="sub">Interface glyphs <small>24px, 1.8 stroke, round caps, currentColor</small></h3><div class="ics">{gly}</div>
<h3 class="sub">Social <small>single ink, footer</small></h3><div class="ics">{soc}</div></div></section>
{chap(5, *CH[4])}<div class="specs">{comp}</div></div></section>
{chap(6, *CH[5])}<div class="specs" style="--accent:var(--tint-endeavor)">{pat}</div></div></section>
</main>
<footer class="colo"><div class="wrap"><b>The American Bahá’í</b><span>Tokens synced from aoaoaoa/usbns. Story tints keep their color in both themes.</span><span><a href="../landing/">The magazine</a></span></div></footer>
<script>(function(){{var G=document.querySelector('.x-gl');if(!G)return;var V=G.querySelector('.x-glv'),K=G.querySelector('.x-glk'),st=[],rm=matchMedia('(prefers-reduced-motion: reduce)').matches;function glide(to){{if(rm){{V.scrollTop=to;return}}var kids=[].slice.call(V.children);kids.forEach(function(k){{k.style.transition='transform .22s ease-in,opacity .22s';k.style.transformOrigin='50% '+(V.scrollTop+V.clientHeight/2-k.offsetTop)+'px';k.style.transform='scale(.94)';k.style.opacity='.35'}});setTimeout(function(){{kids.forEach(function(k){{k.style.transition='none'}});V.scrollTop=to;kids.forEach(function(k){{k.style.transformOrigin='50% '+(V.scrollTop+V.clientHeight/2-k.offsetTop)+'px';k.style.transform='scale(.94)';k.offsetWidth;k.style.transition='transform .34s cubic-bezier(.2,.8,.2,1),opacity .34s';k.style.transform='';k.style.opacity=''}})}},230)}}[].forEach.call(G.querySelectorAll('[data-gl]'),function(a){{a.addEventListener('click',function(e){{e.preventDefault();var t=document.getElementById(a.getAttribute('href').slice(1));st.push(V.scrollTop);K.disabled=false;glide(t.offsetTop-V.firstElementChild.offsetTop)}})}});K.addEventListener('click',function(){{if(!st.length)return;V.scrollTop=st.pop();K.disabled=!st.length}})}})();</script><script>(function(){{var H=document.documentElement,b=document.querySelector('.tg');function cur(){{var t=H.getAttribute('data-theme');return t||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light')}}
function show(){{var c=cur();b.textContent=c==='dark'?'Light':'Dark';b.setAttribute('aria-pressed',c==='dark')}}
try{{var s=localStorage.getItem('tab-ds-theme');if(s)H.setAttribute('data-theme',s)}}catch(e){{}}show();
b.onclick=function(){{var n=cur()==='dark'?'light':'dark';H.setAttribute('data-theme',n);try{{localStorage.setItem('tab-ds-theme',n)}}catch(e){{}}show()}};
var A=[].slice.call(document.querySelectorAll('.rh nav a'));var io=new IntersectionObserver(function(es){{es.forEach(function(x){{if(x.isIntersecting)A.forEach(function(a){{a.classList.toggle('on',a.getAttribute('href')==='#'+x.target.id)}})}})}},{{rootMargin:'-30% 0px -60% 0px'}});
[].forEach.call(document.querySelectorAll('.ch'),function(s){{io.observe(s)}});
[].forEach.call(document.querySelectorAll('.stage a[href^="#"]'),function(a){{a.addEventListener('click',function(e){{e.preventDefault()}})}})}})();</script>
</body></html>'''
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, "index.html"), "w").write(page)
print("ok", len(page))
