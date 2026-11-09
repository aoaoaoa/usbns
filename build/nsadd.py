# Newsstand additions: dateline calendar above the header, airmail survey strip,
# Listen to the issue, Browse by theme, Submit your story. Exec'd by newsstand.py.
import re as _re, os as _os, json as _json, sys as _sys
_sys.path.insert(0, '/home/claude/tab')
import data as _data, member_data as _md

def _clean(h):
    h = _re.sub(r'<!-- nsadd:sw -->.*?<!-- /nsadd:sw -->', '<div class="rowh"><h2 id="in-h">In this issue</h2></div>', h, flags=_re.S)
    h = _re.sub(r'<!-- nsadd:swjs -->.*?<!-- /nsadd:swjs -->', '', h, flags=_re.S)
    h = h.replace('class="band secin"', 'class="band"')
    h = _re.sub(r'<!-- nsadd:toc -->.*?<!-- /nsadd:toc -->', '<div class="cards">\n</div>', h, flags=_re.S)
    h = _re.sub(r'\n?<!-- nsadd:\w+ -->.*?<!-- /nsadd:\w+ -->\n?', '\n', h, flags=_re.S)
    h = _re.sub(r'/\* nsadd \*/.*?/\* /nsadd \*/\n', '', h, flags=_re.S)
    return h

# ---------- calendar data, from the issue ----------
_MONTHS = {m: i for i, m in enumerate(["January","February","March","April","May","June","July","August","September","October","November","December"], 1)}
def _iso(s, year=None):
    m = _re.match(r'([A-Z][a-z]+) (\d+)(?:, (\d{4}))?', s.strip())
    mo, d, y = _MONTHS[m.group(1)], int(m.group(2)), int(m.group(3) or year or (2027 if _MONTHS[m.group(1)] < 3 else 2026))
    return f'{y:04d}-{mo:02d}-{d:02d}'
_ring = [x[1] for a in _data.ARTICLES for x in a['body'] if x[0] == 'chart' and x[1].get('kind') == 'ring'][0]
CAL_MONTHS = [[n, en.replace('Splendour', 'Splendor').replace('Honour', 'Honor'), _iso(s)] for (n, en), s in zip(_ring['months'], _ring['starts']) if s]
CAL_EVENTS = []
for name, detail in _md.RHYTHM['holydays']:
    end = _re.search(r'through sunset ([A-Z][a-z]+ \d+(?:, \d{4})?)', detail)
    bits = [b.strip() for b in detail.split('·')]
    CAL_EVENTS.append([_iso(end.group(1)), name, f'{bits[0]} · {bits[-1].lower()}' if len(bits) > 2 else bits[0]])
for n, en, d in _md.RHYTHM['feasts']:
    CAL_EVENTS.append([_iso(d), f'Feast of {n}', en])
CAL_EVENTS.sort()

