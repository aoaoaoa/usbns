# shared pieces for the story invitation gallery (stories_gallery.py). The first five studies; B is set aside.
import json, os
D = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(D, "usmap.json")))
TINT = {"gregory": "#e8532a", "newyorkers": "#f05a7e", "twoartists": "#b07a4a", "abs": "#c9462c", "endeavor": "#1b5e6b", "comic": "#5b4a8a"}
STORY_AT = {"Hemingway, SC": "gregory", "Charleston, SC": "gregory", "Crown Heights, Brooklyn": "newyorkers", "Harlem, New York": "newyorkers",
            "Los Angeles, CA": "twoartists", "Indianapolis, IN": "comic"}
I = "../../img/"
E = "../../"

dots = []
for k, (x, y) in M["places"].items():
    s = STORY_AT.get(k)
    c = TINT[s] if s else TINT["endeavor"]
    r = 5.5 if s else 3.2
    dots.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" class="{"big" if s else ""}"><title>{k}</title></circle>')
MAP = (f'<svg class="usm" viewBox="-8 -8 {M["w"]+16} {M["h"]+16}" role="img" aria-label="Map of the United States with {len(M["places"])} places named in this issue">'
       f'<path d="{M["nation"]}" class="na"/><path d="{M["states"]}" class="st"/>{"".join(dots)}'
       '<g class="you" hidden><circle r="9" class="yr"/><circle r="4.5" class="yd"/></g></svg>')
NPL = len(M["places"])

PRINT = ('<p>There are amazing stories of unity and spiritual growth happening in neighborhoods everyday as a result of the community building process inspired by the teachings of the Bahá’í Faith.</p>'
         '<p><b>We need your help to find them and share them!</b> Please send us story ideas, article leads, photos of community activities, your field notes on how community building unfolds where you live, and what is being learned along the way.</p>')
PROMISE = '<p class="prom">We’ll write before publishing anything you send. Prefer email? <a href="mailto:tab@usbnc.org">tab@usbnc.org</a></p>'
DONE = '<div class="done" hidden><b>Thank you.</b> Story submissions open soon. This study keeps nothing you type.</div>'

def form(extra=""):
    return ('<form class="sf" novalidate>' + extra +
            '<label>Your story<textarea rows="4" placeholder="A few lines is plenty. Write it the way you’d tell a friend."></textarea></label>'
            '<div class="two"><label>Your name<input autocomplete="name"></label><label>Email or phone<input autocomplete="email"></label></div>'
            '<button class="sbtn" type="submit">Send your story <span aria-hidden="true">→</span></button></form>' + DONE)

# A · the map
A = f'''<section class="ap" id="A" data-n="The map">
<p class="kk">Contribute</p><h1>Every story in this issue began as a report from a community.</h1>
<p class="ld">Below are some of the places named in this issue. Yours next?</p>
<div class="mapw">{MAP}
<ul class="key"><li><i style="--c:{TINT['gregory']}"></i>Hemingway, South Carolina</li><li><i style="--c:{TINT['newyorkers']}"></i>Crown Heights, Brooklyn</li><li><i style="--c:{TINT['twoartists']}"></i>Los Angeles</li><li><i style="--c:{TINT['comic']}"></i>Indianapolis</li><li><i style="--c:{TINT['endeavor']}"></i>Communities engage in a common endeavor</li></ul></div>
<form class="where" novalidate><label for="aw">Where are you?</label><div class="wr"><input id="aw" placeholder="City or neighborhood, state" list="aws"><button class="sbtn" type="submit">Add your town</button></div>
<datalist id="aws">{"".join(f'<option value="{k}">' for k in M["places"])}</datalist></form>
<div class="unf" hidden><p class="yt"></p>{form()}</div>{PROMISE}</section>'''

# B · one question at a time
Q = [("Where did it happen?", '<input placeholder="City or neighborhood, state">', ""),
     ("What happened?", '<textarea rows="5" placeholder="A few lines is plenty. Write it the way you’d tell a friend."></textarea>', "Any language is fine."),
     ("Who was there?", '<input placeholder="Neighbors, a children’s class, a study circle…">', "Names only with their permission."),
     ("Any photographs?", '<input type="file" accept="image/jpeg,image/png" multiple><input placeholder="Photographer’s name">', "JPEG or PNG, as many as you like."),
     ("What did you learn?", '<textarea rows="3" placeholder="What others could take from it"></textarea>', ""),
     ("How can we reach you?", '<input placeholder="Your name" autocomplete="name"><input placeholder="Email or phone" autocomplete="email">', "We’ll write before publishing anything you send.")]
