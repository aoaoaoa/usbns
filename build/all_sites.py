"""All Sites: the bahai.us network menu, cloned in structure and look. A slim network bar above the page, trigger at the top right; the panel slides in from the right."""
import re, os
HERE = os.path.dirname(os.path.abspath(__file__))
GRID = '<svg class="asg" viewBox="0 0 20 20" aria-hidden="true">' + "".join(f'<rect x="{x}" y="{y}" width="5" height="5" rx=".6"/>' for y in (0, 7.5, 15) for x in (0, 7.5, 15)) + '</svg>'
STARP = "M24 2.5l4.6 8 8.7-3.2-1.6 9.1 8.6 3.2-7.1 6 4.6 8-9.2.1-1.6 9.1L24 36.7l-7 5.9-1.6-9.1-9.2-.1 4.6-8-7.1-6 8.6-3.2-1.6-9.1 8.7 3.2z"
HOLE = " M24 13.5l2.7 4.6 5-1.8-.9 5.2 4.9 1.8-4 3.4 2.6 4.6-5.3.1-.9 5.2L24 37l-4 3.4-.9-5.2-5.3-.1 2.6-4.6-4-3.4 4.9-1.8-.9-5.2 5 1.8z"
def star(a, b, sid):
    return (f'<svg viewBox="0 0 48 48" aria-hidden="true"><defs><linearGradient id="{sid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient></defs>'
            f'<path fill="url(#{sid})" fill-rule="evenodd" d="{STARP}{HOLE}"/></svg>')
TEMPLE = ('<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M24 4a20 20 0 0 0 0 40z" fill="#2f5a3a"/><g fill="none" stroke="#2f5a3a" stroke-width="1.6">'
          '<path d="M24 8c6 3 9 8 9 14M24 8v4M27 13v4M30 17v5"/><path d="M24 22h12M24 26h13M24 30h14M24 34h14"/><path d="M27 26v8M31 26v8M35 26v8"/></g></svg>')
def tabstar():
    s = open(os.path.join(HERE, "site", "magazine", "favicon.svg")).read() if os.path.exists(os.path.join(HERE, "site", "magazine", "favicon.svg")) else open("/home/claude/usbns/magazine/favicon.svg").read()
    s = re.sub(r"<\?xml.*?\?>", "", s).replace("<svg", '<svg aria-hidden="true"', 1)
    return re.sub(r'(id="|url\(#)([A-Za-z0-9_-]+)', lambda m: m.group(1) + m.group(2) + "-as", s)

def item(name, desc, href, icon="", here=False):
    tgt = "" if here else ' target="_blank" rel="noopener"'
    ic = f'<span class="asi">{icon}</span>' if icon else ""
    return f'<li{" class=here" if here else ""}><a href="{href}"{tgt}{" aria-current=page" if here else ""}>{ic}<span class="ast"><b>{name}</b><span>{desc}</span></span></a></li>'
def group(label, items): return f'<section class="asgp"><h3>{label}</h3><ul>{"".join(items)}</ul></section>'

def body(here_href):
    US = [item("bahai.us", "The official site of the Bahá’ís of the United States", "https://www.bahai.us/", star("#e3c46a", "#b8892f", "as-g")),
          item("The American Bahá’í", "The national magazine of the U.S. Bahá’í community", here_href, tabstar(), here=True),
          item("Bahá’í House of Worship", "The Mother Temple of the West, in Wilmette, Illinois", "https://www.bahai.us/bahai-temple-welcome/", TEMPLE),
          item("Office of Public Affairs", "The Bahá’í Office of Public Affairs, Washington, D.C.", "https://www.bahai.us/public-affairs/", star("#9b3a2c", "#5a1a16", "as-m"))]
    ADD = [item("Bahá’í Member Services", "Records, contributions and letters, for enrolled members", "https://www.bahai.us/community"),
           item("brilliantstarmagazine.org", "Brilliant Star, the magazine for children and families", "https://brilliantstarmagazine.org/"),
           item("bahaibookstore.com", "The U.S. Bahá’í Bookstore: books, prayer books, gifts", "https://www.bahaibookstore.com/"),
           item("Centers of learning", "Green Acre, Louhelen, Bosch and the Wilmette Institute", "https://www.bahai.us/resources/#Centers-of-Learning"),
           item("bahai.org", "The worldwide Bahá’í community", "https://www.bahai.org/"),
           item("news.bahai.org", "The Bahá’í World News Service", "https://news.bahai.org/")]
    return group("Bahá’í US sites", US) + group("Additional sites", ADD)