CSS_ADD = r'''/* nsadd */
/* dateline above the header */
.dl{background:var(--paper);border-bottom:1px solid var(--rule);font-family:var(--ui);font-size:12.5px;color:var(--mute)}
.dl>summary{list-style:none;cursor:pointer}.dl>summary::-webkit-details-marker{display:none}
.dl .dr{display:flex;align-items:center;gap:6px 18px;flex-wrap:wrap;min-height:34px;padding-top:6px;padding-bottom:6px}
.dl .bd{color:var(--ink);font-weight:600;letter-spacing:.02em}.dl .bd b{font-family:var(--text);font-size:14px}
.dl .gd{flex:1;min-width:0}
.dl .nx{color:var(--ink)}.dl .nx i{font-style:normal;color:var(--gold-ns,#b8782e);font-weight:700;letter-spacing:.08em;text-transform:uppercase;font-size:11px;margin-right:6px}
.dl .tg{display:inline-flex;align-items:center;gap:6px;font-weight:600;color:var(--link)}
.dl .tg svg{width:12px;height:12px;transition:transform .25s}.dl[open] .tg svg{transform:rotate(180deg)}
.dl>summary:focus-visible{outline:2px solid var(--link);outline-offset:-2px}
.dl .panel{border-top:1px solid var(--rule);background:var(--card)}
.dl .panel .wrap{padding-top:14px;padding-bottom:16px}
.cal{display:grid;grid-template-columns:auto minmax(0,1fr);gap:18px;align-items:stretch}
.today{background:#222e4c;color:#f2cfc6;border-radius:4px;padding:12px 16px;display:grid;align-content:center;gap:2px;min-width:170px}
.today .k{font:700 10px/1 var(--ui);letter-spacing:.16em;text-transform:uppercase;opacity:.8;margin-bottom:4px}
.today .d{font:300 30px/1 "Barlow Condensed","Arial Narrow",sans-serif}.today .d b{font-weight:700}
.today .m{font:italic 14px/1.3 var(--text)}
.today .y{display:none}.today .ring{display:none}
.up{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0}
.up li{display:grid;gap:2px;padding:2px 14px;border-left:1px solid var(--rule);align-content:start}
.up li:first-child{border-left:0;padding-left:0}
.up .when{font:700 10.5px/1.25 var(--ui);color:#b8782e;text-transform:uppercase;letter-spacing:.06em}
.up .when b{font:700 13px var(--ui);color:var(--ink);letter-spacing:0;text-transform:none;margin-left:4px}
.up h4{margin:0;font:700 14px/1.3 var(--text);color:var(--ink)}.up p{margin:0;font-size:12px;line-height:1.35;color:var(--mute)}
.calnote{font-size:11.5px;color:var(--mute);margin:8px 0 0}
@media (max-width:760px){.cal{grid-template-columns:1fr}.up{grid-template-columns:1fr 1fr;gap:10px 0}.up li:nth-child(3){border-left:0;padding-left:0}.dl .gd{display:none}.dl .nx{flex-basis:100%;order:3}}

/* airmail survey strip */
.air{position:relative;background:var(--stamp);padding:6px 0;color:var(--ink)}
.air::before,.air::after{content:"";position:absolute;left:0;right:0;height:6px;background:repeating-linear-gradient(-45deg,#c9462c 0 14px,transparent 14px 20px,#2f4f6e 20px 34px,transparent 34px 40px)}
.air::before{top:0}.air::after{bottom:0}
.air .wrap{display:flex;align-items:center;gap:14px;min-height:58px}
.air .pm{flex:none;width:44px;height:44px;border-radius:50%;overflow:hidden;box-shadow:0 0 0 2px var(--stamp),0 0 0 3.5px #b8782e}
.air p{margin:0;flex:1;min-width:0;font:18px/1.2 "Barlow Condensed","Arial Narrow",sans-serif}
.air p b{font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#b8782e;margin-right:8px;font-size:15px}
.air a.go{font:700 15px/1 "Barlow Condensed","Arial Narrow",sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--ink);text-decoration:none;border-bottom:2px solid #b8782e;padding-bottom:3px;white-space:nowrap}
.air a.go:hover{color:#b8782e}
@media (max-width:640px){.air p span{display:none}}

/* shared one-line rows */
.row1{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(0,1fr);gap:14px}
@media (max-width:900px){.row1{grid-auto-columns:minmax(190px,1fr);overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:10px;margin-right:calc(-1*max(16px,env(safe-area-inset-right,0px)))}.row1>*{scroll-snap-align:start}}
.secx .wrap{padding-top:52px;padding-bottom:60px}

/* listen */
.ls .lsi{display:grid;gap:10px;align-content:start;text-align:left;font:inherit;cursor:pointer;color:var(--ink);background:none;border:0;padding:0;min-width:0}
.ls .art{display:block;width:100%;height:auto;aspect-ratio:4/3}
.ls .art .fg{opacity:.55;clip-path:inset(0 100% 0 0);transition:clip-path .25s linear}
.ls .art .br{transform-box:fill-box;transform-origin:center;transform:scaleY(var(--v))}
.ls .lsi[aria-pressed=true] .art .br{animation:breathe .9s ease-in-out var(--d) infinite alternate}
@keyframes breathe{from{transform:scaleY(calc(var(--v) * .35))}to{transform:scaleY(1)}}
.ls .rw{display:flex;align-items:center;gap:10px;min-width:0}
.ls .pb{width:34px;height:34px;border-radius:50%;border:1.5px solid var(--c);color:var(--c);display:grid;place-items:center;flex:none;transition:background .2s,color .2s}
.ls .lsi:hover .pb,.ls .lsi[aria-pressed=true] .pb{background:var(--c);color:#fff}
.ls .pb svg{width:13px;height:13px;fill:currentColor}.ls .ia{display:none}.ls .lsi[aria-pressed=true] .ia{display:block}.ls .lsi[aria-pressed=true] .ip{display:none}
.ls .r{display:grid;min-width:0}
.ls .t{font:600 15px/1.25 var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ls .tm{font:600 10.5px/1.3 var(--ui);letter-spacing:.1em;text-transform:uppercase;color:var(--mute);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ls .lsi:focus-visible{outline:2px solid var(--link);outline-offset:4px;border-radius:4px}
@media (prefers-reduced-motion:reduce){.ls .lsi[aria-pressed=true] .art .br{animation:none}}
/* read / listen switch */
.swh{justify-content:space-between;align-items:center}
.sw{display:inline-flex;border:1.5px solid var(--ink);border-radius:999px;padding:3px}
.sw button{font:600 13px var(--ui);letter-spacing:.08em;text-transform:uppercase;border:0;border-radius:999px;padding:7px 16px;background:transparent;color:var(--ink);cursor:pointer}
.sw button[aria-selected=true]{background:var(--ink);color:var(--card)}
.sw button:focus-visible{outline:2px solid var(--link);outline-offset:2px}
#mode-listen{border-top:2px solid var(--ink);padding-top:18px}
#mode-listen[hidden],#mode-read[hidden]{display:none!important}
/* contents page */
.toc{list-style:none;margin:0;padding:0;border-top:2px solid var(--ink)}
.toc a{display:grid;grid-template-columns:72px minmax(0,1fr) 96px;gap:16px;align-items:center;padding:11px 0;border-bottom:1px solid var(--rule);text-decoration:none;color:var(--ink)}
.toc .pg{font:800 40px/1 var(--text);color:var(--c);letter-spacing:-.03em;font-variant-numeric:lining-nums}
.toc .k{display:block;font:600 11px/1.3 var(--ui);letter-spacing:.14em;text-transform:uppercase;color:var(--c)}
.toc .t{display:block;font:600 18px/1.25 var(--text);margin:3px 0 2px}
.toc .by{display:block;font:12.5px var(--ui);color:var(--mute)}
.toc .th{width:96px;height:64px;object-fit:cover;display:block;border-radius:2px}
.toc a:hover .t{text-decoration:underline;text-decoration-color:var(--c);text-decoration-thickness:2px;text-underline-offset:4px}
.toc a:focus-visible{outline:2px solid var(--link);outline-offset:2px}
@media (max-width:640px){.toc a{grid-template-columns:48px minmax(0,1fr);gap:12px}.toc .pg{font-size:30px}.toc .th{display:none}.toc .t{font-size:16px}}
.secin .wrap{padding-top:36px!important;padding-bottom:40px!important}
.ls .lsi:hover{border-color:var(--ink)}.ls .lsi:focus-visible{outline:2px solid var(--link);outline-offset:3px}
.nsp{position:fixed;left:0;right:0;bottom:0;z-index:25;padding:0 max(12px,env(safe-area-inset-right,0px)) max(10px,env(safe-area-inset-bottom,0px)) max(12px,env(safe-area-inset-left,0px));pointer-events:none}
.nsk{pointer-events:auto;max-width:900px;margin:0 auto;display:flex;align-items:center;gap:12px;padding:8px 10px 8px 8px;background:var(--card);border:1px solid var(--rule);border-top:2px solid #222e4c;border-radius:14px;box-shadow:0 12px 30px rgba(29,26,22,.2);transform:translateY(130%);transition:transform .3s}
.nsp.up .nsk{transform:none}
.nsp .np{flex:none;width:44px;height:44px;border-radius:50%;border:0;background:#222e4c;color:#f2cfc6;display:grid;place-items:center;cursor:pointer}.nsp .np svg{width:16px;height:16px;fill:currentColor}
.nsp .ia{display:none}.nsp.pl .ia{display:block}.nsp.pl .ip{display:none}.nsp.na .np{opacity:.45;cursor:default}
.nsp .nm{flex:1;min-width:0;display:grid;gap:3px}
.nsp .nk{font:600 10.5px var(--ui);letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}
.nsp .nt{font:600 14px/1.25 var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.nsp .nb{display:block;height:4px;background:var(--rule);border-radius:2px;cursor:pointer}.nsp .nb i{display:block;height:100%;width:0;background:#222e4c;border-radius:2px}
.nsp .ntime{font:12px var(--ui);color:var(--mute);white-space:nowrap;font-variant-numeric:tabular-nums}
.nsp .nr{font:600 13px var(--ui);color:var(--link);text-decoration:none;white-space:nowrap}
.nsp .nx{flex:none;width:34px;height:34px;border-radius:50%;border:0;background:transparent;color:var(--mute);cursor:pointer;display:grid;place-items:center}.nsp .nx svg{width:18px;height:18px}
.nsp button:focus-visible,.nsp a:focus-visible{outline:2px solid var(--link);outline-offset:2px}
.nsplay .fstamp{bottom:calc(max(18px,env(safe-area-inset-bottom,0px)) + 84px)}
.ls .s{font-family:var(--ui)}
@media (max-width:600px){.nsp .ntime{display:none}.nsp .nr{font-size:12px}}
@media (prefers-reduced-motion:reduce){.nsk{transition:none}}

/* browse by theme */
.thm a{position:relative;display:block;aspect-ratio:4/5;border-radius:4px;overflow:hidden;text-decoration:none;color:#fff;min-width:0}
.thm img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s}
.thm a::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 40%,rgba(0,0,0,.7))}
.thm a>span{position:absolute;left:14px;right:12px;bottom:12px;z-index:1;font:800 19px/1.1 var(--text)}
.thm small{display:block;font:600 11px var(--ui);letter-spacing:.14em;text-transform:uppercase;opacity:.85;margin-bottom:4px}
.thm .bar{position:absolute;left:0;right:0;top:0;height:5px;background:var(--c);z-index:1}
.thm a:hover img{transform:scale(1.05)}
.thm a:focus-visible,.ls a:focus-visible{outline:2px solid var(--link);outline-offset:3px}

/* submit your story */
.sbm{overflow:hidden}
.sbm .wrap{padding-top:56px;padding-bottom:64px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.05fr);gap:24px 56px;align-items:center}
.sbm .art{position:relative;margin:0}
.sbm .art img{display:block;width:100%;height:auto;filter:drop-shadow(0 18px 28px rgba(29,26,22,.18))}
.sbm .art figcaption{font:12px var(--ui);color:var(--mute);margin-top:8px;text-align:right}
.sbm .kk{font:700 12px/1 var(--ui);letter-spacing:.18em;text-transform:uppercase;color:#b8782e;margin:0 0 12px}
.sbm h2{font-size:clamp(30px,3.6vw,44px);line-height:1.08;margin:0 0 14px}
.sbm .ld{font-size:17px;line-height:1.55;color:var(--soft);margin:0 0 28px;max-width:46ch}
.route{list-style:none;margin:0 0 30px;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0;position:relative}
.route::before{content:"";position:absolute;left:0;right:0;top:30px;height:5px;background:repeating-linear-gradient(-45deg,#c9462c 0 10px,transparent 10px 14px,#2f4f6e 14px 24px,transparent 24px 28px);opacity:.85}
.route li{position:relative;padding-right:16px;min-width:0}
.route .no{position:relative;display:grid;place-items:center;width:62px;height:62px;border-radius:50%;background:var(--paper);border:2px solid var(--ink);font:italic 700 30px/1 var(--text);color:var(--ink);margin-bottom:14px}
.route li:last-child .no{background:#222e4c;border-color:#222e4c;color:#f2cfc6}
.route b{display:block;font:700 20px/1.1 "Barlow Condensed","Arial Narrow",sans-serif;letter-spacing:.04em;text-transform:uppercase;margin-bottom:4px}
.route span{display:block;font-size:14px;line-height:1.45;color:var(--mute)}
.sbtn{display:inline-flex;align-items:center;gap:10px;font:700 19px/1 "Barlow Condensed","Arial Narrow",sans-serif;letter-spacing:.04em;text-transform:uppercase;text-decoration:none;background:#222e4c;color:#f2cfc6;padding:14px 24px;border-radius:3px;transition:transform .2s,box-shadow .2s}
.sbtn:hover{transform:translateY(-2px);box-shadow:0 8px 18px rgba(0,0,0,.2)}.sbtn:focus-visible{outline:2px solid var(--link);outline-offset:3px}
@media (max-width:860px){.sbm .wrap{grid-template-columns:1fr}.sbm .art{max-width:520px}}
@media (max-width:560px){.route{grid-template-columns:1fr;gap:18px;padding-left:0}.route::before{left:29px;right:auto;top:0;bottom:0;width:5px;height:auto;background:repeating-linear-gradient(-45deg,#c9462c 0 10px,transparent 10px 14px,#2f4f6e 14px 24px,transparent 24px 28px)}
 .route li{display:grid;grid-template-columns:62px 1fr;gap:0 16px;align-items:center}.route .no{margin:0;grid-row:1/3}}
@media (prefers-reduced-motion:reduce){.thm img,.sbtn,.dl .tg svg{transition:none}}
/* /nsadd */
'''

