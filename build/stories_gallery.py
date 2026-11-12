# /magazine/test/stories/: a running gallery of story-submission landing ideas. One page per idea, plus the gallery.
# To add an idea: append to IDEAS (code, slug, name, blurb, tags, added, html, css, js) and run this file. Nothing typed on any page is sent or kept.
import json, os, re, datetime
import stories_base as b

D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D, "site", "magazine", "test", "stories")
R = "../../../"            # magazine root, from an idea page
I = R + "img/"
T = b.TINT
SURVEY_URL = "https://aoaoaoa.github.io/usbns/magazine/landing/"
ADDR = "1233 Central St., Evanston, IL 60201"
TODAY = datetime.date(2026, 11, 12)

def depth(h):  # base pieces were written for /test/stories/; idea pages sit one level deeper
    return h.replace('"../../', '"' + R)

def unhide(h):
    return re.sub(r'(<section class="ap"[^>]*?) hidden>', r'\1>', h, count=1)

FORM = b.form
DONE = b.DONE
PROM = b.PROMISE
EMAIL = '<p class="prom">Prefer email? <a href="mailto:tab@usbnc.org">tab@usbnc.org</a></p>'
def reach(extra=""):
    return f'<div class="two">{extra}<label>Your name<input autocomplete="name"></label><label>Email or phone<input autocomplete="email"></label></div>'
def send(t="Send your story"):
    return f'<button class="sbtn" type="submit">{t} <span aria-hidden="true">→</span></button>'
def head(h1, ld="", kk="Contribute"):
    return f'<p class="kk">{kk}</p><h1>{h1}</h1>' + (f'<p class="ld">{ld}</p>' if ld else "")

IDEAS = []
def idea(code, slug, name, blurb, tags, html, css="", js="", added=TODAY):
    IDEAS.append(dict(code=code, slug=slug, name=name, blurb=blurb, tags=tags, html=html, css=css, js=js, added=added))

# ---------------------------------------------------------------- banked from the first studies
idea("A", "map", "The map", "Every place named in the issue on one map. Type your town and the form opens beside it.",
     ["Everyone"], depth(unhide(b.A)),
     js="""var PL=__PL__,A=document.getElementById('A'),wf=A.querySelector('.where'),you=A.querySelector('.you');
wf.addEventListener('submit',function(e){e.preventDefault();var v=wf.querySelector('input').value.trim();if(!v)return;var u=A.querySelector('.unf');
var p=PL[v];if(p){you.setAttribute('transform','translate('+p[0]+','+p[1]+')');you.hidden=false}else you.hidden=true;
u.querySelector('.yt').textContent=v+(p?' · already in this issue. Tell us what’s new.':' · the next place in this issue?');u.hidden=false;u.querySelector('textarea').focus()});""".replace("__PL__", json.dumps(b.M["places"])))

C = depth(unhide(b.C))
C = C.replace('Like <a href="../../../newyorkers/">Crown Heights, Brooklyn</a>', 'Like <a href="../../../newyorkers/">Harlem</a>', 1)
C = C.replace('Like <a href="../../../newyorkers/">New York City</a>', 'Like <a href="../../../newyorkers/">Crown Heights, Brooklyn</a>', 1)
idea("C", "starters", "Story starters", "Six openings, each tied to the story in this issue that began that way. For readers who doubt they have a story.",
     ["Non-writers"], C,
     js="""var C=document.getElementById('C'),cs=[].slice.call(C.querySelectorAll('.st'));
cs.forEach(function(c){c.setAttribute('aria-pressed','false');c.addEventListener('click',function(e){if(e.target.closest('a'))return;cs.forEach(function(x){x.setAttribute('aria-pressed',x===c)});
var u=C.querySelector('.unf');u.querySelector('.yt').textContent=c.dataset.p;u.hidden=false;u.querySelector('input').focus()})});""")

idea("D", "any-way", "Any way you can", "Write, record a voice note, send photographs, pass along a lead, or use your own language.",
     ["Everyone", "Any language", "Non-writers"], depth(unhide(b.Dsec)),
     js="""var Dd=document.getElementById('D'),ws=[].slice.call(Dd.querySelectorAll('.wy')),df=Dd.querySelector('.dw');
ws.forEach(function(w){w.addEventListener('click',function(){ws.forEach(function(x){x.setAttribute('aria-pressed',x===w)});df.hidden=false;
[].forEach.call(df.querySelectorAll('.pn'),function(p){p.hidden=p.dataset.w!==w.dataset.w})})});
REC(Dd);""")

idea("E", "report-to-page", "From report to page", "The printed call, word for word, as step one of three: you send, we write back, it may become a story.",
     ["Everyone"], depth(unhide(b.Esec)))

