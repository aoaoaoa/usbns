import re
P = '/home/claude/usbns/magazine/landing/index.html'
src = open(P).read()
# strip any earlier survey block so the script can be rerun
src = re.sub(r'\n<!-- survey -->.*?<!-- /survey -->\n', '\n', src, flags=re.S)
src = re.sub(r'/\* survey \*/.*?/\* /survey \*/\n', '', src, flags=re.S)
src = re.sub(r'<!-- svydlg -->.*?<!-- /svydlg -->\n', '', src, flags=re.S)
src = re.sub(r'<!-- strip -->.*?<!-- /strip -->\n', '', src, flags=re.S)
src = re.sub(r'<!-- corner -->.*?<!-- /corner -->\n', '', src, flags=re.S)
src = src.replace("<small>The</small> American Bahá'í", "<small>The</small> American Bahá’í")
src = re.sub(r'<figure class="cover"><img src="\.\./img/cover-(?:print-v57n5|full|full-v2)\.jpg" alt="[^"]*"', '<figure class="cover"><img src="../img/cover-full-v2.jpg" alt="Juliet Bogan\u2019s cover painting for The American Bah\u00e1\u2019\u00ed, October/November/December 2026: a green valley of terraced fields and small houses under an orange ridge, with two young women in the foreground"', src, count=1)
src = re.sub(r'<link rel="(apple-touch-icon|manifest)"[^>]*>\n?|<link rel="icon" type="image/png"[^>]*>\n?|<meta name="(application-name|apple-mobile-web-app-title)"[^>]*>\n?', '', src)
src = src.replace('</title>', '</title>\n<link rel="apple-touch-icon" sizes="180x180" href="/usbns/magazine/apple-touch-icon.png">\n<link rel="manifest" href="/usbns/magazine/manifest.webmanifest">\n<link rel="icon" type="image/png" sizes="192x192" href="/usbns/magazine/icon-192.png">\n<link rel="icon" type="image/png" sizes="512x512" href="/usbns/magazine/icon-512.png">\n<meta name="application-name" content="American Bahá’í">\n<meta name="apple-mobile-web-app-title" content="American Bahá’í">\n', 1)
src = re.sub(r'<!-- subx(:btn)? -->.*?<!-- /subx(:btn)? -->\n?', '', src, flags=re.S)
src = re.sub(r'/\* subx \*/.*?/\* /subx \*/\n', '', src, flags=re.S)
src = re.sub(r'<!-- colo -->.*?<!-- /colo -->\n', '', src, flags=re.S)
src = re.sub(r'<!-- takepart -->.*?<!-- /takepart -->\n?', '', src, flags=re.S).replace('<!-- /subx -->', '')
src = re.sub(r'<footer><div class="wrap">Published by[^<]*</div></footer>\n?', '', src)
import sys; sys.path.insert(0, '/home/claude/tab')
from footer import footer_html, FOOTER_CSS

FORM = 'https://form.typeform.com/to/NfIWSbQl'
FONT_OLD = 'family=Bricolage+Grotesque:'
if 'Barlow+Condensed' not in src:
    src = src.replace(FONT_OLD, 'family=Barlow+Condensed:wght@300;400;700&' + FONT_OLD, 1)