steps = "".join(f'<fieldset class="q" data-i="{i}"{"" if i==0 else " hidden"}><legend><span class="qn">{i+1} of {len(Q)}</span>{t}</legend>{f}{("<small>"+h+"</small>") if h else ""}</fieldset>' for i, (t, f, h) in enumerate(Q))
B = f'''<section class="ap" id="B" data-n="One question at a time" hidden>
<div class="bq"><div class="bl"><p class="kk">Contribute</p><h1>Tell us what happened.</h1><p class="ld">Six short questions. Skip any you like.</p>
<img src="{I}story-paint.webp" alt="Children’s hands at a watercolor set beside paintings, one lettered I am kind, loving, and friendly" width="1400" height="1203"></div>
<form class="steps" novalidate><div class="bar" aria-hidden="true"><i></i></div>{steps}
<div class="nav"><button type="button" class="bk">Back</button><button type="button" class="sk">Skip</button><button type="submit" class="sbtn nx">Next <span aria-hidden="true">→</span></button></div></form>{DONE}</div>
{PROMISE}</section>'''

# C · story starters, each tied to the story in this issue that began that way
ST = [("Neighbors came together", "newyorkers", "ny-film.jpg", "Harlem"),
      ("Children learned or made something", "newyorkers", "story-paint.webp", "Crown Heights, Brooklyn"),
      ("Young people took something on", "comic", "comic-1.jpg", "Indianapolis"),
      ("A conversation opened something up", "endeavor", "az-ace.jpg", "Las Vegas"),
      ("A person or place made a difference", "gregory", "gregory-group-hd.jpg", "Hemingway, South Carolina"),
      ("Creativity brought people closer", "twoartists", "ta-portrait.jpg", "Los Angeles")]
cards = "".join(f'<button type="button" class="st" style="--c:{TINT[s]}" data-p="{t}"><img src="{I}{im}" alt="" loading="lazy"><span><b>{t}</b><small>Like <a href="{E}{s}/">{pl}</a></small></span></button>' for t, s, im, pl in ST)
C = f'''<section class="ap" id="C" data-n="Story starters" hidden>
<p class="kk">Contribute</p><h1>Do you have a story?</h1><p class="ld">Each story in this issue started with something small.</p>
<div class="sts">{cards}<button type="button" class="st own" data-p="Something else"><span><b>Something else</b><small>Start from a blank page</small></span></button></div>
<div class="unf" hidden><p class="yt"></p>{form('<label>Where<input placeholder="City or neighborhood, state"></label>')}</div>{PROMISE}</section>'''

