"""Contributor guides (not part of the RFC gallery): a brief board and a field guide, drawn placeholders in place of photographs.
The field guide carries every standard in Capturing Content (bicentenary.bahai.org)."""
from rfc_studies import ARR
# ---------------- figural placeholders: drawn schematics stand in for photographs, so the guide shows the idea, not a particular gathering
def _p(x, y, s=1, c="var(--fg)", o=1):  # a person: head + shoulders
    return f'<g opacity="{o}"><circle cx="{x}" cy="{y}" r="{7*s}" fill="{c}"/><path d="M{x-12*s} {y+26*s}q0-15 {12*s}-15q{12*s} 0 {12*s} 15z" fill="{c}"/></g>'
def _frame(inner, label=""):
    return (f'<svg class="fig" viewBox="0 0 160 120" role="img" aria-label="{label}"><clipPath id="c{label[:3]}{len(label)}"><rect x="1" y="1" width="158" height="118" rx="3"/></clipPath><rect x="1" y="1" width="158" height="118" rx="3" fill="var(--bgf)"/>'
            f'<g clip-path="url(#c{label[:3]}{len(label)})">{inner}</g><rect x="1" y="1" width="158" height="118" rx="3" fill="none" stroke="var(--edge)"/><g fill="none" stroke="var(--acc)" stroke-width="1.6"><path d="M8 20V8h12M140 8h12v12M152 100v12h-12M20 112H8v-12"/></g></svg>')