CSS_COMMON = '''/* survey */
.svy{--navy:#222e4c;--blush:#f2cfc6;--gold:#b8782e;--stamp:#fbf7ef}
.svy .wrap{padding-top:72px;padding-bottom:72px}
.svbrand{font-family:"Barlow Condensed","Arial Narrow",var(--ui),sans-serif;font-weight:300;line-height:1.02;margin:0;color:var(--blush)}.svbrand b{font-weight:700}
.svbtn{display:inline-flex;align-items:center;justify-content:center;font-family:"Barlow Condensed","Arial Narrow",var(--ui),sans-serif;font-weight:700;font-size:20px;letter-spacing:.03em;text-transform:uppercase;text-decoration:none;background:var(--blush);color:var(--navy);padding:12px 28px;border-radius:3px;white-space:nowrap;transition:transform .2s,box-shadow .2s}
.svbtn:hover{transform:translateY(-2px);box-shadow:0 8px 18px rgba(0,0,0,.25)}
.svbtn:focus-visible{outline:2px solid var(--blush);outline-offset:3px}
.svmin{display:flex;align-items:center;justify-content:center;gap:6px;font-family:"Barlow Condensed","Arial Narrow",var(--ui),sans-serif;font-size:17px;color:var(--blush);opacity:.85;margin:12px 0 0}
.svmin svg{width:15px;height:15px;flex:none}
img.mo{display:block;width:100%;height:100%;object-fit:cover}
.svydlg{border:0;border-radius:14px;padding:0;width:min(760px,calc(100vw - 32px));height:min(720px,calc(100dvh - 48px));background:var(--card);color:var(--ink);box-shadow:0 24px 60px rgba(20,16,10,.28);overflow:hidden}
.svydlg[open]{display:flex;flex-direction:column}.svydlg::backdrop{background:rgba(20,16,10,.38)}
.svydlg .svh{display:flex;justify-content:space-between;align-items:start;gap:12px;padding:18px 18px 14px 22px;border-bottom:1px solid var(--rule)}
.svydlg .shk{margin:0;font-family:var(--ui);font-size:11px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--mute)}
.svydlg h2{font-size:20px;line-height:1.2}
.svydlg .shx{flex:none;width:40px;height:40px;border-radius:50%;border:0;background:transparent;color:var(--mute);cursor:pointer}.svydlg .shx svg{width:20px;height:20px}.svydlg .shx:hover{background:var(--ph)}
.svydlg .svf{flex:1;min-height:0}.svydlg iframe{display:block;width:100%;height:100%;border:0;background:#fff}
@media (max-width:640px){.svydlg{width:100vw;max-width:100vw;height:100dvh;max-height:100dvh;border-radius:0;margin:0}.svydlg .svh{padding-top:max(14px,env(safe-area-inset-top,0px))}}
@media (prefers-reduced-motion:reduce){.svbtn{transition:none}}
'''

CSS_F = '''/* F: three motifs behind one card, in a postage-stamp frame */
.stampw{position:relative;max-width:1080px;margin:0 auto;filter:drop-shadow(0 18px 30px rgba(29,26,22,.18))}
.stamp{--r:7px;background:var(--stamp);padding:calc(2.6*var(--r));
  -webkit-mask:radial-gradient(var(--r),#0000 97%,#000) round calc(-1.5*var(--r)) calc(-1.5*var(--r))/calc(3*var(--r)) calc(3*var(--r)),linear-gradient(#000 0 0) calc(1.5*var(--r)) calc(1.5*var(--r))/calc(100% - 3*var(--r)) calc(100% - 3*var(--r)) no-repeat;
  mask:radial-gradient(var(--r),#0000 97%,#000) round calc(-1.5*var(--r)) calc(-1.5*var(--r))/calc(3*var(--r)) calc(3*var(--r)),linear-gradient(#000 0 0) calc(1.5*var(--r)) calc(1.5*var(--r))/calc(100% - 3*var(--r)) calc(100% - 3*var(--r)) no-repeat}
.stamp .plate{position:relative;min-height:460px;display:grid;place-items:center;overflow:hidden;outline:1px solid color-mix(in oklab,var(--navy) 30%,transparent);outline-offset:6px}
.stamp .bg{position:absolute;inset:0;display:grid;grid-template-columns:repeat(3,1fr);gap:0}
.stamp .card2{position:relative;margin:28px 20px;background:color-mix(in oklab,var(--navy) 90%,transparent);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);color:var(--blush);padding:clamp(26px,4vw,44px) clamp(22px,4vw,48px);max-width:580px;text-align:center;border-radius:3px;box-shadow:0 0 0 1px rgba(242,207,198,.35) inset,0 0 0 7px var(--navy) inset,0 0 0 8px rgba(242,207,198,.25) inset}
.stamp .svbrand{font-size:clamp(36px,4.4vw,52px);margin:0 0 14px}
.stamp .card2 p.l{font-family:"Barlow Condensed","Arial Narrow",var(--ui),sans-serif;font-size:21px;margin:0 0 22px;color:var(--blush)}
.stampw .val{position:absolute;right:calc(2.6*7px + 10px);top:calc(2.6*7px + 8px);z-index:2;font-family:"Barlow Condensed","Arial Narrow",var(--ui),sans-serif;font-weight:700;font-size:15px;letter-spacing:.08em;color:var(--navy);background:var(--stamp);padding:3px 8px;border-radius:2px}
.pmark{position:absolute;left:-26px;bottom:-30px;width:150px;height:150px;z-index:3;color:var(--gold);transform:rotate(-14deg);pointer-events:none;opacity:.9}
.pmark text{font-family:"Barlow Condensed","Arial Narrow",sans-serif;font-weight:700;font-size:13.5px;letter-spacing:.2em;fill:currentColor}
@media (max-width:720px){.stamp .bg{grid-template-columns:1fr 1fr}.stamp .bg img:nth-child(3){display:none}.stamp .plate{min-height:420px}.pmark{width:110px;height:110px;left:-10px;bottom:-26px}}
/* /survey */
'''

