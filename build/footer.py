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
    ("Contribute", "Submit your story", "#", ' data-submit'),
    ("Every issue", "Subscribe", "/usbns/magazine/landing/#subscribe", ' data-subscribe'),
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
            f'<p class="cp">{PUBLISHER}</p></div></footer>' + ask_dialogs())

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
.colo .cp{font-size:12.5px;line-height:1.6;color:var(--mute);max-width:none;margin:0}@media (min-width:700px){.colo .cp{white-space:nowrap}}
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

# ---- Subscribe and Submit-your-story popups, shared by every page (emitted with the footer) ----
# Set these to the real endpoints; until then the forms validate and say plainly that sign-up / submissions open soon.
SUBSCRIBE_ACTION = ""
SUBMIT_ACTION = ""
_X = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 7l10 10M17 7 7 17" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
def ask_dialogs():
    sub = (f'<dialog class="askdlg" id="dlg-subscribe" aria-labelledby="dsu-h"><form method="dialog" class="dx"><button aria-label="Close">{_X}</button></form>'
        '<div class="dbody"><span class="dk">Subscribe</span><h2 id="dsu-h">Have the next stories sent to you.</h2><p class="dl2">By email, as they’re published. Choose how much arrives at a time.</p>'
        f'<form class="dform" data-action="{SUBSCRIBE_ACTION}" novalidate><fieldset class="dch"><legend class="vh">Send me</legend>'
        '<label><input type="radio" name="delivery" value="one"><span><b>One story</b><small>as each is published</small></span></label>'
        '<label><input type="radio" name="delivery" value="few" checked><span><b>A few stories</b><small>two or three at a time</small></span></label>'
        '<label><input type="radio" name="delivery" value="issue"><span><b>The full issue</b><small>four to six stories</small></span></label></fieldset>'
        '<label class="dfl"><span>Email address</span><input type="email" name="email" autocomplete="email" required placeholder="you@example.org"></label>'
        '<button class="dgo" type="submit">Subscribe</button><p class="dfine">Unsubscribe from any email.</p></form>'
        '<div class="ddone" hidden><h3>Thank you.</h3><p>Email sign-up opens soon; we’ll have the next stories ready for you.</p></div></div></dialog>')
    st = (f'<dialog class="askdlg wide" id="dlg-submit" aria-labelledby="dsb-h"><form method="dialog" class="dx"><button aria-label="Close">{_X}</button></form>'
        '<div class="dbody"><span class="dk">Contribute</span><h2 id="dsb-h">Know a story like these?</h2>'
        '<div class="dnote"><p>There are amazing stories of unity and spiritual growth happening in neighborhoods everyday as a result of the community building process inspired by the teachings of the Bahá’í Faith.</p>'
        '<p><b>We need your help to find them and share them!</b> Please send us story ideas, article leads, photos of community activities, your field notes on how community building unfolds where you live, and what is being learned along the way.</p></div>'
        f'<form class="dform sform" data-action="{SUBMIT_ACTION}" enctype="multipart/form-data" novalidate>'
        '<ol class="steps">'
        '<li><span class="sn" aria-hidden="true">1</span><div class="sb"><h3>What happened, and where</h3>'
        '<label class="dfl ln"><span>Where</span><input name="place" placeholder="Town or neighborhood, state" required></label>'
        '<label class="dfl ln"><span>What happened <small>A few paragraphs is plenty.</small></span><textarea name="story" rows="6" required></textarea></label></div></li>'
        '<li><span class="sn" aria-hidden="true">2</span><div class="sb"><h3>Who was there</h3>'
        '<label class="dfl ln"><span class="vh">Who was there</span><input name="people" placeholder="Names only with their permission"></label></div></li>'
        '<li><span class="sn" aria-hidden="true">3</span><div class="sb"><h3>A photograph or two</h3>'
        '<label class="drop"><input type="file" name="photos" accept="image/*" multiple class="vh"><span class="dz"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h3l2-2h6l2 2h3v12H4z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><circle cx="12" cy="13" r="3.5" fill="none" stroke="currentColor" stroke-width="1.6"/></svg><b>Choose photographs</b><small class="dzn">JPEG or PNG, as many as you like</small></span></label>'
        '<label class="dfl ln"><span>Photographer’s name</span><input name="photographer"></label></div></li>'
        '<li><span class="sn" aria-hidden="true">4</span><div class="sb"><h3>What you learned</h3>'
        '<label class="dfl ln"><span class="vh">What you learned</span><textarea name="learned" rows="3" placeholder="What others could take from it"></textarea></label></div></li>'
        '</ol>'
        '<fieldset class="you"><legend>About you</legend><div class="two">'
        '<label class="dfl ln"><span>Your name</span><input name="name" autocomplete="name" required></label>'
        '<label class="dfl ln"><span>Email address</span><input type="email" name="email" autocomplete="email" required></label></div>'
        '<p class="dfine l">We’ll write before publishing anything you send.</p></fieldset>'
        '<button class="dgo" type="submit">Send your story</button></form>'
        '<div class="ddone" hidden><h3>Thank you.</h3><p>Story submissions open soon. Please keep your notes and photographs; we’d love to receive them.</p></div></div></dialog>')
    return sub + st + ASK_JS