def calendar_html():
    ev = _json.dumps(CAL_EVENTS, ensure_ascii=False); mo = _json.dumps(CAL_MONTHS, ensure_ascii=False)
    caret = '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2 4l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    return ('<!-- nsadd:cal --><details class="dl"><summary><div class="wrap dr">'
            '<span class="bd" id="dl-b">183 B.E.</span><span class="gd" id="dl-g"></span><span class="nx" id="dl-n"></span>'
            f'<span class="tg">Holy Days and Feasts {caret}</span></div></summary>'
            '<div class="panel"><div class="wrap"><div class="cal">'
            '<div class="today"><span class="k">In the Badí‘ calendar</span><div><div class="d" id="cal-d"></div><div class="m" id="cal-m"></div></div><div class="y" id="cal-y"></div>'
            '<svg class="ring" viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="44" fill="none" stroke="currentColor" stroke-width="1"/><circle cx="50" cy="50" r="30" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 3"/></svg></div>'
            '<div><ul class="up" id="cal-up"></ul><p class="calnote">Each Bahá’í day begins at sunset the evening before.</p></div>'
            '</div></div></div></details>\n'
            "<script>(function(){var M=" + mo + ",E=" + ev + ";"
            "var d=new Date();var mid=new Date(d.getFullYear(),d.getMonth(),d.getDate(),12);"
            "function day(s){var p=s.split('-');return new Date(+p[0],p[1]-1,+p[2],12)}"
            "var cur=-1;for(var i=0;i<M.length;i++){if(day(M[i][2])<=mid)cur=i}"
            "var bd=document.getElementById('dl-b'),g=document.getElementById('dl-g');"
            "g.textContent=mid.toLocaleDateString('en-US',{weekday:'long',month:'long',day:'numeric',year:'numeric'});"
            "document.getElementById('cal-y').textContent='183 B.E. · '+g.textContent;"
            "if(cur>=0){var n=Math.round((mid-day(M[cur][2]))/864e5)+1;if(n>=1&&n<=19){bd.innerHTML='<b>'+n+' '+M[cur][0]+'</b> · 183 B.E.';"
            "document.getElementById('cal-d').innerHTML='<b>'+n+'</b> '+M[cur][0];document.getElementById('cal-m').textContent='The month of '+M[cur][1]}}"
            "var up=document.getElementById('cal-up'),k=0,first=null;E.forEach(function(e){var t=day(e[0]);if(t<mid||k>=4)return;k++;var dd=Math.round((t-mid)/864e5);"
            "var w=dd===0?'Today':dd===1?'Tomorrow':'In '+dd+' days';if(!first)first=[w,e[1]];"
            "var li=document.createElement('li');li.innerHTML='<span class=\"when\">'+w+'<b>'+t.toLocaleDateString('en-US',{month:'short',day:'numeric'})+'</b></span><div><h4></h4><p></p></div>';"
            "li.querySelector('h4').textContent=e[1];li.querySelector('p').textContent=e[2];up.appendChild(li)});"
            "var nx=document.getElementById('dl-n');if(first){nx.innerHTML='<i>'+first[0]+'</i>';nx.appendChild(document.createTextNode(first[1]))}"
            "else{up.innerHTML='<li><span class=\"when\">Next</span><div><h4>With the next issue</h4><p>Each issue carries the Holy Days and Feasts ahead.</p></div></li>'}"
            "})();</script><!-- /nsadd:cal -->\n")