CSS_B = '''/* B: a wall of the motif, one tile asks */
.wall{display:grid;grid-template-columns:repeat(6,1fr);gap:6px}
.wall>*{aspect-ratio:1;overflow:hidden;border-radius:2px}
.wall .ask{grid-column:3/5;grid-row:1/3;aspect-ratio:auto;background:var(--navy);color:var(--blush);padding:clamp(20px,3vw,36px);display:flex;flex-direction:column;justify-content:flex-end;gap:14px}
.wall .ask .svbrand{font-size:clamp(32px,3.8vw,52px)}
.wall .ask p.l{margin:0;font-family:"Barlow Condensed","Arial Narrow",var(--ui),sans-serif;font-size:19px;color:var(--blush);opacity:.92}
.wall .ask .go{display:flex;flex-direction:column;align-items:flex-start}.wall .ask .svmin{justify-content:flex-start}
.wall a.t{display:block;transition:transform .25s}.wall a.t:hover{transform:scale(1.03)}
.wall a.t:focus-visible{outline:2px solid var(--link);outline-offset:2px}
@media (max-width:900px){.wall{grid-template-columns:repeat(4,1fr)}.wall .ask{grid-column:2/4}.wall a.x4,.wall a.x5,.wall a.x6{display:none}}
@media (max-width:600px){.wall{grid-template-columns:repeat(3,1fr)}.wall .ask{grid-column:1/-1;grid-row:2}.wall a.x4,.wall a.x5{display:block}.wall a.x6{display:none}}
@media (prefers-reduced-motion:reduce){.wall a.t{transition:none}}
/* /survey */
'''

CLOCK = '<svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="6.5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M8 4v4l2.5 1.5" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>'
BTN = f'<a class="svbtn" href="{FORM}" data-survey target="_blank" rel="noopener">Give feedback</a>'
MIN = f'<p class="svmin">{CLOCK}Takes 5 minutes</p>'
HEAD = ''