ASK_JS = r'''<script>(function(){
var D={subscribe:document.getElementById('dlg-subscribe'),submit:document.getElementById('dlg-submit')};if(!D.subscribe||!D.submit||!D.subscribe.showModal)return;
function kind(a){if(a.closest('dialog'))return null;if(a.hasAttribute('data-subscribe'))return 'subscribe';if(a.hasAttribute('data-submit'))return 'submit';var h=a.getAttribute('href')||'';if(/#subscribe$/.test(h)&&!document.querySelector('section#subscribe'))return 'subscribe';return null}
document.addEventListener('click',function(e){if(e.defaultPrevented&&!e.target.closest('.nudge'))return;var a=e.target.closest('a,button');if(!a)return;var k=kind(a);if(!k)return;e.preventDefault();var d=D[k];
  d.querySelector('.dform').hidden=false;d.querySelector('.ddone').hidden=true;d.showModal();var f=d.querySelector('input:not([type=radio]):not([type=file]),textarea');if(f)setTimeout(function(){f.focus()},30)},true);
[].forEach.call(document.querySelectorAll('.askdlg .drop'),function(l){var i=l.querySelector('input'),n=l.querySelector('.dzn'),b=l.querySelector('b'),t0=n.textContent;i.addEventListener('change',function(){var k=i.files.length;l.classList.toggle('has',k>0);b.textContent=k?(k==1?i.files[0].name:k+' photographs chosen'):'Choose photographs';n.textContent=k?'Choose again to replace':t0});['dragenter','dragover'].forEach(function(v){l.addEventListener(v,function(){l.classList.add('over')})});['dragleave','drop'].forEach(function(v){l.addEventListener(v,function(){l.classList.remove('over')})})});[D.subscribe,D.submit].forEach(function(d){d.addEventListener('click',function(e){if(e.target===d)d.close()});
  var f=d.querySelector('.dform');f.addEventListener('submit',function(e){e.preventDefault();var bad=[].slice.call(f.querySelectorAll('[required]')).filter(function(x){return !x.checkValidity()});
    f.querySelectorAll('.dfl').forEach(function(l){l.classList.remove('err')});if(bad.length){bad.forEach(function(x){x.closest('.dfl').classList.add('err')});bad[0].focus();return}
    var act=f.dataset.action;if(act){fetch(act,{method:'POST',body:new FormData(f)}).catch(function(){})}
    f.hidden=true;var dn=d.querySelector('.ddone');dn.hidden=false;dn.setAttribute('tabindex','-1');dn.focus()})})})();</script>'''

