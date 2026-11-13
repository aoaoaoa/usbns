"""Labs: guided forms. The story form with the field guide and content guidelines built in, three ways (GF1 to GF3)."""
RULES = [("Send originals", "Full-size files straight from the camera or phone, not screenshots or messaging copies."),
         ("Name the photographer", "Every picture carries a credit."),
         ("Ask first", "Everyone recognizable has agreed to be pictured. For children, a parent or guardian, and first names only."),
         ("Say where and when", "Town or neighborhood, state, and the date."),
         ("Video", "Steady and horizontal for the library; vertical welcome for social. Ten seconds per shot or longer."),
         ("A few lines", "What happened and why it mattered, in your own words and in any language.")]
HABITS = ["Be conscientious of your presence in the space", "Keep a steady hand", "Review your work on a bigger screen", "Capture a series of angles", "Be ready for spontaneous moments"]
MOM = [("Framing", "One wide, some mid, a few close.", "#e8532a", "#f3b562"),
       ("Composition", "Room around the subject; mind the edges.", "#1b5e6b", "#7fc0c9"),
       ("Audience", "Faces are what a reader looks for.", "#f05a7e", "#f7c1cf"),
       ("Stage", "The performer and the people watching.", "#46347e", "#a993ea"),
       ("Community", "Spontaneous, intimate and delicate.", "#b07a4a", "#e9cfa8"),
       ("Action", "People are drawn to faces at work.", "#c9462c", "#f0a07a"),
       ("Devotion", "Creative, careful approaches.", "#23406f", "#8fa6d6"),
       ("Candid and posed", "Both are welcome; send some of each.", "#b8862e", "#ead48f")]
BR = [("Photo", "A children’s class in session", "Wide shot", "Show the room, the teacher and the children together, so a reader understands the whole scene at a glance."),
      ("Photo", "Hands at work", "Detail", "Painting, writing, building, serving. Hands tell the story without faces, which helps when children are present."),
      ("Video", "Sixty seconds of a study circle", "Over the shoulder", "The rhythm of a conversation: who speaks, who listens, the book open on the table."),
      ("Photo", "Young people serving together", "Action", "A junior youth group or youth carrying out a service project in their neighborhood."),
      ("Photo", "The sign at the door", "Context", "The name of the place or the event in the frame, so no one has to guess what it was."),
      ("Pitch", "A home that hosts a class", "Story lead", "Who opened their door, how it began, and what the neighbors noticed. A few lines is enough."),
      ("Words", "What a child learned this week", "Microstory", "A parent, tutor or teacher, in their own words. Two or three sentences."),
      ("Photo", "A moment of devotion", "With care", "Prayers before a class or at a gathering, captured quietly and respectfully.")]

def sw(c1, c2): return f'background:linear-gradient(135deg,{c1} 0 45%,{c2} 45% 70%,{c1} 70%)'
HEAD = ('<p class="gk">Contribute</p><h2 class="gh">Know a story like these?</h2>'
        '<p class="gl">Please send us story ideas, article leads, photos of community activities, your field notes on how community building unfolds where you live, and what is being learned along the way.</p>')
def f_where(): return '<label class="gf"><span>Where</span><input type="text" data-r="3" placeholder="Town or neighborhood, state"></label><label class="gf"><span>What happened</span><textarea rows="3" data-r="5"></textarea><small>A few paragraphs is plenty.</small></label>'
def f_who(): return '<label class="gf"><span>Who was there</span><textarea rows="2"></textarea></label>'
def f_photo(): return '<label class="gdrop"><input type="file" multiple accept="image/jpeg,image/png" data-r="0"><b>Choose photographs</b><small>JPEG or PNG, as many as you like</small></label><label class="gf"><span>Photographer’s name</span><input type="text" data-r="1"></label>'
def f_learn(): return '<label class="gf"><span>What you learned</span><textarea rows="2" data-r="5"></textarea></label>'
def f_about(): return ('<div class="gab"><p class="gk">About you</p><div class="g2"><label class="gf"><span>Your name</span><input type="text"></label><label class="gf"><span>Email address</span><input type="email"></label></div>'
                       '<p class="gpr">We will get in touch and work with you before anything you share is used.</p><button type="button" class="gsend">Send your story</button></div>')
def step(n, t, body, aside=""):
    return f'<section class="gs{" ga" if aside else ""}"><div><h3><i>{n}</i>{t}</h3>{body}</div>{aside}</section>'