def airmail(pre, FORM):
    return (f'<!-- nsadd:air --><div class="strip air svy" role="region" aria-label="Reader survey"><div class="wrap">'
            f'<span class="pm"><img class="mo" src="{pre}img/motif/m09.webp" alt=""></span>'
            '<p><b>Reader survey</b><span>Tell us what you enjoy reading, and what to write about next.</span></p>'
            f'<a class="go" href="{FORM}" data-survey target="_blank" rel="noopener">Give feedback · 5 min</a></div></div><!-- /nsadd:air -->\n')

FEATS = [a for a in _data.ARTICLES if a['slug'] != 'comic']
THUMB = {'gregory': 'gregory-group-hd.jpg', 'newyorkers': 'ny-park.jpg', 'twoartists': 'ta-portrait.jpg', 'abs': 'abs-stage-duo.jpg', 'endeavor': 'az-ace.jpg'}
TINT = {"gregory": "#e8532a", "newyorkers": "#f05a7e", "twoartists": "#b07a4a", "abs": "#c9462c", "endeavor": "#1b5e6b"}

def _bars(seed, n=34, h=24, w=3, g=2):
    import hashlib
    b = hashlib.md5(seed.encode()).digest() * 4
    out = []
    for i in range(n):
        v = int((6 + b[i] % (h - 6) + 6 + b[i+1] % (h - 6)) / 2)
        out.append(f'<rect x="{i*(w+g)}" y="{(h-v)/2:.1f}" width="{w}" height="{v}" rx="1.5"/>')
    return n*(w+g), h, ''.join(out)