TITLE = "Selected National Bahá’í US Websites &amp; Other Resources"
CSS = r"""
.asbar{background:#fff;border-bottom:1px solid #e5e5e5;position:relative;z-index:2}
.asbar .asin{display:flex;align-items:center;justify-content:flex-end;gap:12px;min-height:40px;padding-left:max(32px,env(safe-area-inset-left,0px));padding-right:max(26px,env(safe-area-inset-right,0px))}
.asbar .asn{font:600 12px/1 "Source Sans 3","Source Sans Pro",system-ui,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:#6b6b6b;text-decoration:none}
.ast-btn{display:inline-flex;align-items:center;gap:9px;background:none;border:0;padding:4px 6px;margin-right:-6px;cursor:pointer;color:#4a4a4a;font:600 12.5px/1 "Source Sans 3","Source Sans Pro",system-ui,sans-serif;letter-spacing:.12em;text-transform:uppercase;min-height:36px}
.ast-btn .asg{width:15px;height:15px;fill:#555}.ast-btn:hover{color:#111}.ast-btn:hover .asg{fill:#111}.ast-btn:focus-visible{outline:2px solid #2b5f8a;outline-offset:2px}
.asp{position:fixed;inset:0;z-index:2147483000}.asp[hidden]{display:none}
.asbk{position:absolute;inset:0;background:rgba(150,150,150,.55);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);opacity:0;transition:opacity .3s}
.asd{position:absolute;top:0;right:0;bottom:0;width:min(58.3vw,1100px);background:#fff;color:#222;display:flex;flex-direction:column;transform:translateX(100%);transition:transform .35s cubic-bezier(.2,.7,.2,1);font-family:"Source Sans 3","Source Sans Pro",system-ui,sans-serif;box-shadow:-10px 0 40px rgba(0,0,0,.08);color-scheme:light}
.asp.open .asbk{opacity:1}.asp.open .asd{transform:none}
.ash{display:flex;align-items:center;justify-content:space-between;height:96px;padding:0 26px 0 32px;border-bottom:1px solid #e5e5e5;flex:none;background:#fff}
.ash h2{margin:0;font:600 14.5px/1 "Source Sans 3",system-ui,sans-serif;letter-spacing:.1em;text-transform:uppercase;color:#222}
.asx{width:44px;height:44px;display:grid;place-items:center;background:none;border:0;cursor:pointer;margin-right:-6px;border-radius:0}.asx svg{width:22px;height:22px;stroke:#444;stroke-width:1.6;fill:none}.asx:hover svg{stroke:#000}
.asb{flex:1;display:grid;grid-template-columns:minmax(0,37.6%) minmax(0,1fr);overflow:auto;overscroll-behavior:contain}
.asl{padding:40px 32px;border-right:1px solid #e5e5e5}.ast1{margin:0;font:400 26px/1.17 "Source Serif 4","Source Serif Pro",Georgia,serif;color:#222;text-wrap:balance}
.asr{padding:22px 32px 48px}
.asgp{padding:20px 0 6px}.asgp+.asgp{border-top:1px solid #e5e5e5}
.asgp h3{margin:0 0 14px;font:600 11.5px/1 "Source Sans 3",system-ui,sans-serif;letter-spacing:.04em;text-transform:uppercase;color:#4a4a4a}
.asgp ul{list-style:none;margin:0;padding:0}.asgp li{margin:0 0 18px}
.asgp a{display:flex;gap:14px;align-items:flex-start;color:inherit;text-decoration:none}
.asi{flex:none;width:34px;height:34px;margin-top:1px}.asi svg{width:100%;height:100%;display:block}
.ast b{display:block;font:600 14px/1.35 "Source Sans 3",system-ui,sans-serif;color:#222}.ast>span{display:block;font:400 13px/1.55 "Source Sans 3",system-ui,sans-serif;color:#555}
.asgp a:hover b{text-decoration:underline;text-underline-offset:3px}.asgp a:focus-visible{outline:2px solid #2b5f8a;outline-offset:4px}
.asgp li.here b::after{content:"You are here";margin-left:8px;font:600 10px/1 "Source Sans 3",system-ui,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:#1b5e6b;border:1px solid currentColor;border-radius:999px;padding:2px 6px;vertical-align:2px}
html.asopen{overflow:hidden}
@media (max-width:860px){.asd{width:100%}.asb{grid-template-columns:minmax(0,1fr)}.asl{border-right:0;border-bottom:1px solid #e5e5e5;padding:24px 20px}.asr{padding:8px 20px 40px}.ash{height:64px;padding:0 14px 0 20px}.ast1{font-size:24px}.asbar .asin{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(10px,env(safe-area-inset-right,0px))}}
@media (max-width:420px){.asbar .asn{font-size:11px;letter-spacing:.06em}}
@media (prefers-reduced-motion:reduce){.asd,.asbk{transition:none}}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .asbar{background:#161513;border-color:#2c2a26}:root:not([data-theme="light"]) .asbar .asn{color:#a7a29a}:root:not([data-theme="light"]) .ast-btn{color:#cfcac2}:root:not([data-theme="light"]) .ast-btn .asg{fill:#cfcac2}}
:root[data-theme="dark"] .asbar{background:#161513;border-color:#2c2a26}:root[data-theme="dark"] .asbar .asn{color:#a7a29a}:root[data-theme="dark"] .ast-btn{color:#cfcac2}:root[data-theme="dark"] .ast-btn .asg{fill:#cfcac2}
"""
JS = r"""<script>(function(){var D=document,H=D.documentElement,p=D.querySelector('.asp'),t=D.querySelector('[data-as]'),last=null;if(!p||!t)return;
function open(){last=D.activeElement;p.hidden=false;H.classList.add('asopen');requestAnimationFrame(function(){requestAnimationFrame(function(){p.classList.add('open');p.querySelector('.asx').focus()})})}
function close(){if(p.hidden)return;p.classList.remove('open');H.classList.remove('asopen');setTimeout(function(){p.hidden=true},matchMedia('(prefers-reduced-motion: reduce)').matches?0:320);if(last)last.focus()}
t.addEventListener('click',open);[].forEach.call(p.querySelectorAll('.asx,.asbk'),function(x){x.addEventListener('click',close)});
D.addEventListener('keydown',function(e){if(e.key==='Escape')close();if(e.key==='Tab'&&!p.hidden){var f=p.querySelectorAll('a,button'),a=f[0],z=f[f.length-1];if(e.shiftKey&&D.activeElement===a){e.preventDefault();z.focus()}else if(!e.shiftKey&&D.activeElement===z){e.preventDefault();a.focus()}}})})();</script>"""
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600&family=Source+Serif+4:opsz,wght@8..60,400&display=swap">'

def apply(h, here_href="./", before='<div class="head">'):
    bar = (f'<div class="asbar"><div class="asin">'
           f'<button type="button" class="ast-btn" data-as aria-haspopup="dialog">{GRID}<span>All sites</span></button></div></div>')
    panel = (f'<div class="asp" hidden><div class="asbk"></div><div class="asd" role="dialog" aria-modal="true" aria-labelledby="ash">'
             f'<div class="ash"><h2 id="ash">All sites</h2><button type="button" class="asx" aria-label="Close"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 4l16 16M20 4 4 20"/></svg></button></div>'
             f'<div class="asb"><div class="asl"><p class="ast1">{TITLE}</p></div><nav class="asr" aria-label="All sites">{body(here_href)}</nav></div></div></div>')
    assert before in h, before
    h = h.replace(before, bar + before, 1)
    h = h.replace("</head>", FONTS + f"<style>{CSS}</style></head>", 1)
    i = h.rfind("</body>")
    return h[:i] + panel + JS + h[i:]