FIG = {
 "wide": _frame('<path d="M0 86H160" stroke="var(--edge)"/><rect x="18" y="22" width="22" height="16" fill="var(--soft)"/><rect x="120" y="22" width="22" height="16" fill="var(--soft)"/>' + "".join(_p(24 + i * 18, 64 + (i % 2) * 6, .55) for i in range(7)), "Wide shot"),
 "xwide": _frame('<path d="M0 92H160M30 92L60 40H100L130 92" stroke="var(--edge)" fill="none"/>' + "".join(_p(30 + i * 11, 84, .3) for i in range(10)), "Extreme wide shot"),
 "mid": _frame("".join(_p(28 + i * 34, 52, 1.1) for i in range(4)) + '<rect x="0" y="92" width="160" height="28" fill="var(--soft)"/>', "Mid-shot"),
 "mcu": _frame(_p(56, 40, 1.9) + _p(112, 48, 1.5, "var(--soft)"), "Medium close-up"),
 "cu": _frame('<circle cx="80" cy="54" r="30" fill="var(--fg)"/><path d="M38 120q0-34 42-34t42 34z" fill="var(--fg)"/>', "Close-up"),
 "ecu": _frame('<rect x="0" y="34" width="160" height="52" fill="var(--fg)"/><ellipse cx="54" cy="58" rx="13" ry="7" fill="var(--bgf)"/><ellipse cx="106" cy="58" rx="13" ry="7" fill="var(--bgf)"/><circle cx="54" cy="58" r="4" fill="var(--fg)"/><circle cx="106" cy="58" r="4" fill="var(--fg)"/>', "Extreme close-up"),
 "audview": _frame('<rect x="54" y="18" width="52" height="10" fill="var(--acc)" opacity=".5"/>' + _p(80, 44, .8) + "".join(_p(18 + i * 31, 96, 1.3, "var(--soft)") for i in range(5)), "Audience perspective"),
 "thirds": _frame('<g stroke="var(--acc)" stroke-dasharray="3 3"><path d="M53 0V120M107 0V120M0 40H160M0 80H160"/></g>' + _p(107, 36, 1.4), "Grid of thirds"),
 "vanish": _frame('<g stroke="var(--edge)" fill="none"><path d="M0 0L80 52L160 0M0 120L80 68L160 120M0 30L80 58M160 30L80 58M0 90L80 62M160 90L80 62"/></g>' + _p(80, 52, .4) + _p(40, 70, .9) , "Vanishing point"),
 "depth": _frame(_p(46, 46, 1.8) + _p(112, 44, 1, "var(--soft)", .5) + _p(138, 50, .9, "var(--soft)", .4), "Depth and focus"),
 "shoulder": _frame(_p(110, 46, 1.5) + '<path d="M-10 120q4-60 52-60q30 0 34 60z" fill="var(--soft)" opacity=".9"/><circle cx="34" cy="44" r="22" fill="var(--soft)"/>', "Over the shoulder"),
 "reaction": _frame(_p(46, 46, 1.4) + '<path d="M40 50q6 6 12 0" stroke="var(--bgf)" stroke-width="2" fill="none"/>' + _p(108, 52, 1.2, "var(--soft)"), "Audience reaction"),
 "audwide": _frame("".join(_p(16 + i * 26, 40 + r * 34, .8, "var(--fg)" if (i + r) % 2 else "var(--soft)") for r in range(2) for i in range(6)), "Audience wide shot, faces visible"),
 "stage": _frame('<rect x="20" y="12" width="120" height="16" rx="2" fill="var(--acc)" opacity=".55"/><text x="80" y="24" text-anchor="middle" font-size="9" fill="var(--bgf)" font-family="sans-serif">EVENT TITLE</text>' + _p(80, 56, 1.4) + '<path d="M98 66v-12" stroke="var(--edge)" stroke-width="3"/><circle cx="98" cy="52" r="3.5" fill="var(--edge)"/>', "Stage shot with the title in frame"),
 "light": _frame('<defs><radialGradient id="lg"><stop offset="0" stop-color="var(--acc)" stop-opacity=".55"/><stop offset="1" stop-color="var(--acc)" stop-opacity="0"/></radialGradient></defs><circle cx="80" cy="34" r="60" fill="url(#lg)"/>' + _p(80, 58, 1.3), "Dynamic lighting"),
 "engage": _frame(_p(60, 34, 1.1) + "".join(_p(30 + i * 34, 88, 1, "var(--soft)") for i in range(4)) + '<path d="M70 50q20 14 40 26" stroke="var(--acc)" stroke-dasharray="3 3" fill="none"/>', "Engagement with the audience"),
 "circle": _frame('<ellipse cx="80" cy="74" rx="56" ry="24" fill="none" stroke="var(--edge)"/>' + "".join(_p(80 + 56 * __import__('math').cos(a * 0.785), 66 + 24 * __import__('math').sin(a * 0.785), .7, "var(--fg)" if a % 3 else "var(--soft)") for a in range(8)), "A circle seen from within"),
 "group": _frame("".join(_p(26 + i * 27, 50, .9) for i in range(5)) + "".join(_p(40 + i * 27, 80, .9, "var(--soft)") for i in range(4)), "Group photo, every face visible"),
 "mic": _frame('<circle cx="80" cy="50" r="24" fill="var(--fg)"/><path d="M44 120q0-38 36-38t36 38z" fill="var(--fg)"/><circle cx="71" cy="48" r="3.5" fill="var(--bgf)"/><circle cx="89" cy="48" r="3.5" fill="var(--bgf)"/><path d="M112 100L100 76" stroke="var(--acc)" stroke-width="4"/><ellipse cx="99" cy="72" rx="6" ry="8" fill="var(--acc)" transform="rotate(-25 99 72)"/>', "Microphone below the face, both eyes visible"),
 "phone": _frame('<rect x="56" y="10" width="48" height="100" rx="8" fill="none" stroke="var(--fg)" stroke-width="2"/><circle cx="80" cy="22" r="4" fill="var(--acc)"/><path d="M86 18l8-6" stroke="var(--acc)" stroke-width="2"/><rect x="62" y="34" width="36" height="56" fill="var(--soft)"/>' + _p(80, 52, .7), "A phone: wipe the lens, set the focus"),
 "quiet": _frame(_p(52, 50, 1.2) + _p(108, 50, 1.2, "var(--soft)") + '<circle cx="146" cy="16" r="8" fill="none" stroke="var(--edge)"/><path d="M142 16h8" stroke="var(--edge)"/>', "Conversation, not interrupted"),
 "action": _frame(_p(76, 46, 1.4) + '<g stroke="var(--acc)" stroke-width="2"><path d="M30 40h18M24 54h22M30 68h16"/></g>', "Action at a fast shutter speed"),
 "focus1": _frame(_p(80, 46, 1.5) + _p(30, 52, 1, "var(--soft)", .35) + _p(132, 52, 1, "var(--soft)", .35), "One face in focus"),
 "joy": _frame(_p(80, 46, 1.6) + '<path d="M72 48q8 8 16 0" stroke="var(--bgf)" stroke-width="2.5" fill="none"/><g stroke="var(--acc)" stroke-width="2"><path d="M40 24l6 6M120 24l-6 6M80 10v8"/></g>', "Joy"),
 "devotion": _frame('<circle cx="80" cy="30" r="40" fill="var(--acc)" opacity=".18"/>' + _p(80, 54, 1.3) + '<path d="M70 92q10-8 20 0" stroke="var(--bgf)" stroke-width="2" fill="none"/>', "Devotion, captured with care"),
 "posed": _frame("".join(_p(28 + i * 26, 54, 1) for i in range(5)) + '<path d="M10 92H150" stroke="var(--edge)"/>', "Posed"),
 "candid": _frame(_p(36, 60, 1.1) + _p(66, 50, .9, "var(--soft)") + _p(112, 64, 1.2) + _p(140, 46, .7, "var(--soft)"), "Candid"),
 "hands": _frame('<rect x="20" y="62" width="120" height="40" rx="3" fill="var(--soft)"/><g fill="var(--fg)"><ellipse cx="62" cy="62" rx="16" ry="9"/><ellipse cx="102" cy="64" rx="15" ry="8"/></g><path d="M108 60l22-24" stroke="var(--acc)" stroke-width="3"/>', "Hands at work"),
 "sign": _frame('<rect x="34" y="28" width="92" height="40" rx="3" fill="var(--acc)" opacity=".5"/><text x="80" y="52" text-anchor="middle" font-size="10" fill="var(--bgf)" font-family="sans-serif">PLACE NAME</text><path d="M50 68v34M110 68v34" stroke="var(--edge)" stroke-width="3"/>', "The sign at the door"),
 "home": _frame('<path d="M30 60L80 26L130 60V104H30Z" fill="none" stroke="var(--fg)" stroke-width="2"/><rect x="70" y="74" width="20" height="30" fill="var(--acc)" opacity=".6"/>' + _p(52, 78, .6, "var(--soft)") + _p(108, 78, .6, "var(--soft)"), "A home that hosts a class"),
 "words": _frame('<g fill="var(--soft)"><rect x="24" y="24" width="112" height="8" rx="2"/><rect x="24" y="40" width="96" height="8" rx="2"/><rect x="24" y="56" width="104" height="8" rx="2"/></g><path d="M24 84q20-12 40 0t40 0" stroke="var(--acc)" stroke-width="2" fill="none"/>', "A few lines in a parent’s or teacher’s words"),
 "video": _frame('<rect x="20" y="20" width="120" height="70" rx="4" fill="var(--soft)"/><path d="M70 40v30l26-15z" fill="var(--bgf)"/><rect x="20" y="98" width="120" height="4" fill="var(--edge)"/><rect x="20" y="98" width="44" height="4" fill="var(--acc)"/>', "A short horizontal video"),
 "service": _frame(_p(48, 50, 1.1) + _p(100, 50, 1.1, "var(--soft)") + '<rect x="58" y="78" width="44" height="26" fill="var(--acc)" opacity=".5"/>', "Young people serving together"),
}
from figs import FIG  # redrawn set: light, floor and depth of field
def fig(k): return FIG[k]