# ---------------------------------------------------------------- new proposals
idea("F", "postcard", "A postcard home", "The cover painting on the front; your message and our address on the back. Turn it over to write.",
     ["Everyone"], f'''<section class="ap" id="F">{head("Send us a postcard.", "A few lines from where you live, the way you’d write home.")}
<div class="pc"><div class="pc-in">
<div class="pc-f"><img src="{I}cover-paint-v2.jpg" alt="The cover painting of this issue" loading="lazy"><span class="pc-g">Greetings from <b class="pc-t">your town</b></span></div>
<form class="pc-b" novalidate><textarea aria-label="Your message" placeholder="What happened, and who was there…"></textarea>
<div class="pc-r"><span class="pc-s"><img src="{I}motif/dot03.webp" alt=""></span><span class="pc-pm"><i class="pm-t">YOUR TOWN</i><i>{TODAY.strftime("%b %-d %Y").upper()}</i></span>
<p class="pc-a">The American Bahá’í<br>{ADDR}</p>
<label>From<input class="pc-fr" placeholder="City or neighborhood, state"></label><label>Your name<input autocomplete="name"></label><label>Email or phone<input autocomplete="email"></label></div>
{send("Mail it")}</form></div></div>
<p class="pc-flip"><button type="button" class="pcb">Turn it over</button></p>{DONE}{PROM}</section>''',
     css='''.pc{perspective:1600px;max-width:760px;margin:0 auto}.pc-in{position:relative;aspect-ratio:3/2;transform-style:preserve-3d;transition:transform .7s cubic-bezier(.2,.8,.2,1)}
.pc.back .pc-in{transform:rotateY(180deg)}.pc-f,.pc-b{position:absolute;inset:0;backface-visibility:hidden;-webkit-backface-visibility:hidden;border-radius:6px;box-shadow:0 16px 36px rgba(29,26,22,.2);overflow:hidden}
.pc-f img{width:100%;height:100%;object-fit:cover;display:block}.pc-g{position:absolute;left:18px;bottom:16px;background:var(--card);color:var(--ink);font:italic 400 18px var(--text);padding:6px 12px;border-radius:3px}.pc-g b{font-style:normal}
.pc-b{transform:rotateY(180deg);background:#fffdf6;color:#1d1a16;display:grid;grid-template-columns:1.1fr 1fr;gap:0;text-align:left;padding:18px}
.pc-b textarea{border:0;border-right:1px solid #d9d2c4;border-radius:0;background:transparent;resize:none;font:italic 17px/1.6 var(--text);padding:4px 16px 4px 4px;color:#1d1a16}
.pc-r{display:grid;gap:8px;padding-left:16px;align-content:start;position:relative}.pc-r label{font-size:12px;color:#6a635a}.pc-r input{padding:6px 8px;font-size:15px;background:transparent;border:0;border-bottom:1px solid #d9d2c4;border-radius:0;color:#1d1a16}
.pc-s{justify-self:end;width:58px;height:70px;border:2px dotted #c9b9a0;padding:3px;background:#fff}.pc-s img{width:100%;height:100%;object-fit:cover;display:block}
.pc-pm{position:absolute;right:52px;top:14px;width:84px;height:84px;border:2px solid rgba(34,46,76,.55);border-radius:50%;display:grid;place-content:center;text-align:center;font:700 10px/1.3 var(--ui);color:rgba(34,46,76,.75);transform:rotate(-12deg);letter-spacing:.06em}.pc-pm i{font-style:normal;display:block}
.pc-a{font:15px/1.5 var(--text);margin:4px 0 6px}.pc-b .sbtn{position:absolute;right:18px;bottom:18px;font-size:16px;padding:10px 16px}
.pc-flip{margin:18px 0 0}.pcb{font:600 15px var(--ui);background:none;border:1px solid var(--rule);color:var(--ink);border-radius:999px;padding:10px 18px;cursor:pointer}
@media (max-width:700px){.pc-in{aspect-ratio:auto;height:240px;transition:transform .7s cubic-bezier(.2,.8,.2,1),height 0s .35s}.pc.back .pc-in{height:660px}.pc-b{grid-template-columns:1fr;padding:14px}.pc-b textarea{border-right:0;border-bottom:1px solid #d9d2c4;min-height:160px}.pc-r{padding:12px 0 56px}.pc-pm{right:70px}}
@media (prefers-reduced-motion:reduce){.pc-in{transition:none}}''',
     js='''var F=document.getElementById('F'),pc=F.querySelector('.pc'),bt=F.querySelector('.pcb'),fr=F.querySelector('.pc-fr');
bt.onclick=function(){pc.classList.toggle('back');bt.textContent=pc.classList.contains('back')?'Turn it back':'Turn it over';if(pc.classList.contains('back'))setTimeout(function(){F.querySelector('textarea').focus()},400)};
fr.addEventListener('input',function(){var v=fr.value.trim()||'your town';F.querySelector('.pc-t').textContent=v;F.querySelector('.pm-t').textContent=v.split(',')[0].toUpperCase().slice(0,14)});
F.querySelector('.pc-b').addEventListener('submit',function(e){e.preventDefault();this.closest('.pc').hidden=true;bt.hidden=true;F.querySelector('.done').hidden=false})''')

idea("G", "one-sentence", "One sentence", "The story as one sentence with blanks. Fill four gaps and it’s a report.",
     ["Non-writers", "Young people"], f'''<section class="ap" id="G">{head("Your story in one sentence.", "Fill in the blanks. We’ll write back for the rest.")}
<form class="sn" novalidate><p class="sn-p">In <input size="14" placeholder="Westlake, Indianapolis" aria-label="Where">, <input size="16" placeholder="neighbors and their children" aria-label="Who"> came together to <input size="22" placeholder="wash cars for camp money" aria-label="What happened">. What stayed with us: <input size="26" placeholder="how many hands it took" aria-label="What you learned">.</p>
{reach()}{send()}</form>{DONE}{PROM}</section>''',
     css='''.sn{max-width:820px;margin:0 auto;display:grid;gap:22px;text-align:left}.sn-p{font:400 clamp(22px,2.8vw,32px)/1.9 var(--text);margin:0 0 6px;text-align:center;text-wrap:pretty}
.sn-p input{font:inherit;font-style:italic;width:auto;max-width:100%;background:transparent;border:0;border-bottom:2px solid var(--gold);border-radius:0;padding:0 4px;color:var(--ink);text-align:center}
.sn-p input::placeholder{color:var(--mute);opacity:.7}.sn .sbtn{justify-self:center}''')