def listen_html(pre):
    items = []
    for a in sorted(FEATS, key=lambda a: int(a['pages'].split('–')[0])):
        has = _os.path.exists(f'/home/claude/usbns/audio/{a["slug"]}.mp3')
        sl = a['slug']; im = f'{pre}img/{THUMB[sl]}'
        import hashlib as _h
        bb = _h.md5(sl.encode()).digest() * 8; n = 22; Wd, Hd, gp = 240, 180, 3; bw = (Wd - (n-1)*gp) / n
        raw = [(bb[i] % 100) / 100 for i in range(n+2)]
        vs = [0.2 + 0.8 * ((raw[i] + raw[i+1] + raw[i+2]) / 3) ** 0.9 for i in range(n)]
        rects = ''.join(f'<rect class="br" style="--d:{(i*137)%900}ms;--v:{v:.2f}" x="{i*(bw+gp):.1f}" y="0" width="{bw:.1f}" height="{Hd}" rx="{bw/2:.1f}"/>' for i, v in enumerate(vs))
        art = (f'<svg class="art" viewBox="0 0 {Wd} {Hd}" aria-hidden="true"><defs><clipPath id="br-{sl}">{rects}</clipPath></defs>'
               f'<g clip-path="url(#br-{sl})"><image href="{im}" width="{Wd}" height="{Hd}" preserveAspectRatio="xMidYMid slice"/><rect class="fg" width="{Wd}" height="{Hd}" fill="var(--c)"/></g></svg>')
        items.append(f'<button type="button" class="lsi" style="--c:{TINT[sl]}" data-src="{pre}audio/{sl}.mp3" data-title="{a["title"]}" data-href="{pre}#{sl}" data-kicker="{a["kicker"]}" aria-label="Listen to {a["short"]}">{art}'
                     f'<span class="rw"><span class="pb"><svg class="ip" viewBox="0 0 16 16" aria-hidden="true"><path d="M5 3.5v9l7.5-4.5z"/></svg><svg class="ia" viewBox="0 0 16 16" aria-hidden="true"><path d="M4 3h3v10H4zM9 3h3v10H9z"/></svg></span>'
                     f'<span class="r"><span class="t">{a["short"]}</span><span class="tm"><span class="lst">{"Listen" if has else "Reading coming soon"}</span></span></span></span></button>')
    player = ('<div class="nsp" hidden role="region" aria-label="Audio player"><div class="nsk">'
              '<button type="button" class="np" aria-label="Play"><svg class="ip" viewBox="0 0 16 16" aria-hidden="true"><path d="M5 3.5v9l7.5-4.5z"/></svg><svg class="ia" viewBox="0 0 16 16" aria-hidden="true"><path d="M4 3h3v10H4zM9 3h3v10H9z"/></svg></button>'
              '<div class="nm"><span class="nk"></span><span class="nt"></span><span class="nb" role="progressbar" aria-label="Progress" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><i></i></span></div>'
              '<span class="ntime"></span><a class="nr" href="#">Read the story →</a>'
              '<button type="button" class="nx" aria-label="Close the player"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 7l10 10M17 7 7 17" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button></div></div>')
    js = r"""<script>(function(){var P=document.querySelector('.nsp');if(!P)return;var au=new Audio(),cur=null,np=P.querySelector('.np'),nb=P.querySelector('.nb'),tm=P.querySelector('.ntime');
var fmt=function(t){t=Math.max(0,Math.floor(t||0));return Math.floor(t/60)+':'+String(t%60).padStart(2,'0')};
function st(){var pl=cur&&!au.paused&&!cur.na;P.classList.toggle('pl',!!pl);np.setAttribute('aria-label',pl?'Pause':'Play');document.querySelectorAll('.lsi').forEach(function(b){b.classList.toggle('on',b===(cur&&cur.b));b.setAttribute('aria-pressed',b===(cur&&cur.b)&&pl?'true':'false')})}
function sync(){if(!cur)return;var fg=cur.b.querySelector('.fg'),lc=cur.b.querySelector('.lc');if(!cur.na&&au.duration){var pc=au.currentTime/au.duration*100;fg.style.clipPath='inset(0 '+(100-pc)+'% 0 0)';cur.b.querySelector('.lst').textContent=fmt(au.currentTime)+' / '+fmt(au.duration)}if(cur.na){tm.textContent='Reading coming soon';nb.querySelector('i').style.width='0';return}var p=au.duration?au.currentTime/au.duration*100:0;nb.querySelector('i').style.width=p+'%';nb.setAttribute('aria-valuenow',Math.round(p));tm.textContent=fmt(au.currentTime)+(au.duration?' / '+fmt(au.duration):'')}
function open(b){if(cur&&cur.b===b){if(cur.na)return;if(au.paused)au.play().catch(function(){});else au.pause();return}
 au.pause();cur={b:b,na:false};P.querySelector('.nt').textContent=b.dataset.title;P.querySelector('.nk').textContent=b.dataset.kicker;P.querySelector('.nr').href=b.dataset.href;
 P.hidden=false;document.documentElement.classList.add('nsplay');requestAnimationFrame(function(){P.classList.add('up')});au.src=b.dataset.src;tm.textContent='Loading…';var r=au.play();if(r&&r.catch)r.catch(function(){});st();}
au.addEventListener('error',function(){if(!cur)return;cur.na=true;P.classList.add('na');cur.b.querySelector('.lst').textContent='Reading coming soon';sync();st()});
au.addEventListener('playing',function(){P.classList.remove('na')});
['play','pause','ended'].forEach(function(e){au.addEventListener(e,st)});au.addEventListener('timeupdate',sync);au.addEventListener('loadedmetadata',sync);
document.querySelectorAll('.lsi').forEach(function(b){b.addEventListener('click',function(){open(b)})});
np.addEventListener('click',function(){if(cur)open(cur.b)});
P.querySelector('.nx').addEventListener('click',function(){au.pause();document.documentElement.classList.remove('nsplay');P.classList.remove('up');setTimeout(function(){P.hidden=true},300);cur=null;st()});
nb.addEventListener('click',function(e){if(!au.duration)return;var r=nb.getBoundingClientRect();au.currentTime=(e.clientX-r.left)/r.width*au.duration});
})();</script>"""
    return (f'<!-- nsadd:listen --><div class="row1 ls" id="mode-listen" role="tabpanel" aria-labelledby="tab-listen" hidden>{"".join(items)}</div><!-- /nsadd:listen -->',
            f'<!-- nsadd:player -->{player}{js}<!-- /nsadd:player -->\n')