def form(asides=None):
    a = asides or {}
    return (step(1, "What happened, and where", f_where(), a.get(1, "")) + step(2, "Who was there", f_who(), a.get(2, "")) +
            step(3, "A photograph or two", f_photo(), a.get(3, "")) + step(4, "What you learned", f_learn(), a.get(4, "")) + f_about())

# P1 guide beside the form, rules tick as fields fill
p1_rules = "".join(f'<li data-i="{i}"><span class="ck" aria-hidden="true"></span><div><b>{a}</b><small>{b}</small>' + ('<label class="gask"><input type="checkbox" data-r="2"> Everyone pictured has agreed</label>' if i == 2 else '') + ('<em>if you send any</em>' if i == 4 else '') + '</div></li>' for i, (a, b) in enumerate(RULES))
P1 = (f'<div class="p1"><div class="p1f">{HEAD}{form()}</div><aside class="p1g"><p class="gk">Before you send</p><p class="gready"><b>0</b> of 6 ready</p><ol class="grl">{p1_rules}</ol>'
      '<p class="gk" style="margin-top:18px">Five habits</p><ol class="ghb">' + "".join(f"<li>{x}</li>" for x in HABITS) + '</ol></aside></div>')

# P2 guidance at each step
def rule(i, extra=""): a, b = RULES[i]; return f'<p class="gru"><b>{a}</b>{b}{extra}</p>'
strip = '<div class="gstrip" aria-label="Eight kinds of moment">' + "".join(f'<figure><span style="{sw(c1, c2)}"></span><figcaption>{t}</figcaption></figure>' for t, d, c1, c2 in MOM) + '</div>'
P2 = (f'<div class="p2">{HEAD}' + form({1: '<aside>' + rule(3) + '</aside>', 2: '<aside>' + rule(2) + '</aside>',
       3: '<aside>' + rule(0) + rule(1) + rule(4) + '</aside>', 4: '<aside>' + rule(5) + '</aside>'}).replace('<label class="gdrop">', strip + '<label class="gdrop">', 1) + '</div>')

# P3 picture guide first
P3 = ('<div class="p3"><p class="gk">Field guide</p><h2 class="gh">Capturing the story where you are</h2><p class="gl">Most of it works with a phone. Send a range, then tell us what happened.</p>'
      '<div class="gmom">' + "".join(f'<figure><span style="{sw(c1, c2)}"></span><figcaption><b>{t}</b>{d}</figcaption></figure>' for t, d, c1, c2 in MOM) + '</div>'
      '<ol class="ghb5">' + "".join(f"<li><i>{i + 1}</i>{x}</li>" for i, x in enumerate(HABITS)) + '</ol>'
      f'<div class="p3f">{HEAD}{form()}</div></div>')

