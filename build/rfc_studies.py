# Open call (RFC) studies, compiled with Capturing Content (bicentenary.bahai.org support document). Used by stories_gallery.py.
IMG = {}  # image key -> src; defaults to the magazine's own img/ from a story-ctas page
def im(k, alt=""): return f'<img src="{IMG.get(k, "../../img/" + k)}" alt="{alt}" loading="lazy">'
ARR = '<span aria-hidden="true">→</span>'
THEMES = [("Education", "Winter 2027", "In homes February 2027", "now"), ("National Convention", "Spring 2027", "In homes May 2027", "next"), ("Race Unity", "Summer 2027", "In homes August 2027", "later")]
QUOTE = "“Regard man as a mine rich in gems of inestimable value. Education can, alone, cause it to reveal its treasures, and enable mankind to benefit therefrom.”"
QSRC = "Bahá’u’lláh, Gleanings from the Writings of Bahá’u’lláh, CXXII"
WAYS = [("idea", "Share an idea", "A minute", "A sentence about something worth a closer look where you live.", "Feeds the editors’ list for this theme."),
        ("photo", "Send photographs or video", "A few minutes", "Pictures or short clips from a class, a gathering, a project.", "May run as a microstory, on social media, or join the photo library for future stories."),
        ("pitch", "Pitch a story", "Half an hour", "Who, where, what changed, and why it matters now.", "An editor writes back about where it could go."),
        ("write", "Write with us", "A few weeks", "Report and write a story with an editor beside you.", "Published with your byline."),
        ("join", "Join the contributor network", "Ongoing", "Writers, photographers, videographers and local correspondents.", "Hear about themes first and work from the full guide.")]
USES = [("Feature", "A full story in the magazine"), ("Microstory", "A photograph or clip with a few lines"), ("Social", "Shared on the magazine’s channels"), ("Photo library", "B-roll and stills for future stories")]
FORM = '<form class="mini" onsubmit="event.preventDefault();this.classList.add(\'sent\')"><label for="{i}">{l}</label><div class="fr"><input id="{i}" placeholder="{p}"><button type="submit">{b} ' + ARR + '</button></div><p class="ok" role="status">Thank you. This is a demo; nothing was sent.</p></form>'

# ---------------- R1 The open call
r1 = f'''<section class="r1"><div class="g"><div class="w hero">
<div class="hx"><p class="kk">Open call · Winter 2027</p><h1>Education</h1><p class="ld">The American Bahá’í is gathering stories, photographs and ideas for its Education issue. Whatever you have, there is a way to share it.</p>
<blockquote><p>{QUOTE}</p><cite>{QSRC}</cite></blockquote>
<p class="kd">We’re looking for</p><ul class="chips"><li>Children’s classes</li><li>Junior youth groups</li><li>Study circles</li><li>Tutor training</li><li>Seasonal Bahá’í schools</li><li>Learning wherever it happens</li></ul></div>
<figure class="hf">{im("ny-table.jpg","Children’s hands painting with watercolors at a picnic table")}<figcaption>Crown Heights, Brooklyn · this issue</figcaption></figure></div></div>
<div class="g band"><div class="w"><h2>Five ways to take part</h2><ol class="ways">''' + "".join(f'<li><span class="t">{t}</span><b>{n}</b><p>{d}</p><p class="u">{u}</p></li>' for k,n,t,d,u in WAYS) + f'''</ol></div></div>
<div class="g"><div class="w two"><div><h2>Where it can go</h2><ul class="uses">''' + "".join(f"<li><b>{a}</b>{b}</li>" for a,b in USES) + f'''</ul></div>
<div><h2>Coming up</h2><ul class="up">''' + "".join(f'<li class="{s}"><b>{n}</b><span>{se} · {h}</span><i>{"Gathering now" if s=="now" else "Opens next" if s=="next" else "Later in 2027"}</i></li>' for n,se,h,s in THEMES) + f'''</ul></div></div></div>
<div class="g"><div class="w cta"><p>New to this? Start with the <a href="#" data-go="4">field guide</a>, or just send what you have.</p><a class="btn" href="#">Take part {ARR}</a></div></div></section>'''

