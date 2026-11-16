"""Contributor guides (private demo, not on GitHub): a brief board and a field guide, abstract color placeholders in place of photographs.
The field guide carries every standard in Capturing Content (bicentenary.bahai.org)."""
from rfc_studies import ARR
from figs import FIG  # abstract color placeholders
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
r4 = '<section class="r4"><div class="g"><div class="w"><p class="kk">Open briefs · Education · Winter 2027</p><h1 class="h">What we’re looking for right now</h1><p class="ld">Pick a brief that fits what you have. Each one says what we need, how to capture it, and where it may appear. If none fits, send what you have anyway.</p><p class="cnt">' + f'{len(BR)} open briefs' + '</p>'
r4 += '<div class="flt" role="group" aria-label="Filter briefs"><button aria-pressed="true" data-f="">All</button>' + "".join(f'<button aria-pressed="false" data-f="{x}">{x}</button>' for x in ("Photo","Video","Pitch","Words")) + '</div></div></div><div class="g"><div class="w brd">'
for n,(k,t,fk,sh,d,how,us) in enumerate(BR,1):
    r4 += (f'<article class="br" data-k="{k}"><figure>{fig(fk)}<span class="sh">{sh}</span></figure><div class="bt"><p class="kd"><span class="kn">{k}</span><span class="no">No. {n:02d}</span></p><h2>{t}</h2><p>{d}</p>'
           '<p class="ml">How</p><ul class="how">' + "".join(f"<li>{x}</li>" for x in how) + '</ul><p class="use"><span class="ml">Appears in</span>' + " · ".join(us) + f'</p><a href="#" class="tk">Send a story {ARR}</a></div></article>')
r4 += '</div></div>'
EVERY = [("Consent first", "Everyone recognizable has agreed to be pictured. For children, a parent or guardian, and first names only."),
         ("Credit", "The photographer’s name travels with every file."),
         ("Place and date", "Town or neighborhood, state, and the date, so it can be tagged and found."),
         ("Originals", "Full-size files straight from the camera or phone, not screenshots or copies sent through messaging apps."),
         ("Video", "Horizontal for the library; vertical welcome for social; ten seconds or more per shot, steady."),
         ("Words", "A few lines on what happened, in your own words. Any language.")]
r4 += '<div class="g band"><div class="w"><h2>Every brief, every time</h2><p class="pr">Proposed standards, to be confirmed by the editors.</p><ol class="spec num">' + "".join(f"<li><b>{a}</b>{b}</li>" for a,b in EVERY) + '</ol><a class="fgl" href="#" data-go="1"><span>New to taking pictures at gatherings?</span><b>The field guide covers framing, composition and each kind of moment ' + ARR + '</b></a></div></div></section>'

# ---------------- R5 Field guide (all of Capturing Content, extended for The American Bahá’í)
def card(k, t, d, no=""): return f'<figure class="fc">{fig(k)}<figcaption><span class="fn">Fig. {no}</span><b>{t}</b>{d}</figcaption></figure>'
TIPS = ["Be conscientious of your presence in the space", "Keep a steady hand", "Review your work on a bigger screen", "Capture a series of angles", "Be ready for spontaneous moments"]
r5 = ('<section class="r5"><div class="g"><div class="w gh"><p class="kk">Field guide</p><h1 class="h">Capturing the story where you are</h1>'
      '<p class="ld">A short guide for anyone sending photographs or video to The American Bahá’í. Most of it works with a phone. Color placeholders stand in for photographs.</p>'
      '<h2>Five habits</h2><ol class="tips">' + "".join(f"<li>{t}</li>" for t in TIPS) + '</ol>'
      '<nav class="toc" aria-label="In this guide"><p class="ml">In this guide</p>@@TOC@@</nav></div></div>')
SECS = []
def sec(title, lead, cards, cols=3, band=False, pre=""):
    SECS.append(title); n = len(SECS)
    return (f'<div class="g{" band" if band else ""}" id="fs{n}"><div class="w"><h2><span class="sn">{n:02d}</span>{title}</h2>' + (f'<p class="sl">{lead}</p>' if lead else '') + pre +
            f'<div class="fg c{cols}">' + "".join(card(*c, f"{n}.{i}") for i, c in enumerate(cards, 1)) + '</div></div></div>')
r5 += sec("Framing, from wide to close", "A reminder of the basics. Send a range: one wide, some mid, a few close.", [
    ("wide", "Wide shot", "Gives a sense of the space and provides context."),
    ("mid", "Mid-shot", "Shows many people while staying close enough to see their faces."),
    ("mcu", "Medium close-up", "Makes the viewer feel part of the space."),
    ("cu", "Close-up", "Gives a sense of focus."),
    ("ecu", "Extreme close-up", "Shows emotion in a more dramatic way."),
    ("audview", "Audience perspective", "Shows the event as the audience sees it.")], band=True, pre='<div class="scale" aria-hidden="true"><span>Wide</span><i></i><span>Close</span></div>')
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
r5 += ('<div class="g band"><div class="w"><h2>Before you send</h2><p class="pr">Proposed standards, to be confirmed by the editors.</p><p class="ready" aria-live="polite"><span>0</span> of ' + str(len(SPEC)) + ' ready</p><ul class="spec chk">' + "".join(f'<li><label><input type="checkbox"><b>{a}</b><span>{b}</span></label></li>' for a,b in SPEC) +
       '</ul><p class="mb">For examples of strong pictures of community life, browse the Bahá’í Media Bank at media.bahai.org.</p></div></div></section>')
r5 = r5.replace("@@TOC@@", "<ol>" + "".join(f'<li><a href="#fs{i}" data-to="fs{i}"><span>{i:02d}</span>{t}</a></li>' for i, t in enumerate(SECS, 1)) + "</ol>")