def themes_html(pre):
    tiles = [f'<a href="{pre}#{a["slug"]}" style="--c:{TINT[a["slug"]]}"><i class="bar"></i><img src="{pre}img/{THUMB[a["slug"]]}" alt="" loading="lazy"><span><small>1 story</small>{a["kicker"]}</span></a>' for a in FEATS]
    tiles.append(f'<a href="{pre}member/" style="--c:#5b4a8a"><i class="bar"></i><img src="{pre}img/cover-print-v57n5.jpg" alt="" loading="lazy" style="object-position:50% 30%"><span><small>Members</small>The full issue</span></a>')
    return ('<!-- nsadd:themes --><section class="secx thm-s" aria-labelledby="th-h" style="border-top:1px solid var(--rule)"><div class="wrap">'
            '<div class="rowh"><h2 id="th-h">Browse by theme</h2><p>Every story, under the label it carried in print.</p></div>'
            f'<div class="row1 thm">{"".join(tiles)}</div></div></section><!-- /nsadd:themes -->\n')

def submit_html(pre, href="#"):
    steps = [("Write it", "Who, where, and what you learned. A few paragraphs is plenty."),
             ("Picture it", "Add photographs, with the photographer’s name and permission from those pictured."),
             ("Send it", "An editor reads every one and will reply.")]
    li = "".join(f'<li><span class="no">{i}</span><div><b>{t}</b><span>{s}</span></div></li>' for i, (t, s) in enumerate(steps, 1))
    return ('<!-- nsadd:submit --><section class="sbm" style="border-top:1px solid var(--rule)" aria-labelledby="sb-h"><div class="wrap">'
            f'<figure class="art"><img src="{pre}img/story-paint.webp" alt="Children’s hands at a watercolor set beside paintings, one lettered I am kind, loving, and friendly" width="1400" height="1203" loading="lazy"><figcaption>Painting with neighbors in Crown Heights, Brooklyn, from this issue</figcaption></figure>'
            '<div><p class="kk">From your community</p><h2 id="sb-h">Have a story to tell?</h2>'
            '<p class="ld">The American Bahá’í is written from the reports of Bahá’ís across the country. Yours could be next.</p>'
            f'<ol class="route">{li}</ol><a class="sbtn" href="{href}">Submit your story <span aria-hidden="true">→</span></a></div>'
            '</div></section><!-- /nsadd:submit -->\n')

