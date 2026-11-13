"""Figural placeholders for TAB guides and demos: duotone scenes with light, a floor and depth of field (far figures soft), in the magazine's tokens."""
U = ""
def P(x, y, s=1, d=0, c="var(--fg)", arms=False, bow=0):
    """A person: head and shoulders. d = depth (0 sharp, 1 soft, 2 far)."""
    op = [1, .58, .34][d]; f = f' filter="url(#b{U}{d})"' if d else ""
    hx = x + bow * s
    a = (f'<path d="M{x-12*s} {y+14*s}L{x-20*s} {y-4*s}M{x+12*s} {y+14*s}L{x+20*s} {y-4*s}" stroke="{c}" stroke-width="{4*s}" stroke-linecap="round" fill="none"/>' if arms else "")
    return (f'<g opacity="{op}"{f}>{a}<ellipse cx="{hx}" cy="{y}" rx="{6.2*s}" ry="{7.2*s}" fill="{c}"/>'
            f'<path d="M{x-16*s} {y+32*s}C{x-16*s} {y+17*s} {x-9*s} {y+11.5*s} {x} {y+11.5*s}C{x+9*s} {y+11.5*s} {x+16*s} {y+17*s} {x+16*s} {y+32*s}Z" fill="{c}"/></g>')
def _frame(key, inner, label, floor=88, light=(.5, .15), glow=.18):
    u = key + "@@"
    defs = (f'<defs><linearGradient id="g{u}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" style="stop-color:var(--bgf)"/><stop offset="1" style="stop-color:var(--soft);stop-opacity:.55"/></linearGradient>'
            f'<radialGradient id="l{u}" cx="{light[0]}" cy="{light[1]}" r=".75"><stop offset="0" style="stop-color:var(--acc);stop-opacity:{glow}"/><stop offset="1" style="stop-color:var(--acc);stop-opacity:0"/></radialGradient>'
            f'<filter id="b{u}1" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="1.2"/></filter><filter id="b{u}2" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="2.6"/></filter>'
            f'<clipPath id="c{u}"><rect width="160" height="120" rx="4"/></clipPath></defs>')
    fl = f'<path d="M0 {floor}H160V120H0Z" style="fill:var(--soft)" opacity=".28"/><path d="M0 {floor}H160" style="stroke:var(--edge)" stroke-width=".8"/>' if floor else ""
    t = 1.1
    corners = (f'<g fill="none" style="stroke:var(--acc)" stroke-width="{t}" opacity=".9"><path d="M8 17V8h9M143 8h9v9M152 103v9h-9M17 112H8v-9"/></g>')
    return (f'<svg class="fig" viewBox="0 0 160 120" role="img" aria-label="{label}">{defs}<g clip-path="url(#c{u})"><rect width="160" height="120" fill="url(#g{u})"/>'
            f'<rect width="160" height="120" fill="url(#l{u})"/>{fl}{inner}</g><rect x=".5" y=".5" width="159" height="119" rx="4" fill="none" style="stroke:var(--edge)"/>{corners}</svg>')
import itertools
_n = itertools.count(1)
class _Fig(dict):
    """Each read returns the drawing with ids made unique, so one figure can appear many times on a page."""
    def __getitem__(self, k): return dict.__getitem__(self, k).replace("@@", "-" + str(next(_n)))
FIG = _Fig()
def scene(key, label, build, **kw):
    global U
    U = key + "@@"
    dict.__setitem__(FIG, key, _frame(key, build(), label, **kw))