# ---------------- R2 Ways in, by time
r2 = '<section class="r2"><div class="g"><div class="w"><p class="kk">Open call · Education · Winter 2027</p><h1 class="h">Everyone has something to bring.</h1><p class="ld">Choose by the time you have. Each way in is welcome, and each one helps.</p></div></div><div class="g"><div class="w lad">'
for i,(k,n,t,d,u) in enumerate(WAYS):
    fld = {"idea":("ri1","Your idea","A grandmother teaches a children’s class in Spanish…","Send"),
           "photo":("ri2","Where and when were they taken?","Saturday class, Westlake, Indianapolis","Choose files"),
           "pitch":("ri3","Your pitch, in one line","A junior youth group in our town runs the food pantry…","Pitch it"),
           "write":("ri4","What would you like to write about?","Study circles at the community college","Ask an editor"),
           "join":("ri5","Your email","you@example.org","Join")}[k]
    r2 += f'<article class="step" style="--n:{i}"><p class="tm">{t}</p><div><h2>{n}</h2><p>{d}</p><p class="u">{u}</p>{FORM.format(i=fld[0],l=fld[1],p=fld[2],b=fld[3])}</div></article>'
r2 += '</div></div></section>'

# ---------------- R3 The cycle
PH = [("Call opens", "Themes announced with the issue before"), ("Gathering", "Ideas, pictures, pitches and drafts come in"), ("Editors choose", "We write to everyone whose work we use"), ("In homes", "The issue arrives and the next call opens")]
r3 = '<section class="r3"><div class="g"><div class="w"><p class="kk">The open call</p><h1 class="h">A call with every issue.</h1><p class="ld">Each issue of The American Bahá’í has a theme, and each theme opens a call. Here is where the next three stand.</p></div></div><div class="g"><div class="w cyc">'
for n,se,h,s in THEMES:
    cur = {"now":1,"next":0,"later":-1}[s]
    r3 += f'<article class="iss {s}"><header><p class="se">{se}</p><h2>{n}</h2><p class="hm">{h}</p></header><ol>' + "".join(f'<li class="{"on" if j==cur else "done" if j<cur else ""}"><b>{p}</b><span>{d}</span></li>' for j,(p,d) in enumerate(PH)) + f'</ol><p class="st">{"Gathering now. Send what you have." if s=="now" else "Opens when Education goes to print." if s=="next" else "Opens in spring."}</p></article>'
r3 += f'</div></div><div class="g"><div class="w note3"><p>Dates for each phase are set by the editors. This study shows only the order, and the issues already announced.</p></div></div><div class="g"><div class="w sub3"><p class="kk">Hear when a call opens</p><form class="mini" onsubmit="event.preventDefault();this.classList.add(\'sent\')"><label for="rc">Email address</label><div class="fr"><input id="rc" type="email" placeholder="you@example.org"><button type="submit">Notify me {ARR}</button></div><p class="ok" role="status">Thank you. This is a demo; nothing was sent.</p></form></div></div></section>'

# ---------------- R4 Brief board
BR = [("Photo", "A children’s class in session, wide", "Show the room, the teacher and the children together, faces visible. One wide shot gives the whole scene.", ["Photo library", "Feature"], "gregory-circle.jpg", "Wide shot"),
      ("Photo", "Hands at work", "Close on hands: painting, writing, building, serving. No faces needed, which helps when children are present.", ["Microstory", "Social"], "ny-table.jpg", "Detail"),
      ("Video", "Sixty seconds of a study circle", "Hold the phone steady and horizontal. Shoot over a shoulder so the conversation is the subject.", ["Social", "Photo library"], "ny-film.jpg", "Over the shoulder"),
      ("Pitch", "A home that hosts a class", "Who opened their door, how it began, and what the neighbors noticed. A few lines is enough to start.", ["Feature"], "az-ace.jpg", "Story lead"),
      ("Photo", "The sign at the door", "Get the name of the place or event in the frame, so nobody has to guess what it was.", ["Photo library"], "gregory-sign-hd.jpg", "Context"),
      ("Words", "What a child learned this week", "A parent, tutor or teacher, in their own words. Two or three sentences, and the child’s first name only with permission.", ["Microstory", "Social"], "gv-table.jpg", "Microstory")]