def contents_html(pre):
    order = sorted(FEATS, key=lambda a: int(a['pages'].split('–')[0]))
    rows = []
    for a in order:
        by = a.get('byline') or ''
        rows.append(f'<li><a href="{pre}#{a["slug"]}" style="--c:{TINT[a["slug"]]}"><span class="pg">{a["pages"].split("–")[0]}</span>'
                    f'<span class="tx"><span class="k">{a["kicker"]}</span><span class="t">{a["title"]}</span>{("<span class=by>"+by+"</span>") if by else ""}</span>'
                    f'<img class="th" src="{pre}img/{THUMB[a["slug"]]}" alt="" loading="lazy" width="120" height="80"></a></li>')
    return f'<ol class="toc">{"".join(rows)}</ol>'

SW_JS = ("<!-- nsadd:swjs --><script>(function(){var t=document.querySelectorAll('.sw [role=tab]');t.forEach(function(b){b.addEventListener('click',function(){"
         "t.forEach(function(x){var on=x===b;x.setAttribute('aria-selected',on);document.getElementById(x.getAttribute('aria-controls')).hidden=!on});"
         "try{sessionStorage.setItem('tab-ns-mode',b.id)}catch(e){}})});"
         "try{var m=sessionStorage.getItem('tab-ns-mode');if(m&&document.getElementById(m))document.getElementById(m).click()}catch(e){}})();</script><!-- /nsadd:swjs -->")