# ---------------- R4 Brief board
BR = [("Photo", "A children’s class in session", "wide", "Wide shot",
       "Show the room, the teacher and the children together, so a reader understands the whole scene at a glance.",
       ["Stand at the edge of the room, at the children’s eye level", "Keep faces visible; avoid backs of heads", "Take a few frames a minute apart"],
       ["Photo library", "Feature"]),
      ("Photo", "Hands at work", "hands", "Detail",
       "Painting, writing, building, serving. Hands tell the story without faces, which helps when children are present.",
       ["Fill the frame with the activity", "Light from a window beats the flash", "Several angles of the same moment"],
       ["Microstory", "Social"]),
      ("Video", "Sixty seconds of a study circle", "video", "Over the shoulder",
       "The rhythm of a conversation: who speaks, who listens, the book open on the table.",
       ["Horizontal, phone held steady with both hands", "Shoot over a shoulder so the exchange is the subject", "Ask everyone first; record quietly, in silent mode"],
       ["Social", "Photo library"]),
      ("Photo", "Young people serving together", "service", "Action",
       "A junior youth group or youth carrying out a service project in their neighborhood.",
       ["Raise the shutter speed so movement stays sharp", "Focus on one face; let the rest soften", "One wide frame for context, then come closer"],
       ["Feature", "Social"]),
      ("Photo", "The sign at the door", "sign", "Context",
       "The name of the place or the event in the frame, so no one has to guess what it was.",
       ["Square on, readable from a phone screen", "Include a little of the setting around it"],
       ["Photo library"]),
      ("Pitch", "A home that hosts a class", "home", "Story lead",
       "Who opened their door, how it began, and what the neighbors noticed. A few lines is enough to start.",
       ["Who, where, since when", "One thing that changed", "Whether the family would talk with an editor"],
       ["Feature"]),
      ("Words", "What a child learned this week", "words", "Microstory",
       "A parent, tutor or teacher, in their own words. Two or three sentences.",
       ["The child’s first name only, and only with permission", "What they learned, in their words if you can", "Where and when"],
       ["Microstory", "Social"]),
      ("Photo", "A moment of devotion", "devotion", "With care",
       "Prayers before a class or at a gathering, captured quietly and respectfully.",
       ["Ask first; take few frames", "No flash; use the light in the room", "Hands, a lit room, a bowed head can say enough"],
       ["Photo library", "Feature"])]