idea("H", "field-notes", "Field notes", "A dated notebook page. The print call asks for field notes; this gives them a place.",
     ["Everyone"], f'''<section class="ap" id="H">{head("Send us your field notes.", "How community building unfolds where you live, and what is being learned along the way.")}
<form class="nb" novalidate><div class="nb-h"><span>{TODAY.strftime("%B %-d, %Y")}</span><input placeholder="Place" aria-label="Place"></div>
<textarea rows="9" aria-label="Notes" placeholder="What happened today…"></textarea><div class="nb-m"><label>What we’re learning<textarea rows="3"></textarea></label></div></form>
<div class="nb-f">{reach()}{send("Send the page")}</div>{DONE}{PROM}</section>''',
     css='''.nb{max-width:720px;margin:0 auto 22px;background:#fffdf6;color:#1d1a16;border-radius:4px;box-shadow:0 12px 30px rgba(29,26,22,.14);padding:22px 26px 22px 70px;text-align:left;position:relative;
background-image:linear-gradient(90deg,transparent 52px,#e3a69a 52px,#e3a69a 54px,transparent 54px),repeating-linear-gradient(#fffdf6 0 31px,#cfdbe6 31px 32px)}
.nb-h{display:flex;gap:16px;align-items:baseline;font:600 14px var(--ui);color:#6a635a;margin-bottom:8px}.nb-h input{flex:1;font:italic 18px var(--text);border:0;background:transparent;padding:0;color:#1d1a16}
.nb textarea{border:0;background:transparent;font:18px/32px var(--text);padding:0;color:#1d1a16;resize:vertical}.nb-m{margin-top:12px;border-top:2px solid #e3a69a;padding-top:10px}.nb-m label{color:#b8782e;font-size:13px}
.nb-f{max-width:720px;margin:0 auto;display:grid;gap:14px;text-align:left}.nb-f .sbtn{justify-self:start}''',
     js='''var H=document.getElementById('H');H.querySelector('.nb-f .sbtn').addEventListener('click',function(){H.querySelector('.nb').hidden=true;H.querySelector('.nb-f').hidden=true;H.querySelector('.done').hidden=false})''')

idea("I", "quote-first", "Start with a quote", "Begin with what someone said. The issue’s own pull quote shows how far one line can carry a story.",
     ["Non-writers"], f'''<section class="ap" id="I">{head("What did someone say that stayed with you?")}
<figure class="qx" style="--c:{T['newyorkers']}"><blockquote>“The diversity was so rich – it alone made the night worthwhile.”</blockquote><figcaption>Felicia Sobhani, Harlem · <a href="{R}newyorkers/">New Yorkers create more unified communities through the arts</a></figcaption></figure>
<form class="sf qf" novalidate><label class="qq">Their words<textarea rows="3" placeholder="“…”"></textarea></label><div class="two"><label>Who said it<input placeholder="With their permission"></label><label>Where<input placeholder="City or neighborhood, state"></label></div>
<label>Tell us the rest, if you like<textarea rows="3"></textarea></label>{reach()}{send()}</form>{DONE}{PROM}</section>''',
     css='''.qx{max-width:640px;margin:0 auto 34px;border-left:5px solid var(--c);padding:4px 0 4px 22px;text-align:left}.qx blockquote{margin:0;font:italic 400 clamp(22px,2.6vw,30px)/1.3 var(--text)}.qx figcaption{font:13px/1.5 var(--ui);color:var(--mute);margin-top:10px}
.qq textarea{font:italic 22px/1.4 var(--text)}''')