def F(pre):
    m = lambda n: f'<img class="mo" src="{pre}img/motif/m{n:02d}.webp" alt="" loading="lazy">'
    pm = ('<svg class="pmark" viewBox="0 0 150 150" aria-hidden="true"><defs><path id="pmc" d="M75 75 m-54 0 a54 54 0 1 1 108 0 a54 54 0 1 1 -108 0"/></defs>'
          '<circle cx="75" cy="75" r="66" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="75" cy="75" r="40" fill="none" stroke="currentColor" stroke-width="1.5"/>'
          '<text><textPath href="#pmc">READER SURVEY · THE ARTS ISSUE · 2026 ·</textPath></text>'
          '<text x="75" y="72" text-anchor="middle" style="font-size:15px;letter-spacing:.06em">5 MIN</text><text x="75" y="88" text-anchor="middle" style="font-size:11px">2026</text></svg>')
    return (f'\n<!-- survey -->\n<section id="survey" class="svy" aria-label="Reader survey" hidden><div class="wrap">{HEAD}'
            f'<div class="stampw"><div class="stamp"><div class="plate"><div class="bg">{m(5)}{m(12)}{m(2)}</div>'
            f'<div class="card2"><h3 class="svbrand">The American Bahá’í<br>Reader <b>Survey</b></h3><p class="l">Share your ideas to shape the magazine’s future.</p>{BTN}{MIN}</div></div></div>'
            f'{pm}</div></div></section>\n<!-- /survey -->\n')

def B(pre):
    t = lambda n, c='': f'<a class="t {c}" href="{FORM}" data-survey target="_blank" rel="noopener" tabindex="-1" aria-hidden="true"><img class="mo" src="{pre}img/motif/m{n:02d}.webp" alt="" loading="lazy"></a>'
    ask = (f'<div class="ask"><h3 class="svbrand">Tell us what<br>you <b>read</b></h3><p class="l">What you enjoy, and what you’d like next.</p>'
           f'<div class="go">{BTN}{MIN}</div></div>')
    tiles = [t(2), t(4), ask, t(6, 'x5'), t(9, 'x6'), t(11), t(5), t(10, 'x4'), t(12, 'x6')]
    return (f'\n<!-- survey -->\n<section id="survey" class="svy" aria-label="Reader survey" hidden><div class="wrap">{HEAD}'
            f'<div class="wall">{"".join(tiles)}</div></div></section>\n<!-- /survey -->\n')

DLG = ('<!-- svydlg --><dialog class="svydlg" aria-labelledby="svy-h"><div class="svh"><div><p class="shk">Reader survey</p><h2 id="svy-h">Shape the future of The American Bahá’í</h2></div>'
       '<button class="shx" type="button" aria-label="Close the survey"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button></div>'
       f'<div class="svf"><iframe title="TAB Reader Survey" allow="camera; microphone; autoplay; encrypted-media; fullscreen" data-src="{FORM}?typeform-medium=embed-snippet"></iframe></div></dialog>'
       "<script>(function(){var d=document.querySelector('.svydlg');if(!d||!d.showModal)return;var f=d.querySelector('iframe'),op=null;"
       "function open(o){op=o||null;if(!f.src)f.src=f.dataset.src;if(!d.open)d.showModal()}"
       "document.addEventListener('click',function(e){var b=e.target.closest('[data-survey]');if(!b)return;e.preventDefault();open(b)});"
       "d.querySelector('.shx').addEventListener('click',function(){d.close()});d.addEventListener('click',function(e){if(e.target===d)d.close()});"
       "d.addEventListener('close',function(){if(op)op.focus()});if(location.hash==='#take-survey')open();})();</script><!-- /svydlg -->\n")