r4 = '<section class="r4"><div class="g"><div class="w"><p class="kk">Open briefs · Education · Winter 2027</p><h1 class="h">What we’re looking for right now</h1><p class="ld">Pick a brief that fits what you have. Each one says what we need and where it may appear.</p>'
r4 += '<div class="flt" role="group" aria-label="Filter briefs"><button aria-pressed="true" data-f="">All</button>' + "".join(f'<button aria-pressed="false" data-f="{x}">{x}</button>' for x in ("Photo","Video","Pitch","Words")) + '</div></div></div><div class="g"><div class="w brd">'
for k,t,d,us,img,sh in BR:
    r4 += f'<article class="br" data-k="{k}"><figure>{im(img,"")}<span class="sh">{sh}</span></figure><div class="bt"><p class="kd">{k}</p><h2>{t}</h2><p>{d}</p><ul>' + "".join(f"<li>{u}</li>" for u in us) + f'</ul><a href="#" class="tk">Answer this brief {ARR}</a></div></article>'
r4 += '</div></div></section>'

# ---------------- R5 Field guide
FR = [("Wide shot", "Gives a sense of the space and the context.", "gregory-circle.jpg"),
      ("Mid-shot", "Shows many people while staying close enough to see their faces.", "gregory-panel-hd.jpg"),
      ("Medium close-up", "Makes the viewer feel part of the space.", "gv-table.jpg"),
      ("Close-up", "Gives a sense of focus.", "ta-portrait.jpg"),
      ("Extreme close-up", "Shows emotion in a more dramatic way.", None),
      ("Audience view", "Shows the event from where the audience sits.", "ny-film.jpg")]
SIT = [("Audience", "A wide shot with many faces clearly visible. Add reaction shots: one person listening, laughing, moved."),
       ("Stage", "Keep the event’s title in the frame. Make sure the microphone doesn’t hide a speaker’s face. Look for warm engagement with the audience."),
       ("Community", "Neighborhood gatherings can be spontaneous, intimate and delicate. A phone is fine: wipe the lens and set your focus. Use silent mode or a zoom so you don’t interrupt."),
       ("Action", "Raise the shutter speed to match the light and the movement. Focus on one person; faces draw the eye."),
       ("Devotion", "Devotion takes different forms and asks for a quiet, creative approach. Be especially mindful of your presence.")]
TIPS = ["Be conscientious of your presence in the room", "Be ready for spontaneous moments", "Capture a series of angles", "Keep a steady hand", "Review your work on a bigger screen"]
SPEC = [("Send originals", "Full-size files straight from the camera or phone, not screenshots or messaging copies."),
        ("Name the photographer", "Every picture carries a credit."),
        ("Ask first", "Everyone recognizable has agreed to be pictured. For children, a parent or guardian."),
        ("Say where and when", "Town or neighborhood, state, and the date."),
        ("Video", "Steady and horizontal for the photo library; vertical is welcome for social. Ten seconds per shot or longer.")]
r5 = '<section class="r5"><div class="g"><div class="w gh"><p class="kk">Field guide</p><h1 class="h">Capturing the story where you are</h1><p class="ld">A short guide for anyone sending photographs or video. Most of it works with a phone.</p><ol class="tips">' + "".join(f"<li>{t}</li>" for t in TIPS) + '</ol></div></div>'
r5 += '<div class="g"><div class="w"><h2>Framing, from wide to close</h2><div class="fr6">' + "".join(f'<figure>{im(i,"") if i else "<div class=ph aria-hidden=true></div>"}<figcaption><b>{n}</b>{d}</figcaption></figure>' for n,d,i in FR) + '</div><p class="cap">Examples from this issue. The guide asks for a range: one wide, some mid, a few close.</p></div></div>'
r5 += '<div class="g"><div class="w two"><div><h2>Composition</h2><dl class="cmp"><dt>Thirds</dt><dd>Balance the picture on a grid of thirds; place the subject on a line, not dead center.</dd><dt>Vanishing point</dt><dd>Lines that run into the distance add depth.</dd><dt>Depth and focus</dt><dd>A sharp subject against a softer background.</dd><dt>Over the shoulder</dt><dd>Catches warm exchanges between people.</dd><dt>Candid and posed</dt><dd>Both are welcome. Group photos let us see everyone’s face; no group is too small.</dd></dl></div>'
r5 += '<div><h2>By situation</h2><dl class="cmp">' + "".join(f"<dt>{a}</dt><dd>{b}</dd>" for a,b in SIT) + '</dl></div></div></div>'
r5 += '<div class="g band"><div class="w"><h2>Before you send</h2><p class="pr">Proposed starter specs, to be confirmed by the editors.</p><ul class="spec">' + "".join(f"<li><b>{a}</b>{b}</li>" for a,b in SPEC) + '</ul><p class="mb">For examples of strong pictures of community life, browse the Bahá’í Media Bank at media.bahai.org.</p></div></div></section>'

