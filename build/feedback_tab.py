"""Labs study FB1: the edge tab. A tab fixed to the right edge of the curated edition opens a feedback drawer about the
issue that has just launched. Shown over the live magazine, like the other studio pages."""
ISSUE, NAME = "October / November / December 2026", "The Arts Issue"
STORIES = [("Race amity", "The Louis Gregory Bahá’í Institute", "#e8532a"),
           ("Community", "New Yorkers create more unified communities through the arts", "#f05a7e"),
           ("In conversation", "Two artists reimagine the role of art", "#b07a4a"),
           ("Scholarship", "Association for Bahá’í Studies at 50", "#c9462c"),
           ("Across America", "Communities engage in a common endeavor", "#1b5e6b")]
SCALE = ["Not for me", "Mixed", "Good", "Very good", "Excellent"]

def html():
    scale = "".join(f'<label><input type="radio" name="fe-r" value="{i}"><span class="dot" aria-hidden="true"></span><span class="lb">{t}</span></label>' for i, t in enumerate(SCALE, 1))
    reads = "".join(f'<label class="chip" style="--t:{c}"><input type="checkbox" name="fe-s" value="{i}"><span><b>{k}</b>{e}</span></label>' for i, (k, e, c) in enumerate(STORIES, 1))
    return f'''<button type="button" class="fe-tab" aria-haspopup="dialog" aria-controls="fe-d"><span>Feedback</span></button>
<div class="fe-scrim" hidden></div>
<aside class="fe-d" id="fe-d" role="dialog" aria-modal="true" aria-labelledby="fe-h" hidden>
<header class="fe-hd"><img class="fe-cv" src="../../img/cover-full-v2.jpg" alt="" width="52" height="68"><div><p class="fe-k">New issue · {ISSUE}</p><h2 id="fe-h">{NAME}: your take</h2></div>
<button type="button" class="fe-x" aria-label="Close">×</button></header>
<form class="fe-f">
<div class="fe-q fe-lead"><label for="fe-look">What do you think of the new look?</label><p class="fe-hint">The magazine has a new design this issue. Anything you notice helps: type, pictures, reading on a phone, finding your way.</p><textarea id="fe-look" rows="4"></textarea></div>
<fieldset class="fe-q"><legend>How is this issue so far?</legend><div class="fe-scale">{scale}</div></fieldset>
<fieldset class="fe-q"><legend>Which stories have you read?</legend><div class="fe-chips">{reads}</div></fieldset>
<div class="fe-q"><label for="fe-next">What should we cover next?</label><textarea id="fe-next" rows="2" placeholder="A theme, a place, a question"></textarea></div>
<div class="fe-q"><label for="fe-em">Email, if you would like a reply <span class="fe-opt">optional</span></label><input id="fe-em" type="email" autocomplete="email"></div>
<footer class="fe-ft"><span>The editors read every note.</span><button type="submit">Send</button></footer>
</form>
<div class="fe-ty" hidden><p class="fe-big">Thank you.</p><p>Your note goes to the editors, and what readers say shapes the next issue. In this study nothing is sent.</p><button type="button" class="fe-again">Write another</button></div>
</aside>'''