ASK_CSS = """
.askdlg{border:0;padding:0;border-radius:14px;width:min(560px,calc(100vw - 24px));max-height:calc(100dvh - 24px);background:var(--card,var(--bar,#fdfcf9));color:var(--ink,#1d1a16);box-shadow:0 24px 60px rgba(20,16,10,.3);overflow:auto;font-family:var(--ui,system-ui,sans-serif)}
.askdlg.wide{width:min(720px,calc(100vw - 24px))}
.askdlg::backdrop{background:rgba(20,16,10,.45)}
.askdlg[open]{animation:dlgin .25s ease-out}@keyframes dlgin{from{opacity:0;transform:translateY(12px)}}
.askdlg .dx{position:sticky;top:0;display:flex;justify-content:flex-end;margin:0;padding:10px 10px 0;height:0;z-index:2}
.askdlg .dx button{width:40px;height:40px;border-radius:50%;border:0;background:var(--card,var(--bar,#fdfcf9));color:var(--mute,#6a635a);cursor:pointer;display:grid;place-items:center}.askdlg .dx svg{width:20px;height:20px}.askdlg .dx button:hover{color:var(--ink,#1d1a16)}
.askdlg .dbody{padding:30px 30px 28px}
.askdlg .dk{display:block;font:700 11px/1 var(--ui,sans-serif);letter-spacing:.2em;text-transform:uppercase;color:#b8782e;margin:0 0 10px}
.askdlg h2{font:800 clamp(24px,3vw,30px)/1.12 "Literata",Georgia,serif;letter-spacing:-.015em;margin:0 0 8px;padding-right:36px}
.askdlg .dl2{margin:0 0 18px;font-size:15px;color:var(--mute,#6a635a)}
.askdlg .dnote{position:relative;background:#fffdf6;color:#1d1a16;padding:16px 20px 14px;margin:14px 2px 22px;box-shadow:0 8px 20px rgba(29,26,22,.12);transform:rotate(-.6deg)}
.askdlg .dnote::before{content:"";position:absolute;top:-9px;left:50%;width:80px;height:20px;transform:translateX(-50%) rotate(2deg);background:rgba(242,207,198,.85)}
.askdlg .dnote p{font:15px/1.55 "Literata",Georgia,serif;margin:0 0 6px}.askdlg .dnote p:last-child{margin:0}
.askdlg .dch{border:0;margin:0 0 16px;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}
.askdlg .dch label{cursor:pointer;position:relative}.askdlg .dch input{position:absolute;opacity:0}
.askdlg .dch span{display:grid;gap:2px;height:100%;padding:10px 12px;border:1.5px solid var(--rule,#d9d2c4);border-radius:10px;text-align:center}
.askdlg .dch b{font-weight:600;font-size:14.5px}.askdlg .dch small{font-size:12px;color:var(--mute,#6a635a)}
.askdlg .dch input:checked+span{border-color:var(--ink,#1d1a16);box-shadow:inset 0 0 0 1px var(--ink,#1d1a16)}.askdlg .dch input:focus-visible+span{outline:2px solid #b8782e;outline-offset:2px}
.askdlg .dgrid{display:grid;grid-template-columns:1fr 1fr;gap:14px 16px;margin:0 0 18px}.askdlg .dfl.full{grid-column:1/-1}
.askdlg .dfl{display:grid;gap:6px;margin:0 0 14px}.askdlg .dgrid .dfl{margin:0}
.askdlg .dfl>span{font-weight:600;font-size:13.5px}.askdlg .dfl small{font-weight:400;color:var(--mute,#6a635a);margin-left:6px}
.askdlg input:not([type=radio]),.askdlg textarea{width:100%;box-sizing:border-box;min-height:46px;border:1.5px solid var(--rule,#d9d2c4);border-radius:10px;padding:10px 14px;font:16px var(--ui,sans-serif);background:var(--paper,#f5f1e8);color:var(--ink,#1d1a16)}
.askdlg textarea{resize:vertical;line-height:1.5}.askdlg input[type=file]{padding:10px;font-size:14px}
.askdlg input:focus,.askdlg textarea:focus{outline:2px solid #222e4c;outline-offset:1px}
.askdlg .dfl.err input,.askdlg .dfl.err textarea{border-color:#c9462c}.askdlg .dfl.err>span::after{content:" required";color:#c9462c;font-weight:500}
.askdlg .dgo{width:100%;min-height:50px;border:0;border-radius:999px;background:#222e4c;color:#fff;font:600 16px var(--ui,sans-serif);cursor:pointer}.askdlg .dgo:hover{background:#2c3a60}
.askdlg .dfine{margin:12px 0 0;text-align:center;font-size:13px;color:var(--mute,#6a635a)}
.askdlg .ddone{padding:10px 0 4px}.askdlg .ddone h3{font:700 22px "Literata",Georgia,serif;margin:0 0 6px}.askdlg .ddone p{margin:0;color:var(--mute,#6a635a);font-size:15.5px;line-height:1.5}.askdlg .ddone:focus{outline:none}
.vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.askdlg .steps{list-style:none;margin:0 0 6px;padding:0;counter-reset:none}
.askdlg .steps>li{display:grid;grid-template-columns:40px minmax(0,1fr);gap:0 14px;padding:16px 0 18px;border-top:1px solid var(--rule,#d9d2c4)}
.askdlg .sn{font:800 30px/1 var(--disp,"Bricolage Grotesque",sans-serif);color:#b8782e;letter-spacing:-.03em;padding-top:2px}
.askdlg .sb h3{margin:4px 0 10px;font:700 17px/1.25 "Literata",Georgia,serif}
.askdlg .dfl.ln{margin:0 0 12px}.askdlg .dfl.ln:last-child{margin-bottom:0}
.askdlg .dfl.ln>span{font:600 11.5px var(--ui,sans-serif);letter-spacing:.12em;text-transform:uppercase;color:var(--mute,#6a635a)}.askdlg .dfl.ln>span small{text-transform:none;letter-spacing:0;font-size:12.5px}
.askdlg .dfl.ln input,.askdlg .dfl.ln textarea{border:0;border-bottom:1.5px solid var(--rule,#d9d2c4);border-radius:0;background:transparent;padding:8px 2px;min-height:40px}
.askdlg .dfl.ln textarea{background:repeating-linear-gradient(transparent 0 31px,var(--rule,#d9d2c4) 31px 32px);line-height:32px;padding:0 2px;border-bottom:0}
.askdlg .dfl.ln input:focus,.askdlg .dfl.ln textarea:focus{outline:none;border-bottom-color:#222e4c;box-shadow:0 2px 0 #222e4c}
.askdlg .dfl.ln textarea:focus{box-shadow:inset 0 -2px 0 #222e4c}
.askdlg .dfl.ln.err input,.askdlg .dfl.ln.err textarea{border-bottom-color:#c9462c;box-shadow:0 2px 0 #c9462c}
.askdlg .drop{display:block;cursor:pointer;margin:0 0 12px}.askdlg .dz{display:grid;justify-items:center;gap:4px;padding:18px 14px;border:1.5px dashed #b8782e;border-radius:10px;text-align:center;color:var(--ink,#1d1a16);transition:background .2s}
.askdlg .dz svg{width:28px;height:28px;color:#b8782e}.askdlg .dz b{font-weight:600;font-size:15px}.askdlg .dz small{font-size:12.5px;color:var(--mute,#6a635a)}
.askdlg .drop:hover .dz,.askdlg .drop.over .dz{background:rgba(184,120,46,.08)}.askdlg .drop input:focus-visible+.dz{outline:2px solid #222e4c;outline-offset:2px}.askdlg .drop.has .dz{border-style:solid}
.askdlg .you{border:0;margin:0 0 18px;padding:16px 0 0;border-top:1px solid var(--rule,#d9d2c4)}.askdlg .you legend{font:700 17px "Literata",Georgia,serif;padding:0;margin:0 0 10px;float:left;width:100%}
.askdlg .two{clear:both;display:grid;grid-template-columns:1fr 1fr;gap:0 18px;align-items:end}.askdlg .two .dfl{margin:0}.askdlg .dfine.l{text-align:left;margin:4px 0 0}
@media (max-width:560px){.askdlg .two{grid-template-columns:1fr}.askdlg .steps>li{grid-template-columns:30px minmax(0,1fr);gap:0 10px}.askdlg .sn{font-size:24px}}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .askdlg .dgo{background:#f2cfc6;color:#222e4c}}:root[data-theme="dark"] .askdlg .dgo{background:#f2cfc6;color:#222e4c}
@media (max-width:560px){.askdlg .dbody{padding:26px 18px 20px}.askdlg .dch{grid-template-columns:1fr}.askdlg .dgrid{grid-template-columns:1fr}}
@media (prefers-reduced-motion:reduce){.askdlg[open]{animation:none}}
"""
FOOTER_CSS += ASK_CSS