def add_sections(h, pre, FORM):
    h = _clean(h)
    h = h.replace('</style>', CSS_ADD + '</style>', 1)
    # dateline calendar above the header
    h = h.replace('<header>', calendar_html() + '<header>', 1)
    # In this issue as a contents page
    i = h.index('<section class="band" aria-labelledby="in-h">'); a0 = h.index('<div class="cards">', i); a1 = h.index('</div>\n</div></section>', a0)
    h = h[:i] + h[i:a0].replace('class="band"','class="band secin"',1) + '<!-- nsadd:toc -->' + contents_html(pre) + '<!-- /nsadd:toc -->' + h[a1+len('</div>'):]
    # Listen joins In this issue as the second mode of one section
    row, player = listen_html(pre)
    sw = ('<div class="sw" role="tablist" aria-label="Read or listen">'
          '<button type="button" role="tab" id="tab-read" aria-selected="true" aria-controls="mode-read">Read</button>'
          '<button type="button" role="tab" id="tab-listen" aria-selected="false" aria-controls="mode-listen">Listen</button></div>')
    h = h.replace('<div class="rowh"><h2 id="in-h">In this issue</h2></div>', '<!-- nsadd:sw --><div class="rowh swh"><h2 id="in-h">In this issue</h2>' + sw + '</div><!-- /nsadd:sw -->', 1)
    h = h.replace('<ol class="toc">', '<ol class="toc" id="mode-read" role="tabpanel" aria-labelledby="tab-read">', 1)
    h = h.replace('<!-- /nsadd:toc -->', '<!-- /nsadd:toc -->' + row, 1)
    h = h.replace('</body>', player + SW_JS + '</body>', 1)
    # themes after the archive
    i = h.index('<section id="archive"'); j = h.index('</div></section>', i) + len('</div></section>')
    h = h[:j] + '\n' + themes_html(pre) + h[j:]
    # Featured Reports: off for now (kept in the page as a comment)
    if '<section id="special"' in h and '<!-- Featured Reports: hidden' not in h:
        i = h.index('<section id="special"'); j = h.index('</div></section>', i) + len('</div></section>')
        h = h[:i] + '<!-- Featured Reports: hidden for now\n' + h[i:j].replace('--', '- -') + '\n-->' + h[j:]
    # submit after Browse by theme
    i = h.index('<!-- /nsadd:themes -->') + len('<!-- /nsadd:themes -->')
    h = h[:i] + '\n' + submit_html(pre) + h[i:]
    return h