FG, SOFT, ACC, CARD = "var(--fg)", "var(--soft)", "var(--acc)", "var(--card)"
def win(x, y, w, h): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="1.5" style="fill:var(--card)" opacity=".7"/><path d="M{x+w/2} {y}V{y+h}" style="stroke:var(--edge)" stroke-width=".8"/>'
scene("wide", "Wide shot", lambda: win(18, 16, 26, 22) + win(116, 16, 26, 22) + "".join(P(26 + i * 15, 60 + (i % 2) * 4, .5, 1 if i % 2 else 0) for i in range(6)) + P(132, 46, .78), floor=80)
scene("xwide", "Extreme wide shot", lambda: '<path d="M0 88L52 34H108L160 88" fill="none" style="stroke:var(--edge)" stroke-width=".8"/>' + win(62, 40, 36, 18) + "".join(P(22 + i * 13, 78 + (i % 3), .3, 2 if i in (0, 9) else 1) for i in range(10)), floor=88)
scene("mid", "Mid-shot", lambda: "".join(P(28 + i * 35, 48, 1.05, 0 if i in (1, 2) else 1) for i in range(4)), floor=96)
scene("mcu", "Medium close-up", lambda: P(122, 46, 1.5, 2) + P(60, 40, 1.95), floor=None)
scene("cu", "Close-up", lambda: f'<ellipse cx="80" cy="52" rx="25" ry="29" fill="{FG}"/><path d="M34 120C34 92 54 82 80 82S126 92 126 120Z" fill="{FG}"/>', floor=None, light=(.3, .3))
scene("ecu", "Extreme close-up", lambda: f'<rect y="22" width="160" height="78" fill="{FG}"/><path d="M30 46q22-8 44 0M86 46q22-8 44 0" stroke="var(--bgf)" stroke-width="2" fill="none" opacity=".5"/>'
      + "".join(f'<ellipse cx="{cx}" cy="62" rx="15" ry="8" fill="var(--bgf)"/><circle cx="{cx}" cy="62" r="6" fill="{FG}"/><circle cx="{cx+2}" cy="60" r="1.6" fill="var(--bgf)"/>' for cx in (52, 108)), floor=None)