CSS_EF = """/* E→F: a strip under the header that becomes a stamp in the corner once the reader scrolls */
.strip{background:var(--navy);color:var(--blush);overflow:hidden}
.strip .wrap{display:flex;align-items:center;gap:16px;min-height:64px;padding-top:0;padding-bottom:0}
.strip .ms{display:flex;height:64px;flex:none}.strip .ms img{width:64px;height:64px}
.strip p{margin:0;flex:1;min-width:0;font:19px/1.2 "Barlow Condensed","Arial Narrow",sans-serif}.strip p b{font-weight:700}
.strip .svbtn{font-size:16px;padding:9px 16px;border-radius:999px}
@media (max-width:640px){.strip .ms img:nth-child(n+2){display:none}.strip p{font-size:17px}.strip .svbtn{font-size:14px;padding:8px 12px}.strip .lg{display:none}}
.fstamp{position:fixed;right:max(18px,env(safe-area-inset-right,0px));bottom:max(18px,env(safe-area-inset-bottom,0px));z-index:20;width:150px;transform:translateY(150%) rotate(10deg);opacity:0;visibility:hidden;transition:transform .5s cubic-bezier(.2,.8,.2,1),opacity .3s,visibility 0s .5s;filter:drop-shadow(0 10px 18px rgba(29,26,22,.3))}
.fstamp.on{transform:translateY(0) rotate(4deg);opacity:1;visibility:visible;transition:transform .5s cubic-bezier(.2,.8,.2,1),opacity .3s,visibility 0s}
.fstamp>a{display:block;text-decoration:none}
.fstamp .pf{--r:5px;background:var(--stamp);padding:calc(2.4*var(--r));display:block;
 -webkit-mask:radial-gradient(var(--r),#0000 97%,#000) round calc(-1.5*var(--r)) calc(-1.5*var(--r))/calc(3*var(--r)) calc(3*var(--r)),linear-gradient(#000 0 0) calc(1.5*var(--r)) calc(1.5*var(--r))/calc(100% - 3*var(--r)) calc(100% - 3*var(--r)) no-repeat;
 mask:radial-gradient(var(--r),#0000 97%,#000) round calc(-1.5*var(--r)) calc(-1.5*var(--r))/calc(3*var(--r)) calc(3*var(--r)),linear-gradient(#000 0 0) calc(1.5*var(--r)) calc(1.5*var(--r))/calc(100% - 3*var(--r)) calc(100% - 3*var(--r)) no-repeat}
.fstamp .im{display:block;aspect-ratio:1;overflow:hidden;position:relative}
.fstamp .lb{display:block;background:var(--navy);color:var(--blush);text-align:center;font:700 14px/1.1 "Barlow Condensed","Arial Narrow",sans-serif;letter-spacing:.06em;text-transform:uppercase;padding:8px 4px}
.fstamp .x{position:absolute;top:-10px;left:-10px;width:28px;height:28px;border-radius:50%;border:0;background:var(--card);color:var(--ink);box-shadow:0 2px 6px rgba(0,0,0,.2);cursor:pointer;display:grid;place-items:center}
.fstamp .x svg{width:14px;height:14px}
.fstamp>a:focus-visible,.fstamp .x:focus-visible{outline:2px solid var(--link);outline-offset:3px}
@media (max-width:600px){.fstamp{width:108px}}
@media (prefers-reduced-motion:reduce){.fstamp,.fstamp.on{transition:none}}
"""
HEADER_END = '</div></header>'
assert HEADER_END in src

def strip(pre):
    m = lambda n: f'<img class="mo" src="{pre}img/motif/m{n:02d}.webp" alt="">'
    return (f'\n<!-- strip -->\n<div class="strip svy" role="region" aria-label="Reader survey"><div class="wrap"><span class="ms">{m(2)}{m(9)}{m(5)}</span>'
            f'<p><b>Reader survey.</b> <span class="lg">Share your ideas to shape the magazine’s future. </span>Takes 5 minutes.</p>'
            f'<a class="svbtn" href="{FORM}" data-survey target="_blank" rel="noopener">Give feedback</a></div></div>\n<!-- /strip -->\n')

