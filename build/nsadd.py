# Newsstand additions: dateline calendar above the header, airmail survey strip,
# Listen to the issue, Browse by theme, Submit your story. Exec'd by newsstand.py.
import re as _re, os as _os, json as _json, sys as _sys
_sys.path.insert(0, '/home/claude/tab')
import data as _data, member_data as _md

def _clean(h):
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
.dl .panel .wrap{padding-top:28px;padding-bottom:32px}
.cal{display:grid;grid-template-columns:minmax(240px,.8fr) 1.2fr;gap:28px;align-items:stretch}
.today{background:#222e4c;color:#f2cfc6;border-radius:4px;padding:24px;display:grid;align-content:space-between;gap:16px;position:relative;overflow:hidden}
.today .k{font:700 11px/1 var(--ui);letter-spacing:.18em;text-transform:uppercase;opacity:.8}
.today .d{font:300 58px/.95 "Barlow Condensed","Arial Narrow",sans-serif}.today .d b{font-weight:700}
.today .m{font:italic 19px/1.3 var(--text)}
.today .y{font:16px "Barlow Condensed","Arial Narrow",sans-serif;opacity:.85}
.today .ring{position:absolute;right:-40px;bottom:-40px;width:170px;height:170px;opacity:.45}
.up{list-style:none;margin:0;padding:0}
.up li{display:grid;grid-template-columns:78px 1fr;gap:14px;padding:13px 0;border-top:1px solid var(--rule);align-items:start}
.up li:first-child{border-top:0;padding-top:0}
.up .when{font:700 11.5px/1.25 var(--ui);color:#b8782e;text-transform:uppercase;letter-spacing:.06em}
.up .when b{display:block;font:800 28px/1 var(--text);color:var(--ink);letter-spacing:0;text-transform:none}
.up h4{margin:0 0 3px;font:700 17px/1.3 var(--text);color:var(--ink)}.up p{margin:0;font-size:13.5px;color:var(--mute)}
.calnote{font-size:12.5px;color:var(--mute);margin:16px 0 0}
@media (max-width:760px){.cal{grid-template-columns:1fr}.dl .gd{display:none}.dl .nx{flex-basis:100%;order:3}}

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
.ls a{display:grid;grid-template-columns:56px minmax(0,1fr);gap:10px;align-items:center;text-decoration:none;color:var(--ink);padding:9px;border:1px solid var(--rule);border-radius:4px;background:var(--paper);min-width:0}
.ls .th{position:relative;width:56px;height:56px;border-radius:3px;overflow:hidden}
.ls .th img{width:100%;height:100%;object-fit:cover;display:block}
.ls .th::after{content:"";position:absolute;inset:0;margin:auto;width:26px;height:26px;border-radius:50%;background:rgba(29,26,22,.72) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M5.5 4v8l6.5-4z' fill='%23fff'/%3E%3C/svg%3E") center/15px no-repeat}
.ls .t{display:block;font:600 14px/1.25 var(--ui);overflow:hidden;text-overflow:ellipsis;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
.ls .s{display:block;font-size:12px;color:var(--mute);margin-top:2px}
.ls a:hover{border-color:var(--ink)}

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
            '<div><ul class="up" id="cal-up"></ul><p class="calnote">From the issue’s Rhythm of Bahá’í Life listing. Each Bahá’í day begins at sunset the evening before.</p></div>'
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

def listen_html(pre):
    items = []
    for a in FEATS:
        has = _os.path.exists(f'/home/claude/usbns/audio/{a["slug"]}.mp3')
        items.append(f'<a href="{pre}#{a["slug"]}"><span class="th"><img src="{pre}img/{THUMB[a["slug"]]}" alt="" loading="lazy"></span>'
                     f'<span><span class="t">{a["short"]}</span><span class="s">{a["kicker"]} · {"Listen" if has else "Reading coming soon"}</span></span></a>')
    return ('<!-- nsadd:listen --><section class="band secx ls-s" aria-labelledby="ls-h"><div class="wrap">'
            '<div class="rowh"><h2 id="ls-h">Listen to the issue</h2><p>Each story, read aloud.</p></div>'
            f'<div class="row1 ls">{"".join(items)}</div></div></section><!-- /nsadd:listen -->\n')

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

def add_sections(h, pre, FORM):
    h = _clean(h)
    h = h.replace('</style>', CSS_ADD + '</style>', 1)
    # dateline calendar above the header
    h = h.replace('<header>', calendar_html() + '<header>', 1)
    # listen after "In this issue"
    i = h.index('<section class="band" aria-labelledby="in-h">'); j = h.index('</div></section>', i) + len('</div></section>')
    h = h[:j] + '\n' + listen_html(pre) + h[j:]
    # themes after the archive
    i = h.index('<section id="archive"'); j = h.index('</div></section>', i) + len('</div></section>')
    h = h[:j] + '\n' + themes_html(pre) + h[j:]
    # submit before Featured Reports
    i = h.index('<section id="special"')
    h = h[:i] + submit_html(pre) + h[i:]
    return h