kick = ["Community", "Race amity", "In conversation", "Across America", "Scholarship", "Adventures in pioneering"]
by = [("Race amity", "Linda Ahdieh Grant", "gregory"), ("Community", "Michelle Goering", "newyorkers"), ("In conversation", "Neena Rouhani", "twoartists"), ("Adventures in pioneering", "Cher Gupta, as told to Joyce Litoff", "comic")]
idea("J", "next-byline", "The next byline", "The issue’s bylines, then yours: type a headline and watch it set as an entry in the contents.",
     ["Writers"], f'''<section class="ap" id="J">{head("The next byline could be yours.", "Every story here was written by someone close to it.")}
<ul class="bys">{"".join(f'<li style="--c:{T[s]}"><span>{k}</span>{n}</li>' for k, n, s in by)}</ul>
<div class="jb"><form class="sf" novalidate><label>Section<select class="j-k">{"".join(f"<option>{k}</option>" for k in kick)}</select></label><label>Your headline<input class="j-t" placeholder="Neighbors build a garden for the children of Elm Street"></label>
<label>Where<input class="j-p" placeholder="City or neighborhood, state"></label><label>What happened<textarea rows="4"></textarea></label>{reach()}{send()}</form>
<div class="jp" aria-live="polite"><p class="jp-h">Contents · next issue</p><div class="jp-e"><span class="pg">?</span><span><span class="k j-ko">Community</span><span class="t j-to">Your headline</span><span class="by j-bo">By you</span></span></div></div></div>{DONE}{PROM}</section>''',
     css='''.bys{list-style:none;margin:0 auto 34px;padding:0;display:flex;flex-wrap:wrap;justify-content:center;gap:8px 22px;font:15px var(--text)}.bys li{border-left:4px solid var(--c);padding-left:8px;text-align:left}.bys span{display:block;font:700 11px var(--ui);letter-spacing:.12em;text-transform:uppercase;color:var(--mute)}
select{font:16px var(--text);padding:10px;border:1px solid var(--rule);border-radius:4px;background:var(--card);color:var(--ink)}
.jb{display:grid;grid-template-columns:1fr 1fr;gap:32px;max-width:960px;margin:0 auto;align-items:start}.jb .sf{margin:0}
.jp{position:sticky;top:70px;background:var(--card);border:1px solid var(--rule);padding:18px 20px;text-align:left}.jp-h{font:700 11px var(--ui);letter-spacing:.14em;text-transform:uppercase;color:var(--mute);margin:0 0 12px;border-bottom:1px solid var(--rule);padding-bottom:8px}
.jp-e{display:grid;grid-template-columns:44px 1fr;gap:12px}.jp .pg{font:italic 700 34px/1 var(--text);color:var(--gold)}.jp .k{display:block;font:700 12px var(--ui);letter-spacing:.14em;text-transform:uppercase;color:var(--gold)}.jp .t{display:block;font:700 22px/1.2 var(--text);margin:4px 0}.jp .by{font:14px var(--ui);color:var(--mute)}
@media (max-width:760px){.jb{grid-template-columns:1fr}.jp{position:static;order:-1}}''',
     js='''var J=document.getElementById('J');function up(){J.querySelector('.j-ko').textContent=J.querySelector('.j-k').value;J.querySelector('.j-to').textContent=J.querySelector('.j-t').value||'Your headline';
var n=J.querySelector('input[autocomplete=name]').value,p=J.querySelector('.j-p').value;J.querySelector('.j-bo').textContent='By '+(n||'you')+(p?' · '+p:'')}
J.addEventListener('input',up);J.addEventListener('change',up);''')

idea("K", "coming-up", "Coming up", "Tell us before it happens. Captures leads while there is still time to ask for photographs.",
     ["Leads"], f'''<section class="ap" id="K">{head("Something coming up?", "Tell us before it happens. We may ask for a photograph or a few lines afterward.")}
<form class="sf" novalidate><div class="two"><label>When<input type="date" min="{TODAY.isoformat()}"></label><label>Where<input placeholder="City or neighborhood, state"></label></div>
<label>What’s planned<textarea rows="3" placeholder="A devotional gathering, a children’s class picnic, a neighborhood conversation…"></textarea></label>
<fieldset class="ck"><legend>Afterward, you could</legend><label><input type="checkbox"> Send a few photographs</label><label><input type="checkbox"> Write a few lines</label><label><input type="checkbox"> Talk with an editor by phone</label></fieldset>
{reach()}{send("Tell us")}</form>{DONE}{PROM}</section>''',
     css='''.ck{border:0;padding:0;margin:0;display:grid;gap:8px}.ck legend{font:600 14px var(--ui);color:var(--soft);margin-bottom:6px}.ck label{display:flex;gap:10px;align-items:center;font:400 16px var(--text);color:var(--ink)}.ck input{width:18px;height:18px;accent-color:var(--gold)}''')

idea("L", "photo-first", "Photo first", "Start with a picture. The form grows around it: where, who took it, and that everyone pictured agreed.",
     ["Non-writers", "Any language"], f'''<section class="ap" id="L">{head("Start with a photograph.", "A picture from your neighborhood, and a line about it.")}
<form class="sf lf" novalidate><label class="dz"><input type="file" accept="image/jpeg,image/png" class="lf-i"><span class="dz-t"><b>Choose a photograph</b><small>JPEG or PNG</small></span><img alt="" hidden></label>
<div class="lf-m" hidden><label>What’s happening<input placeholder="Where, and what we’re seeing"></label><label>Who took it<input placeholder="Photographer’s name"></label>
<label class="cb"><input type="checkbox"> Everyone pictured agreed to share it</label>{reach()}{send("Send it")}</div></form>{DONE}{PROM}</section>''',
     css='''.dz{display:grid;place-items:center;min-height:300px;border:2px dashed var(--rule);border-radius:6px;background:var(--card);cursor:pointer;position:relative;overflow:hidden}.dz input{position:absolute;opacity:0;inset:0;cursor:pointer}
.dz-t{display:grid;gap:4px;text-align:center}.dz-t b{font:600 20px var(--text);color:var(--ink)}.dz-t small{font:13px var(--ui);color:var(--mute)}.dz img{width:100%;height:100%;object-fit:cover;position:absolute;inset:0}
.cb{display:flex;gap:10px;align-items:center;font:400 16px var(--text);color:var(--ink)}.cb input{width:18px;height:18px;accent-color:var(--gold)}.lf-m{display:grid;gap:14px}''',
     js='''var L=document.getElementById('L'),fi=L.querySelector('.lf-i'),im=L.querySelector('.dz img');fi.addEventListener('change',function(){var f=fi.files[0];if(!f)return;im.src=URL.createObjectURL(f);im.hidden=false;L.querySelector('.dz-t').hidden=true;L.querySelector('.lf-m').hidden=false;L.querySelector('.lf-m input').focus()})''')