CSS = r"""
html,body{min-height:100%}body{overflow:hidden;background:var(--paper)}.behind{position:fixed;inset:0;width:100%;height:100%;border:0}
[hidden]{display:none!important}
.fe-tab{position:fixed;right:0;top:50%;z-index:30;transform:translateY(-50%);border:0;background:var(--ink);color:var(--paper);border-radius:10px 0 0 10px;padding:18px 11px;cursor:pointer;font:700 14px var(--ui);letter-spacing:.06em;box-shadow:-4px 6px 18px rgba(0,0,0,.14)}
.fe-tab span{writing-mode:vertical-rl;transform:rotate(180deg);display:block}.fe-tab:hover{padding-right:15px}
.fe-tab::before{content:"";position:absolute;top:10px;left:50%;width:8px;height:8px;margin-left:-4px;border-radius:50%;background:#e8532a}
.fe-scrim{position:fixed;inset:0;z-index:40;background:rgba(20,18,15,.42)}
.fe-d{position:fixed;top:0;right:0;bottom:0;z-index:50;width:min(480px,100%);background:var(--paper);color:var(--ink);display:flex;flex-direction:column;box-shadow:-20px 0 50px rgba(0,0,0,.2);animation:feIn .28s cubic-bezier(.2,.8,.2,1)}
@keyframes feIn{from{transform:translateX(40px);opacity:0}}
.fe-hd{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:14px;align-items:center;padding:20px 22px 18px;background:var(--card);border-bottom:6px solid #e8532a}
.fe-cv{width:52px;height:68px;object-fit:cover;border-radius:2px;box-shadow:0 2px 8px rgba(0,0,0,.18)}
.fe-k{margin:0 0 4px;font:500 11.5px/1.3 var(--ui);letter-spacing:.12em;text-transform:uppercase;color:var(--mute)}
.fe-hd h2{margin:0;font:800 24px/1.05 var(--ui);letter-spacing:-.025em}
.fe-x{width:44px;height:44px;border-radius:50%;border:1px solid var(--rule);background:transparent;color:var(--ink);font-size:22px;cursor:pointer}
.fe-f{flex:1;overflow:auto;padding:22px 22px 0;display:flex;flex-direction:column;gap:24px}
.fe-q{border:0;margin:0;padding:0;min-width:0;display:flex;flex-direction:column;gap:10px}
.fe-q legend,.fe-q>label{font:700 16px/1.3 var(--ui);padding:0}.fe-opt{font-weight:400;color:var(--mute)}
.fe-lead>label{font:400 26px/1.15 var(--text);letter-spacing:-.01em}.fe-hint{margin:0;font:14.5px/1.45 var(--ui);color:var(--mute)}
.fe-f textarea,.fe-f input[type=email]{width:100%;box-sizing:border-box;border:1.5px solid var(--rule);border-radius:10px;background:var(--card);color:var(--ink);padding:12px 14px;font:16px/1.45 var(--text);min-height:48px;resize:vertical}
.fe-lead textarea{border-color:var(--ink);min-height:120px}
.fe-f :focus-visible{outline:2px solid var(--link,#1b5e6b);outline-offset:2px}
.fe-scale{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));border:1.5px solid var(--rule);border-radius:10px;overflow:hidden}
.fe-scale label{position:relative;display:flex;flex-direction:column;align-items:center;gap:6px;padding:12px 4px;cursor:pointer;text-align:center}.fe-scale label+label{border-left:1px solid var(--rule)}
.fe-scale input,.fe-chips input{position:absolute;opacity:0;pointer-events:none}
.fe-scale .dot{width:14px;height:14px;border-radius:50%;border:1.5px solid var(--ink)}.fe-scale .lb{font:600 12.5px/1.2 var(--ui)}
.fe-scale label:has(input:checked){background:var(--ink);color:var(--paper)}.fe-scale label:has(input:checked) .dot{background:var(--paper);border-color:var(--paper)}
.fe-scale label:has(input:focus-visible){outline:2px solid #1b5e6b;outline-offset:-3px}
.fe-chips{display:flex;flex-direction:column;gap:6px}
.fe-chip{}.chip{position:relative;display:flex;cursor:pointer}.chip span{flex:1;display:flex;flex-direction:column;gap:2px;padding:10px 14px 10px 16px;border:1.5px solid var(--rule);border-left:6px solid var(--t);border-radius:8px;font:14.5px/1.3 var(--ui)}
.chip b{font:600 11px var(--ui);letter-spacing:.1em;text-transform:uppercase;color:var(--mute)}
.chip:has(input:checked) span{border-color:var(--ink);border-left-color:var(--t);background:var(--card)}.chip:has(input:checked) span::after{content:"Read ✓";font:700 12px var(--ui);color:var(--ink);align-self:flex-start;margin-top:2px}
.chip:has(input:focus-visible) span{outline:2px solid #1b5e6b;outline-offset:2px}
.fe-ft{position:sticky;bottom:0;margin:0 -22px;padding:14px 22px max(14px,env(safe-area-inset-bottom,0px));background:var(--paper);border-top:1px solid var(--rule);display:flex;gap:12px;align-items:center;justify-content:space-between;font:13.5px var(--ui);color:var(--mute)}
.fe-ft button,.fe-again{min-height:48px;padding:0 26px;border-radius:999px;border:0;background:var(--ink);color:var(--paper);font:700 15px var(--ui);cursor:pointer}
.fe-ty{padding:28px 22px}.fe-big{margin:0 0 8px;font:400 34px/1.1 var(--text)}.fe-ty p{margin:0 0 18px}.fe-again{background:transparent;color:var(--ink);border:1.5px solid var(--ink)}
@media (max-width:600px){.fe-tab{top:auto;bottom:max(88px,env(safe-area-inset-bottom,0px));right:12px;transform:none;border-radius:999px;padding:12px 16px}.fe-tab span{writing-mode:horizontal-tb;transform:none}.fe-tab::before{top:-3px;left:auto;right:-3px;margin:0}
.fe-d{top:auto;width:100%;height:92dvh;border-radius:16px 16px 0 0;animation-name:feUp}.fe-hd{border-radius:16px 16px 0 0}.fe-scale .lb{font-size:11.5px}}
@keyframes feUp{from{transform:translateY(40px);opacity:0}}
@media (prefers-reduced-motion:reduce){.fe-d{animation:none}}
"""

JS = r"""
var T=document.querySelector('.fe-tab'),D=document.getElementById('fe-d'),Sc=document.querySelector('.fe-scrim'),F=D.querySelector('.fe-f'),Y=D.querySelector('.fe-ty');
function op(){Sc.hidden=false;D.hidden=false;T.setAttribute('aria-expanded','true');setTimeout(function(){document.getElementById('fe-look').focus()},60)}
function cl(){D.hidden=true;Sc.hidden=true;T.setAttribute('aria-expanded','false');T.focus()}
T.onclick=op;Sc.onclick=cl;D.querySelector('.fe-x').onclick=cl;
document.addEventListener('keydown',function(e){if(D.hidden)return;if(e.key==='Escape')cl();
 if(e.key==='Tab'){var f=[].filter.call(D.querySelectorAll('button,input,textarea'),function(x){return x.offsetParent!==null});if(!f.length)return;
  if(e.shiftKey&&document.activeElement===f[0]){e.preventDefault();f[f.length-1].focus()}else if(!e.shiftKey&&document.activeElement===f[f.length-1]){e.preventDefault();f[0].focus()}}});
F.onsubmit=function(e){e.preventDefault();F.hidden=true;Y.hidden=false;Y.querySelector('button').focus()};
D.querySelector('.fe-again').onclick=function(){F.reset();Y.hidden=true;F.hidden=false;document.getElementById('fe-look').focus()};
"""
