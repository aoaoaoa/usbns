# /magazine/test/contact-cta/: the contact page with the "Submitting articles or photographs" section swapped for candidate CTAs.
# Facts used are the print page's: link.bahai.us/TAB_submit (BOSA login), TAB@usbnc.org, 800 words, TIFF or JPEG, may edit, no guarantee.
import os, re
D = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(D, "site", "magazine", "contact", "index.html")).read()
URL = "https://link.bahai.us/TAB_submit"
ML = '<a href="mailto:TAB@usbnc.org">TAB@usbnc.org</a>'
ARR = '<span aria-hidden="true">→</span>'
FACTS = '<ul class="fx"><li>Up to 800 words</li><li>Photos in TIFF or JPEG, people identified</li><li>We may edit for length and style</li></ul>'

V = [
("Two doors", f'''<div class="v2">
<a class="door" href="{URL}"><span class="dk">Online</span><b>Submit a story or photographs</b><span class="ds">Log in with your Bahá’í Online Services account (BOSA).</span><span class="go">Submit {ARR}</span></a>
<a class="door" href="mailto:TAB@usbnc.org"><span class="dk">By email</span><b>Write to the editors</b><span class="ds">Questions, leads, or a story idea in a few lines.</span><span class="go">TAB@usbnc.org {ARR}</span></a></div>{FACTS}'''),
("One button", f'''<div class="v1"><a class="sbtn" href="{URL}">Submit your story {ARR}</a><p class="sm">Log in with your Bahá’í Online Services account (BOSA). Or email {ML}.</p>{FACTS}</div>'''),
("From the issue", f'''<div class="v3"><p class="big">Every story in this issue began as a report from a community.</p><p class="sm">Send yours: a few paragraphs, a photograph, or a lead.</p>
<p class="acts"><a class="sbtn" href="{URL}">Submit your story {ARR}</a><span>or email {ML}</span></p></div>'''),
("Button and guidelines", f'''<div class="v1"><a class="sbtn" href="{URL}">Submit your story {ARR}</a><p class="sm">Log in with your Bahá’í Online Services account (BOSA). Or email {ML}.</p></div>
<details class="gd"><summary>Guidelines</summary><p>Every item will be carefully considered, but we cannot guarantee publication.</p>
<p>Articles should be clear, concise and relevant to the aims of the current Plan. Limit: 800 words. <b>We may edit stories for length and style.</b> We cannot print advance articles to publicize locally sponsored events, but may be able to list them in the Calendar pages.</p>
<p>Photographs should be bright, well-composed and in focus. Please identify people when possible. <b>Electronic images</b> should be high resolution, in TIFF or JPEG format.</p></details>'''),
("One line", f'''<p class="v5"><b>Have a story or photographs?</b> <a href="{URL}">Submit online</a> with your BOSA login, or email {ML}.</p>'''),
("Story and photo, side by side", f'''<div class="v6"><div><span class="ic"><svg viewBox="0 0 24 24"><path d="M4 20l4-1 11-11-3-3L5 16z"/><path d="M14 6l3 3"/></svg></span><b>Articles</b><p>Clear, concise, up to 800 words.</p></div>
<div><span class="ic"><svg viewBox="0 0 24 24"><path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/></svg></span><b>Photographs</b><p>Bright, in focus, TIFF or JPEG. Please identify people.</p></div></div>
<p class="acts"><a class="sbtn" href="{URL}">Submit {ARR}</a><span>BOSA login · or email {ML}</span></p>'''),
]