CSS = r"""
.gp{position:fixed;inset:0;z-index:100;display:grid;place-items:center;padding:max(16px,env(safe-area-inset-top,0px)) max(12px,env(safe-area-inset-right,0px)) 76px max(12px,env(safe-area-inset-left,0px))}
.gp[hidden]{display:none!important}.gbk0{position:absolute;inset:0;background:rgba(20,18,14,.55)}
.gbox{position:relative;width:min(1000px,100%);max-height:100%;overflow:auto;background:var(--paper,#f5f1e8);color:var(--ink,#1d1a16);border-radius:6px;box-shadow:0 30px 80px -20px rgba(0,0,0,.6);padding:20px clamp(18px,4vw,40px) 32px;font-family:var(--ui);box-sizing:border-box}
.gtop{position:sticky;top:-20px;z-index:2;display:flex;justify-content:space-between;align-items:center;margin:-20px calc(-1*clamp(18px,4vw,40px)) 18px;padding:12px clamp(18px,4vw,40px);background:var(--paper,#f5f1e8);border-bottom:1px solid var(--rule,#d6cebf)}
.gtag{display:inline-flex;gap:8px;align-items:center;font:700 11px/1 var(--ui);letter-spacing:.1em;text-transform:uppercase;color:#fff;background:#23406f;border-radius:999px;padding:6px 12px 6px 6px}.gtag b{background:#fff;color:#23406f;border-radius:9px;padding:3px 6px}
.gx{width:40px;height:40px;border:1px solid var(--rule,#d6cebf);background:none;border-radius:50%;font:400 22px/1 var(--ui);color:inherit;cursor:pointer}
.gk{margin:0;font:700 11px/1.3 var(--ui);letter-spacing:.14em;text-transform:uppercase;color:#b8862e}
.gh{margin:6px 0 8px;font:700 clamp(26px,3.4vw,34px)/1.12 var(--text);text-wrap:balance}
.gl{margin:0 0 18px;font:17px/1.55 var(--text);color:var(--mute);max-width:62ch}
.gs{border-top:1px solid var(--rule,#d6cebf);padding:16px 0}.gs h3{display:flex;gap:10px;align-items:baseline;margin:0 0 10px;font:700 18px var(--text)}.gs h3 i{font:700 12px var(--ui);font-style:normal;color:#fff;background:#23406f;border-radius:50%;min-width:22px;height:22px;display:grid;place-items:center}
.gs.ga{display:grid;grid-template-columns:minmax(0,1fr) 250px;gap:28px}
.gf{display:flex;flex-direction:column;gap:5px;margin:0 0 10px;font:600 13px var(--ui)}.gf small{font-weight:400;color:var(--mute)}
.gf input,.gf textarea{font:16px var(--text);color:inherit;background:var(--bar,#fdfcf9);border:1px solid var(--rule,#d6cebf);border-radius:4px;padding:9px 11px;min-height:42px;box-sizing:border-box;width:100%}
.gdrop{display:flex;flex-direction:column;align-items:center;gap:3px;border:1.5px dashed var(--rule,#cfc6b4);border-radius:6px;padding:16px;margin:0 0 10px;cursor:pointer;font:14px var(--ui);text-align:center}.gdrop input{position:absolute;opacity:0;width:1px;height:1px}.gdrop small{color:var(--mute)}.gdrop.on{border-style:solid;border-color:#1b5e6b}
.g2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px 18px}
.gab{border-top:3px double var(--rule,#d6cebf);padding-top:14px}.gpr{font:italic 15px var(--text);color:var(--mute);margin:4px 0 12px}
.gsend{font:600 14px/1 var(--ui);letter-spacing:.06em;text-transform:uppercase;background:#23406f;color:#fff;border:0;border-radius:3px;padding:14px 20px;cursor:pointer;min-height:44px}
/* P1 */
.p1{display:grid;grid-template-columns:minmax(0,1fr) 290px;gap:32px;align-items:start}
.p1g{position:sticky;top:60px;background:var(--bar,#fdfcf9);border:1px solid var(--rule,#d6cebf);border-top:3px solid #23406f;padding:16px}
.gready{margin:4px 0 10px;font:600 14px var(--ui)}.gready b{font:700 22px var(--text);color:#23406f}
.grl{list-style:none;margin:0;padding:0}.grl li{display:grid;grid-template-columns:22px 1fr;gap:10px;padding:9px 0;border-top:1px solid var(--rule,#e6dfd2);font:13px/1.4 var(--ui)}.grl b{display:block;font-size:14px}.grl small{color:var(--mute)}.grl em{display:block;font-size:12px;color:var(--mute)}
.ck{width:18px;height:18px;border:1.5px solid var(--rule,#bfb6a4);border-radius:50%;margin-top:1px;transition:.2s}.grl li.on .ck{background:#1b5e6b;border-color:#1b5e6b;box-shadow:inset 0 0 0 3px var(--bar,#fdfcf9)}
.gask{display:flex;gap:6px;align-items:center;margin-top:6px;font:600 12.5px var(--ui);min-height:32px}
.ghb{margin:6px 0 0;padding-left:18px;font:13px/1.45 var(--ui);color:var(--mute)}
/* P2 */
.p2 aside{border-left:2px solid #b8862e;padding-left:14px;align-self:start}.gru{margin:0 0 12px;font:13px/1.45 var(--ui);color:var(--mute)}.gru b{display:block;font-size:13.5px;color:var(--ink,#1d1a16);margin-bottom:2px}
.gstrip{display:grid;grid-template-columns:repeat(8,minmax(0,1fr));gap:6px;margin:0 0 12px}.gstrip figure{margin:0}.gstrip span{display:block;aspect-ratio:1;border-radius:3px}.gstrip figcaption{font:600 10.5px/1.2 var(--ui);margin-top:4px;color:var(--mute)}
/* P3 */
.gmom{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}.gmom figure{margin:0}.gmom span{display:block;aspect-ratio:4/3;border-radius:3px}.gmom figcaption{font:13px/1.4 var(--ui);color:var(--mute);margin-top:6px}.gmom b{display:block;color:var(--ink,#1d1a16);font:700 15px var(--text)}
.ghb5{list-style:none;margin:22px 0 28px;padding:0;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));border-block:1px solid var(--rule,#d6cebf)}.ghb5 li{padding:12px 12px 12px 0;font:600 13.5px/1.35 var(--ui)}.ghb5 li+li{border-left:1px solid var(--rule,#d6cebf);padding-left:12px}.ghb5 i{display:block;font:700 22px var(--text);color:#b8862e;font-style:normal}
.p3f{border-top:3px double var(--ink,#1d1a16);padding-top:18px}
@media (max-width:760px){.p1,.gs.ga,.g2{grid-template-columns:minmax(0,1fr)}.p1g{position:static}.gmom,.gbrs{grid-template-columns:repeat(2,minmax(0,1fr))}.ghb5{grid-template-columns:minmax(0,1fr)}.ghb5 li+li{border-left:0;border-top:1px solid var(--rule,#d6cebf);padding-left:0}.gstrip{grid-template-columns:repeat(4,minmax(0,1fr))}.gp-sw button{padding:10px 9px}.gp-sw button span{display:none}}
"""
V = [("GF1", "form-beside", "Guide beside the form", "The four steps on the left; the six rules on the right tick themselves as the form fills, with the five habits beneath.", P1),
     ("GF2", "form-steps", "Guidance at each step", "Each step carries its own rule in the margin; the photograph step holds the eight kinds of moment as a strip.", P2),
     ("GF3", "form-pictures", "Picture guide first", "The eight kinds of moment and the five habits come first, the form follows on the same scroll.", P3)]