# ---------------- R6 Contributor desk
ROLES = [("Contributing writer", "Report and write features with an editor."), ("Photographer", "Cover gatherings and classes near you, and build the photo library."), ("Videographer", "Short clips and b-roll for social and future stories."), ("Local correspondent", "Keep an eye out in your area and send leads.")]
OFFER = ["Each theme before it’s announced", "An editor’s notes on your work", "The full content guide and specs", "Your name with everything we use"]
r6 = f'''<section class="r6"><div class="g"><div class="w d6"><div class="dl"><p class="kk">Contributor network</p><h1 class="h">Tell the stories of your community, with us.</h1>
<p class="ld">The American Bahá’í is building a circle of contributors across the country. No experience in journalism is needed: care for your community and a willingness to learn are enough.</p>
<h2>What we offer</h2><ul class="of">''' + "".join(f"<li>{o}</li>" for o in OFFER) + '''</ul></div>
<form class="apply" onsubmit="event.preventDefault();this.classList.add('sent')"><h2>Express interest</h2><fieldset><legend>I’d like to</legend>''' + "".join(f'<label><input type="checkbox" name="role" id="ro{i}"><span><b>{a}</b>{b}</span></label>' for i,(a,b) in enumerate(ROLES)) + '''</fieldset>
<label for="an">Name</label><input id="an" autocomplete="name"><label for="ae">Email</label><input id="ae" type="email" autocomplete="email"><label for="aw">Where you live</label><input id="aw" placeholder="Town or neighborhood, state">
<label for="ak">A link to something you’ve made (optional)</label><input id="ak" placeholder="Photos, writing, video"><button type="submit">Send ''' + ARR + '''</button><p class="ok" role="status">Thank you. This is a demo; nothing was sent.</p></form></div></div></section>'''

V = [("Open call", "One page per issue: the theme, five ways in, where things go, and what’s coming.", r1),
     ("Ways in", "Organized by the time a visitor has, from a minute to ongoing, each with its own small form.", r2),
     ("The cycle", "The call as a rhythm: every issue opens one, and each card shows its phase.", r3),
     ("Brief board", "Specific open requests for the current theme, each tagged with format and where it may appear.", r4),
     ("Field guide", "The standards page, compiled from Capturing Content and illustrated with this issue’s photographs.", r5),
     ("Contributor desk", "An invitation to join the network of writers, photographers, videographers and correspondents.", r6)]
SLUGS = ["rfc-open-call", "rfc-ways-in", "rfc-cycle", "rfc-brief-board", "rfc-field-guide", "rfc-contributor-desk"]
tabs = "".join(f'<button type="button" role="tab" id="t{i}" aria-controls="v{i}" aria-selected="{str(i==0).lower()}"><b>R{i+1}</b>{n}</button>' for i,(n,_,_) in enumerate(V))
views = "".join(f'<div class="v" id="v{i}" role="tabpanel" aria-labelledby="t{i}"{"" if i==0 else " hidden"}><p class="note g"><b>R{i+1} · {n}.</b> {d}</p>{h}</div>' for i,(n,d,h) in enumerate(V))