scene("audview", "Audience perspective", lambda: f'<rect x="20" y="12" width="120" height="50" rx="2" fill="{SOFT}" opacity=".45"/>' + P(80, 28, .75) + "".join(P(14 + i * 33, 98, 1.45, 2) for i in range(5)), floor=62, light=(.5, .2), glow=.3)
scene("thirds", "Grid of thirds", lambda: '<g style="stroke:var(--acc)" stroke-dasharray="2 3" stroke-width=".8" opacity=".8"><path d="M53.3 0V120M106.7 0V120M0 40H160M0 80H160"/></g>' + f'<circle cx="106.7" cy="40" r="3" fill="none" style="stroke:var(--acc)"/>' + P(106.7, 38, 1.4), floor=92)
scene("vanish", "Vanishing point", lambda: '<g fill="none" style="stroke:var(--edge)" stroke-width=".8"><path d="M0 0L80 52L160 0M0 120L80 64L160 120M0 26L80 55M160 26L80 55M0 94L80 61M160 94L80 61"/></g>' + P(80, 50, .35, 1) + P(38, 66, .95), floor=None)
scene("depth", "Depth and focus", lambda: P(138, 48, .95, 2) + P(112, 44, 1.05, 2) + P(48, 42, 1.8), floor=94)
scene("shoulder", "Over the shoulder", lambda: P(108, 42, 1.4) + f'<g filter="url(#bshoulder@@2)" opacity=".75"><ellipse cx="32" cy="46" rx="22" ry="25" fill="{SOFT}"/><path d="M-14 120C-10 74 10 66 34 66S76 80 80 120Z" fill="{SOFT}"/></g>', floor=None)
scene("reaction", "Audience reaction", lambda: P(114, 50, 1.2, 2) + P(52, 42, 1.5) + '<path d="M46 47q6 5 12 0" style="stroke:var(--bgf)" stroke-width="1.6" fill="none"/>', floor=None)
scene("audwide", "Audience wide shot, faces visible", lambda: "".join(P(18 + i * 25, 36, .72, 1) for i in range(6)) + "".join(P(30 + i * 25, 66, .85) for i in range(5)), floor=None)
scene("stage", "Stage shot with the title in frame", lambda: f'<rect x="22" y="12" width="116" height="18" rx="2" fill="{ACC}" opacity=".75"/><text x="80" y="24.5" text-anchor="middle" font-size="8" letter-spacing="1.5" style="fill:var(--card)" font-family="sans-serif">EVENT TITLE</text>' + P(80, 54, 1.3) + f'<path d="M104 92V62" style="stroke:var(--fg)" stroke-width="1.6"/><path d="M104 62l-8 -4" style="stroke:var(--fg)" stroke-width="1.6"/><ellipse cx="95" cy="57" rx="2.6" ry="3.4" fill="{FG}"/>', floor=92, glow=.28)
scene("light", "Dynamic lighting", lambda: '<path d="M62 0H98L132 92H28Z" style="fill:var(--acc)" opacity=".16"/>' + P(80, 54, 1.3), floor=92, light=(.5, .05), glow=.45)
scene("engage", "Engagement with the audience", lambda: P(56, 30, 1.05) + '<path d="M70 48q22 10 36 26" fill="none" style="stroke:var(--acc)" stroke-dasharray="2 3"/>' + "".join(P(28 + i * 34, 94, 1.15, 2 if i in (0, 3) else 1) for i in range(4)), floor=70)
import math
scene("circle", "A circle seen from within", lambda: '<ellipse cx="80" cy="76" rx="60" ry="22" fill="none" style="stroke:var(--edge)"/>' + "".join(P(80 + 58 * math.cos(a), 64 + 20 * math.sin(a), .55 + .35 * (1 + math.sin(a)) / 2, 0 if math.sin(a) > .2 else 1) for a in sorted([i * math.pi / 4 + .3 for i in range(8)], key=lambda t: math.sin(t))), floor=None)
scene("group", "Group photo, every face visible", lambda: "".join(P(28 + i * 26, 44, .85) for i in range(5)) + "".join(P(41 + i * 26, 72, .9) for i in range(4)), floor=100)
scene("phone", "A phone: wipe the lens, set the focus", lambda: f'<rect x="54" y="8" width="52" height="104" rx="9" fill="{FG}"/><rect x="58" y="18" width="44" height="84" rx="3" fill="var(--bgf)"/><g transform="translate(0 0)">{P(80, 50, .75)}</g><path d="M66 60h28" style="stroke:var(--acc)" stroke-width=".8" stroke-dasharray="2 2"/><circle cx="80" cy="13" r="1.6" fill="var(--bgf)"/><circle cx="80" cy="50" r="15" fill="none" style="stroke:var(--acc)" stroke-width="1"/>', floor=None)
scene("quiet", "Conversation, not interrupted", lambda: P(108, 46, 1.15, 1) + P(54, 46, 1.25) + '<g transform="translate(140 18)" fill="none" style="stroke:var(--mute,var(--edge))" stroke-width="1"><path d="M-5 3h10M-4 3v-4a4 4 0 0 1 8 0v4M-7 -7L7 7"/></g>', floor=None)
scene("action", "Action at a fast shutter speed", lambda: P(118, 46, 1.1, 2) + P(30, 50, 1, 2) + P(76, 42, 1.4, arms=True) + '<g style="stroke:var(--acc)" stroke-width="1.4" stroke-linecap="round"><path d="M44 34h12M40 46h14M46 58h10"/></g>', floor=96)
scene("focus1", "One face in focus", lambda: P(30, 50, 1.1, 2) + P(130, 50, 1.1, 2) + P(80, 44, 1.5), floor=None)
scene("joy", "Joy", lambda: P(80, 46, 1.5, arms=True) + '<path d="M74 51q6 5 12 0" style="stroke:var(--bgf)" stroke-width="1.6" fill="none"/>', floor=None, glow=.3)
scene("devotion", "Devotion, captured with care", lambda: P(80, 52, 1.3, bow=2.5) + f'<rect x="114" y="82" width="5" height="12" rx="1" fill="{CARD}"/><ellipse cx="116.5" cy="78" rx="2" ry="3.5" fill="{ACC}"/><circle cx="116.5" cy="79" r="12" fill="{ACC}" opacity=".12"/>', floor=94, light=(.72, .66), glow=.4)
scene("posed", "Posed", lambda: "".join(P(28 + i * 26, 52, 1) for i in range(5)), floor=96)
scene("candid", "Candid", lambda: P(140, 44, .7, 2) + P(66, 48, .9, 1) + P(36, 58, 1.15) + P(110, 62, 1.25), floor=104)
scene("hands", "Hands at work", lambda: f'<rect x="20" y="58" width="120" height="50" rx="2" fill="{CARD}"/><g fill="{ACC}" opacity=".55"><circle cx="48" cy="80" r="7"/><circle cx="72" cy="90" r="5"/><circle cx="98" cy="76" r="6"/></g><ellipse cx="58" cy="62" rx="15" ry="8" fill="{FG}"/><ellipse cx="104" cy="66" rx="14" ry="7.5" fill="{FG}"/><path d="M110 62L132 36" style="stroke:var(--acc)" stroke-width="2.4" stroke-linecap="round"/>', floor=50)
scene("sign", "The sign at the door", lambda: f'<rect x="10" y="10" width="140" height="60" fill="{SOFT}" opacity=".3"/><rect x="36" y="26" width="88" height="34" rx="2" fill="{ACC}" opacity=".85"/><text x="80" y="47" text-anchor="middle" font-size="9" letter-spacing="1.4" style="fill:var(--card)" font-family="sans-serif">PLACE NAME</text><path d="M52 60V100M108 60V100" style="stroke:var(--fg)" stroke-width="2"/>', floor=100)
scene("home", "A home that hosts a class", lambda: f'<path d="M32 58L80 26L128 58V100H32Z" fill="{CARD}" style="stroke:var(--fg)" stroke-width="1.5"/><rect x="70" y="70" width="20" height="30" fill="{ACC}" opacity=".7"/><rect x="42" y="66" width="16" height="12" fill="{ACC}" opacity=".35"/><rect x="102" y="66" width="16" height="12" fill="{ACC}" opacity=".35"/>' + P(52, 86, .45, 1) + P(110, 86, .45, 1), floor=100)
scene("words", "A few lines in a parent’s or teacher’s words", lambda: f'<rect x="26" y="14" width="108" height="92" rx="2" fill="{CARD}"/><g fill="{SOFT}">' + "".join(f'<rect x="38" y="{30 + i * 11}" width="{84 - (i % 3) * 14}" height="3" rx="1.5"/>' for i in range(5)) + f'</g><path d="M38 92q10-8 20 0t20 0t20 0" fill="none" style="stroke:var(--acc)" stroke-width="1.4"/>', floor=None)
scene("video", "A short horizontal video", lambda: f'<rect x="18" y="18" width="124" height="72" rx="3" fill="{FG}" opacity=".85"/>' + P(80, 44, .9, 1, c="var(--bgf)") + f'<circle cx="80" cy="54" r="13" fill="{FG}" opacity=".55"/><path d="M76 47v14l11-7z" style="fill:var(--bgf)"/><rect x="18" y="98" width="124" height="3" rx="1.5" fill="{SOFT}"/><rect x="18" y="98" width="46" height="3" rx="1.5" fill="{ACC}"/>', floor=None)
scene("service", "Young people serving together", lambda: P(104, 46, 1.1, 1, arms=True) + P(52, 46, 1.15) + f'<rect x="60" y="76" width="44" height="24" rx="2" fill="{ACC}" opacity=".6"/><path d="M60 84h44" style="stroke:var(--card)" stroke-width=".8"/>', floor=96)
scene("mic", "Microphone below the face, both eyes visible", lambda: f'<ellipse cx="80" cy="50" rx="24" ry="28" fill="{FG}"/><path d="M38 120C38 92 56 82 80 82S122 92 122 120Z" fill="{FG}"/><ellipse cx="71" cy="47" rx="3.5" ry="2.4" fill="var(--bgf)"/><ellipse cx="89" cy="47" rx="3.5" ry="2.4" fill="var(--bgf)"/><path d="M116 104L101 80" style="stroke:var(--acc)" stroke-width="4" stroke-linecap="round"/><ellipse cx="99" cy="75" rx="6" ry="8" fill="{ACC}" transform="rotate(-30 99 75)"/>', floor=None)