# D · any way you can
W = [("w", "Write a few lines", "pen"), ("v", "Record a voice note", "mic"), ("p", "Send photographs", "cam"), ("l", "Pass along a lead", "arrow"), ("g", "Use your own language", "globe")]
ICO = {"pen": '<path d="M4 20l4-1 11-11-3-3L5 16z"/><path d="M14 6l3 3"/>', "mic": '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0014 0M12 18v3"/>',
       "cam": '<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>', "arrow": '<path d="M4 12h14M13 6l6 6-6 6"/>',
       "globe": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.6 2.6 2.6 14.4 0 17M12 3.5c-2.6 2.6-2.6 14.4 0 17"/>'}
tiles = "".join(f'<button type="button" class="wy" data-w="{k}" aria-pressed="false"><svg viewBox="0 0 24 24" aria-hidden="true">{ICO[ic]}</svg>{t}</button>' for k, t, ic in W)
pan = {
 "w": '<label>Tell us your story<textarea rows="5" placeholder="A few lines is plenty. Write it the way you’d tell a friend."></textarea></label>',
 "v": '<div class="rec"><button type="button" class="rb"><i></i><span>Start recording</span></button><span class="rt">Up to 3 minutes, in your own words.</span><audio controls hidden></audio></div>',
 "p": '<label>Photographs<input type="file" accept="image/jpeg,image/png" multiple></label><label>Who took them<input placeholder="Photographer’s name"></label><label>A line about the photograph<input placeholder="Where it was taken, and what we’re seeing"></label>',
 "l": '<label>Who or what should we know about?<textarea rows="3" placeholder="A person, a gathering, a project. We’ll follow up."></textarea></label><label>How to reach them, if you know<input></label>',
 "g": '<label>Language<input placeholder="Español, Tagalog, Farsi, ASL…"></label><label>Your story, in that language<textarea rows="4"></textarea></label>'}
pans = "".join(f'<div class="pn" data-w="{k}" hidden>{v}</div>' for k, v in pan.items())
Dsec = f'''<section class="ap" id="D" data-n="Any way you can" hidden>
<p class="kk">Contribute</p><h1>Send it however it comes to you.</h1><p class="ld">Every story in this issue began as a report from a community. Yours can begin as a few lines, a voice note, a photograph or a name.</p>
<div class="wys" role="group" aria-label="How would you like to send it?">{tiles}</div>
<form class="sf dw" novalidate hidden>{pans}<div class="two"><label>Your name<input autocomplete="name"></label><label>Email or phone<input autocomplete="email"></label></div>
<button class="sbtn" type="submit">Send <span aria-hidden="true">→</span></button></form>{DONE}{PROMISE}</section>'''

# E · from report to page
pages = "".join(f'<a href="{E}{s}/" style="--c:{TINT[s]}"><img src="{I}{im}" alt="" loading="lazy"><span>{pl}</span></a>' for s, im, pl in
                [("gregory", "gregory-group-hd.jpg", "Hemingway, South Carolina"), ("newyorkers", "ny-park.jpg", "Crown Heights, Brooklyn"), ("twoartists", "ta-portrait.jpg", "Los Angeles")])
Esec = f'''<section class="ap" id="E" data-n="From report to page" hidden>
<p class="kk">Contribute</p><h1>Every story in this issue began as a report from a community.</h1>
<ol class="rt3">
<li><span class="no">1</span><b>You send a few paragraphs</b><div class="nt">{PRINT}</div></li>
<li><span class="no">2</span><b>Our editors read every item</b></li>
<li><span class="no">3</span><b>We contact you before anything is published</b><div class="pg">{pages}</div></li></ol>
<div class="ef">{form('<label>Where<input placeholder="City or neighborhood, state"></label>')}</div><p class="prom">Prefer email? <a href="mailto:tab@usbnc.org">tab@usbnc.org</a></p></section>'''

CSS = r'''
:root{--paper:#f5f1e8;--card:#fdfcf9;--ink:#1d1a16;--soft:#3d3831;--mute:#6a635a;--rule:#d9d2c4;--link:#1b5e6b;--ph:#e7e1d4;--navy:#222e4c;--blush:#f2cfc6;--gold:#b8782e;--ui:"Bricolage Grotesque",system-ui,sans-serif;--text:"Literata",Georgia,serif;--cond:"Barlow Condensed","Arial Narrow",sans-serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#17150f;--card:#211e17;--ink:#f1ece2;--soft:#d6cfc2;--mute:#a59d90;--rule:#3a352c;--link:#7cc0cc;--ph:#2a2620;--navy:#f2cfc6;--blush:#222e4c;--gold:#e0a85e}}
:root[data-theme="dark"]{--paper:#17150f;--card:#211e17;--ink:#f1ece2;--soft:#d6cfc2;--mute:#a59d90;--rule:#3a352c;--link:#7cc0cc;--ph:#2a2620;--navy:#f2cfc6;--blush:#222e4c;--gold:#e0a85e}
*{box-sizing:border-box}[hidden]{display:none!important}html{-webkit-text-size-adjust:100%}body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.55 var(--text)}
a{color:var(--link);text-decoration-thickness:1px;text-underline-offset:3px}
.bar0{position:sticky;top:0;z-index:5;background:var(--card);border-bottom:1px solid var(--rule);font:13px var(--ui);display:flex;gap:6px;align-items:center;padding:8px 16px;overflow-x:auto;scrollbar-width:none}
.bar0 b{font-weight:700;letter-spacing:.12em;text-transform:uppercase;font-size:11px;color:var(--mute);white-space:nowrap;margin-right:6px}
.bar0 button{font:600 13px var(--ui);border:1px solid var(--rule);background:none;color:var(--ink);border-radius:999px;padding:6px 12px;cursor:pointer;white-space:nowrap}
.bar0 button[aria-pressed=true]{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.bar0 .nk{margin-left:auto;color:var(--mute);white-space:nowrap}
.ap{max-width:1040px;margin:0 auto;padding:clamp(40px,7vw,88px) 16px 72px;text-align:center}
.kk{font:700 12px/1 var(--ui);letter-spacing:.18em;text-transform:uppercase;color:var(--gold);margin:0 0 14px}
.kk::before{content:"";display:block;width:94px;height:4px;border:1px solid var(--ink);border-width:1px 0;margin:0 auto 14px}
h1{font:700 clamp(32px,4.6vw,54px)/1.06 var(--text);letter-spacing:-.01em;margin:0 auto 16px;max-width:20ch;text-wrap:balance}
.ld{font-size:clamp(17px,1.6vw,20px);color:var(--soft);margin:0 auto 32px;max-width:44ch;text-wrap:balance}
.sbtn{display:inline-flex;align-items:center;gap:10px;font:700 19px/1 var(--cond);letter-spacing:.04em;text-transform:uppercase;border:0;background:var(--navy);color:var(--blush);padding:14px 24px;border-radius:3px;cursor:pointer;white-space:nowrap}
.sbtn:focus-visible,button:focus-visible,input:focus-visible,textarea:focus-visible{outline:2px solid var(--link);outline-offset:2px}
.sf,.steps{display:grid;gap:14px;text-align:left;max-width:640px;margin:0 auto}
label,legend{display:grid;gap:6px;font:600 14px var(--ui);color:var(--soft)}
input,textarea{font:16px/1.4 var(--text);color:var(--ink);background:var(--card);border:1px solid var(--rule);border-radius:4px;padding:11px 12px;width:100%}
textarea{resize:vertical}
.two{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.sf .sbtn{justify-self:start}
.prom{font:14px/1.5 var(--ui);color:var(--mute);margin:26px auto 0}
.done{max-width:640px;margin:18px auto 0;background:var(--card);border:1px solid var(--rule);border-left:4px solid var(--gold);padding:16px 18px;text-align:left;font:15px/1.5 var(--ui)}
/* A */
.mapw{position:relative;max-width:820px;margin:0 auto 26px}
.usm{width:100%;height:auto;display:block}
.usm .na{fill:var(--ph)}.usm .st{fill:none;stroke:var(--paper);stroke-width:.8}
.usm circle{stroke:var(--paper);stroke-width:1.2}.usm circle.big{stroke-width:1.6}
.usm .yr{fill:none;stroke:var(--gold);stroke-width:2}.usm .yd{fill:var(--gold);stroke:none}
.key{list-style:none;margin:10px 0 0;padding:0;display:flex;flex-wrap:wrap;justify-content:center;gap:4px 16px;font:700 14px/1.5 var(--cond);letter-spacing:.06em;text-transform:uppercase;color:var(--soft)}
.key i{display:inline-block;width:10px;height:10px;border-radius:50%;background:var(--c);margin-right:6px;vertical-align:-1px}
.where{max-width:640px;margin:0 auto 22px;text-align:left}.where label{margin-bottom:6px}
.wr{display:flex;gap:10px}.wr input{flex:1;min-width:0}
.yt{font:700 18px var(--cond);letter-spacing:.06em;text-transform:uppercase;color:var(--gold);margin:6px 0 14px}
/* B */
.bq{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1fr);gap:clamp(28px,5vw,64px);align-items:start;text-align:left}
.bq h1,.bq .ld{margin-left:0}.bq .kk::before{margin-left:0}.bq img{width:min(260px,70%);height:auto;display:block}
.steps{max-width:none;margin:0;min-height:300px;align-content:start}
.bar{height:4px;background:var(--rule);border-radius:2px;overflow:hidden}.bar i{display:block;height:100%;width:0;background:var(--gold);transition:width .3s}
.q{border:0;margin:0;padding:0;display:grid;gap:12px}
.q legend{font:700 clamp(24px,2.8vw,32px)/1.15 var(--text);color:var(--ink);padding:0;margin-bottom:12px}
.qn{display:block;font:700 12px var(--ui);letter-spacing:.14em;text-transform:uppercase;color:var(--mute);margin-bottom:8px}
.q small{font:14px var(--ui);color:var(--mute)}
.nav{display:flex;gap:10px;align-items:center;margin-top:8px}
.nav .bk,.nav .sk{font:600 15px var(--ui);background:none;border:0;color:var(--soft);cursor:pointer;padding:10px 6px}
.nav .nx{margin-left:auto}
/* C */
.sts{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:14px;margin:0 auto 26px;text-align:left}
.st{display:grid;grid-template-columns:76px 1fr;gap:12px;align-items:center;background:var(--card);border:1px solid var(--rule);border-left:5px solid var(--c,var(--gold));border-radius:4px;padding:10px;cursor:pointer;color:var(--ink);font:inherit;text-align:left}
.st img{width:76px;height:76px;object-fit:cover;border-radius:2px;display:block}
.st b{display:block;font:600 17px/1.25 var(--text);margin-bottom:4px}.st small{font:13px var(--ui);color:var(--mute)}
.st.own{grid-template-columns:1fr;border-left-style:dashed;grid-column:1/-1;text-align:center;justify-items:center}
.st[aria-pressed=true]{outline:2px solid var(--c,var(--gold));outline-offset:2px}
/* D */
.wys{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin:0 auto 26px;max-width:760px}
.wy{display:inline-flex;align-items:center;gap:10px;font:600 16px var(--ui);background:var(--card);color:var(--ink);border:1px solid var(--rule);border-radius:999px;padding:12px 18px;cursor:pointer}
.wy svg{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
.wy[aria-pressed=true]{background:var(--navy);color:var(--blush);border-color:var(--navy)}
.rec{display:grid;gap:10px;justify-items:start}
.rb{display:inline-flex;align-items:center;gap:10px;font:600 16px var(--ui);background:var(--card);color:var(--ink);border:1px solid var(--rule);border-radius:999px;padding:12px 18px;cursor:pointer}
.rb i{width:12px;height:12px;border-radius:50%;background:#c9462c}.rb.on i{border-radius:2px}
.rt{font:14px var(--ui);color:var(--mute)}
/* E */
.rt3{list-style:none;padding:0;margin:8px 0 36px;display:grid;grid-template-columns:1.25fr 1fr 1fr;gap:28px;text-align:left;position:relative}
.rt3::before{content:"";position:absolute;left:0;right:0;top:30px;height:5px;background:repeating-linear-gradient(-45deg,#c9462c 0 10px,transparent 10px 14px,#2f4f6e 14px 24px,transparent 24px 28px);opacity:.85}
.rt3 .no{position:relative;display:grid;place-items:center;width:62px;height:62px;border-radius:50%;background:var(--paper);border:2px solid var(--ink);font:italic 700 30px/1 var(--text);margin-bottom:14px}
.rt3 li:last-child .no{background:var(--navy);border-color:var(--navy);color:var(--blush)}
.rt3>li>b{display:block;font:700 20px/1.1 var(--cond);letter-spacing:.04em;text-transform:uppercase;margin-bottom:8px}
.rt3 .sm{font:15px/1.5 var(--ui);color:var(--mute);margin:0 0 12px}
.nt{background:#fffdf6;color:#1d1a16;box-shadow:0 8px 22px rgba(29,26,22,.12);padding:14px 16px;transform:rotate(-.8deg);font-size:15px;line-height:1.5}.nt p{margin:0 0 .6em}.nt p:last-child{margin:0}
.pg{display:grid;gap:8px}.pg a{display:grid;grid-template-columns:54px 1fr;gap:10px;align-items:center;text-decoration:none;color:var(--ink);font:700 14px/1.2 var(--cond);letter-spacing:.05em;text-transform:uppercase;border-left:4px solid var(--c);padding-left:8px}
.pg img{width:54px;height:40px;object-fit:cover;display:block}
.ef{max-width:640px;margin:0 auto}
@media (max-width:760px){.bq,.rt3{grid-template-columns:1fr}.rt3::before{display:none}.bq img{display:none}.two{grid-template-columns:1fr}.wr{flex-direction:column}.wr .sbtn{justify-content:center}}
@media (prefers-reduced-motion:reduce){.bar i{transition:none}}
'''

JS = r'''
(function(){var bar=document.querySelector('.bar0'),S=[].slice.call(document.querySelectorAll('.ap'));
S.forEach(function(s){var b=document.createElement('button');b.type='button';b.textContent=s.id+' · '+s.dataset.n;b.setAttribute('aria-pressed',!s.hidden);b.onclick=function(){go(s.id)};bar.insertBefore(b,bar.querySelector('.nk'))});
function go(id){S.forEach(function(s){s.hidden=s.id!==id});[].forEach.call(bar.querySelectorAll('button'),function(b){b.setAttribute('aria-pressed',b.textContent[0]===id)});history.replaceState(null,'','#'+id);scrollTo(0,0)}
function hs(){if(/^#[A-E]$/.test(location.hash))go(location.hash[1])}hs();addEventListener('hashchange',hs);
function done(f){var d=f.parentNode.querySelector('.done')||f.closest('.ap').querySelector('.done');f.hidden=true;if(d){d.hidden=false;d.setAttribute('tabindex','-1');d.focus()}}
[].forEach.call(document.querySelectorAll('form.sf'),function(f){f.addEventListener('submit',function(e){e.preventDefault();done(f)})});
// A: add your town
var PL=__PL__,A=document.getElementById('A'),wf=A.querySelector('.where'),you=A.querySelector('.you');
wf.addEventListener('submit',function(e){e.preventDefault();var v=wf.querySelector('input').value.trim();if(!v)return;var u=A.querySelector('.unf');
  var p=PL[v];if(p){you.setAttribute('transform','translate('+p[0]+','+p[1]+')');you.hidden=false}else you.hidden=true;
  u.querySelector('.yt').textContent=v+(p?' · already in this issue. Tell us what’s new.':' · the next place in this issue?');u.hidden=false;u.querySelector('textarea').focus()});
// B: one question at a time
var B=document.getElementById('B'),f=B.querySelector('.steps'),Q=[].slice.call(f.querySelectorAll('.q')),k=0,nx=f.querySelector('.nx'),bk=f.querySelector('.bk'),bi=f.querySelector('.bar i');
function show(){Q.forEach(function(q,i){q.hidden=i!==k});bi.style.width=(k/Q.length*100)+'%';bk.style.visibility=k?'visible':'hidden';nx.firstChild.textContent=k===Q.length-1?'Send ':'Next ';var x=Q[k].querySelector('input,textarea');if(x&&show.on)x.focus();show.on=1}
bk.onclick=function(){if(k){k--;show()}};f.querySelector('.sk').onclick=function(){if(k<Q.length-1){k++;show()}else done(f)};
f.addEventListener('submit',function(e){e.preventDefault();if(k<Q.length-1){k++;show()}else{bi.style.width='100%';done(f)}});show();
// C: starters
var C=document.getElementById('C'),cs=[].slice.call(C.querySelectorAll('.st'));
cs.forEach(function(c){c.setAttribute('aria-pressed','false');c.addEventListener('click',function(e){if(e.target.closest('a'))return;cs.forEach(function(x){x.setAttribute('aria-pressed',x===c)});
  var u=C.querySelector('.unf');u.querySelector('.yt').textContent=c.dataset.p;u.style.setProperty('--c',getComputedStyle(c).getPropertyValue('--c'));u.hidden=false;u.querySelector('input').focus()})});
// D: any way you can
var Dd=document.getElementById('D'),ws=[].slice.call(Dd.querySelectorAll('.wy')),df=Dd.querySelector('.dw');
ws.forEach(function(w){w.addEventListener('click',function(){ws.forEach(function(x){x.setAttribute('aria-pressed',x===w)});df.hidden=false;
  [].forEach.call(df.querySelectorAll('.pn'),function(p){p.hidden=p.dataset.w!==w.dataset.w})})});
var rb=Dd.querySelector('.rb'),au=Dd.querySelector('.rec audio'),mr=null,ch=[];
rb.addEventListener('click',function(){if(mr&&mr.state==='recording'){mr.stop();return}
  if(!navigator.mediaDevices||!window.MediaRecorder){rb.querySelector('span').textContent='Recording isn’t available in this browser';return}
  navigator.mediaDevices.getUserMedia({audio:true}).then(function(s){ch=[];mr=new MediaRecorder(s);mr.ondataavailable=function(e){ch.push(e.data)};
    mr.onstop=function(){s.getTracks().forEach(function(t){t.stop()});au.src=URL.createObjectURL(new Blob(ch));au.hidden=false;rb.classList.remove('on');rb.querySelector('span').textContent='Record again'};
    mr.start();rb.classList.add('on');rb.querySelector('span').textContent='Stop';setTimeout(function(){if(mr.state==='recording')mr.stop()},180000)}).catch(function(){rb.querySelector('span').textContent='Microphone not allowed'})});
})();
'''.replace("__PL__", json.dumps(M["places"]))

HTML = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>Story Invitation Studies</title><link rel="icon" href="{E}favicon.svg">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;700&family=Bricolage+Grotesque:opsz,wght@12..96,300..800&family=Literata:ital,opsz,wght@0,7..72,300..900;1,7..72,300..700&display=swap">
<style>{CSS}</style></head><body>
<nav class="bar0" aria-label="Studies"><b>Story invitation</b><span class="nk">Studies · nothing is sent</span></nav>
<main>{A}{B}{C}{Dsec}{Esec}</main><script>{JS}</script></body></html>'''