def corner(pre):
    return ('<!-- corner -->\n<div class="fstamp svy"><a href="' + FORM + '" data-survey target="_blank" rel="noopener" aria-label="Take the reader survey">'
            f'<span class="pf"><span class="im"><img class="mo" src="{pre}img/motif/m12.webp" alt="" loading="lazy"></span><span class="lb">Reader survey · 5 min</span></span></a>'
            '<button class="x" type="button" aria-label="Dismiss the survey stamp"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 7l10 10M17 7 7 17" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg></button></div>\n'
            "<script>(function(){var s=document.querySelector('.fstamp'),st=document.querySelector('.air')||document.querySelector('#current .cta');if(!s||!st||!('IntersectionObserver' in window))return;"
            "var K='tab-ns-stamp',off=false;try{off=!!sessionStorage.getItem(K)}catch(e){}"
            "var seen={strip:true,big:false,foot:false};function up(){s.classList.toggle('on',!off&&!seen.strip&&!seen.big&&!seen.foot)}"
            "function watch(el,k){if(!el)return;new IntersectionObserver(function(e){seen[k]=e[0].isIntersecting;up()}).observe(el)}"
            "function sc(){seen.strip=scrollY<140;up()}addEventListener('scroll',sc,{passive:true});sc();watch(document.getElementById('survey'),'big');watch(document.querySelector('.colo'),'foot');"
            "s.querySelector('.x').addEventListener('click',function(){off=true;up();try{sessionStorage.setItem(K,'1')}catch(e){}});"
            "s.querySelector('a').addEventListener('click',function(){off=true;setTimeout(up,400)})})();</script>\n<!-- /corner -->\n")

exec(open('nsadd.py').read())

