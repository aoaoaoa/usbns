"""The field guide (FG1): Capturing Content in three steps, before you go, at the gathering, before you send.
One numbering system only, the steps; nothing inside a step is numbered. Used by build.py for /magazine/field-guide/, which is also the popup."""
import guided_forms as gf

IMG = "../img/guide2/"
TIPS, SEC, RULES = gf.TIPS, gf.SEC, gf.RULES
STEPS = ["Before you go", "At the gathering", "Before you send"]
SEND = '<a class="send" href="#" data-submit="guide">Ready? Send a story <span aria-hidden="true">→</span></a>'

def _img(p, alt): return f'<img src="{IMG}p{p:02d}.jpg" alt="{alt}" loading="lazy">'
def _foot(i):
    if i < 2: return f'<div class="sf"><span>Step {i + 1} of 3</span><button type="button" class="next" data-t="{i + 1}">{STEPS[i + 1]} <span aria-hidden="true">→</span></button></div>'
    return f'<div class="sf"><span>Step 3 of 3</span>{SEND}</div>'

def _during():
    out = []
    for k, t, ld, items in SEC:
        figs = "".join(f'<figure>{_img(n, ti or t)}' + (f'<figcaption><b>{ti}</b>{d}</figcaption>' if (d or (ti and ti != t)) else "") + '</figure>' for n, ti, d in items)
        out.append(f'<section class="bs"><h3>{t}</h3>{f"<p class=bl>{ld}</p>" if ld else ""}<div class="reel">{figs}</div></section>')
    return "".join(out)

HTML = ('<div class="fg1">'
    '<div class="tabs" role="tablist" aria-label="Steps">' + "".join(f'<button type="button" role="tab" id="fgt-{i}" aria-controls="fgp-{i}" aria-selected="{str(i == 0).lower()}" data-t="{i}"><i aria-hidden="true">{i + 1}</i><span>{x}</span></button>' for i, x in enumerate(STEPS)) + '</div>'
    '<div class="tp" role="tabpanel" id="fgp-0" aria-labelledby="fgt-0" data-t="0"><ul class="hb">' + "".join(f'<li>{x}</li>' for x in (TIPS[0], TIPS[1], TIPS[4])) + '</ul>'
    '<p class="note"><b>On a phone.</b> Wipe the lens, set your focus, and switch to silent mode before you arrive.</p>' + _foot(0) + '</div>'
    f'<div class="tp" role="tabpanel" id="fgp-1" aria-labelledby="fgt-1" data-t="1" hidden><p class="lead">{TIPS[3]}: wide, mid and close, from more than one place in the room.</p>{_during()}{gf.MB}{_foot(1)}</div>'
    f'<div class="tp" role="tabpanel" id="fgp-2" aria-labelledby="fgt-2" data-t="2" hidden><p class="lead">{TIPS[2]} before you choose what to send. Then check each of these.</p>'
    '<p class="ckn" aria-live="polite"><b>0</b> of 6 ready</p><ul class="ck">' + "".join(f'<li><label><input type="checkbox"><span><b>{a}</b>{b}</span></label></li>' for a, b in RULES) + '</ul>' + _foot(2) + '</div>'
    '</div>')