r4 = '<section class="r4"><div class="g"><div class="w"><p class="kk">Open briefs · Education · Winter 2027</p><h1 class="h">What we’re looking for right now</h1><p class="ld">Pick a brief that fits what you have. Each one says what we need, how to capture it, and where it may appear. If none fits, send what you have anyway.</p>'
r4 += '<div class="flt" role="group" aria-label="Filter briefs"><button aria-pressed="true" data-f="">All</button>' + "".join(f'<button aria-pressed="false" data-f="{x}">{x}</button>' for x in ("Photo","Video","Pitch","Words")) + '</div></div></div><div class="g"><div class="w brd">'
for k,t,fk,sh,d,how,us in BR:
    r4 += (f'<article class="br" data-k="{k}"><figure>{fig(fk)}<span class="sh">{sh}</span></figure><div class="bt"><p class="kd">{k}</p><h2>{t}</h2><p>{d}</p>'
           '<ul class="how">' + "".join(f"<li>{x}</li>" for x in how) + '</ul><ul class="use">' + "".join(f"<li>{u}</li>" for u in us) + f'</ul><a href="#" class="tk">Send a story {ARR}</a></div></article>')
r4 += '</div></div>'
EVERY = [("Consent first", "Everyone recognizable has agreed to be pictured. For children, a parent or guardian, and first names only."),
         ("Credit", "The photographer’s name travels with every file."),
         ("Place and date", "Town or neighborhood, state, and the date, so it can be tagged and found."),
         ("Originals", "Full-size files straight from the camera or phone, not screenshots or copies sent through messaging apps."),
         ("Video", "Horizontal for the library; vertical welcome for social; ten seconds or more per shot, steady."),
         ("Words", "A few lines on what happened, in your own words. Any language.")]
r4 += '<div class="g band"><div class="w"><h2>Every brief, every time</h2><p class="pr">Proposed standards, to be confirmed by the editors.</p><ul class="spec">' + "".join(f"<li><b>{a}</b>{b}</li>" for a,b in EVERY) + '</ul><p class="mb">New to taking pictures at gatherings? The <a href="#" data-go="1">field guide</a> covers framing, composition and each kind of moment.</p></div></div></section>'

# ---------------- R5 Field guide (all of Capturing Content, extended for The American Bahá’í)
def card(k, t, d): return f'<figure class="fc">{fig(k)}<figcaption><b>{t}</b>{d}</figcaption></figure>'
TIPS = ["Be conscientious of your presence in the space", "Keep a steady hand", "Review your work on a bigger screen", "Capture a series of angles", "Be ready for spontaneous moments"]
r5 = ('<section class="r5"><div class="g"><div class="w gh"><p class="kk">Field guide</p><h1 class="h">Capturing the story where you are</h1>'
      '<p class="ld">A short guide for anyone sending photographs or video to The American Bahá’í. Most of it works with a phone. The drawings stand in for photographs, to show the idea.</p>'
      '<h2>Five habits</h2><ol class="tips">' + "".join(f"<li>{t}</li>" for t in TIPS) + '</ol></div></div>')
def sec(title, lead, cards, cols=3, band=False):
    return (f'<div class="g{" band" if band else ""}"><div class="w"><h2>{title}</h2>' + (f'<p class="sl">{lead}</p>' if lead else '') +
            f'<div class="fg c{cols}">' + "".join(card(*c) for c in cards) + '</div></div></div>')
