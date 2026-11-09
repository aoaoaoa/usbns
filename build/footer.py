"""The global footer (the colophon), shared by both editions and the newsstand.

Fill in LINKS and FOLLOW with the real addresses; everything else follows."""

LINKS = [  # (label, href)
    ("About", "#"),
    ("Contact", "#"),
    ("Terms of use", "#"),
    ("Privacy policy", "#"),
]
FOLLOW = [  # (label, href, icon file in icons/)
    ("Facebook", "#", "facebook"),
    ("Instagram", "#", "instagram"),
    ("YouTube", "#", "youtube"),
    ("X", "#", "x-twitter"),
    ("LinkedIn", "#", "linkedin"),
]
import os as _os
_ICONS = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "icons")
def _icon(name):
    """Font Awesome Free brand icon (CC BY 4.0, license note kept inside the SVG), drawn in currentColor."""
    svg = open(_os.path.join(_ICONS, name + ".svg")).read().strip()
    return svg.replace("<svg ", '<svg aria-hidden="true" focusable="false" ', 1)
ASKS = [  # (label, link text, href, extra attributes)
    ("Reader survey", "Give feedback", "https://form.typeform.com/to/NfIWSbQl", ' data-survey'),
    ("Contribute", "Submit your story", "#", ''),
    ("Every issue", "Subscribe", "/usbns/magazine/landing/#subscribe", ''),
]
PUBLISHER = "Published by the National Spiritual Assembly of the Bahá’ís of the United States, 1233 Central St., Evanston, IL 60201."

_MARK = ('<svg class="cm" width="22" height="22" viewBox="0 0 48 48" aria-hidden="true"><defs><linearGradient id="colo-g" x1="26" y1="1" x2="26" y2="48" gradientUnits="userSpaceOnUse">'
         '<stop stop-color="#73E4C4"/><stop offset=".47" stop-color="#357686"/><stop offset="1" stop-color="#255875"/></linearGradient></defs>'
         '<path fill="url(#colo-g)" d="M22.0121 12.0305L23.9836 8.64366L25.9552 12.0305L27.4999 14.6878L30.3894 13.6493L34.0717 12.3258L33.4077 16.1878L32.8894 19.2183L35.7688 20.2839L39.4375 21.6414L36.4531 24.1731L34.1089 26.1584L35.6333 28.8292L37.5744 32.233L33.6618 32.25L30.5927 32.2636L30.0473 35.2907L29.3529 39.1459L26.3447 36.6414L23.9836 34.6731L21.6225 36.6414L18.6144 39.1459L17.92 35.2907L17.3746 32.2636L14.3055 32.25L10.3929 32.233L12.334 28.8292L13.8583 26.1584L11.5142 24.1731L8.52977 21.6414L12.2018 20.2839L15.0812 19.2183L14.5629 16.1878L13.899 12.3258L17.5812 13.6493L20.4708 14.6878L22.0155 12.0305H22.0121ZM18.523 9.3733L8.32652 5.70475L10.1626 16.4016L0 20.1584L8.26894 27.1697L2.89294 36.5905L13.7262 36.638L15.6537 47.3179L23.9836 40.3778L32.3136 47.3179L34.241 36.638L45.0743 36.5905L39.6983 27.1697L47.9673 20.1584L37.8047 16.4016L39.6408 5.70475L29.4443 9.3733L23.9803 0L18.523 9.3767V9.3733Z"/></svg>')

def footer_html(home="./"):
    """home: link target for the wordmark (the newsstand)."""
    nav = "".join(f'<li><a href="{h}">{t}</a></li>' for t, h in LINKS)
    fol = "".join(f'<a href="{h}" rel="noopener" aria-label="{t}" title="{t}">{_icon(i)}</a>' for t, h, i in FOLLOW)
    return (f'<footer class="colo"><div class="ci">'
            f'<a class="cw" href="{home}">{_MARK}<span><small>The</small> American Bahá’í</span></a>'
            '<div class="cr" aria-hidden="true"></div>'
            '<div class="c3">' + ''.join(f'<div><span>{l}</span><a href="{h}"{x}>{t}</a></div>' for l, t, h, x in ASKS) + '</div>'
            f'<nav aria-label="Footer"><ul>{nav}</ul></nav>'
            f'<div class="cs"><span>Follow us</span><span class="ic">{fol}</span></div>'
            f'<p class="cp">{PUBLISHER}</p></div></footer>')