idea("M", "nominate", "Who should we write about?", "Point us to a person, a group or a place. Nobody has to write a word.",
     ["Leads", "Non-writers"], f'''<section class="ap" id="M">{head("Who should we write about?", "A person, a group or a place doing something worth telling. You point; we follow up.")}
<form class="sf" novalidate><div class="seg" role="radiogroup" aria-label="Who"><label><input type="radio" name="mw" checked> A person</label><label><input type="radio" name="mw"> A group</label><label><input type="radio" name="mw"> A place</label></div>
<label>Name<input></label><label>Where<input placeholder="City or neighborhood, state"></label><label>In a line, why<input placeholder="She has hosted a children’s class every Saturday for six years"></label>
<label class="cb"><input type="checkbox" checked> I’ll let them know first</label>{reach()}{send("Send the name")}</form>{DONE}{PROM}</section>''',
     css='''.seg{display:flex;border:1px solid var(--rule);border-radius:999px;overflow:hidden;justify-self:start}.seg label{display:block;font:600 15px var(--ui);color:var(--ink);padding:10px 16px;cursor:pointer;border-right:1px solid var(--rule)}.seg label:last-child{border:0}.seg input{position:absolute;opacity:0}.seg label:has(input:checked){background:var(--navy);color:var(--blush)}.seg label:has(input:focus-visible){outline:2px solid var(--link);outline-offset:-2px}
.cb{display:flex;gap:10px;align-items:center;font:400 16px var(--text);color:var(--ink)}.cb input{width:18px;height:18px;accent-color:var(--gold)}''')

idea("N", "in-pictures", "Tell it in pictures", "Three panels, after the issue’s comic. Drawings or photos, a caption under each.",
     ["Young people", "Any language", "Non-writers"], f'''<section class="ap" id="N">{head("Tell it in pictures.", "Three panels, a caption under each. Drawings or photographs both work.")}
<p class="nx"><a href="{R}comic/"><img src="{I}comic-1.jpg" alt="A page from Sparkling spirits in Indianapolis" loading="lazy"></a><span>Like <a href="{R}comic/">Sparkling spirits in Indianapolis</a>, story by Cher Gupta, illustrated by Aria Ghalili.</span></p>
<form class="sf" novalidate><div class="pn3">{"".join(f'<div class="pnl"><label class="pz"><input type="file" accept="image/*"><span>{n}</span><img alt="" hidden></label><input placeholder="Caption" aria-label="Caption {n}"></div>' for n in ("1", "2", "3"))}</div>
<label>Where<input placeholder="City or neighborhood, state"></label>{reach()}{send()}</form>{DONE}{PROM}</section>''',
     css='''.nx{display:flex;gap:14px;align-items:center;max-width:640px;margin:0 auto 26px;text-align:left;font:14px/1.5 var(--ui);color:var(--mute)}.nx img{width:84px;height:auto;display:block;border:1px solid var(--rule)}
.sf:has(.pn3){max-width:880px}.pn3{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.pnl{display:grid;gap:8px}
.pz{position:relative;aspect-ratio:1;border:3px solid var(--ink);background:var(--card);display:grid;place-items:center;cursor:pointer;overflow:hidden}.pz input{position:absolute;inset:0;opacity:0;cursor:pointer}
.pz span{font:italic 700 42px var(--text);color:var(--rule)}.pz img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.pnl>input{font:italic 15px var(--text)}
@media (max-width:600px){.pn3{grid-template-columns:1fr}}''',
     js='''[].forEach.call(document.querySelectorAll('#N .pz input'),function(f){f.addEventListener('change',function(){var x=f.files[0];if(!x)return;var im=f.parentNode.querySelector('img');im.src=URL.createObjectURL(x);im.hidden=false})})''')

idea("O", "young-voices", "Young voices", "For children and junior youth, with a grown-up. Big choices, few words, a grown-up’s contact.",
     ["Young people"], f'''<section class="ap" id="O"><div class="yv"><img src="{I}story-paint.webp" alt="Children’s hands at a watercolor set beside paintings, one lettered I am kind, loving, and friendly">
<div>{head("What did you make? What did you see?", "Show us, with a grown-up’s help.", "Young voices")}
<div class="yb" role="group" aria-label="How"><button type="button" data-w="d" aria-pressed="false"><span>✎</span>Draw it</button><button type="button" data-w="s" aria-pressed="false"><span>●</span>Say it</button><button type="button" data-w="w" aria-pressed="false"><span>¶</span>Write it</button></div>
<form class="sf" novalidate hidden><div class="pn" data-w="d" hidden><label>Your drawing<input type="file" accept="image/*"></label></div>
<div class="pn" data-w="s" hidden><div class="rec"><button type="button" class="rb"><i></i><span>Start recording</span></button><span class="rt">Tell us what happened.</span><audio controls hidden></audio></div></div>
<div class="pn" data-w="w" hidden><label>Your story<textarea rows="4"></textarea></label></div>
<div class="two"><label>Your first name<input></label><label>Your age<input inputmode="numeric"></label></div>
<div class="two"><label>A grown-up’s name<input></label><label>A grown-up’s email or phone<input></label></div>{send("Send it")}</form>{DONE}</div></div>{PROM}</section>''',
     css='''.yv{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1fr);gap:clamp(24px,5vw,56px);align-items:start;text-align:left}.yv>img{width:100%;height:auto;display:block}.yv .kk::before{margin-left:0}.yv h1,.yv .ld{margin-left:0}
.yb{display:flex;gap:12px;flex-wrap:wrap;margin:0 0 22px}.yb button{display:grid;justify-items:center;gap:4px;width:118px;padding:18px 8px;border:2px solid var(--ink);border-radius:18px;background:var(--card);color:var(--ink);font:700 18px var(--cond);letter-spacing:.04em;text-transform:uppercase;cursor:pointer}
.yb span{font:400 30px/1 var(--text)}.yb button[aria-pressed=true]{background:#f3c623;border-color:#f3c623;color:#1d1a16}.yv .sf{margin:0}
@media (max-width:760px){.yv{grid-template-columns:1fr}.yv>img{max-width:280px}}''',
     js='''var O=document.getElementById('O'),yb=[].slice.call(O.querySelectorAll('.yb button')),of=O.querySelector('form');yb.forEach(function(w){w.onclick=function(){yb.forEach(function(x){x.setAttribute('aria-pressed',x===w)});of.hidden=false;
[].forEach.call(of.querySelectorAll('.pn'),function(p){p.hidden=p.dataset.w!==w.dataset.w})}});REC(O);''')