r5 += sec("Framing, from wide to close", "A reminder of the basics. Send a range: one wide, some mid, a few close.", [
    ("wide", "Wide shot", "Gives a sense of the space and provides context."),
    ("mid", "Mid-shot", "Shows many people while staying close enough to see their faces."),
    ("mcu", "Medium close-up", "Makes the viewer feel part of the space."),
    ("cu", "Close-up", "Gives a sense of focus."),
    ("ecu", "Extreme close-up", "Shows emotion in a more dramatic way."),
    ("audview", "Audience perspective", "Shows the event as the audience sees it.")], band=True)
r5 += sec("Composition", "", [
    ("thirds", "Grid of thirds", "Balance the picture on a grid of thirds; place the subject on a line or where two meet."),
    ("vanish", "Vanishing point", "Lines running into the distance add a sense of depth."),
    ("depth", "Depth and focus", "A sharp subject against a softer background gives depth and focus."),
    ("shoulder", "Over the shoulder", "Captures warm interactions between people.")], cols=4)
r5 += sec("Audience", "Faces are what a reader looks for.", [
    ("audwide", "Audience wide shot", "Many people, with faces clearly visible."),
    ("xwide", "Extreme wide shot", "The context of the space, a diverse range of people, the atmosphere."),
    ("reaction", "Reaction shot", "One person listening, laughing, moved."),
    ("audview", "Toward the stage", "The stage as the audience sees it.")], cols=4, band=True)
r5 += sec("Stage", "", [
    ("stage", "Title in the frame", "Capturing the event’s title leaves no doubt about what it was."),
    ("mic", "Faces clear of the microphone", "Make sure the microphone doesn’t hide the speaker’s face; both eyes visible."),
    ("light", "Dynamic lighting", "Notice the range of light and shadow, and use it."),
    ("engage", "Close to the audience", "Engagement between speaker and audience adds a sense of community.")], cols=4)
r5 += sec("Community", "Neighborhood gatherings can be spontaneous, intimate and delicate.", [
    ("circle", "From within the circle", "An angle that lets the viewer feel part of the circle; many layers of engagement, with diversity of age, gender and activity."),
    ("phone", "A phone is fine", "Wipe your lens and set your focus before you begin."),
    ("group", "Group photos", "A chance to see everyone’s face. No group is too small."),
    ("quiet", "Without interrupting", "Conversation between friends, captured without entering the space. Use silent mode, or a zoom lens.")], cols=4, band=True)
r5 += sec("Action", "Whatever is happening in the space, people are naturally drawn to faces.", [
    ("focus1", "One face in focus", "Focusing on one person and blurring the rest brings a sense of focus to the subject."),
    ("action", "Shutter speed", "Make the shutter fast enough for the movement; match it to the light and the speed of the action. Faster means less blur."),
    ("joy", "Joy", "Capturing joy, in whatever form, sometimes says more than words.")])
r5 += sec("Devotion", "Devotion takes different forms and asks for creative, careful approaches.", [
    ("devotion", "Ask first", "Let those present know you are there, and take only a few frames."),
    ("light", "Use the light in the room", "No flash. Candlelight, a window, a lamp carry the mood."),
    ("hands", "Show it another way", "Hands, an open prayer book, a lit room: a detail can say enough.")], cols=3, band=True)
r5 += sec("Candid and posed", "Both are welcome; send some of each.", [
    ("posed", "Posed", "Everyone facing the camera, faces clear: good for groups and credits."),
    ("candid", "Candid", "People as they are, unaware of the camera: good for telling the story.")], cols=2)
SPEC = [("Send originals", "Full-size files straight from the camera or phone, not screenshots or messaging copies."),
        ("Name the photographer", "Every picture carries a credit."),
        ("Ask first", "Everyone recognizable has agreed to be pictured. For children, a parent or guardian, and first names only."),
        ("Say where and when", "Town or neighborhood, state, and the date."),
        ("Video", "Steady and horizontal for the library; vertical welcome for social. Ten seconds per shot or longer."),
        ("A few lines", "What happened and why it mattered, in your own words and in any language.")]
r5 += ('<div class="g band"><div class="w"><h2>Before you send</h2><p class="pr">Proposed standards, to be confirmed by the editors.</p><ul class="spec">' + "".join(f"<li><b>{a}</b>{b}</li>" for a,b in SPEC) +
       '</ul><p class="mb">For examples of strong pictures of community life, browse the Bahá’í Media Bank at media.bahai.org.</p></div></div></section>')