FOOTER_CSS = """
/* navy and blush */
.colo{position:relative;z-index:2;background:var(--card,var(--bar,#fdfcf9));border-top:1px solid var(--rule);text-align:center;color:var(--ink);font-family:var(--ui)}
.colo .ci{max-width:1240px;margin:0 auto;padding:52px max(16px,env(safe-area-inset-right,0px)) calc(40px + env(safe-area-inset-bottom,0px)) max(16px,env(safe-area-inset-left,0px));display:grid;justify-items:center;gap:18px}
.colo .cw{font:700 26px/1 "Literata",Georgia,serif;letter-spacing:-.01em;display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--ink)}
.colo .cw small{font:italic 400 17px "Literata",Georgia,serif}
.colo .cr{width:min(520px,80%);height:12px;background:radial-gradient(circle,#b8782e 1.6px,transparent 2px) center/18px 12px repeat-x}
.colo ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;justify-content:center;gap:6px 0}
.colo li{font-weight:600;font-size:12.5px;line-height:1;letter-spacing:.16em;text-transform:uppercase}
.colo li+li::before{content:"·";margin:0 14px;color:#b8782e}
.colo nav a{color:var(--ink);text-decoration:none;padding:6px 0;display:inline-block}
.colo nav a:hover{color:var(--link,var(--accent))}
.colo nav{margin:0;display:block;width:100%}
.colo .cs{display:flex;flex-direction:column;align-items:center;gap:10px;margin:0;font:italic 400 15px "Literata",Georgia,serif;color:var(--mute)}
.colo .cs .ic{display:flex;flex-wrap:wrap;justify-content:center;gap:10px}
.colo .cs a{width:42px;height:42px;border-radius:50%;border:1px solid var(--rule);display:grid;place-items:center;color:var(--ink);transition:color .2s,border-color .2s,background .2s}
.colo .cs a svg{width:18px;height:18px;display:block}
.colo .cs a:hover{color:var(--card,var(--bar,#fdfcf9));background:var(--ink);border-color:var(--ink)}
.colo .cp{font-size:12.5px;line-height:1.6;color:var(--mute);max-width:60ch;margin:0}
.colo a:focus-visible{outline:2px solid var(--link,var(--accent));outline-offset:3px;border-radius:2px}
@media (max-width:640px){.colo ul{flex-direction:column;align-items:center;gap:2px}.colo li+li::before{content:none}.colo li{padding-left:.16em}}
@media (prefers-reduced-motion:reduce){.colo .cs a{transition:none}}
.colo{background:#222e4c;border-top:0;color:#f2cfc6}
.colo .ci{gap:18px;padding-top:44px;padding-bottom:calc(38px + env(safe-area-inset-bottom,0px))}
.colo .cw{color:#f2cfc6}.colo .cr{display:none}
.colo nav a{color:#f2cfc6;font:700 17px/1 "Barlow Condensed","Arial Narrow",sans-serif;letter-spacing:.08em}
.colo li{font-size:17px}.colo li+li::before{content:"";margin:0 13px}
.colo nav a:hover{color:#fff;text-decoration:underline;text-underline-offset:4px}
.colo .cs>span:first-child{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.colo .cs a{color:#f2cfc6;border-color:rgba(242,207,198,.35)}
.colo .cs a:hover{background:#f2cfc6;color:#222e4c;border-color:#f2cfc6}
.colo .cp{color:rgba(242,207,198,.75)}
.colo a:focus-visible{outline-color:#f2cfc6}
@media (max-width:640px){.colo nav a{font-size:16px}}
.colo .c3{display:grid;grid-template-columns:repeat(3,auto);justify-content:center}.colo .c3>div{padding:4px 28px;text-align:center}.colo .c3>div+div{border-left:1px solid rgba(242,207,198,.3)}.colo .c3 span{display:block;font:700 11px var(--ui);letter-spacing:.18em;text-transform:uppercase;color:rgba(242,207,198,.7);margin-bottom:6px}.colo .c3 a{font:italic 600 18px "Literata",Georgia,serif;color:#fff;text-decoration:none}.colo .c3 a:hover{text-decoration:underline;text-underline-offset:4px}
@media (max-width:600px){.colo .c3{grid-template-columns:1fr;gap:14px}.colo .c3>div+div{border-left:0}}
"""