CSS = r"""
.fg1{--gold:#b8862e;--teal:#1b5e6b;--navy:#222e4c}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]) .fg1{--gold:#d7a24a;--teal:#7fc0c9}}
.fg1 .tabs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border-bottom:1px solid var(--rule);margin:8px 0 22px;position:sticky;top:0;background:var(--paper);z-index:2}
.fg1 .tabs button{background:none;border:0;border-bottom:3px solid transparent;margin-bottom:-1px;padding:14px 4px 13px;display:flex;align-items:center;gap:10px;text-align:left;font:700 15px/1.2 var(--ui);color:var(--mute);cursor:pointer}
.fg1 .tabs i{flex:none;width:26px;height:26px;border-radius:50%;border:1.5px solid currentColor;display:grid;place-items:center;font:700 13px/1 var(--ui);font-style:normal}
.fg1 .tabs button[aria-selected=true]{color:var(--ink);border-bottom-color:var(--ink)}.fg1 .tabs button[aria-selected=true] i{background:var(--ink);border-color:var(--ink);color:var(--paper)}
.fg1 .tabs button.done:not([aria-selected=true]) i{background:var(--teal);border-color:var(--teal);color:#fff;font-size:0}.fg1 .tabs button.done:not([aria-selected=true]) i::before{content:"✓";font-size:13px}
.fg1 .tabs button:focus-visible{outline:2px solid var(--link);outline-offset:-2px}
.fg1 .hb{list-style:none;margin:0 0 20px;padding:0}.fg1 .hb li{position:relative;padding:10px 0 10px 22px;font:600 17px/1.4 var(--ui)}.fg1 .hb li::before{content:"";position:absolute;left:0;top:20px;width:10px;height:2px;background:var(--gold)}
.fg1 p.note{margin:4px 0 0;padding:14px 16px;background:var(--card);border:1px solid var(--rule);border-radius:8px;font:15px/1.5 var(--ui)}
.fg1 p.lead{margin:0 0 6px;font:600 18px/1.45 var(--ui);max-width:56ch}
.fg1 .bs{padding:20px 0 6px}.fg1 .bs+.bs{border-top:1px solid var(--rule)}.fg1 .bs h3{margin:0 0 4px;font:700 21px var(--text)}.fg1 p.bl{margin:0 0 10px;font:15.5px/1.5 var(--text);color:var(--mute);max-width:60ch}
.fg1 .reel{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(200px,28%);gap:12px;overflow-x:auto;padding-bottom:10px;scroll-snap-type:x mandatory}
.fg1 figure{margin:0;scroll-snap-align:start}.fg1 figure img{display:block;width:100%;aspect-ratio:3/2;object-fit:cover;border-radius:3px;background:var(--rule)}.fg1 figcaption{font:13px/1.4 var(--ui);color:var(--mute);margin-top:6px}.fg1 figcaption b{display:block;color:var(--ink);font-size:13.5px}
.fg1 p.xmb{margin:14px 0 0;padding-top:14px;border-top:1px solid var(--rule);font:14.5px/1.5 var(--ui);color:var(--mute)}
.fg1 .sf{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px;margin-top:22px;padding-top:16px;border-top:1px solid var(--rule)}.fg1 .sf>span{font:600 13px var(--ui);color:var(--mute);letter-spacing:.04em}
.fg1 .next{min-height:48px;padding:0 20px;border:1.5px solid var(--ink);border-radius:999px;background:none;color:var(--ink);font:700 15px var(--ui);cursor:pointer}
.fg1 .send{display:inline-flex;align-items:center;gap:10px;min-height:52px;padding:0 24px;border-radius:4px;background:var(--navy);color:#fff!important;text-decoration:none;font:700 15px var(--ui);letter-spacing:.08em;text-transform:uppercase}
.fg1 p.ckn{margin:14px 0 4px;font:600 15px var(--ui)}.fg1 .ckn b{font:700 22px var(--text);color:var(--teal)}
.fg1 .ck{list-style:none;margin:0;padding:0}.fg1 .ck li+li{border-top:1px solid var(--rule)}.fg1 .ck label{display:grid;grid-template-columns:24px 1fr;gap:12px;align-items:start;padding:12px 0;cursor:pointer}
.fg1 .ck input{width:22px;height:22px;margin:2px 0 0;accent-color:var(--teal)}.fg1 .ck b{display:block;font:700 16px var(--ui);color:var(--ink)}.fg1 .ck span{font:15px/1.45 var(--ui);color:var(--mute)}.fg1 .ck label:has(input:checked) b{color:var(--teal)}
@media (max-width:760px){.fg1 .tabs button{flex-direction:column;align-items:flex-start;gap:6px;font-size:13px}.fg1 .reel{grid-auto-columns:72%}}
"""

JS = r"""<script>(function(){var R=document.querySelector('.fg1');if(!R)return;var T=[].slice.call(R.querySelectorAll('[role=tab]')),P=[].slice.call(R.querySelectorAll('.tp'));
function tab(i,focus){T.forEach(function(t){if(t.getAttribute('aria-selected')==='true'&&+t.dataset.t<+i)t.classList.add('done');t.setAttribute('aria-selected',t.dataset.t===i);t.tabIndex=t.dataset.t===i?0:-1});
  P.forEach(function(p){p.hidden=p.dataset.t!==i});var tb=R.querySelector('.tabs');if(tb.getBoundingClientRect().top<0)tb.scrollIntoView({block:'start'});if(focus)T[+i].focus()}
T.forEach(function(t,n){t.onclick=function(){tab(t.dataset.t)};t.onkeydown=function(e){var d=e.key==='ArrowRight'?1:e.key==='ArrowLeft'?-1:0;if(d){e.preventDefault();tab(String((n+d+3)%3),true)}}});tab('0');
[].forEach.call(R.querySelectorAll('.next'),function(b){b.onclick=function(){tab(b.dataset.t,true)}});
var C=[].slice.call(R.querySelectorAll('.ck input')),N=R.querySelector('.ckn b');C.forEach(function(x){x.onchange=function(){N.textContent=C.filter(function(y){return y.checked}).length}})})();</script>"""