idea("P", "print-and-post", "Print and post", "A one-page flyer with the printed call, a QR code and tear-off tabs, for readers who aren’t online.",
     ["Offline", "Everyone"], f'''<section class="ap" id="P">{head("Print and post.", "For the library board, the community center and the devotional gathering: a flyer that brings the invitation to people who don’t read online.")}
<p><button type="button" class="sbtn pp">Print the flyer <span aria-hidden="true">↓</span></button></p>
<div class="fly"><p class="fk">The American Bahá’í</p><h2>Every story in this issue began as a report from a community.</h2><div class="fpr">{b.PRINT}</div>
<div class="fq"><div class="qr" aria-label="QR code for the submission page"></div><p>Scan to send your story, or write to <b>tab@usbnc.org</b>.<br><small>Placeholder link until submissions open.</small></p></div>
<ul class="tabs">{"<li>tab@usbnc.org<br>Send your story</li>" * 8}</ul></div>{EMAIL}</section>''',
     css='''.fly{width:min(100%,640px);aspect-ratio:8.5/11;margin:26px auto 0;background:#fff;color:#1d1a16;box-shadow:0 12px 32px rgba(29,26,22,.16);padding:40px 40px 0;text-align:left;display:flex;flex-direction:column}
.fk{font:700 12px var(--ui);letter-spacing:.18em;text-transform:uppercase;color:#b8782e;margin:0 0 10px}.fly h2{font:700 30px/1.08 var(--text);margin:0 0 18px}.fpr{font:15px/1.55 var(--text)}.fpr p{margin:0 0 .7em}
.fq{display:flex;gap:18px;align-items:center;margin:auto 0 18px;font:14px/1.5 var(--ui)}.qr{flex:none;width:120px;height:120px}.qr img,.qr canvas{width:120px!important;height:120px!important}.fq small{color:#6a635a}
.tabs{list-style:none;margin:0 -40px;padding:0;display:grid;grid-template-columns:repeat(8,1fr);border-top:2px dashed #999}.tabs li{writing-mode:vertical-rl;transform:rotate(180deg);font:600 11px/1.3 var(--ui);padding:10px 4px;border-left:1px dashed #999;height:120px;text-align:center}
@media (max-width:600px){.fly{aspect-ratio:auto;padding:22px 20px 0}.fly h2{font-size:24px}.tabs{margin:0 -20px}}
@media print{body>*:not(main),.ap>*:not(.fly){display:none!important}body,main,.ap{background:#fff;padding:0;margin:0;max-width:none}.fly{box-shadow:none;width:100%;margin:0}@page{size:letter;margin:.4in}}''',
     js=f'''var P=document.getElementById('P');P.querySelector('.pp').onclick=function(){{print()}};
var s=document.createElement('script');s.src='../qrcode.min.js';s.onload=function(){{new QRCode(P.querySelector('.qr'),{{text:'{SURVEY_URL}',width:240,height:240,correctLevel:QRCode.CorrectLevel.M}})}};document.head.appendChild(s);''')

idea("Q", "dear-editors", "Dear editors", "A letter on paper: the salutation is already written, so the first line is the easy one.",
     ["Everyone", "Any language"], f'''<section class="ap" id="Q">{head("Write to the editors.", "As a letter, in your own words and your own language.")}
<form class="lt" novalidate><p class="lt-d">{TODAY.strftime("%B %-d, %Y")}</p><p class="lt-s">Dear editors,</p><textarea rows="8" aria-label="Your letter"></textarea>
<p class="lt-c">With love,</p><input class="lt-n" placeholder="Your name" aria-label="Your name"><input class="lt-p" placeholder="Your town" aria-label="Your town"><input class="lt-e" placeholder="Email or phone, so we can write back" aria-label="Email or phone">
{send("Send the letter")}</form>{DONE}{PROM}</section>''',
     css='''.lt{max-width:640px;margin:0 auto;background:#fffdf6;color:#1d1a16;box-shadow:0 12px 30px rgba(29,26,22,.14);padding:34px 40px;text-align:left;display:grid;gap:4px}
.lt p{margin:0}.lt-d{text-align:right;font:italic 15px var(--text);color:#6a635a;margin-bottom:18px!important}.lt-s,.lt-c{font:italic 20px var(--text)}
.lt textarea{border:0;background:transparent;font:18px/1.7 var(--text);padding:6px 0;color:#1d1a16;resize:vertical}.lt-c{margin-top:14px!important}
.lt input{border:0;border-bottom:1px solid #d9d2c4;border-radius:0;background:transparent;padding:6px 0;font:italic 18px var(--text);color:#1d1a16;max-width:340px}.lt .sbtn{justify-self:end;margin-top:18px}''')