SUBX_CSS = '/* subx */.vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}\n.sbx .wrap{padding-top:80px;padding-bottom:80px;text-align:center}\n.sbx h2{font-family:"Literata",Georgia,serif;font-weight:800;font-size:clamp(28px,3vw,38px);line-height:1.1;letter-spacing:-.015em;margin:0 0 12px}\n.sbx h2::before{content:"Subscribe";display:table;margin:0 auto 10px;border-top:4px double var(--ink);padding-top:12px;font:700 11px/1 var(--ui);letter-spacing:.2em;text-transform:uppercase;color:#b8782e}\n.sbx .ld{font:17px/1.55 "Literata",serif;color:var(--soft);max-width:48ch;margin:0 auto 26px}\n.sf{display:flex;gap:8px;max-width:520px;margin:0 auto}.sf input{flex:1;min-width:0;min-height:50px;border:1.5px solid var(--rule);border-radius:999px;padding:0 20px;font:16px var(--ui);background:var(--card);color:var(--ink)}.sf input:focus{outline:2px solid #222e4c;outline-offset:1px}\n.sf button{min-height:50px;padding:0 24px;border:0;border-radius:999px;background:#222e4c;color:#fff;font:600 15px var(--ui);cursor:pointer}.sf button:hover{background:#2c3a60}\n.dv{border:0;margin:0 auto 18px;padding:0;display:flex;flex-wrap:wrap;justify-content:center;gap:8px}.dv legend{width:100%;font:600 12px var(--ui);letter-spacing:.14em;text-transform:uppercase;color:var(--mute);margin-bottom:10px}\n.dv label{cursor:pointer}.dv input{position:absolute;opacity:0}.dv span{display:grid;gap:2px;padding:10px 18px;border:1.5px solid var(--rule);border-radius:10px;background:var(--card);text-align:center;min-width:150px}.dv b{font:600 15px var(--ui)}.dv small{font:12.5px var(--ui);color:var(--mute)}\n.dv input:checked+span{border-color:#222e4c;box-shadow:inset 0 0 0 1px #222e4c}.dv input:focus-visible+span{outline:2px solid #222e4c;outline-offset:2px}\n.fine{font:13px var(--ui);color:var(--mute);margin:14px 0 0}\n@media (max-width:600px){.sf{flex-direction:column}.dv span{min-width:0}.dv label{flex:1 1 100%}}\n.sbx{background:var(--paper);border-top:1px solid var(--rule)}\n#archive{background:var(--card)!important;border-top:1px solid var(--rule)!important}.sbm{background:var(--card)!important;border-top:1px solid var(--rule)}.svy{background:var(--card)!important}\nhtml{scroll-behavior:smooth}@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}#subscribe{scroll-margin-top:12px}\nheader nav{margin-left:auto}.hsub{display:inline-flex;align-items:center;min-height:40px;padding:0 18px;border-radius:6px;background:#222e4c;color:#fff;font:700 13px var(--ui);letter-spacing:.14em;text-transform:uppercase;text-decoration:none}.hsub:hover{background:#2c3a60}.hsub:focus-visible{outline:2px solid var(--link);outline-offset:3px}\n@media (max-width:600px){header .wrap{display:grid!important;grid-template-columns:minmax(0,1fr) auto;align-items:center;gap:8px 12px;padding-bottom:0!important}header .brand{grid-column:1;grid-row:1;min-width:0}header .brand span{white-space:nowrap}.hsub{grid-column:2;grid-row:1;margin:0;min-height:34px;padding:0 12px;font-size:11.5px}header nav{grid-column:1/-1;grid-row:2;margin:0 -16px!important;padding:8px 16px 9px;border-top:1px solid var(--rule);display:flex;gap:22px;font-size:14px}}\n@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .dv input:checked+span{border-color:var(--ink);box-shadow:inset 0 0 0 1px var(--ink)}:root:not([data-theme="light"]) .sf button,:root:not([data-theme="light"]) .hsub{background:#f2cfc6;color:#222e4c}}:root[data-theme="dark"] .dv input:checked+span{border-color:var(--ink);box-shadow:inset 0 0 0 1px var(--ink)}:root[data-theme="dark"] .sf button,:root[data-theme="dark"] .hsub{background:#f2cfc6;color:#222e4c}\n/* /subx */\n'
SUBX_BTN = '<!-- subx:btn --><a class="hsub" href="#subscribe" data-subscribe>Subscribe</a><!-- /subx:btn -->'
SUBX_SEC = '<!-- subx --><section id="subscribe" class="sbx" aria-labelledby="sx-h"><div class="wrap"><h2 id="sx-h">Have the next stories sent to you.</h2><p class="ld">Choose how much arrives at a time.</p><fieldset class="dv"><legend>Send me</legend><label><input type="radio" name="dv" value="1"><span><b>One story</b><small>as each is published</small></span></label><label><input type="radio" name="dv" value="3" checked><span><b>A few stories</b><small>two or three at a time</small></span></label><label><input type="radio" name="dv" value="all"><span><b>The full issue</b><small>four to six stories</small></span></label></fieldset><form class="sf" action="#" onsubmit="return false"><label class="vh" for="em-sub">Email address</label><input id="em-sub" type="email" name="email" autocomplete="email" placeholder="Your email address" required><button type="submit">Subscribe</button></form></div></section><!-- /subx -->\n'
def make(block, css, pre, home):
    h = src.replace('</style>', CSS_COMMON + css.replace('/* /survey */\n', '') + CSS_EF + '/* colo */' + FOOTER_CSS + '/* /colo */\n/* /survey */\n</style>', 1)
    h = add_sections(h, pre, FORM)
    h = h.replace('</style>', SUBX_CSS + '</style>', 1).replace('<a href="#">About</a>', '<a href="#about">About</a>')
    _n = h.index('</nav>', h.index('<nav aria-label="Site">')) + 6
    h = h[:_n] + SUBX_BTN + h[_n:]
    h = h.replace('<section id="archive"', SUBX_SEC + '<section id="archive"', 1)
    # Two issues band sits one place lower: after Subscribe, before the archive
    import re as _r
    _m = _r.search(r'<!-- nsadd:twoissues -->.*?<!-- /nsadd:twoissues -->', h, _r.S)
    if _m:
        _b = _m.group(0); h = h[:_m.start()] + h[_m.end():]
        h = h.replace('<section id="archive"', _b + chr(10) + '<section id="archive"', 1)
    # airmail strip under the header: off for now; restore by uncommenting
    # h = h.replace(HEADER_END, HEADER_END + airmail(pre, FORM), 1)
    h = h.replace('</body>', block + '<!-- colo -->\n' + footer_html(home, issue='../') + '\n<!-- /colo -->\n' + corner(pre) + DLG + '</body>', 1)
    # Take part: Contribute and Subscribe become two halves of one band (design shift 4)
    _s0 = h.index('<!-- subx --><section id="subscribe"'); _s1 = h.index('</section>', _s0) + len('</section>')
    _subsec = h[_s0 + len('<!-- subx -->'):_s1]; h = h[:_s0] + '<!-- tkp-here -->' + h[_s1:]
    h = re.sub(r'<!-- nsadd:submit -->.*?<!-- /nsadd:submit -->\n?', '', h, flags=re.S)
    h = h.replace('<!-- tkp-here -->', takepart_html(pre, _subsec).replace('.tkp{background:var(--card);', '.tkp{background:var(--paper);', 1), 1)
    # Earlier issues sits just above the footer
    _i = h.index('<section id="archive"'); _j = h.index('</div></section>', _i) + len('</div></section>')
    _a = h[_i:_j]; h = h[:_i] + h[_j:]
    h = h.replace('<!-- colo -->', _a + chr(10) + '<!-- colo -->', 1)
    h = re.sub(r'\n{3,}', '\n\n', h)
    return h