CSS += r"""
.gp{padding-top:56px}.gbox{max-height:calc(100% - 8px)}.gtop{display:none}.gbox{padding-top:28px}
.gx2{position:sticky;top:-28px;float:right;margin:-14px -8px 0 0;width:40px;height:40px;border:1px solid var(--rule,#d6cebf);background:var(--paper,#f5f1e8);border-radius:50%;font:400 22px/1 var(--ui);color:inherit;cursor:pointer;z-index:3}
.reopen2{position:fixed;right:max(16px,env(safe-area-inset-right,0px));bottom:max(16px,env(safe-area-inset-bottom,0px));z-index:90;font:600 14px var(--ui);background:#23406f;color:#fff;border:0;border-radius:3px;padding:14px 18px;cursor:pointer}
.gdone{padding:24px 0}.gdone h3{font:700 24px var(--text);margin:0 0 6px}.gdone p{font:17px/1.5 var(--text);color:var(--mute);margin:0}
"""
JS = r"""var D=document,P=D.querySelector('.gp'),R=D.querySelector('.reopen2');
function op(){P.hidden=false;R.hidden=true;D.querySelector('.gx2').focus()}function cl(){P.hidden=true;R.hidden=false;R.focus()}
D.querySelector('.gx2').onclick=cl;D.querySelector('.gbk0').onclick=cl;R.onclick=op;D.addEventListener('keydown',function(e){if(e.key==='Escape'&&!P.hidden)cl()});
var p1=D.querySelector('.p1');if(p1){var tick=function(){var on=[0,0,0,0,0,0];[].forEach.call(p1.querySelectorAll('[data-r]'),function(f){var r=+f.dataset.r,v=f.type==='checkbox'?f.checked:f.type==='file'?f.files.length:f.value.trim();if(v){on[r]=1;if(r===0)on[4]=1}});
var n=0;[].forEach.call(p1.querySelectorAll('.grl li'),function(li,i){li.classList.toggle('on',!!on[i]);n+=on[i]});p1.querySelector('.gready b').textContent=n};p1.addEventListener('input',tick);p1.addEventListener('change',tick)}
[].forEach.call(D.querySelectorAll('.gdrop input'),function(f){f.onchange=function(){var l=f.parentNode;l.classList.toggle('on',!!f.files.length);l.querySelector('b').textContent=f.files.length?f.files.length+' chosen':'Choose photographs'}});
D.querySelector('.gsend').onclick=function(){var a=this.parentNode;a.innerHTML='<div class="gdone" role="status"><h3>Thank you.</h3><p>Story submissions open soon. Please keep your notes and photographs; we’d love to receive them.</p></div>'};
op();"""