echo = [("gregory", "gregory-group-hd.jpg", "Race amity", "Is a place near you carrying on a legacy?"),
        ("newyorkers", "ny-park.jpg", "Community", "Have the arts brought your neighbors together?"),
        ("twoartists", "ta-portrait.jpg", "In conversation", "Do you make art that grows from your faith?"),
        ("endeavor", "az-ace.jpg", "Across America", "Did “A Common Endeavor” start a conversation where you live?"),
        ("abs", "abs-stage-duo.jpg", "Scholarship", "Is your study group bringing its field to bear on your neighborhood?")]
idea("R", "story-echoes", "Story echoes", "An ask at the end of each story, in its own color: did something like this happen where you are?",
     ["Everyone"], f'''<section class="ap" id="R">{head("Something like this where you are?", "The invitation moves into the stories: each one ends by asking about yours. Here are all five.")}
<div class="ec">{"".join(f'<form class="ecf" novalidate style="--c:{T[s]}"><img src="{I}{im}" alt="" loading="lazy"><div><p class="k">{k}</p><p class="q">{q}</p><div class="eci"><input placeholder="Tell us in a line, and where" aria-label="{q}"><button class="sbtn" type="submit">Send</button></div><p class="ok" hidden>Thank you. We’ll write back.</p></div></form>' for s, im, k, q in echo)}</div>{PROM}</section>''',
     css='''.ec{display:grid;gap:14px;max-width:820px;margin:0 auto;text-align:left}.ecf{display:grid;grid-template-columns:120px 1fr;gap:18px;align-items:center;background:var(--card);border:1px solid var(--rule);border-top:4px solid var(--c);padding:14px}
.ecf img{width:120px;height:90px;object-fit:cover;display:block}.ecf .k{font:700 11px var(--ui);letter-spacing:.14em;text-transform:uppercase;color:var(--c);margin:0 0 4px;filter:brightness(.85)}.ecf .q{font:600 20px/1.25 var(--text);margin:0 0 10px}
.eci{display:flex;gap:8px}.eci input{flex:1;min-width:0}.eci .sbtn{font-size:16px;padding:10px 16px;background:var(--c);color:#fff}.ok{font:14px var(--ui);color:var(--mute);margin:0}
@media (max-width:600px){.ecf{grid-template-columns:1fr}.ecf img{width:100%;height:120px}}''',
     js='''[].forEach.call(document.querySelectorAll('#R .ecf'),function(f){f.addEventListener('submit',function(e){e.preventDefault();f.querySelector('.eci').hidden=true;f.querySelector('.ok').hidden=false})})''')

# ---------------------------------------------------------------- shared runtime
REC = r'''function REC(root){var rb=root.querySelector('.rb');if(!rb)return;var au=root.querySelector('.rec audio'),mr=null,ch=[];
rb.addEventListener('click',function(){if(mr&&mr.state==='recording'){mr.stop();return}
if(!navigator.mediaDevices||!window.MediaRecorder){rb.querySelector('span').textContent='Recording isn’t available in this browser';return}
navigator.mediaDevices.getUserMedia({audio:true}).then(function(s){ch=[];mr=new MediaRecorder(s);mr.ondataavailable=function(e){ch.push(e.data)};
mr.onstop=function(){s.getTracks().forEach(function(t){t.stop()});au.src=URL.createObjectURL(new Blob(ch));au.hidden=false;rb.classList.remove('on');rb.querySelector('span').textContent='Record again'};
mr.start();rb.classList.add('on');rb.querySelector('span').textContent='Stop';setTimeout(function(){if(mr.state==='recording')mr.stop()},180000)}).catch(function(){rb.querySelector('span').textContent='Microphone not allowed'})})}'''
DONEJS = r'''[].forEach.call(document.querySelectorAll('form.sf,form.lt,form.sn'),function(f){f.addEventListener('submit',function(e){e.preventDefault();var d=f.closest('.ap').querySelector('.done');f.hidden=true;[].forEach.call(f.closest('.ap').querySelectorAll('.unf form,.where'),function(x){if(x!==f)x.hidden=true});if(d){d.hidden=false;d.setAttribute('tabindex','-1');d.focus()}})});'''
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;700&family=Bricolage+Grotesque:opsz,wght@12..96,300..800&family=Literata:ital,opsz,wght@0,7..72,300..900;1,7..72,300..700&display=swap">'
NAVCSS = '''.bar0 a{font:600 13px var(--ui);color:var(--ink);text-decoration:none;white-space:nowrap}.bar0 .cd{font:700 13px var(--ui);background:var(--ink);color:var(--paper);border-radius:999px;padding:5px 10px;white-space:nowrap}
.bar0 .pn2{margin-left:auto;display:flex;gap:14px}.bar0 .pn2 a{color:var(--mute)}'''