_main = make(F('../'), CSS_F, '../', './')
alt = make(B('../'), CSS_B, '../', '../')
# alt lives one level deeper
alt = alt.replace('src="../', 'src="../../').replace('href="../', 'href="../../').replace('href="./"', 'href="../"')
alt = alt.replace('<title>', '<meta name="robots" content="noindex"><title>', 1)
import os
os.makedirs('/home/claude/usbns/magazine/landing/alt', exist_ok=True)
import sys; sys.path.insert(0,'/home/claude/tab')
from typo import curl
OG=('<meta name="description" content="This issue explores the many ways creative expression can contribute to the transformation of individuals and communities, from music and visual art to the creative practices woven into grassroots efforts.">\n<meta property="og:type" content="website">\n<meta property="og:site_name" content="The American Bahá’í">\n<meta property="og:title" content="The American Bahá’í: The Arts Issue">\n<meta property="og:description" content="This issue explores the many ways creative expression can contribute to the transformation of individuals and communities, from music and visual art to the creative practices woven into grassroots efforts.">\n<meta property="og:url" content="https://aoaoaoa.github.io/usbns/magazine/landing/">\n<meta property="og:image" content="https://aoaoaoa.github.io/usbns/magazine/img/share-cover.jpg">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<meta name="twitter:card" content="summary_large_image">\n')
import re as _re
def _addog(h):
    h=_re.sub(r'<meta name="description"[^>]*>\n?|<meta (?:property="og:[^"]*"|name="twitter:card")[^>]*>\n?','',h)
    return h.replace('</title>','</title>\n'+OG.rstrip('\n'),1)

def _arch(h):
    h = re.sub(r'<p class="more"><a href="#">Browse every issue →</a></p>\n?', '', h)
    h = re.sub(r'<style id="archimg">.*?</style>\n?', '', h, flags=re.S)
    for k, hh in (('v57n4', 823), ('v57n2', 836), ('v57n1', 821), ('v56n1', 827)):
        h = re.sub(r'src="\.\./img/(?:art|cover)-' + k + r'\.jpg" alt="" width="640" height="\d+"', 'src="../img/cover-' + k + '.jpg" alt="" width="640" height="' + str(hh) + '"', h)
    if '.tile .cv.ph{' not in h:
        h = h.replace('</head>', '<style>.tile .cv.ph{padding:0!important;background:var(--card);overflow:hidden}.tile .cv.ph img{display:block;width:100%;height:100%;object-fit:cover}</style>\n</head>', 1)
    return h
_main = _arch(_main)
open(P, 'w').write(curl(_addog(_main)))
open('/home/claude/usbns/magazine/landing/alt/index.html', 'w').write(curl(alt))
print('ok')