CSS = """
/* Layout: one open-call page at a time, in the magazine's own palette; each study is a full landing. */
:root{--paper:#f5f1e8;--card:#fdfcf9;--ink:#1d1a16;--mute:#6a635a;--rule:#d9d2c4;--navy:#222e4c;--blush:#f2cfc6;--onnavy:#fbf7ef;--gold:#9a6224;--teal:#2f6b79;
--text:"Literata",Georgia,serif;--ui:"Bricolage Grotesque",system-ui,sans-serif;--cond:"Barlow Condensed","Arial Narrow",sans-serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#15130f;--card:#1f1c17;--ink:#efe9dd;--mute:#a39b8e;--rule:#2f2a22;--navy:#1a2340;--gold:#d9a35f;--teal:#73b8c4;color-scheme:dark}}
:root[data-theme="dark"]{--paper:#15130f;--card:#1f1c17;--ink:#efe9dd;--mute:#a39b8e;--rule:#2f2a22;--navy:#1a2340;--gold:#d9a35f;--teal:#73b8c4;color-scheme:dark}
*{box-sizing:border-box}body{background:var(--paper);color:var(--ink);font:16px/1.55 var(--ui)}
.g{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.w{max-width:1120px;margin:0 auto}img{max-width:100%;display:block}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--card)}
.bar{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--card);border-bottom:1px solid var(--rule);padding-block:10px}
.bar .w{display:flex;gap:6px;overflow-x:auto;scrollbar-width:none}
.bar button{flex:none;font:600 13px var(--ui);color:var(--ink);background:none;border:1px solid var(--rule);border-radius:999px;padding:7px 13px 7px 7px;cursor:pointer;display:flex;gap:7px;align-items:center}
.bar button b{font:700 11px var(--ui);background:var(--rule);color:var(--ink);border-radius:999px;padding:3px 7px}
.bar button[aria-selected=true]{background:var(--ink);color:var(--paper);border-color:var(--ink)}.bar button[aria-selected=true] b{background:var(--paper);color:var(--ink)}
:focus-visible{outline:2px solid var(--teal);outline-offset:2px}
.note{max-width:1120px;margin:0 auto;padding-block:10px;font:13px/1.45 var(--ui);color:var(--mute)}.note b{color:var(--ink)}
.kk{font:700 12px/1 var(--ui);letter-spacing:.18em;text-transform:uppercase;color:var(--gold);margin:0 0 14px}
.kd{font:600 11px var(--ui);letter-spacing:.16em;text-transform:uppercase;color:var(--mute);margin:0 0 8px}
h1,h2{font-family:var(--text);text-wrap:balance;margin:0}
.h{font:700 clamp(32px,4.6vw,52px)/1.08 var(--text);margin:0 0 14px;max-width:18ch}
.ld{font:clamp(17px,1.8vw,20px)/1.55 var(--text);color:var(--mute);margin:0 0 28px;max-width:60ch;text-wrap:pretty}
h2{font-size:clamp(21px,2.2vw,26px);line-height:1.2;margin:0 0 16px}
.btn{display:inline-flex;gap:8px;align-items:center;font:700 18px var(--cond);letter-spacing:.06em;text-transform:uppercase;text-decoration:none;background:var(--navy);color:var(--blush);padding:13px 24px;border-radius:3px}
section>.g{padding-block:48px}section>.g+.g{padding-top:0}
.band{background:var(--card);border-block:1px solid var(--rule);padding-block:48px!important}
.two{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:48px}
.mini{display:grid;gap:6px;margin-top:14px}.mini label{font:600 13px var(--ui)}.fr{display:flex;gap:8px;flex-wrap:wrap}
.mini input,.apply input{flex:1 1 200px;min-width:0;font:15px var(--text);padding:10px 12px;border:1px solid var(--rule);background:var(--card);color:var(--ink);border-radius:3px}
.mini button,.apply button{font:700 15px var(--cond);letter-spacing:.06em;text-transform:uppercase;background:var(--navy);color:var(--blush);border:0;border-radius:3px;padding:10px 16px;cursor:pointer}
.ok{display:none;margin:4px 0 0;font:13px var(--ui);color:var(--teal)}.sent .ok{display:block}
/* R1 */
.hero{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:48px;align-items:center}
.r1 h1{font:800 clamp(52px,8vw,104px)/.95 var(--text);letter-spacing:-.02em;margin:0 0 18px}
.r1 blockquote{margin:0 0 26px;padding-left:18px;border-left:2px solid var(--gold)}.r1 blockquote p{margin:0 0 6px;font:italic 17px/1.55 var(--text)}.r1 cite{font:12px var(--ui);color:var(--mute);font-style:normal}
.chips{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:8px}.chips li{font:500 14px var(--ui);border:1px solid var(--rule);background:var(--card);border-radius:999px;padding:5px 12px}.chips li:last-child{border-style:dashed}
.hf{margin:0}.hf img{width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:3px;transform:rotate(1.5deg);box-shadow:0 18px 40px rgba(29,26,22,.18)}.hf figcaption{font:12px var(--ui);color:var(--mute);margin-top:12px}
.ways{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:16px;counter-reset:w}
.ways li{background:var(--paper);border:1px solid var(--rule);border-radius:4px;padding:18px;display:grid;align-content:start;gap:6px}
.ways .t{font:600 12px var(--cond);letter-spacing:.12em;text-transform:uppercase;color:var(--gold)}.ways b{font:700 18px/1.25 var(--text)}.ways p{margin:0;font-size:14px}.ways .u{color:var(--mute);font-size:13px}
.uses,.up{list-style:none;margin:0;padding:0;display:grid;gap:0}.uses li,.up li{display:grid;gap:2px;padding:12px 0;border-top:1px solid var(--rule)}.uses b,.up b{font:700 17px var(--text)}
.up li{grid-template-columns:1fr auto;align-items:center}.up span{grid-column:1;font-size:14px;color:var(--mute)}.up i{grid-row:1/3;grid-column:2;font:600 12px var(--ui);font-style:normal;border-radius:999px;padding:4px 10px;border:1px solid var(--rule)}
.up .now i{background:var(--navy);color:var(--blush);border-color:var(--navy)}
.cta{display:flex;flex-wrap:wrap;gap:16px 32px;align-items:center;justify-content:space-between;border-top:1px solid var(--rule);padding-top:28px}.cta p{margin:0;font:18px var(--text)}.cta a:not(.btn){color:var(--teal)}
/* R2 */
.lad{display:grid;gap:0}.step{display:grid;grid-template-columns:200px minmax(0,1fr);gap:32px;padding:28px 0;border-top:1px solid var(--rule)}
.step .tm{margin:0;font:600 clamp(26px,3vw,34px)/1 var(--cond);letter-spacing:.02em;text-transform:uppercase;color:color-mix(in oklab,var(--gold) calc(40% + var(--n)*15%),var(--mute))}
.step h2{margin:0 0 6px}.step p{margin:0 0 4px;max-width:60ch}.step .u{color:var(--mute);font-size:14px}.step .mini{max-width:560px}
/* R3 */
.cyc{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.iss{border:1px solid var(--rule);background:var(--card);border-radius:4px;padding:22px;display:grid;gap:16px;align-content:start}
.iss.now{background:var(--navy);color:var(--onnavy);border-color:var(--navy)}.iss.now .se,.iss.now .hm,.iss.now span{color:var(--blush)}
.iss .se{margin:0;font:600 12px var(--ui);letter-spacing:.14em;text-transform:uppercase;color:var(--gold)}.iss h2{margin:4px 0}.iss .hm{margin:0;font-size:14px;color:var(--mute)}
.iss ol{list-style:none;margin:0;padding:0;display:grid;gap:10px}.iss li{display:grid;grid-template-columns:14px 1fr;column-gap:10px;opacity:.6}.iss li::before{content:"";width:10px;height:10px;border-radius:50%;border:1.5px solid currentColor;margin-top:6px;grid-row:1/3}
.iss li b{font:600 15px var(--ui)}.iss li span{font-size:13px;color:var(--mute)}.iss li.done{opacity:.85}.iss li.done::before{background:currentColor}.iss li.on{opacity:1}.iss li.on::before{background:var(--blush);border-color:var(--blush);box-shadow:0 0 0 4px color-mix(in oklab,var(--blush) 35%,transparent)}
.iss .st{margin:0;font:600 14px var(--ui)}.note3 p{margin:0;font-size:13px;color:var(--mute)}.sub3{max-width:560px;margin:0}
/* R4 */
.flt{display:flex;gap:8px;flex-wrap:wrap}.flt button{font:600 13px var(--ui);border:1px solid var(--rule);background:var(--card);color:var(--ink);border-radius:999px;padding:7px 13px;cursor:pointer}.flt button[aria-pressed=true]{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.brd{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}
.br{background:var(--card);border:1px solid var(--rule);border-radius:4px;overflow:hidden;display:grid;grid-template-rows:auto 1fr}
.br figure{margin:0;position:relative}.br img{width:100%;aspect-ratio:16/9;object-fit:cover}.br .sh{position:absolute;left:12px;bottom:12px;font:600 12px var(--ui);background:var(--card);color:var(--ink);padding:3px 9px;border-radius:999px}
.bt{padding:18px 20px 20px;display:grid;gap:8px;align-content:start}.bt h2{font-size:20px;margin:0}.bt p{margin:0;font-size:14px}
.bt ul{list-style:none;margin:4px 0 0;padding:0;display:flex;gap:6px;flex-wrap:wrap}.bt li{font:600 11px var(--ui);letter-spacing:.06em;text-transform:uppercase;color:var(--teal);border:1px solid currentColor;border-radius:3px;padding:2px 7px}
.tk{font:600 14px var(--ui);color:var(--ink);margin-top:6px}
/* R5 */
.tips{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:8px}.tips li{font:500 14px var(--ui);background:var(--card);border:1px solid var(--rule);border-radius:3px;padding:7px 12px}
.fr6{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:14px}.fr6 figure{margin:0;display:grid;gap:8px;align-content:start}
.fr6 img,.fr6 .ph{width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:2px;background:repeating-linear-gradient(45deg,var(--card),var(--card) 6px,var(--rule) 6px,var(--rule) 7px)}
.fr6 figure:nth-child(1) img{object-position:center}.fr6 figure:nth-child(4) img{object-position:50% 20%}
.fr6 figcaption{font-size:13px;line-height:1.4;color:var(--mute)}.fr6 b{display:block;font:700 15px var(--text);color:var(--ink)}
.cap{font-size:13px;color:var(--mute);margin:14px 0 0}
.cmp{margin:0;display:grid;grid-template-columns:150px minmax(0,1fr);gap:0}.cmp dt,.cmp dd{padding:11px 0;border-top:1px solid var(--rule);margin:0}.cmp dt{font:700 15px var(--text)}.cmp dd{font-size:15px}
.spec{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px}.spec li{display:grid;gap:4px;font-size:14px}.spec b{font:700 16px var(--text)}
.pr{margin:-8px 0 18px;font:13px var(--ui);color:var(--gold)}.mb{margin:22px 0 0;font-size:14px;color:var(--mute)}
/* R6 */
.d6{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:56px;align-items:start}
.of{list-style:none;margin:0;padding:0;display:grid;gap:10px}.of li{padding-left:22px;position:relative}.of li::before{content:"";position:absolute;left:0;top:.6em;width:10px;height:2px;background:var(--gold)}
.apply{background:var(--card);border:1px solid var(--rule);border-radius:4px;padding:24px;display:grid;gap:8px}.apply h2{margin:0 0 4px}
.apply fieldset{border:0;margin:0 0 10px;padding:0;display:grid;gap:8px}.apply legend{font:600 13px var(--ui);margin-bottom:8px}
.apply fieldset label{display:grid;grid-template-columns:20px 1fr;gap:10px;align-items:start;border:1px solid var(--rule);border-radius:3px;padding:10px 12px;cursor:pointer}
.apply fieldset span{display:grid;font-size:13px;color:var(--mute)}.apply fieldset b{font:700 15px var(--text);color:var(--ink)}
.apply>label{font:600 13px var(--ui);margin-top:6px}.apply button{justify-self:start;margin-top:10px}
@media (max-width:900px){.ways{grid-template-columns:repeat(2,minmax(0,1fr))}.fr6{grid-template-columns:repeat(3,minmax(0,1fr))}.cyc{grid-template-columns:minmax(0,1fr)}}
@media (max-width:700px){.hero,.two,.d6{grid-template-columns:minmax(0,1fr);gap:32px}.step{grid-template-columns:minmax(0,1fr);gap:8px}.ways{grid-template-columns:minmax(0,1fr)}.fr6{grid-template-columns:repeat(2,minmax(0,1fr))}.cmp{grid-template-columns:minmax(0,1fr)}.cmp dd{border-top:0;padding-top:0}}
"""
JS = """var T=[].slice.call(document.querySelectorAll('[role=tab]'));function go(i){T.forEach(function(x,j){x.setAttribute('aria-selected',j===i);document.getElementById('v'+j).hidden=j!==i});scrollTo(0,0)}
T.forEach(function(t,i){t.onclick=function(){go(i)}});[].forEach.call(document.querySelectorAll('[data-go]'),function(a){a.onclick=function(e){e.preventDefault();go(+a.dataset.go)}});
[].forEach.call(document.querySelectorAll('a[href="#"]:not([data-go])'),function(a){a.addEventListener('click',function(e){e.preventDefault()})});
var F=[].slice.call(document.querySelectorAll('.flt button')),B=[].slice.call(document.querySelectorAll('.br'));F.forEach(function(b){b.onclick=function(){F.forEach(function(x){x.setAttribute('aria-pressed',x===b)});B.forEach(function(c){c.hidden=b.dataset.f&&c.dataset.k!==b.dataset.f})}});"""