def page(i, x):
    pv, nx = IDEAS[i - 1] if i else None, IDEAS[i + 1] if i + 1 < len(IDEAS) else None
    nav = (f'<nav class="bar0" aria-label="Ideas"><a href="../">← All ideas</a><span class="cd">{x["code"]}</span><b>{x["name"]}</b>'
           f'<span class="pn2">{f"""<a href="../{pv["slug"]}/">← {pv["code"]}</a>""" if pv else ""}{f"""<a href="../{nx["slug"]}/">{nx["code"]} →</a>""" if nx else ""}</span></nav>')
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">'
            f'<title>{x["code"]} · {x["name"]}</title><link rel="icon" href="{R}favicon.svg">{FONTS}<style>{b.CSS}{NAVCSS}{x["css"]}</style></head><body>{nav}<main>{x["html"]}</main>'
            f'<script>(function(){{{REC}{DONEJS}{x["js"]}}})();</script></body></html>')

GCSS = '''.gw{max-width:1180px;margin:0 auto;padding:clamp(36px,6vw,72px) 16px 80px}.gh{max-width:720px;margin:0 0 28px}.gh h1{margin:0 0 12px;max-width:none;text-align:left}.gh .kk::before{margin-left:0}.gh .ld{margin:0;text-align:left;text-wrap:pretty}
.fl{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 24px}.fl button{font:600 13px var(--ui);border:1px solid var(--rule);background:var(--card);color:var(--ink);border-radius:999px;padding:7px 13px;cursor:pointer}.fl button[aria-pressed=true]{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.gg{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:22px}
.gc a{display:grid;grid-template-columns:minmax(0,1fr);grid-template-rows:auto 1fr;text-decoration:none;color:var(--ink);background:var(--card);border:1px solid var(--rule);border-radius:4px;overflow:hidden;height:100%}.gc a:hover{border-color:var(--ink)}
.gc img{width:100%;height:auto;align-self:start;aspect-ratio:16/10;object-fit:cover;object-position:top;display:block;border-bottom:1px solid var(--rule);background:var(--paper)}
.gc .tx{padding:14px 16px 16px;display:grid;gap:6px;align-content:start}.gc .cn{display:flex;gap:8px;align-items:baseline}.gc .cd{font:700 12px var(--ui);background:var(--ink);color:var(--paper);border-radius:999px;padding:2px 8px}.gc b{font:700 19px/1.2 var(--text)}
.gc p{font:14px/1.45 var(--ui);color:var(--soft);margin:0}.gc .tg{font:600 11px var(--ui);letter-spacing:.1em;text-transform:uppercase;color:var(--mute)}'''
def gallery():
    tags = sorted({t for x in IDEAS for t in x["tags"]}, key=lambda t: (t != "Everyone", t))
    cards = "".join(f'<li class="gc" data-t="{"|".join(x["tags"])}"><a href="{x["slug"]}/"><img src="thumbs/{x["slug"]}.jpg" alt="" loading="lazy" width="800" height="500">'
                    f'<span class="tx"><span class="cn"><span class="cd">{x["code"]}</span><b>{x["name"]}</b></span><p>{x["blurb"]}</p><span class="tg">{" · ".join(x["tags"])} · {x["added"].strftime("%b %-d, %Y")}</span></span></a></li>' for x in IDEAS)
    fl = '<button type="button" aria-pressed="true" data-t="">All</button>' + "".join(f'<button type="button" aria-pressed="false" data-t="{t}">{t}</button>' for t in tags)
    js = '''var B=[].slice.call(document.querySelectorAll('.fl button')),C=[].slice.call(document.querySelectorAll('.gc'));B.forEach(function(b){b.onclick=function(){B.forEach(function(x){x.setAttribute('aria-pressed',x===b)});var t=b.dataset.t;C.forEach(function(c){c.hidden=t&&c.dataset.t.split('|').indexOf(t)<0})}})'''
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">'
            f'<title>Story Invitation Ideas</title><link rel="icon" href="../../favicon.svg">{FONTS}<style>{b.CSS}{GCSS}</style></head><body><main class="gw">'
            f'<header class="gh"><p class="kk">The American Bahá’í · Studies</p><h1>Story invitation ideas</h1><p class="ld">Ways to turn “Every story in this issue began as a report from a community” into a page that invites everyone to send theirs. {len(IDEAS)} ideas so far. Each opens as a working page; nothing typed is sent or kept.</p></header>'
            f'<div class="fl" role="group" aria-label="Filter by who it reaches">{fl}</div><ul class="gg">{cards}</ul></main><script>{js}</script></body></html>')

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i, x in enumerate(IDEAS):
        os.makedirs(os.path.join(OUT, x["slug"]), exist_ok=True)
        open(os.path.join(OUT, x["slug"], "index.html"), "w").write(page(i, x))
    open(os.path.join(OUT, "index.html"), "w").write(gallery())
    import shutil; shutil.copy(os.path.join(D, "vendor", "qrcode.min.js"), OUT)  # qrcodejs 1.0.0, MIT
    shutil.copytree(os.path.join(D, "stories_thumbs"), os.path.join(OUT, "thumbs"), dirs_exist_ok=True)  # screenshots of each idea page, refreshed by hand
    json.dump([x["slug"] for x in IDEAS], open(os.path.join(OUT, "slugs.json"), "w"))
    print("ok", len(IDEAS))