CSS = '''
.bar0{position:sticky;top:0;z-index:5;display:flex;gap:6px;align-items:center;overflow-x:auto;scrollbar-width:none;padding:8px 16px;background:var(--card);border-bottom:1px solid var(--rule)}
.bar0 b{font:700 11px var(--ui);letter-spacing:.12em;text-transform:uppercase;color:var(--mute);white-space:nowrap;margin-right:6px}
.bar0 button{font:600 13px var(--ui);border:1px solid var(--rule);background:none;color:var(--ink);border-radius:999px;padding:6px 12px;cursor:pointer;white-space:nowrap}.bar0 button[aria-pressed=true]{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.vv[hidden]{display:none}.vv{outline:2px dashed #b8782e;outline-offset:10px;border-radius:2px}
.sbtn{display:inline-flex;align-items:center;gap:10px;font:700 19px/1 "Barlow Condensed","Arial Narrow",sans-serif;letter-spacing:.04em;text-transform:uppercase;text-decoration:none;background:#222e4c;color:#f2cfc6!important;padding:14px 24px;border-radius:3px}
main .sm{font:15px/1.5 var(--ui);color:var(--mute);margin:10px 0 0}
.fx{list-style:none;padding:0;margin:16px 0 0;display:flex;flex-wrap:wrap;gap:6px 18px;font:14px var(--ui);color:var(--mute)}.fx li::before{content:"·";margin-right:8px;color:#b8782e;font-weight:700}.fx li:first-child::before{content:none}
.v2{display:grid;grid-template-columns:1fr 1fr;gap:14px}.door{display:grid;gap:6px;align-content:start;text-decoration:none;color:var(--ink)!important;background:var(--card);border:1px solid var(--rule);border-top:4px solid #222e4c;padding:18px}.door+.door{border-top-color:#b8782e}.door:hover{border-color:var(--ink)}
.dk{font:700 11px var(--ui);letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}.door b{font:700 20px/1.2 var(--text)}.ds{font:14px/1.5 var(--ui);color:var(--mute)}.go{font:700 16px var(--ui);color:var(--link);margin-top:6px}
.v3{background:var(--card);border:1px solid var(--rule);padding:26px 24px;text-align:center}.v3 .big{font:700 clamp(22px,3vw,28px)/1.2 var(--text);margin:0 auto 8px;max-width:24ch;text-wrap:balance}
.acts{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:12px 16px;margin:18px 0 0!important;font:15px var(--ui)!important;color:var(--mute)}
.gd{margin-top:18px;border-top:1px solid var(--rule)}.gd summary{font:600 15px var(--ui);cursor:pointer;padding:12px 0}.gd p{font-size:16px!important}
.v5{font:18px/1.6 var(--text)!important;background:var(--card);border-left:4px solid #b8782e;padding:14px 18px}
.v6{display:grid;grid-template-columns:1fr 1fr;gap:14px}.v6>div{background:var(--card);border:1px solid var(--rule);padding:16px}.v6 b{display:block;font:700 18px var(--text);margin:8px 0 2px}.v6 p{font:14px/1.5 var(--ui)!important;color:var(--mute);margin:0!important}
.ic svg{width:26px;height:26px;fill:none;stroke:#b8782e;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}.v6+.acts{justify-content:flex-start}
@media (max-width:560px){.v2,.v6{grid-template-columns:1fr}}
'''
JS = '''(function(){var V=[].slice.call(document.querySelectorAll('.vv')),B=[].slice.call(document.querySelectorAll('.bar0 button'));
function go(k){V.forEach(function(v,i){v.hidden=i!==k});B.forEach(function(b,i){b.setAttribute('aria-pressed',i===k)});history.replaceState(null,'','#v'+(k+1))}
B.forEach(function(b,i){b.onclick=function(){go(i);document.getElementById('submit').scrollIntoView({block:'start'})}});var m=/^#v(\\d)$/.exec(location.hash);go(m?Math.min(+m[1]-1,V.length-1):0)})();'''

i = src.index('<h2 id="submit">'); j = src.index('<h2 id="subs">')
vv = "".join(f'<div class="vv" data-n="{n}"{"" if k == 0 else " hidden"}>{h}</div>' for k, (n, h) in enumerate(V))
h = src[:i] + '<h2 id="submit">Submitting articles or photographs</h2>' + vv + src[j:]
bar = '<nav class="bar0" aria-label="Variants"><b>Submit section</b>' + "".join(f'<button type="button">{k+1} · {n}</button>' for k, (n, _) in enumerate(V)) + '</nav>'
h = h.replace('<header class="pt">', bar + '<header class="pt">', 1).replace('</style>', CSS + '</style>', 1).replace('</body>', f'<script>{JS}</script></body>', 1)
h = h.replace('href="../favicon.svg"', 'href="../../favicon.svg"').replace('<head>', '<head>\n<meta name="robots" content="noindex">', 1)
h = re.sub(r'<title>[^<]*</title>', '<title>Submit Section Studies</title>', h, count=1)
out = os.path.join(D, "site", "magazine", "test", "contact-cta"); os.makedirs(out, exist_ok=True)
open(os.path.join(out, "index.html"), "w").write(h); print("ok", len(V))
