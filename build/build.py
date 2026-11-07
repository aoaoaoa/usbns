"""Builds The American Bahá'í arts-issue site from data.py.

Outputs:
  out/tab.html, out/plates.html, out/reader.html   artifact pages (no html/head/body skeleton)
  site/                                            GitHub Pages tree: index.html (TAB), alt/plates, alt/reader, img/
Images are read from out/img/.
"""
import html, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import ISSUE, VOICES, ARTICLES
SUB = "A U.S. Bah\u00e1\u2019\u00ed News publication"

def esc(s): return html.escape(s, quote=False) if s else ""
def qesc(s):
    return re.sub("\u201c([^\u201d]+)\u201d", lambda m: '<i class="qt">\u201c' + m.group(1) + '\u201d</i>', esc(s))
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
SIDES = '<meta name="claude:viewport-fit-sides" content="cover">'
GUT = "padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));"

def body_html(blocks):
    out = []
    for b in blocks:
        k = b[0]
        if k == "p": out.append(f"<p>{qesc(b[1])}</p>")
        elif k == "h": out.append(f"<h3>{esc(b[1])}</h3>")
        elif k == "q": out.append(f'<blockquote class="pull"><p>{esc(b[1])}</p><cite>{esc(b[2])}</cite></blockquote>')
        elif k == "note": out.append(f'<p class="note">{esc(b[1])}</p>')
        elif k == "qa": out.append(f'<p class="qa">{esc(b[1])}</p>')
        elif k == "a": out.append(f'<p class="ans"><b>{esc(b[1])}</b> {qesc(b[2])}</p>')
        elif k == "pair":
            w = next((x for x in b[1:] if isinstance(x, int)), None)
            st = f' style="max-width:{w}px"' if w else ""
            out.append(f'<figure class="photo pair{" capped" if w else ""}"{st}>' + "".join(f'<div><img src="img/{f}" alt="{esc(c)}" loading="lazy"><figcaption>{esc(c)}</figcaption></div>' for f,c in (x for x in b[1:] if isinstance(x, tuple))) + '</figure>')
        elif k == "ext": out.append(f'<blockquote class="ext"><p>{qesc(b[1])}</p></blockquote>')
        elif k == "ext2": out.append(f'<blockquote class="ext ext2"><p>{qesc(b[1])}</p></blockquote>')
        elif k == "list": out.append('<ul class="qs">' + "".join(f"<li>{qesc(x)}</li>" for x in b[1]) + "</ul>")
        elif k == "kv": out.append('<dl class="kv">' + "".join(f"<dt>{esc(x)}</dt><dd>{esc(y)}</dd>" for x,y in b[1]) + "</dl>")
        elif k == "chart": out.append(chart_html(b[1]))
        elif k == "concept": out.append(concept_html(b[1]))
        elif k == "figures": out.append('<div class="figs">' + "".join(f'<div{" class=has" if len(f) > 2 else ""}{pop(f[0] + " " + f[1], f[2] if len(f) > 2 else "")}><b>{esc(f[0])}</b><span>{esc(f[1])}</span></div>' for f in b[1]) + "</div>")
        elif k == "portraits":
            out.append('<div class="portraits">' + "".join(f'<figure class="{cl}"><img src="img/{f}" alt="{esc(cap)}" loading="lazy"><figcaption>{esc(cap)}</figcaption></figure>' for f, cap, cl in b[1]) + '</div>')
        elif k == "band":
            # full-bleed room: a toned wall or stage on which several photographs hang together
            c = b[1]; items = "".join(f'<figure class="bi {cl}"><img src="img/{f}" alt="{esc(cap)}" loading="lazy"><figcaption>{esc(cap)}</figcaption></figure>' for f, cap, cl in c["items"])
            lab = f'<p class="blab">{esc(c["label"])}</p>' if c.get("label") else ""
            out.append(f'<section class="band {c["tone"]}"><div class="bin">{lab}{items}</div></section>')
        elif k == "img":
            w = b[3] if len(b) > 3 else None
            cls = "photo small" if w else "photo"
            st = f' style="--w:{w}px"' if w else ""
            out.append(f'<figure class="{cls}"{st}><img src="img/{b[1]}" alt="{esc(b[2])}" loading="lazy"><figcaption>{esc(b[2])}</figcaption></figure>')
    return "\n".join(out)

import json as _json
USMAP = _json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "usmap.json")))

def pop(title, body):
    """Attributes that make an element open the shared popup."""
    if not body: return ""
    return f' tabindex="0" role="button" data-pt="{html.escape(title, quote=True)}" data-pb="{html.escape(body, quote=True)}"'

def size_cls(c):
    w = c.get("w"); return "" if not w else (" sized span" if w > 640 else " sized")
def size_sty(c):
    return f' style="--cw:{c["w"]}px"' if c.get("w") else ""

def chart_html(c):
    """Small inline SVG charts drawn to scale from the record's numbers."""
    def money(v): return f"${v:,.0f}"
    fmt = money if c.get("fmt") == "money" else (lambda v: f"{v:,}")
    title = f'<p class="ct">{esc(c["title"])}</p>'; note = f'<p class="cn">{esc(c["note"])}</p>' if c.get("note") else ""
    if c["kind"] == "bars":
        data = c["data"]; mx = max(it[1] for it in data); n = len(data); rowh = 34; W = 600; labw = 150; barw = W - labw - 110
        rows = []
        for i, it in enumerate(data):
            lab, v = it[0], it[1]; story = it[2] if len(it) > 2 else ""
            y = i * rowh; w = max(2, round(barw * v / mx))
            rows.append(f'<g class="hit"{pop(f"{lab}: {fmt(v)}", story)}><rect x="0" y="{y}" width="{W}" height="{rowh}" class="ghost"/><text x="{labw-10}" y="{y+22}" text-anchor="end" class="cl">{esc(lab)}</text><rect x="{labw}" y="{y+6}" width="{w}" height="22" class="cb"/><text x="{labw+w+8}" y="{y+22}" class="cv">{fmt(v)}</text></g>')
        svg = f'<svg viewBox="0 0 {W} {n*rowh}" width="100%" role="img" aria-label="{esc(c["title"])}">{"".join(rows)}</svg>'
    elif c["kind"] == "progress":
        data = c["data"]; mx = c["max"]; W = 600; H = 92
        parts = [f'<rect x="0" y="40" width="{W}" height="14" class="ctrack"/>']
        for i, it in enumerate(data):
            lab, v = it[0], it[1]; story = it[2] if len(it) > 2 else ""
            x = round(W * v / mx)
            parts.append(f'<rect x="0" y="40" width="{x}" height="14" class="cb" style="opacity:{.35 + .3*i}"/><circle cx="{x}" cy="47" r="11" class="ghost hit"{pop(f"{lab}: {v}", story)}/>')
            parts.append(f'<line x1="{x}" y1="30" x2="{x}" y2="62" class="ctick"/><text x="{x+ (4 if i<2 else 0)}" y="{22 if i%2==0 else 80}" text-anchor="{"start" if i<2 else "middle"}" class="cl"><tspan class="cv">{v}</tspan> {esc(lab)}</text>')
        parts.append(f'<text x="{W}" y="80" text-anchor="end" class="cn2">{esc(c["maxlabel"])}</text>')
        svg = f'<svg viewBox="0 -4 {W} {H}" width="100%" role="img" aria-label="{esc(c["title"])}">{"".join(parts)}</svg>'
    elif c["kind"] == "bands":
        rows = c["rows"]; W = 600; labw = 160; rowh = 44; mx = max(bd[1] for _, bs in rows for bd in bs)
        parts = []
        for r, (lab, bands) in enumerate(rows):
            y = r * rowh; parts.append(f'<text x="{labw-10}" y="{y+20}" text-anchor="end" class="cl">{esc(lab)}</text>')
            x = labw
            for j, bd in enumerate(bands):
                bl, v = bd[0], bd[1]; story = bd[2] if len(bd) > 2 else ""
                w = max(6, round((W - labw) * v / (mx + 6)))
                parts.append(f'<rect x="{x}" y="{y+6}" width="{w}" height="22" class="cb hit" style="opacity:{1 - j*.3}"{pop(f"{lab}, {bl}: {v} clusters", story)}/><text x="{x+w/2}" y="{y+22}" text-anchor="middle" class="cvin">{v}</text><text x="{x+w/2}" y="{y+40}" text-anchor="middle" class="cn2">{esc(bl)}</text>')
                x += w + 6
        svg = f'<svg viewBox="0 0 {W} {len(rows)*rowh+4}" width="100%" role="img" aria-label="{esc(c["title"])}">{"".join(parts)}</svg>'
    elif c["kind"] == "timeline":
        ev = c["events"]; y0 = c.get("start", ev[0][0]); y1 = c.get("end", ev[-1][0]); W = 600; pad = 14
        X = lambda y: pad + (W - 2*pad) * (y - y0) / (y1 - y0)
        parts = [f'<line x1="{pad}" y1="30" x2="{W-pad}" y2="30" class="cax"/>']
        for era in c.get("eras", []):
            a, b, lab = era; parts.append(f'<rect x="{X(a):.1f}" y="24" width="{X(b)-X(a):.1f}" height="12" class="cera"/><text x="{(X(a)+X(b))/2:.1f}" y="16" text-anchor="middle" class="cn2">{esc(lab)}</text>')
        rows = []
        for i, e in enumerate(ev):
            y, lab = e[0], e[1]; story = e[2] if len(e) > 2 else ""
            x = X(y); ly = 56 if i % 2 == 0 else 72
            anc = "start" if x < 40 else ("end" if x > W - 40 else "middle")
            parts.append(f'<circle cx="{x:.1f}" cy="30" r="4.5" class="cdot"/><circle cx="{x:.1f}" cy="30" r="11" class="ghost hit"{pop(f"{y}: {lab}", story)}/><line x1="{x:.1f}" y1="35" x2="{x:.1f}" y2="{ly-10}" class="cstem"/><text x="{x - 6 if anc == "start" else x + 6 if anc == "end" else x:.1f}" y="{ly}" text-anchor="{anc}" class="cv">{y}</text>')
            rows.append(f'<li{" class=has" if story else ""}{pop(f"{y}: {lab}", story)}><b>{y}</b><span>{esc(lab)}</span></li>')
        for t in c.get("ticks", []):
            parts.append(f'<text x="{X(t):.1f}" y="92" text-anchor="middle" class="cn2">{t}</text>')
        svg = f'<svg viewBox="0 0 {W} 96" width="100%" role="img" aria-label="{esc(c["title"])}">{"".join(parts)}</svg><ol class="tl">{"".join(rows)}</ol>'
    elif c["kind"] == "ring":
        import math
        months = c["months"]; hi = set(c.get("highlight", [])); n = len(months); cx = cy = 210; r0, r1 = 118, 160
        parts = []
        for i, (name, mean) in enumerate(months):
            a0 = -math.pi/2 + 2*math.pi*i/n + .012; a1 = -math.pi/2 + 2*math.pi*(i+1)/n - .012
            p = lambda r, a: f"{cx + r*math.cos(a):.1f},{cy + r*math.sin(a):.1f}"
            d = f"M{p(r1,a0)} A{r1},{r1} 0 0 1 {p(r1,a1)} L{p(r0,a1)} A{r0},{r0} 0 0 0 {p(r0,a0)} Z"
            st = c.get("stories", {}).get(name, "")
            base = c.get("starts", [None]*n)[i]
            body = " ".join(x for x in [f"Month {i+1} of 19." , f"First day: {base}, beginning at sunset the evening before." if base else "", st] if x)
            parts.append(f'<path d="{d}" class="{"cseg on" if name in hi else "cseg"} hit"{pop(f"{name}, {mean}", body)}/>')
            am = (a0 + a1) / 2; tx, ty = cx + 174*math.cos(am), cy + 174*math.sin(am)
            anchor = "start" if math.cos(am) > .15 else ("end" if math.cos(am) < -.15 else "middle")
            parts.append(f'<text x="{tx:.1f}" y="{ty+4:.1f}" text-anchor="{anchor}" class="{"cl on" if name in hi else "cl"}">{esc(mean)}</text>')
            nx, ny = cx + (r0+r1)/2*math.cos(am), cy + (r0+r1)/2*math.sin(am)
            parts.append(f'<text x="{nx:.1f}" y="{ny+4:.1f}" text-anchor="middle" class="cvin">{i+1}</text>')
        parts.append(f'<text x="{cx}" y="{cy-6}" text-anchor="middle" class="cbig">19</text><text x="{cx}" y="{cy+18}" text-anchor="middle" class="cn2">months of 19 days</text><text x="{cx}" y="{cy+32}" text-anchor="middle" class="cn2">plus Ayyám-i-Há</text>')
        svg = f'<svg viewBox="-60 0 540 420" width="100%" role="img" aria-label="{esc(c["title"])}">{"".join(parts)}</svg>'
    elif c["kind"] == "map":
        M = USMAP; parts = [f'<use href="#usmap"/>']
        for name, story in c.get("reports", []):
            x, y = M["places"][name]
            parts.append(f'<g class="hit pin rep"{pop(name, story)}><circle cx="{x}" cy="{y}" r="9" class="ghost"/><circle cx="{x}" cy="{y}" r="4.2" class="crep"/></g>')
        for i, pl in enumerate(c["places"]):
            name, lab, story = pl[0], pl[1], pl[2] if len(pl) > 2 else ""
            x, y = M["places"][name]; side = pl[3] if len(pl) > 3 else ("end" if x > M["w"] * .6 else "start")
            dx = -9 if side == "end" else 9
            parts.append(f'<g class="hit pin"{pop(name, story)}><circle cx="{x}" cy="{y}" r="13" class="ghost"/><circle cx="{x}" cy="{y}" r="6.5" class="cdot big"/><text x="{x+dx*1.15:.0f}" y="{y+4}" text-anchor="{side}" class="cl on">{esc(lab)}</text></g>')
        svg = f'<svg viewBox="-40 -10 {M["w"]+80} {M["h"]+20}" width="100%" role="img" aria-label="{esc(c["title"])}">{"".join(parts)}</svg>'
        if c.get("reports"): svg += '<p class="key"><span><i></i>In this issue</span></p>'
    elif c["kind"] == "pictogram":
        rows = c["rows"]; W = 600; parts = []; rowh = 40
        for r, row in enumerate(rows):
            lab, count, story = row[0], row[1], row[2] if len(row) > 2 else ""
            y = r * rowh
            dots = "".join(f'<circle cx="{170 + k*26}" cy="{y+18}" r="9" class="cdot"/>' for k in range(count))
            parts.append(f'<g class="hit"{pop(f"{lab}: {count}", story)}><rect x="0" y="{y}" width="{W}" height="{rowh}" class="ghost"/><text x="156" y="{y+22}" text-anchor="end" class="cl">{esc(lab)}</text>{dots}<text x="{170 + count*26 + 4}" y="{y+23}" class="cv">{count}</text></g>')
        svg = f'<svg viewBox="0 0 {W} {len(rows)*rowh}" width="100%" role="img" aria-label="{esc(c["title"])}">{"".join(parts)}</svg>'
    hint = ""
    return f'<figure class="chart{size_cls(c)}"{size_sty(c)}>{title}{svg}{note}{hint}</figure>'

def concept_html(c):
    """Diagrams for ideas rather than numbers. Every part can open the shared popup."""
    import math
    kind = c["form"]; W = 600; P = []
    arrow = '<defs><marker id="ah{i}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" class="carr"/></marker></defs>'.format(i=id(c) % 100000)
    mk = f'url(#ah{id(c) % 100000})'
    if c.get("bold"):
        arrow += '<defs><marker id="ahb{i}" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" class="carrb"/></marker></defs>'.format(i=id(c) % 100000)
        mk = f'url(#ahb{id(c) % 100000})'
    def lines(txt, x, y, cls="cl", anchor="middle", lh=17):
        return "".join(f'<text x="{x}" y="{y + k*lh}" text-anchor="{anchor}" class="{cls}">{esc(t)}</text>' for k, t in enumerate(txt.split("|")))
    H = 300
    if kind == "spiral":
        # learning as a widening spiral: no arrows; the line thickens as it grows, returning to its start one turn higher
        st = c["steps"]; W = 760; cx, cy = 380, 236; r0, r1 = 10, 170; T = 3 * 2 * math.pi; N = 360
        rad = lambda t: r0 + (r1 - r0) * (t / T) ** 1.15
        pt = lambda t, rr: (cx + rr * math.sin(t), cy - rr * math.cos(t))
        pts = [pt(T * k / N, rad(T * k / N)) for k in range(N + 1)]
        for k in range(N):
            f = k / N
            P.append(f'<line x1="{pts[k][0]:.1f}" y1="{pts[k][1]:.1f}" x2="{pts[k+1][0]:.1f}" y2="{pts[k+1][1]:.1f}" class="csp" style="stroke-width:{.8 + 13*f**2:.2f};stroke:color-mix(in oklab,var(--accent) {12 + 88*f**1.3:.0f}%,var(--paper))"/>')
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        P.append(f'<path id="sp{id(c)%100000}" d="{d}" fill="none" stroke="none"/><circle r="6.5" class="ctrav"><animateMotion dur="12s" repeatCount="indefinite"><mpath href="#sp{id(c)%100000}"/></animateMotion></circle>')
        place = [(0, "middle"), (math.pi/2, "start"), (math.pi, "middle"), (3*math.pi/2, "end")]
        for i, (lab, story) in enumerate(st):
            a, anc = place[i % 4]; t = T if a == 0 else 2 * 2 * math.pi + a; x, y = pt(a, rad(t) + (22 if a == 0 else 30))
            if anc == "middle" and a == 0: y -= 4
            if anc == "middle" and a > 0: y += 42
            if anc != "middle": y += 13
            P.append(f'<g class="hit"{pop(lab, story)}><text x="{x:.1f}" y="{y - 40:.1f}" text-anchor="{anc}" class="csn">0{i+1}</text><text x="{x:.1f}" y="{y:.1f}" text-anchor="{anc}" class="csw">{esc(lab)}</text></g>')
        H = 450
    elif kind == "cycle":
        st = c["steps"]; n = len(st); bold = c.get("bold")
        cx, cy, r = (300, 190, 128) if bold else (300, 150, 100); H = 380 if bold else 300
        gap = .26 if bold else .32
        for i, (lab, story) in enumerate(st):
            a = -math.pi/2 + 2*math.pi*i/n; b = -math.pi/2 + 2*math.pi*(i+1)/n
            pa = (cx + r*math.cos(a + gap), cy + r*math.sin(a + gap)); pb = (cx + r*math.cos(b - gap), cy + r*math.sin(b - gap))
            P.append(f'<path d="M{pa[0]:.1f},{pa[1]:.1f} A{r},{r} 0 0 1 {pb[0]:.1f},{pb[1]:.1f}" class="cline{" cbold" if bold else ""}" marker-end="{mk}"/>')
        for i, (lab, story) in enumerate(st):
            a = -math.pi/2 + 2*math.pi*i/n; x, y = cx + r*math.cos(a), cy + r*math.sin(a)
            off = 34 if bold else 26
            lx, ly = cx + (r + off)*math.cos(a), cy + (r + off)*math.sin(a)
            anc = "start" if math.cos(a) > .3 else ("end" if math.cos(a) < -.3 else "middle")
            P.append(f'<g class="hit"{pop(lab, story)}><circle cx="{x:.1f}" cy="{y:.1f}" r="{24 if bold else 16}" class="ghost"/><circle cx="{x:.1f}" cy="{y:.1f}" r="{15 if bold else 9}" class="cdot{" big" if bold else ""}"/><text x="{lx:.1f}" y="{ly + (8 if bold else 5):.1f}" text-anchor="{anc}" class="cv{" cvbig" if bold else ""}">{esc(lab)}</text></g>')
        P.append(lines(c.get("center", ""), cx, cy - (6 if bold else 4), "cv" if bold else "cl", lh=22 if bold else 17))
    elif kind == "rings":
        rs = c["rings"]; n = len(rs); cx, cy = 300, 175; step = 160 / n; H = 350
        for i in range(n - 1, -1, -1):
            lab, story = rs[i]; R = step * (i + 1)
            P.append(f'<circle cx="{cx}" cy="{cy}" r="{R:.1f}" class="carea hit cringf" style="fill:color-mix(in oklab,var(--accent) {100 - i*(78/max(1,n-1)):.0f}%,var(--paper))"{pop(lab, story)}/>')
        for i, (lab, story) in enumerate(rs):
            R0 = step * i; R1 = step * (i + 1); y = cy if i == 0 else cy - (R0 + R1)/2
            P.append(lines(lab, cx, y + (4 if i == 0 else 5) - (8 if "|" in lab else 0), "cring cin" if i == 0 else "cring", lh=15))
    elif kind == "path":
        st = c["steps"]; n = len(st); x0, x1 = 70, 530; y = 110 if c.get("bracket") else 50; H = y + 90
        xs = [x0 + (x1 - x0) * i / (n - 1) for i in range(n)]
        for i in range(n - 1):
            P.append(f'<line x1="{xs[i] + 14:.1f}" y1="{y}" x2="{xs[i+1] - 16:.1f}" y2="{y}" class="cline" marker-end="{mk}"/>')
        for i, s_ in enumerate(st):
            lab, story, sty = s_[0], s_[1], (s_[2] if len(s_) > 2 else "")
            shape = f'<rect x="{xs[i]-9:.1f}" y="{y-9}" width="18" height="18" class="csq"/>' if sty == "admin" else f'<circle cx="{xs[i]:.1f}" cy="{y}" r="{11 if sty == "sacred" else 8}" class="{"cdot big" if sty == "sacred" else "cdot"}"/>'
            P.append(f'<g class="hit"{pop(lab.replace("|", " "), story)}><circle cx="{xs[i]:.1f}" cy="{y}" r="22" class="ghost"/>{shape}{lines(lab, round(xs[i],1), y + 36, "cv" if sty else "cl")}</g>')
        if c.get("bracket"):
            a, b, note = c["bracket"]; xa, xb = xs[a], xs[b]
            P.append(f'<path d="M{xa:.1f},{y-22} L{xa:.1f},{y-40} L{xb:.1f},{y-40} L{xb:.1f},{y-22}" class="cbr"/><text x="{(xa+xb)/2:.1f}" y="{y-48}" text-anchor="middle" class="cv">{esc(note)}</text>')
    elif kind == "contrast":
        H = 250
        for k, panel in enumerate(c["panels"]):
            title, story, sch = panel; ox = k * 310; cx, cy = ox + 145, 100
            g = []
            if sch in ("outside", "inside"):
                g.append(f'<circle cx="{cx+(20 if sch=="outside" else 0)}" cy="{cy}" r="72" class="carea" style="opacity:.25"/>')
                pts = [(-30,-30),(20,-40),(40,0),(10,35),(-35,20),(-5,-5)]
                for dx, dy in pts: g.append(f'<circle cx="{cx+(20 if sch=="outside" else 0)+dx}" cy="{cy+dy}" r="7" class="cdotm"/>')
                if sch == "outside":
                    g.append(f'<circle cx="{cx-100}" cy="{cy}" r="9" class="cdot"/><line x1="{cx-88}" y1="{cy}" x2="{cx-58}" y2="{cy}" class="cline" marker-end="{mk}"/>')
                else:
                    g.append(f'<circle cx="{cx+28}" cy="{cy+30}" r="9" class="cdot"/>')
            elif sch == "apart":
                for dx, dy in [(-70,-20),(0,40),(70,-20)]:
                    g.append(f'<circle cx="{cx+dx}" cy="{cy+dy}" r="26" class="carea" style="opacity:.55"/>')
                    g.append(f'<line x1="{cx+dx*0.55:.0f}" y1="{cy+dy*0.55:.0f}" x2="{cx+dx*1.55:.0f}" y2="{cy+dy*1.55+(-14 if dy<0 else 14):.0f}" class="cline" marker-end="{mk}"/>' if False else "")
                g.append(f'<line x1="{cx-40}" y1="{cy-10}" x2="{cx-12}" y2="{cy+18}" class="cline" marker-start="{mk}" marker-end="{mk}"/><line x1="{cx+40}" y1="{cy-10}" x2="{cx+12}" y2="{cy+18}" class="cline" marker-start="{mk}" marker-end="{mk}"/>')
            elif sch == "whole":
                g.append(f'<circle cx="{cx}" cy="{cy}" r="80" class="carea" style="opacity:.25"/>')
                for dx, dy in [(-34,-18),(0,32),(34,-18)]: g.append(f'<circle cx="{cx+dx}" cy="{cy+dy}" r="30" class="carea" style="opacity:.6"/>')
            elif sch == "oneway":
                g.append(f'<rect x="{cx-110}" y="{cy-26}" width="80" height="52" class="carea" style="opacity:.6"/><line x1="{cx-24}" y1="{cy}" x2="{cx+60}" y2="{cy}" class="cline" marker-end="{mk}"/><circle cx="{cx+78}" cy="{cy}" r="10" class="cdot"/>')
            elif sch == "loop":
                pts = [(cx + 62*math.cos(t), cy + 62*math.sin(t)) for t in [-math.pi/2, 0, math.pi/2, math.pi]]
                for i in range(4):
                    a = pts[i]; b = pts[(i+1) % 4]
                    g.append(f'<path d="M{a[0]+(b[0]-a[0])*.22:.1f},{a[1]+(b[1]-a[1])*.22:.1f} Q{cx+(a[0]+b[0]-2*cx)*.9:.1f},{cy+(a[1]+b[1]-2*cy)*.9:.1f} {a[0]+(b[0]-a[0])*.78:.1f},{a[1]+(b[1]-a[1])*.78:.1f}" class="cline" marker-end="{mk}"/>')
                for x, y in pts: g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="10" class="cdot"/>')
            P.append(f'<g class="hit"{pop(title.replace("|"," "), story)}><rect x="{ox}" y="0" width="290" height="{H}" class="cpanel"/>{"".join(g)}{lines(title, cx, 206, "cv")}</g>')
    elif kind == "spectrum":
        pts = c["points"]; n = len(pts); x0, x1 = 60, 560; y = 40; H = 120
        P.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" class="cline" marker-end="{mk}"/>')
        for i, (lab, story) in enumerate(pts):
            x = x0 + (x1 - x0 - 70) * i / (n - 1); on = i == n - 1
            P.append(f'<g class="hit"{pop(lab.replace("|"," "), story)}><circle cx="{x:.1f}" cy="{y}" r="20" class="ghost"/><circle cx="{x:.1f}" cy="{y}" r="{12 if on else 8}" class="{"cdot" if on else "cdotm"}"/>{lines(lab, round(x,1), y + 36, "cv" if on else "cl")}</g>')
    elif kind == "strands":
        st = c["strands"]; n = len(st); xj, yj = 360, 120; H = 240
        for i, (lab, story) in enumerate(st):
            y0 = 40 + i * 80
            P.append(f'<g class="hit"{pop(lab, story)}><path d="M200,{y0} C290,{y0} 300,{yj} {xj},{yj}" class="cstrand"/><path d="M200,{y0} C290,{y0} 300,{yj} {xj},{yj}" class="ghostline"/><circle cx="200" cy="{y0}" r="7" class="cdot"/>{lines(lab, 186, y0 + 5, "cv", "end")}</g>')
        jl, js = c["joined"]
        P.append(f'<g class="hit"{pop(jl.replace("|"," "), js)}><line x1="{xj}" y1="{yj}" x2="585" y2="{yj}" class="cjoin"/>{lines(jl, 472, yj + 34, "cv")}</g>')
    svg = f'<svg viewBox="0 -10 {W} {H + 10}" width="100%" role="img" aria-label="{esc(c["title"])}">{arrow}{"".join(P)}</svg>'
    title = f'<p class="ct">{esc(c["title"])}</p>'; note = f'<p class="cn">{esc(c["note"])}</p>' if c.get("note") else ""
    return f'<figure class="chart concept{size_cls(c)}{" bold" if c.get("bold") else ""}{" spiral" if kind == "spiral" else ""}"{size_sty(c)}>{title}{svg}{note}</figure>'

def first_para_dropcap(h):
    return h.replace("<p>", '<p class="first">', 1)

# ------------------------------------------------------------------ TAB (the published site)
def listen(a):
    """Launcher for a feature's audio reading; playback runs in the docked player."""
    if not a.get("audio"): return ""
    by = f'<span class="lby">Read by {esc(a["audio_reader"])}</span>' if a.get("audio_reader") else ""
    return f'''<button class="listen" type="button" data-src="{a["audio"]}" data-title="{esc(a["title"])}" aria-label="Listen to this story">
      <span class="lp"><svg class="ic-play" viewBox="0 0 16 16" aria-hidden="true"><path d="M4 2.5v11l9-5.5z"/></svg><svg class="ic-pause" viewBox="0 0 16 16" aria-hidden="true"><path d="M3.5 2.5h3.2v11H3.5zM9.3 2.5h3.2v11H9.3z"/></svg></span>
      <span class="lt">Listen to this story</span><span class="ltime">Audio reading</span>{by}
    </button>'''

DOCK = '''<div class="dock" id="dock" role="region" aria-label="Audio player" hidden>
  <div class="dk">
    <button class="dp" type="button" aria-label="Pause"><svg class="ic-play" viewBox="0 0 16 16" aria-hidden="true"><path d="M4 2.5v11l9-5.5z"/></svg><svg class="ic-pause" viewBox="0 0 16 16" aria-hidden="true"><path d="M3.5 2.5h3.2v11H3.5zM9.3 2.5h3.2v11H9.3z"/></svg></button>
    <button class="ds" type="button" aria-label="Playback speed">1×</button>
    <button class="dj" type="button" data-j="-15" aria-label="Back 15 seconds"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5V2L7 6l5 4V7a6 6 0 1 1-6 6H4a8 8 0 1 0 8-8z"/><text x="12" y="16.2" text-anchor="middle">15</text></svg></button>
    <button class="dj" type="button" data-j="15" aria-label="Forward 15 seconds"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5V2l5 4-5 4V7a6 6 0 1 0 6 6h2a8 8 0 1 1-8-8z"/><text x="12" y="16.2" text-anchor="middle">15</text></svg></button>
    <a class="dt" href="#"></a>
    <span class="dtime">0:00 / 0:00</span>
    <div class="dbar" role="slider" tabindex="0" aria-label="Seek" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><i></i><b></b></div>
    <button class="dx" type="button" aria-label="Close player"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3.5 3.5l9 9M12.5 3.5l-9 9"/></svg></button>
  </div>
</div>'''

def build_tab(member=False):
    tints = {"gregory":"#e8532a","newyorkers":"#f05a7e","twoartists":"#b07a4a","abs":"#c9462c","endeavor":"#1b5e6b","comic":"#e9a21f"}
    secs = []
    bands = ["#1b5e6b", "#8a3a1e", "#3b3f7a", "#5c2a4e", "#2f5d3a", "#8b6a1a"]
    for i, a in enumerate(ARTICLES):
        art = ""
        if a.get("art"):
            if a["slug"] == "comic":
                art = f'''<figure class="plate comic"><img src="img/{a["art"]}" alt="{esc(a["art_alt"])}"><img src="img/{a["art2"]}" alt="{esc(a["art2_alt"])}"><figcaption>{esc(a["art_credit"])}</figcaption></figure>'''
            else:
                cls = "plate bare" if a.get("art_transparent") else "plate"
                if a.get("art_width"): cls += " capped"
                cap = f'<figcaption>{esc(a["art_credit"])}</figcaption>' if a.get("art_credit") else ""
                ov = a.get("art_overlay")
                ov_open = f'<div class="ovw" style="--ar:{ov["ar"]}">' if ov else ""
                ov_close = f'<div class="ov" aria-hidden="true">{ov["html"]}</div></div>' if ov else ""
                art = f'''<figure class="{cls}" style="--aw:{a.get("art_width",0)}px">{ov_open}<img src="img/{a["art"]}" alt="{esc(a["art_alt"])}">{ov_close}{cap}</figure>'''
        else:
            art = '<div class="numeral" aria-hidden="true">50</div>'
        dek = f'<p class="dek">{esc(a["dek"])}</p>' if a.get("dek") else ""
        by = (f'<p class="by{" nob" if a["byline"].startswith(("Adapted","Story")) else ""}">{esc(a["byline"])}</p>') if a.get("byline") else ""
        blooms = '<div class="blooms" aria-hidden="true"><i></i><i></i><i></i></div>' if a["slug"] == "newyorkers" else ""
        pal = {"gregory":("#f26b2b","#2448c8","#f05a7e","#f3c623"),"newyorkers":("#2448c8","#f05a7e","#f3c623","#5f8f3a"),"twoartists":("#b07a4a","#e9a21f","#2f6a4a","#f26b2b"),"abs":("#c9462c","#1b5e6b","#e9a21f","#2448c8"),"endeavor":("#1b5e6b","#e9a21f","#9ec3cc","#f26b2b"),"comic":("#f3c623","#2448c8","#f26b2b","#5f8f3a")}[a["slug"]]
        torn = f'<div class="torn" data-v="{i % 6}" aria-hidden="true" style="--a:{pal[0]};--b:{pal[1]};--c:{pal[2]};--d:{pal[3]}"><i></i><i></i><i></i><i></i></div>'
        secs.append(f'''<article class="story" id="{a["slug"]}" style="--accent:{tints[a["slug"]]}">{blooms}
  {art}
  <header class="shead">{torn}
    <h2>{esc(a["title"])}</h2>
    {dek}
  </header>
  <aside class="margin">
    <p class="kicker">{esc(a["kicker"])}</p>
    {by}
    <p class="pp">Pages {a["pages"]}</p>
    {listen(a)}
  </aside>
  <div class="prose">{first_para_dropcap(body_html(a["body"]))}</div>
</article>''')
        if i < len(VOICES):
            v = VOICES[i]
            secs.append(f'''</div><aside class="voice" style="--band:{bands[i % len(bands)]}"><div class="vin"><p>{esc(v[0])}</p><cite>{esc(v[1])}</cite></div></aside><div class="wrap">''')
    head = "".join(f'<a href="#{a["slug"]}" style="--tint:{tints[a["slug"]]}"><span>{esc(a["short"])}</span><i class="fill"></i></a>' for a in ARTICLES)
    index = "".join(f'<li><a href="#{a["slug"]}"><span class="t">{esc(a["title"])}</span><span class="pg">{a["pages"].split("–")[0]}</span></a></li>' for a in ARTICLES)
    lead = ""; depts = ""; dindex = ""; dhead = ""
    if member:
        from member_data import LETTER, HUQUQ, ABIDING, FUND, RHYTHM, BOOKS, NOTICES
        L = LETTER
        lead = f'''<article class="story letter members" id="{L["slug"]}">
  <header class="shead"><p class="kicker-top">{esc(L["kicker"])}</p><h2>{esc(L["title"])}</h2><p class="dek">{esc(L["dek"])}</p></header>
  <aside class="margin"><p class="kicker">Mid-year letter</p><p class="pp">Pages {L["pages"]}</p></aside>
  <div class="prose"><p class="salute">{esc(L["salutation"])}</p>{first_para_dropcap(body_html(L["body"]))}<p class="sign">{esc(L["closing"][0])}<br><b>{esc(L["closing"][1])}</b></p></div>
</article>'''
        def dept_open(d, tint):
            dek = f'<p class="dek">{esc(d["dek"])}</p>' if d.get("dek") else ""
            return f'''<article class="story dept members" id="{d["slug"]}">
  <header class="shead"><p class="kicker-top">{esc(d["kicker"])}</p><h2>{esc(d["title"])}</h2>{dek}</header>
  <aside class="margin"><p class="kicker">{esc(d["kicker"])}</p><p class="pp">Pages {d["pages"]}</p></aside>'''
        huq = dept_open(HUQUQ, "#3b3f7a") + f'<div class="prose">{first_para_dropcap(body_html(HUQUQ["body"]))}</div></article>'
        qs = "".join(f'<section class="qblock"><h3>{esc(q)}</h3>' + "".join(f'<blockquote class="passage"><p>{esc(t)}</p><cite>{esc(c)}</cite></blockquote>' for t,c in items) + '</section>' for q,items in ABIDING["questions"])
        abide = dept_open(ABIDING, "#5c2a4e") + f'''<div class="prose compilation"><blockquote class="passage lead"><p>{esc(ABIDING["epigraph"][0])}</p><cite>{esc(ABIDING["epigraph"][1])}</cite></blockquote>{qs}</div></article>'''
        fund = dept_open(FUND, "#2f5d3a") + f'<div class="prose">{first_para_dropcap(body_html(FUND["body"]))}</div></article>'
        R = RHYTHM
        hd = "".join(f'<li><b>{esc(n)}</b><span>{esc(w)}</span></li>' for n,w in R["holydays"])
        fs = "".join(f'<li><b>{esc(n)}</b><i>{esc(m)}</i><span>{esc(d)}</span></li>' for n,m,d in R["feasts"])
        rhythm = dept_open(R, "#8b6a1a") + f'''<div class="prose calendar">
  <div class="cal"><div><h3>Holy Days</h3><ul class="hd">{hd}</ul></div><div><h3>Upcoming Feasts</h3><ul class="feast">{fs}</ul></div></div>
  {chart_html(R["ring"]) if R.get("ring") else ""}
  <p class="note">{esc(R["note"])}</p>
  <blockquote class="passage prayer"><p>{esc(R["prayer"][0])}</p><cite>{esc(R["prayer"][1])}</cite></blockquote>
</div></article>'''
        B = BOOKS
        def book(it):
            t, sub, desc, price = it[:4]; url = it[4] if len(it) > 4 else None
            h = f'<a href="{url}" target="_blank" rel="noopener">{esc(t)}</a>' if url else esc(t)
            buy = f' <a class="buy" href="{url}" target="_blank" rel="noopener">View at the Bahá\'í Bookstore</a>' if url else ""
            return f'<li><h4>{h}</h4>{("<p class=sub>"+esc(sub)+"</p>") if sub else ""}<p>{esc(desc)}</p>{("<p class=price>"+esc(price)+buy+"</p>") if price else ""}</li>'
        bk = "".join(book(it) for it in B["items"])
        books = dept_open(B, "#8a3a1e") + f'<div class="prose shelf"><ul class="books">{bk}</ul><p class="note">{esc(B["contact"])}</p></div></article>'
        nt = "".join(f'''<li>{('<img src="img/'+n["img"]+'" alt="'+esc(n["title"])+' cover">') if n.get("img") else ""}<p class="k">{esc(n["kicker"])}</p><h4>{esc(n["title"])}</h4><p>{esc(n["text"])}</p><cite>{esc(n["src"])}</cite></li>''' for n in NOTICES)
        notices = f'''<article class="story dept members" id="notices"><header class="shead"><p class="kicker-top">Announcements</p><h2>Notices</h2></header><aside class="margin"><p class="kicker">Notices</p><p class="pp">Pages 40–48</p></aside><div class="prose"><ul class="notices">{nt}</ul></div></article>'''
        depts = f'<h2 class="reg members" id="members">The full issue<small>The National Spiritual Assembly\'s mid-year letter and the departments of the printed issue</small></h2>' + lead + huq + abide + fund + rhythm + books + notices
        lead = ""
        D = [("huquq","Ḥuqúqu'lláh","30"),("abiding","Abiding in God's Law","32"),("fund","Bahá'í Fund","42"),("rhythm","Rhythm of Bahá'í Life","39"),("books","Bookstore","36"),("notices","Notices","40")]
        dindex = '<h2 style="margin-top:36px;color:var(--mem)">The full issue</h2><ol class="index mem">' + f'<li><a href="#letter"><span class="t">{esc(L["title"])}</span><span class="pg">2</span></a></li>' + "".join(f'<li><a href="#{s}"><span class="t">{esc(t)}</span><span class="pg">{p}</span></a></li>' for s,t,p in D) + '</ol>'
        shorts = {"gregory":"Gregory","newyorkers":"New Yorkers","twoartists":"Two artists","abs":"ABS","endeavor":"Endeavor","comic":"Comic"}
        dhead = "".join(f'<a href="#{a["slug"]}" style="--tint:{tints[a["slug"]]}"><span>{shorts[a["slug"]]}</span><i class="fill"></i></a>' for a in ARTICLES) + f'<a href="#letter" class="mem more" style="--tint:var(--mem)"><span>Letter</span><i class="fill"></i></a><a href="#huquq" class="mem" style="--tint:var(--mem)"><span>Departments</span><i class="fill"></i></a>'
        head = dhead
    title = esc(ISSUE["title"]) + (" Full Edition" if member else "")
    return f'''<title>{title}</title>
{SIDES}
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,300..800&family=Literata:ital,opsz,wght@0,7..72,300..700;1,7..72,300..700&family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..600;1,6..96,400..600&family=Pinyon+Script&display=swap">
<style>
/* Layout: one long page. Running head with color tabs; masthead with the framed cover painting; index and front matter; each feature on a three-column field (margin, text, open) opened by its art; a colored band between features carries one passage from the issue's pages on the arts. */
:root{{
  --paper:#f5f1e8; --ink:#1d1a16; --mute:#6a635a; --rule:#d9d2c4; --accent:#1b5e6b; --cream:#f7f2ea; --bar:#fdfcf9; --tabon:#f5f1e8; --barrule:#d9d2c4; --tabon-white:#ffffff; --mem:#5b4a8a;
  --disp:"Bricolage Grotesque","Helvetica Neue",Arial,sans-serif; --text:"Literata",Georgia,serif; --ui:"Bricolage Grotesque","Helvetica Neue",Arial,sans-serif;
}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--paper:#15130f;--ink:#efe9dd;--mute:#a39b8e;--rule:#2f2a22;--accent:#7fc0c9;--cream:#1c1915;--bar:#221e19;--tabon:#15130f;--barrule:#2f2a22;--tabon-white:#1f1c17;--mem:#b3a3e0;color-scheme:dark}}}}
:root[data-theme="dark"]{{--paper:#15130f;--ink:#efe9dd;--mute:#a39b8e;--rule:#2f2a22;--accent:#7fc0c9;--cream:#1c1915;--bar:#221e19;--tabon:#15130f;--barrule:#2f2a22;--tabon-white:#1f1c17;--mem:#b3a3e0;color-scheme:dark}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
body{{margin:0;overflow-x:clip;background:var(--paper);color:var(--ink);font-family:var(--text);font-size:18px;line-height:1.55}}
.story,#top{{scroll-margin-top:calc(env(safe-area-inset-top,0px) + 64px)}}
.wrap{{max-width:1120px;margin:0 auto;{GUT}}}
.ui{{font-family:var(--ui);font-size:12px;letter-spacing:.12em;text-transform:uppercase}}
/* motion: terraces behind the open right third; brush strokes under the masthead on load; watercolor blooms in the New Yorkers margin. All off under reduced motion. */
.terraces{{position:fixed;top:0;right:0;bottom:0;width:30%;z-index:0;pointer-events:none;opacity:.32;filter:blur(44px) saturate(.85)}}
.terraces i{{position:absolute;left:-20%;right:-20%;height:34%;border-radius:50% 50% 40% 40%/60% 60% 40% 40%;animation:drift 28s ease-in-out infinite alternate}}
.terraces i:nth-child(1){{top:-12%;background:linear-gradient(90deg,#d9742a,#e9a21f);animation-duration:32s}}
.terraces i:nth-child(2){{top:22%;background:#5f8f3a;animation-delay:-8s}}
.terraces i:nth-child(3){{top:50%;background:#2f6a4a;animation-delay:-16s;animation-duration:36s}}
.terraces i:nth-child(4){{top:78%;background:#b7d35a;animation-delay:-4s}}
@keyframes drift{{from{{transform:translate(-3%,0) rotate(-1.2deg)}}to{{transform:translate(3%,-2%) rotate(1.2deg)}}}}
main,.head{{position:relative;z-index:1}}
.mast{{position:relative}}
.stroke{{position:absolute;left:-2%;top:38%;width:min(760px,80%);height:90px;z-index:-1;pointer-events:none}}
.stroke path{{fill:none;stroke:#b7d35a;stroke-width:34;stroke-linecap:round;opacity:.5;stroke-dasharray:900;stroke-dashoffset:900;animation:paint 2.6s cubic-bezier(.5,0,.2,1) .4s forwards}}
.stroke path+path{{stroke:#e9a21f;stroke-width:22;animation-delay:1.1s;opacity:.45}}
@keyframes paint{{to{{stroke-dashoffset:0}}}}
.story{{position:relative}}
.blooms{{position:absolute;left:-4%;top:30%;width:28%;height:54%;z-index:0;pointer-events:none;filter:blur(26px);opacity:.7}}
.blooms i{{position:absolute;width:78%;aspect-ratio:1;border-radius:50%;mix-blend-mode:multiply;animation:bloom 22s ease-in-out infinite alternate}}
.blooms i:nth-child(1){{left:0;top:0;background:#f05a7e}}
.blooms i:nth-child(2){{left:30%;top:32%;background:#2448c8;animation-delay:-7s;animation-duration:27s}}
.blooms i:nth-child(3){{left:5%;top:60%;background:#f3c623;animation-delay:-13s}}
@keyframes bloom{{from{{transform:scale(.9)}}to{{transform:scale(1.15) translate(6%,-6%)}}}}
.story>*{{position:relative;z-index:1}}
.story>.blooms{{position:absolute;z-index:0}}
@media (prefers-reduced-motion:reduce){{.terraces i,.blooms i,.torn i{{animation:none}}.stroke path{{animation:none;stroke-dashoffset:0}}.torn i{{transition:none}}}}
@media (max-width:980px){{.terraces,.blooms,.torn{{display:none}}}}
/* charts */
.chart .cline{{fill:none;stroke:var(--mute);stroke-width:1.6}} .chart .carr{{fill:var(--mute)}} .chart .carea{{fill:var(--accent)}} .chart .cdotm{{fill:var(--mute);opacity:.55}}
.chart .csq{{fill:var(--paper);stroke:var(--accent);stroke-width:2.5}} .chart .cdot.big{{stroke:var(--paper);stroke-width:3}}
.chart .cbr{{fill:none;stroke:var(--accent);stroke-width:1.5;stroke-dasharray:4 3}} .chart .cpanel{{fill:transparent;stroke:transparent}}
.chart .cringf{{stroke:var(--paper);stroke-width:2.5}} .chart text.cin{{fill:#fff}} .chart .cring{{font-family:var(--ui);font-weight:600;font-size:13.5px;fill:var(--ink)}} .chart circle.carea.hit:hover{{filter:brightness(1.08)}}
.chart .cstrand{{fill:none;stroke:var(--accent);stroke-width:5;opacity:.7}} .chart .ghostline{{fill:none;stroke:transparent;stroke-width:22}} .chart .cjoin{{stroke:var(--accent);stroke-width:16;stroke-linecap:round}}
.chart g.hit:hover .cstrand{{opacity:1}}
.chart .ghost{{fill:transparent}} .chart .hit{{cursor:pointer;outline:none}}
.chart .hit:hover .cb,.chart .hit:focus-visible .cb,.chart rect.hit:hover,.chart path.hit:hover{{filter:brightness(1.12)}}
.chart path.hit:focus-visible,.chart rect.hit:focus-visible,.chart .hit:focus-visible .cdot{{stroke:var(--ink);stroke-width:2}}
.chart .pin:hover .cdot,.chart .pin:focus-visible .cdot{{r:7.5}}
.cland{{fill:var(--cream);stroke:var(--rule);stroke-width:1}} .cstate{{fill:none;stroke:var(--rule);stroke-width:.6}} .chart text{{pointer-events:none}}
.chart .tl li.has,.figs div.has{{cursor:pointer}} .chart .tl li.has span{{text-decoration:underline dotted;text-underline-offset:3px;text-decoration-color:var(--rule)}}
.figs div.has b::after{{content:"+";font-size:.45em;vertical-align:super;margin-left:3px;color:var(--accent)}}
.figs div.has:focus-visible,.chart .tl li.has:focus-visible{{outline:2px solid var(--accent);outline-offset:4px}}
.chart .tap{{font-family:var(--ui);font-size:12px;letter-spacing:.04em;color:var(--mute);margin:6px 0 0;opacity:.8}}
.popup{{position:fixed;z-index:30;max-width:min(340px,calc(100vw - 32px));background:var(--tabon-white);color:var(--ink);border:1px solid var(--rule);border-top:3px solid var(--pa,var(--accent));box-shadow:0 10px 30px rgba(30,25,15,.16);padding:14px 16px 14px;font-family:var(--ui);font-size:14px;line-height:1.5;opacity:0;transform:translateY(4px);transition:opacity .15s,transform .15s;pointer-events:none}}
.popup.show{{opacity:1;transform:none;pointer-events:auto}}
.popup b{{display:block;font-family:var(--disp);font-weight:700;font-size:15.5px;letter-spacing:-.01em;margin:0 18px 6px 0}}
.popup p{{margin:0;color:var(--ink)}}
.popup button{{position:absolute;top:6px;right:6px;border:0;background:none;font-size:18px;line-height:1;color:var(--mute);cursor:pointer;padding:4px 6px}}
@media (prefers-reduced-motion:reduce){{.popup{{transition:none}}}}
.chart .cax{{stroke:var(--rule);stroke-width:2}} .chart .cdot{{fill:var(--accent)}} .chart .cstem{{stroke:var(--rule);stroke-width:1}} .chart .cera{{fill:var(--accent);opacity:.18}}
.chart .cseg{{fill:var(--rule)}} .chart .cseg.on{{fill:var(--accent)}} .chart .cl.on{{fill:var(--ink);font-weight:600}} .chart .cbig{{font-family:var(--disp);font-weight:800;font-size:48px;fill:var(--ink)}}
.chart .cvin{{font-family:var(--disp);font-weight:700;font-size:12px;fill:#fff}}
.chart .tl{{list-style:none;margin:12px 0 0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:6px 22px}}
.chart .tl li{{display:grid;grid-template-columns:3.4em 1fr;gap:10px;font-family:var(--ui);font-size:14px;line-height:1.45;color:var(--mute)}} .chart .tl b{{color:var(--ink);font-variant-numeric:tabular-nums}}
.prose .chart.wide{{max-width:none}}
.prose .chart{{margin:1.8em 0 2.2em;max-width:600px}}
.prose .chart.sized{{max-width:var(--cw)}}
/* bands: full-bleed rooms for high-resolution sets */
.prose>.band{{grid-column:1/-1;width:100vw;margin:clamp(48px,7vw,96px) 0 clamp(48px,7vw,96px) calc(50% - 50vw);padding:clamp(40px,6vw,88px) 0;position:relative}}
.band .bin{{max-width:1240px;margin:0 auto;{GUT}display:grid;grid-template-columns:repeat(12,1fr);gap:clamp(14px,2.2vw,32px);align-items:start}}
.band .bi{{margin:0;min-width:0}} .band .bi img{{display:block;width:100%;height:auto}}
.band figcaption{{font-family:var(--ui);font-size:13px;line-height:1.45;margin-top:10px;max-width:42ch}}
.band .blab{{grid-column:1/-1;font-family:var(--ui);font-size:12px;letter-spacing:.16em;text-transform:uppercase;margin:0 0 6px}}
.band.wall{{background:#e7c3c6;color:#5a3a3e}}
.band.wall::before{{content:"";position:absolute;inset:0;opacity:.35;mix-blend-mode:multiply;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 .55 0 0 0 0 .35 0 0 0 0 .38 0 0 0 .55 0'/%3E%3C/filter%3E%3Crect width='160' height='160' filter='url(%23n)'/%3E%3C/svg%3E");pointer-events:none}}
.band.wall .bin{{position:relative}}
.band.wall .bi img{{box-shadow:0 14px 30px -12px rgba(70,30,35,.45),0 2px 4px rgba(70,30,35,.18)}}
.band.wall .w1{{grid-column:1/8;grid-row:2}} .band.wall .w2{{grid-column:8/13;grid-row:2/4;margin-top:clamp(30px,5vw,70px)}}
.band.wall .w3{{grid-column:1/5;grid-row:3;margin-top:clamp(10px,2vw,28px)}} .band.wall .w4{{grid-column:5/8;grid-row:3;margin-top:clamp(10px,2vw,28px)}}
.band.stage{{background:radial-gradient(120% 90% at 30% 20%,#2a211b 0%,#100d0b 55%,#070605 100%);color:#d9cfc2}}
.band.stage .s1{{grid-column:1/8}} .band.stage .s2{{grid-column:8/13;margin-top:clamp(60px,12vw,200px)}}
.band.stage figcaption{{color:#b8ab9b}}
.band.stage .blab{{color:#8f8273}}
.prose>.portraits{{grid-column:1/-1;display:grid;grid-template-columns:repeat(12,1fr);gap:clamp(14px,2vw,28px);margin:clamp(40px,6vw,80px) 0;align-items:start}}
.portraits figure{{margin:0}} .portraits img{{display:block;width:100%;height:auto}}
.portraits figcaption{{font-family:var(--ui);font-size:13px;color:var(--mute);margin-top:10px;line-height:1.45}}
.portraits .q1{{grid-column:2/7}} .portraits .q2{{grid-column:7/12;margin-top:clamp(60px,9vw,140px)}} .portraits .p1{{grid-column:1/6}} .portraits .p2{{grid-column:6/9;margin-top:clamp(60px,9vw,140px)}} .portraits .p3{{grid-column:9/13;margin-top:clamp(20px,3vw,44px)}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]) .band.wall{{background:#4a3436;color:#ecd6d8}}}}
:root[data-theme="dark"] .band.wall{{background:#4a3436;color:#ecd6d8}}
@media (max-width:760px){{.band .bin>.bi,.portraits>figure{{grid-column:1/-1!important;grid-row:auto!important;margin-top:0!important;transform:none!important}}}}

.chart .carrb{{fill:var(--accent)}}
.chart .csp{{stroke-linecap:round}} .chart .ctrav{{fill:var(--accent);stroke:var(--paper);stroke-width:3}}
.chart text.csw{{font-family:var(--disp);font-weight:800;font-size:40px;letter-spacing:-.045em;fill:var(--ink)}}
.chart text.csn{{font-family:var(--ui);font-weight:600;font-size:13px;letter-spacing:.18em;fill:var(--accent)}}
.chart text.csc{{font-family:var(--text);font-style:italic;font-size:19px;fill:var(--mute)}}
.chart .hit:hover text.csw{{fill:var(--accent)}}
.chart.spiral .ct{{font-family:var(--disp);font-weight:800;font-size:clamp(22px,2.2vw,30px);line-height:1.15;letter-spacing:-.025em;max-width:24ch;margin-bottom:22px}} .chart.spiral .cn{{margin-top:22px}}
@media (prefers-reduced-motion:reduce){{.chart .ctrav{{display:none}}}} .chart.bold .ct{{font-size:clamp(17px,1.6vw,20px);line-height:1.35;max-width:40ch;letter-spacing:.01em}}
.chart .cline.cbold{{stroke:var(--accent);stroke-width:5;opacity:.85}} .chart text.cvbig{{font-size:25px;font-weight:800;letter-spacing:-.01em}}
@media (min-width:981px){{.prose>.chart.span{{grid-column:2/4}}}}
.chart .crep{{fill:var(--mute);opacity:.75;transition:opacity .15s}} .chart .rep:hover .crep,.chart .rep:focus-visible .crep{{opacity:1;r:5}}
.chart .key{{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--ui);font-size:13px;color:var(--mute);margin:10px 0 0}} .chart .key i{{display:inline-block;width:9px;height:9px;border-radius:50%;background:var(--accent);margin-right:6px;vertical-align:0}} .chart .key i.g{{background:var(--mute);opacity:.75;width:8px;height:8px}}
.chart .ct{{font-family:var(--ui);font-weight:600;font-size:15px;letter-spacing:.04em;margin:0 0 10px;color:var(--ink)}}
.chart .cn{{font-family:var(--ui);font-size:13.5px;color:var(--mute);margin:8px 0 0}}
.chart svg{{display:block;overflow:visible}}
.chart .cb{{fill:var(--accent)}} .chart .ctrack{{fill:var(--rule)}} .chart .ctick{{stroke:var(--ink);stroke-width:1.5}}
.chart .cl{{font-family:var(--ui);font-size:14px;fill:var(--mute)}} .chart .cv{{font-family:var(--disp);font-weight:700;font-size:15.5px;fill:var(--ink);font-variant-numeric:tabular-nums}}
.chart .cvin{{font-family:var(--disp);font-weight:700;font-size:13.5px;fill:#fff}} .chart .cn2{{font-family:var(--ui);font-size:12px;fill:var(--mute)}}
/* member-only areas */
.story.members{{--accent:var(--mem)}}
.members .margin::before{{content:"Full issue";display:inline-block;font-family:var(--ui);font-size:10px;letter-spacing:.14em;text-transform:uppercase;font-weight:600;color:var(--mem);border:1px solid var(--mem);border-radius:999px;padding:3px 8px;margin-bottom:12px}}
.reg.members{{border-top-color:var(--mem);color:var(--mem)}}
.reg.members small{{display:block;font-family:var(--ui);font-weight:400;font-size:14px;letter-spacing:.02em;color:var(--mute);margin-top:8px}}
.head nav a.mem{{background:color-mix(in oklab,var(--mem) 10%,var(--bar))}}
.head nav a.mem.on{{background:color-mix(in oklab,var(--mem) 16%,var(--tabon))}}
.index.mem a .t::after{{content:"Full issue";font-family:var(--ui);font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--mem);margin-left:10px;vertical-align:middle}}
/* departments and letter */
.kicker-top{{font-family:var(--ui);font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);font-weight:600;margin:0 0 14px}}
.reg{{grid-column:1/-1;font-family:var(--disp);font-weight:800;font-size:clamp(34px,5vw,64px);letter-spacing:-.035em;margin:clamp(64px,10vw,140px) 0 0;padding-top:28px;border-top:3px solid var(--ink)}}
.letter .shead h2{{font-size:clamp(40px,5.6vw,78px);max-width:18ch}}
.prose .salute{{font-style:italic;margin-bottom:1.2em}}
.prose .sign{{margin-top:2em;font-style:italic}} .prose .sign b{{font-style:normal;font-family:var(--ui);font-size:12px;letter-spacing:.12em;text-transform:uppercase;font-weight:600;color:var(--accent)}}
.prose .ext{{margin:1.4em 0 1.6em;padding:0 0 0 20px;border-left:2px solid var(--rule);font-size:.94em}}
.prose .ext p{{margin:0}} .prose .ext2{{margin-left:20px}}
.prose .qs{{margin:0 0 1.4em;padding-left:1.2em}} .prose .qs li{{margin:0 0 .6em;text-wrap:pretty}}
.prose .kv{{margin:1.2em 0 1.8em;display:grid;grid-template-columns:minmax(10ch,14ch) 1fr;gap:8px 18px;font-size:15.5px;line-height:1.5}}
.prose .kv dt{{font-family:var(--ui);font-weight:600;font-size:12.5px;letter-spacing:.04em;color:var(--accent);padding-top:2px}} .prose .kv dd{{margin:0}}
.prose .figs{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:18px;margin:1.8em 0 2.2em}}
.prose .figs div{{border-top:3px solid var(--accent);padding-top:10px}}
.prose .figs b{{display:block;font-family:var(--disp);font-weight:800;font-size:clamp(36px,3.8vw,52px);letter-spacing:-.03em;line-height:1;font-variant-numeric:tabular-nums}}
.prose .figs span{{display:block;font-family:var(--ui);font-size:14px;color:var(--mute);margin-top:6px;line-height:1.4}}
.compilation .qblock{{margin:2.4em 0 0}}
.compilation h3{{font-family:var(--disp);font-weight:700;font-size:22px;letter-spacing:-.02em;text-transform:none;border:0;padding:0;margin:0 0 .8em;color:var(--ink)}}
.passage{{margin:0 0 1.4em;padding:16px 0 0;border-top:1px solid var(--rule)}}
.passage p{{margin:0 0 8px;font-size:17.5px;line-height:1.55}}
.passage cite{{font-style:normal;font-family:var(--ui);font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--mute)}}
.passage.lead{{border:0;padding:0;font-style:italic;font-size:1.05em}}
.calendar .cal{{display:grid;grid-template-columns:1.4fr 1fr;gap:32px;margin:0 0 1.6em}}
.calendar h3{{border:0;padding:0;margin:0 0 .8em}}
.calendar ul{{list-style:none;margin:0;padding:0}}
.calendar .hd li{{padding:12px 0;border-top:1px solid var(--rule);display:grid;gap:4px}} .calendar .hd b{{font-family:var(--disp);font-size:17px;letter-spacing:-.01em}} .calendar .hd span{{font-family:var(--ui);font-size:13px;color:var(--mute);line-height:1.5}}
.calendar .feast li{{padding:12px 0;border-top:1px solid var(--rule);display:grid;grid-template-columns:auto 1fr auto;gap:10px;align-items:baseline}} .calendar .feast b{{font-family:var(--disp);font-size:17px}} .calendar .feast i{{color:var(--mute);font-size:14px}} .calendar .feast span{{font-family:var(--ui);font-size:13px;font-variant-numeric:tabular-nums}}
.passage.prayer{{border-top:3px solid var(--accent);margin-top:1.6em}} .passage.prayer p{{font-style:italic;font-size:19px;line-height:1.5}}
.shelf .books{{list-style:none;margin:0 0 1.6em;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:22px 28px}}
.shelf .books li{{border-top:1px solid var(--rule);padding-top:12px}}
.shelf h4{{font-family:var(--disp);font-weight:700;font-size:18px;letter-spacing:-.015em;margin:0 0 4px}}
.shelf .sub{{font-family:var(--ui);font-size:12.5px;color:var(--mute);margin:0 0 8px}}
.shelf .books p{{font-size:15px;line-height:1.5;margin:0 0 8px}}
.shelf .price{{font-family:var(--ui);font-size:12.5px;font-weight:600;color:var(--accent)}}
.shelf h4 a{{color:inherit;text-decoration:none;background-image:linear-gradient(var(--accent),var(--accent));background-size:100% 1px;background-repeat:no-repeat;background-position:0 100%}}
.shelf h4 a:hover,.shelf h4 a:focus-visible{{color:var(--accent)}}
.shelf .buy{{display:block;margin-top:4px;font-weight:500;color:var(--accent)}}
.notices{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:28px}}
.dept .prose:has(.notices){{grid-column:2/4;display:block;max-width:none}}
.notices li{{border-top:3px solid var(--accent);padding-top:14px}}
.notices img{{display:block;width:120px;height:auto;border:1px solid var(--rule);margin:0 0 12px}}
.notices .k{{font-family:var(--ui);font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--mute);margin:0 0 6px}}
.notices h4{{font-family:var(--disp);font-weight:700;font-size:20px;letter-spacing:-.02em;margin:0 0 8px}}
.notices p{{font-size:15.5px;line-height:1.55;margin:0 0 8px}}
.notices cite{{font-style:normal;font-family:var(--ui);font-size:12.5px;color:var(--accent)}}
.prose>.shelf,.prose>.calendar{{grid-column:2/4}}
.dept .prose.shelf,.dept .prose.calendar{{grid-column:1/-1;display:block;max-width:none}}
.dept .prose.calendar{{max-width:72ch;grid-column:2/4}}
.dept .prose.shelf{{grid-column:2/4}}
.dept .margin,.letter .margin{{grid-row:2}}
.dept .prose,.letter .prose{{grid-row:2}}
.dept .shead,.letter .shead{{grid-row:1}}

.head.member nav a{{padding:18px 13px 0;font-size:14.5px}}
@media (max-width:980px){{.calendar .cal{{grid-template-columns:1fr}}}}
/* running head */
body::before{{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--paper)}}
.head{{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:color-mix(in oklab,var(--bar) 94%,transparent);backdrop-filter:blur(10px);border-bottom:1px solid var(--barrule)}}
.head .in{{max-width:1120px;margin:0 auto;{GUT}display:flex;align-items:stretch;gap:0;overflow-x:auto;scrollbar-width:none;position:relative}}
.head .brand{{font-family:var(--disp);font-size:17px;font-weight:700;letter-spacing:-.02em;color:var(--ink);text-decoration:none;white-space:nowrap;align-self:center;margin-right:28px}}
.head .brand .bn{{display:inline-flex;align-items:center;gap:6px}}
.head .brand .star{{width:17px;height:17px;flex:none;transform:translateY(-1px)}}
.head .brand small{{display:block;font-weight:400;font-size:11px;color:var(--mute);letter-spacing:.02em}}
.head nav{{display:flex;margin-left:auto}}
.head nav a{{display:flex;align-items:flex-end;position:relative;padding:18px 16px 0;border-bottom:4px solid var(--tint);color:var(--ink);text-decoration:none;font-family:var(--disp);font-weight:600;font-size:15px;letter-spacing:-.01em;white-space:nowrap}}
.head nav a span{{padding-bottom:12px}}
.head nav a.on,.head nav a:hover,.head nav a:focus-visible{{background:var(--tabon)}}
.head nav a .fill{{position:absolute;left:0;bottom:-4px;height:4px;width:0;background:var(--ink);opacity:.9;transition:width .4s cubic-bezier(.2,.8,.2,1)}}
.head nav a.on .fill{{width:var(--p,0%)}}
.head .ind{{position:absolute;bottom:-1px;height:2px;background:var(--ink);transition:left .5s cubic-bezier(.2,.8,.2,1),width .5s cubic-bezier(.2,.8,.2,1)}}
@media (prefers-reduced-motion:reduce){{.head nav a .fill,.head .ind{{transition:none}}}}
@media (max-width:900px){{.head .brand small{{display:none}} .head nav{{margin-left:0}} .head nav a{{padding:14px 12px 0;font-size:14px}}}}
/* cover */
.cover{{padding-block:clamp(28px,5vw,64px) 0}}
.cover .mast .the{{font-family:var(--disp);font-weight:500;font-size:clamp(18px,2.2vw,26px);margin:0 0 -.1em .05em}}
.cover h1{{font-family:var(--disp);font-size:clamp(56px,11vw,150px);line-height:.9;margin:0;letter-spacing:-.04em;font-weight:800;font-variation-settings:"opsz" 96}}
.cover .sub{{font-family:var(--text);font-size:clamp(15px,1.5vw,20px);margin:12px 0 0 .05em;font-style:italic;font-weight:300}}
.cover .line{{display:flex;flex-wrap:wrap;gap:8px 32px;margin-top:24px;font-family:var(--ui);font-size:13px;letter-spacing:.06em;color:var(--mute)}}
.painting{{margin:clamp(28px,4vw,48px) auto 0;width:fit-content;max-width:100%;border:1px solid var(--rule);background:var(--cream);padding:clamp(10px,1.4vw,18px)}}
.painting .mat{{border:1px solid var(--rule)}}
.painting img{{display:block;width:auto;max-width:100%;height:auto;max-height:96vh}}
.painting figcaption{{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;font-family:var(--ui);font-size:12px;letter-spacing:.06em;color:var(--mute);padding:12px 2px 0}}
/* front matter */
.front{{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:48px clamp(32px,6vw,96px);padding-block:clamp(40px,7vw,96px);border-bottom:1px solid var(--rule)}}
.front h2{{font-family:var(--disp);font-size:clamp(32px,4vw,52px);font-weight:800;margin:0 0 20px;letter-spacing:-.03em}}
.index{{list-style:none;margin:0;padding:0;border-top:1px solid var(--rule)}}
.index a{{display:flex;justify-content:space-between;gap:16px;align-items:baseline;padding:14px 0;border-bottom:1px solid var(--rule);color:inherit;text-decoration:none;font-family:var(--text);font-style:italic;font-size:22px;line-height:1.25;font-weight:300}}
.index a:hover .t,.index a:focus-visible .t{{color:var(--accent)}}
.index .pg{{font-family:var(--ui);font-size:13px;color:var(--mute);font-variant-numeric:tabular-nums}}
.uhjf{{padding:clamp(16px,2.2vw,28px);background:#2f5a2a url(img/motif-uhj.jpg) center/cover;border:1px solid var(--rule);box-shadow:inset 0 0 0 1px rgba(0,0,0,.08)}}
.uhj{{margin:0;background:var(--tabon-white,#fff);border:1px solid var(--rule);padding:clamp(20px,2.6vw,32px) clamp(22px,2.8vw,36px)}}
.uhj p{{font-family:var(--text);font-style:italic;font-weight:400;font-size:clamp(24px,2.6vw,32px);line-height:1.28;margin:0 0 14px;text-wrap:pretty;color:var(--ink)}}
.uhj cite{{font-style:normal;font-family:var(--ui);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);font-weight:600}}
.about{{margin-top:28px;color:var(--mute);font-size:15.5px;line-height:1.6}}
.about b{{color:var(--ink);font-weight:700}}
/* stories */
.story{{padding-block:clamp(48px,8vw,112px) 0}}
.plate{{margin:0 0 clamp(28px,4vw,48px);background:var(--cream);border:1px solid var(--rule)}}
.plate img{{display:block;width:100%;height:auto;max-height:88vh;object-fit:contain;background:var(--cream)}}
.plate.capped{{max-width:var(--aw);margin-left:auto;margin-right:auto}}
/* typographic overlay recapturing the print opener */
.plate:has(.ovw){{background:#1a0f0b;border-color:#1a0f0b}}
.ovw{{position:relative;width:min(100%,calc(92vh * var(--ar)));margin:0 auto;container-type:inline-size}}
.ovw img{{max-height:none;background:none}}
.ov{{position:absolute;inset:0;color:#fff;pointer-events:none;text-shadow:0 1px 2px rgba(20,6,2,.35),0 6px 28px rgba(30,10,5,.55)}}
.ov span{{position:absolute;white-space:nowrap;line-height:.9}}
.ov .t1{{left:2%;top:5%;font-family:"Bodoni Moda",serif;font-weight:500;font-size:20cqw;letter-spacing:-.03em;font-variation-settings:"opsz" 48}}
.ov .t1 i{{font-style:italic}}
.ov .t2{{left:36%;top:17%;font-family:"Pinyon Script",cursive;font-size:17cqw}}
.ov .t3{{right:8%;top:29%;font-family:"Bodoni Moda",serif;font-weight:500;font-size:15.5cqw;letter-spacing:-.035em;font-variation-settings:"opsz" 48}}
.ov .byl{{left:9%;top:58%;font-family:"Bodoni Moda",serif;font-weight:600;font-size:3.2cqw;letter-spacing:.02em;font-variation-settings:"opsz" 11}}
.ov .sub{{right:1.5%;top:50%;font-family:"Bodoni Moda",serif;font-style:italic;font-weight:400;font-size:4.8cqw;line-height:1.12;text-align:right;white-space:normal;width:48%;font-variation-settings:"opsz" 18}}
@media (prefers-reduced-motion:no-preference){{.ov span{{animation:ovin 1.6s cubic-bezier(.2,.7,.2,1) both}} .ov .t2{{animation-delay:.25s}} .ov .t3{{animation-delay:.45s}} .ov .byl,.ov .sub{{animation-delay:.7s}}}}
@keyframes ovin{{from{{opacity:0;filter:blur(6px)}}}}

.plate.bare{{background:transparent;border:0}}
.plate.bare img{{max-height:none;object-fit:contain;max-width:1000px}}
.plate.bare figcaption{{padding-left:0}}
.plate.comic{{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--rule)}}
.plate.comic img{{max-height:none;background:#fff}}
.plate.comic figcaption{{grid-column:1/-1;background:var(--cream)}}
.plate figcaption{{font-family:var(--ui);font-size:12px;letter-spacing:.06em;color:var(--mute);padding:10px 14px}}
.numeral{{font-family:var(--disp);font-weight:800;font-size:clamp(160px,28vw,360px);line-height:.8;color:var(--accent);margin:0 0 .05em -.03em;letter-spacing:-.06em}}
/* article grid: a 3-column field. Margin column at left holds kicker, byline, pages; the headline spans the field; prose sits in the middle column with air on both sides; pull quotes hang into the left margin, photographs span margin and text. */
.story{{display:grid;grid-template-columns:minmax(200px,26ch) minmax(0,64ch) minmax(0,1fr);column-gap:clamp(24px,4vw,56px)}}
.story>.plate,.story>.numeral{{grid-column:1/-1}}
.shead{{grid-column:1/-1;margin:0 0 clamp(40px,6vw,88px);position:relative}}
.shead>*{{position:relative;z-index:1}}
.torn{{position:absolute;inset:-14% -2% -10% 46%;z-index:0!important;pointer-events:none;opacity:.5}}
.shead{{pointer-events:auto}}
.torn i{{position:absolute;animation:settle 20s ease-in-out infinite alternate}}
.torn i:nth-child(1){{right:6%;top:-6%;width:44%;height:70%;background:var(--a);clip-path:polygon(4% 0,96% 6%,100% 60%,88% 100%,10% 94%,0 40%);animation-delay:-3s}}
.torn i:nth-child(2){{right:30%;top:30%;width:38%;height:60%;background:var(--b);clip-path:polygon(0 12%,80% 0,100% 50%,92% 100%,18% 96%,4% 60%);animation-delay:-9s;animation-duration:24s}}
.torn i:nth-child(3){{right:0;bottom:-4%;width:26%;height:46%;background:var(--c);clip-path:polygon(10% 0,100% 10%,90% 100%,0 86%);animation-delay:-14s}}
.torn i:nth-child(4){{right:48%;top:0;width:16%;aspect-ratio:1;height:auto;background:var(--d);border-radius:50%;animation-duration:16s}}
/* 1: tall strip and two discs */
.torn[data-v="1"] i:nth-child(1){{right:14%;top:-14%;width:18%;height:120%;clip-path:polygon(0 2%,100% 0,92% 100%,8% 96%)}}
.torn[data-v="1"] i:nth-child(2){{right:36%;top:36%;width:30%;aspect-ratio:1;height:auto;clip-path:none;border-radius:50%}}
.torn[data-v="1"] i:nth-child(3){{right:-4%;top:10%;width:22%;height:40%;clip-path:polygon(0 0,100% 12%,86% 100%,6% 80%)}}
.torn[data-v="1"] i:nth-child(4){{right:54%;top:-4%;width:10%}}
/* 2: three horizontal tears */
.torn[data-v="2"] i:nth-child(1){{right:0;top:4%;width:58%;height:26%;clip-path:polygon(0 20%,100% 0,98% 90%,4% 100%)}}
.torn[data-v="2"] i:nth-child(2){{right:10%;top:38%;width:46%;height:24%;clip-path:polygon(2% 0,100% 14%,94% 100%,0 86%)}}
.torn[data-v="2"] i:nth-child(3){{right:4%;top:70%;width:52%;height:24%;clip-path:polygon(0 0,96% 8%,100% 100%,6% 90%)}}
.torn[data-v="2"] i:nth-child(4){{right:60%;top:50%;width:12%}}
/* 3: one large disc, a wedge */
.torn[data-v="3"] i:nth-child(1){{right:2%;top:-10%;width:50%;aspect-ratio:1;height:auto;clip-path:none;border-radius:50%}}
.torn[data-v="3"] i:nth-child(2){{right:40%;top:50%;width:34%;height:50%;clip-path:polygon(0 100%,100% 0,100% 100%)}}
.torn[data-v="3"] i:nth-child(3){{right:-2%;bottom:0;width:20%;height:34%;clip-path:polygon(10% 0,100% 10%,90% 100%,0 86%)}}
.torn[data-v="3"] i:nth-child(4){{display:none}}
/* 4: stacked squares, offset */
.torn[data-v="4"] i:nth-child(1){{right:8%;top:0;width:30%;aspect-ratio:1;height:auto;clip-path:polygon(2% 4%,100% 0,96% 100%,0 94%)}}
.torn[data-v="4"] i:nth-child(2){{right:24%;top:28%;width:30%;aspect-ratio:1;height:auto;clip-path:polygon(0 0,98% 6%,100% 96%,4% 100%)}}
.torn[data-v="4"] i:nth-child(3){{right:0;top:52%;width:30%;aspect-ratio:1;height:auto;clip-path:polygon(4% 0,100% 2%,94% 100%,0 96%)}}
.torn[data-v="4"] i:nth-child(4){{right:56%;top:10%;width:10%}}
/* 5: a sun and rays */
.torn[data-v="5"] i:nth-child(1){{right:20%;top:6%;width:34%;aspect-ratio:1;height:auto;clip-path:none;border-radius:50%}}
.torn[data-v="5"] i:nth-child(2){{right:0;top:-10%;width:14%;height:120%;clip-path:polygon(40% 0,60% 0,100% 100%,0 100%)}}
.torn[data-v="5"] i:nth-child(3){{right:50%;top:40%;width:26%;height:50%;clip-path:polygon(0 100%,50% 0,100% 100%)}}
.torn[data-v="5"] i:nth-child(4){{display:none}}
@keyframes settle{{from{{transform:translate(0,0) rotate(0)}}to{{transform:translate(-1.5%,1.5%) rotate(1.5deg)}}}}
.torn i{{transition:transform .7s cubic-bezier(.2,.8,.2,1)}}
.shead.hov .torn i{{animation:none}}
.shead h2{{font-family:var(--disp);font-size:clamp(50px,9vw,104px);line-height:.92;font-weight:700;letter-spacing:-.035em;font-variation-settings:"opsz" 96;hyphens:none;overflow-wrap:normal;margin:0 0 22px;text-wrap:balance;max-width:14ch}}
.dek{{font-family:var(--disp);font-weight:300;font-size:clamp(20px,2vw,28px);margin:0;color:var(--mute);max-width:34ch}}
.margin{{grid-column:1;grid-row:3;font-family:var(--ui);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--mute);line-height:1.6;align-self:start}}
.margin p{{margin:0}}
.kicker{{color:var(--accent);font-weight:600;margin-bottom:10px!important}}
.by::before{{content:"By ";}}
.by.nob::before{{content:""}}
.pp{{margin-top:10px!important;font-variant-numeric:tabular-nums}}
/* listen: launcher in the margin, player docked at the foot */
.listen{{margin-top:22px;font:inherit;font-family:var(--ui);text-transform:none;letter-spacing:0;color:var(--ink);background:none;border:0;padding:0;cursor:pointer;text-align:left;display:grid;grid-template-columns:44px 1fr;gap:2px 12px;align-items:center;max-width:26ch}}
.listen .lp{{grid-row:1/4;width:44px;height:44px;border-radius:50%;background:var(--accent);color:#fff;display:grid;place-items:center;transition:transform .15s}}
.listen:hover .lp{{transform:scale(1.06)}}
.listen svg{{width:16px;height:16px;fill:currentColor}} .listen .ic-pause{{display:none}}
.listen.playing .ic-play{{display:none}} .listen.playing .ic-pause{{display:block}}
.listen:focus-visible{{outline:2px solid var(--accent);outline-offset:4px;border-radius:24px}}
.listen .lt{{font-size:13.5px;font-weight:600;line-height:1.2}}
.listen .ltime,.listen .lby{{font-size:12px;color:var(--mute);font-variant-numeric:tabular-nums}}
.listen.na .lp{{background:color-mix(in oklab,var(--accent) 45%,var(--rule))}}
@media (max-width:980px){{.listen{{margin:6px 0 0;max-width:none}}}}
.dock{{position:fixed;left:0;right:0;bottom:0;z-index:8;padding:0 max(12px,env(safe-area-inset-right,0px)) max(10px,env(safe-area-inset-bottom,0px)) max(12px,env(safe-area-inset-left,0px));pointer-events:none;font-family:var(--ui);color:var(--ink)}}
.dock[hidden]{{display:block;visibility:hidden}}
.dock .dk{{pointer-events:auto;max-width:1120px;margin:0 auto;display:flex;align-items:center;gap:6px 10px;padding:8px 10px 8px 8px;background:color-mix(in oklab,var(--bar) 95%,transparent);backdrop-filter:blur(12px);border:1px solid var(--barrule);border-top:2px solid var(--accent);border-radius:14px;box-shadow:0 8px 30px rgba(20,16,10,.14);transform:translateY(calc(100% + 24px));transition:transform .35s cubic-bezier(.2,.8,.2,1)}}
.dock.on .dk{{transform:none}}
.dock button{{border:0;background:none;color:inherit;cursor:pointer;padding:0;display:grid;place-items:center;flex:none}}
.dock button:focus-visible,.dock .dbar:focus-visible,.dock .dt:focus-visible{{outline:2px solid var(--accent);outline-offset:2px;border-radius:8px}}
.dock svg{{fill:currentColor}}
.dock .dp{{width:42px;height:42px;border-radius:50%;background:var(--accent);color:#fff}} .dock .dp svg{{width:16px;height:16px}}
.dock .ic-play{{display:none}} .dock.paused .ic-play{{display:block}} .dock.paused .ic-pause{{display:none}}
.dock .ds{{min-width:42px;height:30px;font:600 12.5px var(--ui);border:1px solid var(--rule)!important;border-radius:999px;font-variant-numeric:tabular-nums}}
.dock .dj{{width:34px;height:34px;border-radius:50%}} .dock .dj:hover,.dock .dx:hover,.dock .ds:hover{{background:var(--tabon)}}
.dock .dj svg{{width:24px;height:24px}} .dock .dj text{{font:700 6.5px var(--ui);fill:currentColor}}
.dock .dt{{flex:0 1 auto;min-width:0;font-size:13.5px;font-weight:600;color:inherit;text-decoration:none;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-left:4px}}
.dock .dt:hover{{color:var(--accent)}}
.dock .dtime{{flex:none;font-size:12px;color:var(--mute);font-variant-numeric:tabular-nums}}
.dock .dbar{{flex:1 1 120px;position:relative;height:22px;cursor:pointer;min-width:80px}}
.dock .dbar::before{{content:"";position:absolute;left:0;right:0;top:9px;height:4px;border-radius:2px;background:var(--rule)}}
.dock .dbar i{{position:absolute;left:0;top:9px;height:4px;border-radius:2px;width:var(--p,0%);background:var(--accent)}}
.dock .dbar b{{position:absolute;top:5px;left:calc(var(--p,0%) - 6px);width:12px;height:12px;border-radius:50%;background:var(--accent);box-shadow:0 0 0 3px var(--bar)}}
.dock .dx{{width:34px;height:34px;border-radius:50%}} .dock .dx svg{{width:14px;height:14px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round}}
html.docked body{{padding-bottom:84px}}
.dock.na .dp,.dock.na .ds,.dock.na .dj,.dock.na .dbar{{opacity:.35;pointer-events:none}} .dock.na .dbar b{{display:none}} .dock.na .dtime{{font-style:italic}}
@media (max-width:700px){{
 .dock .dk{{flex-wrap:wrap;padding:8px 8px 6px}}
 .dock .dt{{order:-1;flex:1 1 100%;margin:0 0 2px 4px;font-size:13px}}
 .dock .dbar{{order:9;flex:1 1 100%}}
 .dock .dtime{{margin-left:auto}}
 html.docked body{{padding-bottom:128px}}
}}
@media (prefers-reduced-motion:reduce){{.dock .dk{{transition:none}}}}
.prose{{grid-column:1/-1;display:grid;grid-template-columns:subgrid;column-gap:inherit;font-size:19.5px;line-height:1.6;font-variation-settings:"opsz" 18}}
.prose>*{{grid-column:2;min-width:0}}
.prose p{{margin:0 0 1.25em;text-wrap:pretty}}
.prose p.first{{font-size:1.1em;line-height:1.5}}
#comic .prose p{{font-size:1.1em;line-height:1.5}}
.prose p.first::first-letter{{font-family:var(--disp);font-weight:700;font-size:4.2em;float:left;line-height:.8;padding:.06em .1em 0 0;color:var(--accent)}}
.prose h3{{font-family:var(--ui);font-weight:600;font-size:13px;letter-spacing:.14em;text-transform:uppercase;margin:3.2em 0 1em;color:var(--accent);padding-top:1.2em;border-top:1px solid var(--rule)}}
.prose .pull{{grid-column:1;grid-row:span 2;margin:.4em 0 2em;padding:0 0 0 18px;border-left:3px solid var(--accent);align-self:start;max-width:26ch}}
.prose .pull p{{font-family:var(--disp);font-weight:500;font-size:clamp(20px,1.9vw,26px);line-height:1.24;letter-spacing:-.015em;margin:0 0 10px;text-wrap:pretty}}
.prose .pull cite{{font-style:normal;font-family:var(--ui);font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--mute)}}
.prose .photo{{grid-column:1/-1;margin:2.4em 0;display:grid;grid-template-columns:subgrid;column-gap:inherit;align-items:end}}
.prose .photo>img{{grid-column:1/-1}}
.prose .photo>figcaption{{grid-column:1;grid-row:2;margin-top:10px}}
.prose .photo.small{{grid-column:2;display:block;max-width:var(--w)}}
.prose .photo.small>figcaption{{margin-top:10px}}
.prose .photo.pair{{grid-column:1/-1;grid-template-columns:1fr 1fr;gap:20px;align-items:start}}
.prose .photo.pair>div{{grid-column:auto}}
.prose .photo.pair.capped{{grid-column:2/4}}
.prose .photo.pair>div{{min-width:0}}
@media (max-width:640px){{.prose .photo.pair{{grid-template-columns:1fr}}}}
.prose .photo img{{display:block;width:100%;height:auto;border:1px solid var(--rule)}}
.prose .photo figcaption{{font-family:var(--ui);font-size:12.5px;letter-spacing:.02em;color:var(--mute);margin-top:8px;line-height:1.5}}
.prose .note{{font-family:var(--ui);font-size:15px;color:var(--mute);border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:14px 0;margin:2em 0}}
.prose .qa{{font-family:var(--disp);font-weight:700;font-size:20px;letter-spacing:-.01em;margin-top:1.8em}}
.prose .ans b{{font-family:var(--ui);font-weight:600;font-size:14px;letter-spacing:.06em;text-transform:uppercase;color:var(--accent);margin-right:.4em}}
/* voices */
.voice{{background:var(--band);color:#f7f2ea;margin-top:clamp(48px,8vw,112px)}}
.voice+.wrap .story{{padding-top:clamp(48px,8vw,112px)}}
.vin{{max-width:1120px;margin:0 auto;{GUT}padding-block:clamp(40px,6vw,80px)}}
.voice p{{font-family:var(--text);font-weight:600;font-size:clamp(24px,2.8vw,38px);line-height:1.36;letter-spacing:-.01em;max-width:30ch;margin:0 0 26px;text-wrap:pretty;font-variation-settings:"opsz" 72;position:relative;padding-left:clamp(28px,4vw,56px)}}
.voice p::before{{content:"\u201C";position:absolute;left:0;top:-.08em;font-family:var(--text);font-weight:600;font-size:2.4em;line-height:1;opacity:.35}}
.voice cite{{display:flex;align-items:center;gap:12px;font-style:normal;font-family:var(--ui);font-size:12px;letter-spacing:.14em;text-transform:uppercase;font-weight:600;opacity:.85;padding-left:clamp(28px,4vw,56px)}}
.voice cite::before{{content:"";width:28px;height:2px;background:currentColor;opacity:.7}}
.colophon{{padding-block:clamp(48px,8vw,96px);font-family:var(--ui);font-size:13px;color:var(--mute);max-width:60ch;line-height:1.6;border-top:1px solid var(--rule);margin-top:clamp(48px,8vw,112px)}}
a:focus-visible{{outline:2px solid var(--accent);outline-offset:3px}}
@media (max-width:980px){{
  .story{{grid-template-columns:minmax(0,1fr)}}
  .shead,.margin,.prose{{grid-column:1}}
  .margin{{grid-row:auto;position:static;display:flex;gap:18px;flex-wrap:wrap;margin-bottom:28px}}
  .shead h2{{font-size:clamp(46px,12.5vw,76px);line-height:.94;max-width:none}}
  .margin .kicker,.margin .pp{{margin:0!important}}
  .prose{{display:block}}
  .prose .pull{{margin:1.6em 0}}
  .prose .photo{{display:block}}
  .prose .photo.pair{{display:grid;grid-template-columns:1fr 1fr}}

  .front{{grid-template-columns:1fr}}
  .prose .pull{{margin-left:0}}
  .plate.comic{{grid-template-columns:1fr}}
}}
</style>
<div class="head{" member" if member else ""}"><div class="in"><a class="brand" href="#top"><span class="bn"><svg class="star" viewBox="0 0 48 48" aria-hidden="true"><defs><linearGradient id="star-g" x1="26" y1="1" x2="26" y2="48.4" gradientUnits="userSpaceOnUse"><stop stop-color="#73E4C4"/><stop offset=".19" stop-color="#54ADA5"/><stop offset=".47" stop-color="#357686"/><stop offset=".79" stop-color="#265B76"/><stop offset="1" stop-color="#255875"/></linearGradient></defs><path d="M22.0121 12.0305L23.9836 8.64366L25.9552 12.0305L27.4999 14.6878L30.3894 13.6493L34.0717 12.3258L33.4077 16.1878L32.8894 19.2183L35.7688 20.2839L39.4375 21.6414L36.4531 24.1731L34.1089 26.1584L35.6333 28.8292L37.5744 32.233L33.6618 32.25L30.5927 32.2636L30.0473 35.2907L29.3529 39.1459L26.3447 36.6414L23.9836 34.6731L21.6225 36.6414L18.6144 39.1459L17.92 35.2907L17.3746 32.2636L14.3055 32.25L10.3929 32.233L12.334 28.8292L13.8583 26.1584L11.5142 24.1731L8.52977 21.6414L12.2018 20.2839L15.0812 19.2183L14.5629 16.1878L13.899 12.3258L17.5812 13.6493L20.4708 14.6878L22.0155 12.0305H22.0121ZM18.523 9.3733L8.32652 5.70475L10.1626 16.4016L0 20.1584L8.26894 27.1697L2.89294 36.5905L13.7262 36.638L15.6537 47.3179L23.9836 40.3778L32.3136 47.3179L34.241 36.638L45.0743 36.5905L39.6983 27.1697L47.9673 20.1584L37.8047 16.4016L39.6408 5.70475L29.4443 9.3733L23.9803 0L18.523 9.3767V9.3733Z" fill="url(#star-g)"/></svg>The American Bahá'í</span><small>{SUB}</small></a><nav aria-label="Features">{head}</nav><span class="ind" aria-hidden="true"></span></div></div>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><g id="usmap"><path d="{USMAP["nation"]}" class="cland"/><path d="{USMAP["states"]}" class="cstate"/></g></defs></svg>
<div class="popup" role="dialog" aria-modal="false" aria-live="polite" hidden><button type="button" aria-label="Close">×</button><b></b><p></p></div>
<div class="terraces" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
<header class="cover wrap" id="top">
  <div class="mast">
    <svg class="stroke" viewBox="0 0 720 90" preserveAspectRatio="none" aria-hidden="true"><path d="M20 55 C 160 20, 300 80, 440 45 S 640 30, 700 50"/><path d="M40 70 C 200 40, 380 90, 560 55 S 660 50, 690 62"/></svg>
    <p class="the">The</p>
    <h1>American Bahá'í</h1>
    <p class="sub">{SUB}</p>
    <div class="line"><span>{esc(ISSUE["date"])}</span><span>{"Full edition" if member else "Curated edition"}</span><span>legacy: <a href="https://{esc(ISSUE["url"])}">{esc(ISSUE["url"])}</a></span>{'<span><a href="../">Curated edition</a></span>' if member else ''}</div>
  </div>
  <figure class="painting"><div class="mat"><img src="img/cover-paint.jpg" alt="Oil painting by Juliet Bogan: two figures in a flowering meadow look toward terraced green farmland and ochre mountains under a pale sky"></div><figcaption><span>Cover painting by {esc(ISSUE["cover_artist"])}</span><span>Oil on canvas</span></figcaption></figure>
</header>
<main>
<div class="wrap">
<section class="front">
  <div>
    <h2>Features</h2>
    <ol class="index">{index}</ol>
    <p class="about"><b>About this issue.</b> {esc(ISSUE["about"])}</p>
    {dindex}
  </div>
  <div class="epi">
    <div class="uhjf"><blockquote class="uhj"><p>“{esc(ISSUE["epigraph"])}”</p>
    <cite>{esc(ISSUE["epigraph_src"])}</cite></blockquote></div>
    <p class="about"><b>About the cover.</b> “{esc(ISSUE["cover_note"])}” <i>Juliet Bogan</i></p>
  </div>
</section>
{lead}
{"".join(secs)}
{depts}
<footer class="colophon">{esc(ISSUE["publisher"])}</footer>
</div>
</main>
{DOCK}
<script>
(function(){{ /* trim the empty bands above and below each diagram */
  [].forEach.call(document.querySelectorAll('.chart>svg[viewBox]'),function(svg){{
    try{{var vb=svg.viewBox.baseVal,bb=svg.getBBox();if(!bb.height)return;var y=Math.max(vb.y,bb.y-6),h=Math.min(vb.y+vb.height,bb.y+bb.height+6)-y;
    if(vb.height-h>8)svg.setAttribute('viewBox',vb.x+' '+y+' '+vb.width+' '+h);}}catch(e){{}}
  }});
}})();
(function(){{
  var links=[].slice.call(document.querySelectorAll('.head nav a'));
  var secs=[].slice.call(document.querySelectorAll('article.story'));
  var ind=document.querySelector('.head .ind'), inn=document.querySelector('.head .in');
  var cur=null;
  function place(a){{if(!a||!ind)return;var r=a.getBoundingClientRect(),b=inn.getBoundingClientRect();ind.style.left=(r.left-b.left+inn.scrollLeft)+'px';ind.style.width=r.width+'px';}}
  var alias={{abiding:'huquq',fund:'huquq',rhythm:'huquq',books:'huquq',notices:'huquq'}};
  function tabFor(id){{return links.filter(function(l){{return l.getAttribute('href')==='#'+(alias[id]||id)}})[0];}}
  function progress(){{if(!cur)return;var a=tabFor(cur.id);if(!a)return;
    var r=cur.getBoundingClientRect();var top=r.top+scrollY, h=r.height;var p=(scrollY+innerHeight*0.4-top)/h;p=Math.max(0,Math.min(1,p));a.style.setProperty('--p',(p*100).toFixed(1)+'%');}}
  if('IntersectionObserver' in window){{
    var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(!e.isIntersecting)return;cur=e.target;
      var t=tabFor(e.target.id);links.forEach(function(a){{var on=a===t;a.classList.toggle('on',on);if(on)place(a);}});progress();}});}},{{rootMargin:'-30% 0px -60% 0px'}});
    secs.forEach(function(x){{io.observe(x)}});
  }}
  addEventListener('scroll',progress,{{passive:true}}); addEventListener('resize',function(){{place(document.querySelector('.head nav a.on'))}});
  if(matchMedia('(prefers-reduced-motion: reduce)').matches||!matchMedia('(hover: hover)').matches)return;
  [].slice.call(document.querySelectorAll('.shead')).forEach(function(h){{
    var pieces=[].slice.call(h.querySelectorAll('.torn i')); if(!pieces.length)return;
    h.addEventListener('mousemove',function(e){{h.classList.add('hov');var b=h.getBoundingClientRect();var cx=(e.clientX-b.left)/b.width-.5, cy=(e.clientY-b.top)/b.height-.5;
      pieces.forEach(function(p,k){{var d=(k%2?1:-1)*(36+k*14);p.style.transform='translate('+(-cx*d)+'px,'+(-cy*d)+'px) rotate('+(cx*(k%2?8:-8))+'deg)';}});}});
    h.addEventListener('mouseleave',function(){{h.classList.remove('hov');pieces.forEach(function(p){{p.style.transform=''}});}});
  }});
}})();

(function(){{
  var box=document.querySelector('.popup'); if(!box)return;
  var bt=box.querySelector('b'), bp=box.querySelector('p'), cur=null, pinned=false;
  function place(el){{var r=el.getBoundingClientRect(),w=box.offsetWidth,h=box.offsetHeight,x=r.left+r.width/2-w/2,y=r.top-h-12;
    if(y<70)y=r.bottom+12; x=Math.max(16,Math.min(x,innerWidth-w-16)); y=Math.min(y,innerHeight-h-16); box.style.left=x+'px'; box.style.top=y+'px';}}
  function show(el,pin){{cur=el;pinned=!!pin;bt.textContent=el.dataset.pt;bp.textContent=el.dataset.pb;
    var art=el.closest('article'); box.style.setProperty('--pa', art?getComputedStyle(art).getPropertyValue('--accent'):'');
    box.hidden=false; place(el); requestAnimationFrame(function(){{box.classList.add('show')}});}}
  function hide(){{box.classList.remove('show');cur=null;pinned=false;setTimeout(function(){{if(!cur)box.hidden=true}},160);}}
  var hov=matchMedia('(hover: hover)').matches;
  document.addEventListener('mouseover',function(e){{if(!hov||pinned)return;var el=e.target.closest('[data-pb]');if(el&&el!==cur)show(el);}});
  document.addEventListener('mouseout',function(e){{if(!hov||pinned)return;var el=e.target.closest('[data-pb]');if(el&&!el.contains(e.relatedTarget)&&!box.contains(e.relatedTarget))hide();}});
  document.addEventListener('click',function(e){{var el=e.target.closest('[data-pb]');if(el){{e.preventDefault();(cur===el&&pinned)?hide():show(el,true);return;}}
    if(e.target.closest('.popup button')||!box.contains(e.target))hide();}});
  document.addEventListener('keydown',function(e){{if(e.key==='Escape'&&cur){{var c=cur;hide();c.focus();return;}}
    var el=e.target.closest&&e.target.closest('[data-pb]');if(el&&(e.key==='Enter'||e.key===' ')){{e.preventDefault();show(el,true);}}}});
  document.addEventListener('focusin',function(e){{var el=e.target.closest&&e.target.closest('[data-pb]');if(el&&!pinned)show(el);}});
  addEventListener('scroll',function(){{if(cur)place(cur)}},{{passive:true}}); addEventListener('resize',function(){{if(cur)place(cur)}});
}})();

(function(){{
  var L=[].slice.call(document.querySelectorAll('.listen')); if(!L.length)return;
  var dock=document.getElementById('dock'), dk=dock.querySelector('.dk'), dp=dock.querySelector('.dp'), ds=dock.querySelector('.ds'), dt=dock.querySelector('.dt'), dtime=dock.querySelector('.dtime'), bar=dock.querySelector('.dbar'), dx=dock.querySelector('.dx');
  var speeds=[1,1.25,1.5,2,0.85], si=0, cur=null;
  var fmt=function(t){{t=Math.max(0,Math.floor(t||0));return Math.floor(t/60)+':'+String(t%60).padStart(2,'0');}};
  function sync(){{if(!cur)return;if(cur.na){{bar.style.setProperty('--p','0%');dtime.textContent='Audio not yet added';return;}}var au=cur.au,p=au.duration?au.currentTime/au.duration*100:0;bar.style.setProperty('--p',p+'%');bar.setAttribute('aria-valuenow',Math.round(p));bar.setAttribute('aria-valuetext',fmt(au.currentTime)+' of '+fmt(au.duration));dtime.textContent=fmt(au.currentTime)+' / '+fmt(au.duration);}}
  function state(){{var pl=cur&&!cur.na&&!cur.au.paused;dock.classList.toggle('paused',!pl);dp.setAttribute('aria-label',pl?'Pause':'Play');L.forEach(function(x){{x.classList.toggle('playing',!!(cur&&x===cur.el&&pl));}});}}
  function open(p){{
    if(cur&&cur!==p)cur.au.pause();
    cur=p; dock.classList.toggle('na',!!p.na); var st=getComputedStyle(p.el).getPropertyValue('--accent'); if(st)dock.style.setProperty('--accent',st.trim());
    dt.textContent=p.el.dataset.title; dt.href='#'+(p.el.closest('.story')||{{}}).id;
    p.au.playbackRate=speeds[si];
    dock.hidden=false; document.documentElement.classList.add('docked'); requestAnimationFrame(function(){{dock.classList.add('on');}});
    sync(); state();
  }}
  L.forEach(function(el){{
    var au=new Audio(); au.preload='none'; var p={{el:el,au:au}}, probed=false, t=el.querySelector('.ltime');
    function probe(){{if(probed)return;probed=true;au.src=el.dataset.src;au.preload='metadata';au.load();}}
    au.addEventListener('error',function(){{p.na=true;au.pause();el.classList.add('na');t.textContent='Audio not yet added';if(cur===p){{dock.classList.add('na');sync();state();}}}});
    au.addEventListener('loadedmetadata',function(){{t.textContent=fmt(au.duration);if(cur===p)sync();}});
    au.addEventListener('timeupdate',function(){{if(cur===p)sync();}});
    ['play','pause'].forEach(function(e){{au.addEventListener(e,state);}});
    au.addEventListener('ended',function(){{au.currentTime=0;state();}});
    el.addEventListener('click',function(){{probe();if(p.na){{open(p);return;}}if(cur===p&&!au.paused){{au.pause();return;}}open(p);var r=au.play();if(r&&r.catch)r.catch(function(){{}});}});
    if('IntersectionObserver' in window){{var io=new IntersectionObserver(function(es){{if(es[0].isIntersecting){{probe();io.disconnect();}}}},{{rootMargin:'400px'}});io.observe(el);}}else probe();
  }});
  function close(){{if(cur)cur.au.pause();dock.classList.remove('on');document.documentElement.classList.remove('docked');setTimeout(function(){{if(!dock.classList.contains('on'))dock.hidden=true;}},360);state();}}
  dp.addEventListener('click',function(){{if(!cur)return;if(cur.au.paused){{var r=cur.au.play();if(r&&r.catch)r.catch(function(){{}});}}else cur.au.pause();}});
  ds.addEventListener('click',function(){{si=(si+1)%speeds.length;ds.textContent=speeds[si]+'×';if(cur)cur.au.playbackRate=speeds[si];}});
  [].forEach.call(dock.querySelectorAll('.dj'),function(b){{b.addEventListener('click',function(){{if(!cur||!cur.au.duration)return;cur.au.currentTime=Math.max(0,Math.min(cur.au.duration,cur.au.currentTime+ +b.dataset.j));sync();}});}});
  dx.addEventListener('click',close);
  function seek(x){{if(!cur||!cur.au.duration)return;var r=bar.getBoundingClientRect();cur.au.currentTime=Math.max(0,Math.min(1,(x-r.left)/r.width))*cur.au.duration;sync();}}
  var drag=false;
  bar.addEventListener('pointerdown',function(e){{drag=true;bar.setPointerCapture(e.pointerId);seek(e.clientX);}});
  bar.addEventListener('pointermove',function(e){{if(drag)seek(e.clientX);}});
  bar.addEventListener('pointerup',function(){{drag=false;}});
  bar.addEventListener('keydown',function(e){{if(!cur||!cur.au.duration)return;var d={{ArrowRight:10,ArrowLeft:-10,Home:-1e9,End:1e9}}[e.key];if(d===undefined)return;e.preventDefault();cur.au.currentTime=Math.max(0,Math.min(cur.au.duration,cur.au.currentTime+d));sync();}});
  document.addEventListener('keydown',function(e){{if(e.key==='Escape'&&dock.classList.contains('on')&&dock.contains(document.activeElement))close();}});
}})();
</script>
'''

# ------------------------------------------------------------------ PLATES (alternate, kept under alt/)
def build_plates():
    chapters = []
    for i, a in enumerate(ARTICLES):
        n = i + 1
        if a.get("art"):
            if a["slug"] == "comic":
                plate = f'<div class="img two"><img src="img/{a["art"]}" alt="{esc(a["art_alt"])}"><img src="img/{a["art2"]}" alt="{esc(a["art2_alt"])}"></div>'
            else:
                plate = f'<div class="img{" bare" if a.get("art_transparent") else ""}{" capped" if a.get("art_width") else ""}" style="--aw:{a.get("art_width",0)}px"><img src="img/{a["art"]}" alt="{esc(a["art_alt"])}"></div>'
        else:
            plate = '<div class="img type"><span>50</span></div>'
        dek = f'<p class="dek">{esc(a["dek"])}</p>' if a.get("dek") else ""
        by = f'<p class="by">{esc(a["byline"])}</p>' if a.get("byline") else ""
        pal = {"gregory":("#f26b2b","#2448c8","#f05a7e","#f3c623"),"newyorkers":("#2448c8","#f05a7e","#f3c623","#5f8f3a"),"twoartists":("#b07a4a","#e9a21f","#2f6a4a","#f26b2b"),"abs":("#c9462c","#1b5e6b","#e9a21f","#2448c8"),"endeavor":("#e9a21f","#1b5e6b","#9ec3cc","#f26b2b"),"comic":("#f3c623","#2448c8","#f26b2b","#5f8f3a")}[a["slug"]]
        torn = f'<div class="torn" aria-hidden="true" style="--a:{pal[0]};--b:{pal[1]};--c:{pal[2]};--d:{pal[3]}"><i></i><i></i><i></i><i></i></div>'
        chapters.append(f'''<section class="chapter" id="{a["slug"]}">
  <div class="plate">
    {plate}
    <div class="cap"><span class="n">Plate {n}</span><span>{esc(a["art_credit"] or "Set in type")}</span><span>pp. {a["pages"]}</span></div>
  </div>
  <header class="chead">{torn}
    <p class="kicker">{esc(a["kicker"])}</p>
    <h2>{esc(a["title"])}</h2>
    {dek}{by}
  </header>
  <div class="prose">{body_html(a["body"])}</div>
</section>''')
    nav = "".join(f'<a href="#{a["slug"]}">{esc(a["short"])}</a>' for a in ARTICLES)
    return f'''<title>{esc(ISSUE["title"])} Plates</title>
{SIDES}
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..700;1,6..96,400..700&family=Source+Serif+4:ital,opsz,wght@0,8..60,300..600;1,8..60,300..600&family=DM+Mono:wght@400;500&display=swap">
<style>
/* Layout: a dark gallery. Each feature is hung as a plate on a charcoal wall, its illustration at full width with a caption strip in mono; the headline follows in Bodoni italic, and the text runs in one lit column. One deliberate theme. */
:root{{
  --wall:#141312; --card:#1c1a18; --fg:#f1ebe0; --dim:#a69d8e; --rule:#2c2926; --gold:#d6b25e; --rose:#e8a3a3;
  --disp:"Bodoni Moda","Didot","Bodoni 72",Georgia,serif; --text:"Source Serif 4",Georgia,serif; --mono:"DM Mono","SF Mono",Menlo,monospace;
  color-scheme:dark;
}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{margin:0;background:var(--wall);color:var(--fg);font-family:var(--text);font-size:19px;line-height:1.55}}
.bar{{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:color-mix(in oklab,var(--wall) 88%,transparent);backdrop-filter:blur(10px);border-bottom:1px solid var(--rule)}}
body::before{{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--wall)}}
.bar .in{{max-width:1280px;margin:0 auto;{GUT}display:flex;gap:24px;align-items:center;min-height:52px;overflow-x:auto;scrollbar-width:none}}
.bar .brand{{font-family:var(--disp);font-size:18px;white-space:nowrap;color:var(--fg);text-decoration:none;flex:none}}
.bar nav{{display:flex;gap:26px;margin-left:auto}}
.bar nav a{{font-family:var(--disp);font-style:italic;font-size:17px;letter-spacing:.01em;color:var(--dim);text-decoration:none;white-space:nowrap;padding:6px 0;font-variation-settings:"opsz" 24}}
.bar nav a:hover,.bar nav a:focus-visible{{color:var(--gold)}}
.wrap{{max-width:1280px;margin:0 auto;{GUT}}}
/* cover */
.cover{{padding-block:clamp(40px,7vw,96px) clamp(32px,5vw,64px);display:grid;grid-template-columns:minmax(0,1fr);gap:clamp(32px,5vw,64px)}}
.cover .img{{background:var(--card);border:1px solid var(--rule);padding:clamp(12px,1.6vw,22px);width:fit-content;max-width:100%;margin:0 auto}}
.cover .img .mat{{border:1px solid color-mix(in oklab,var(--gold) 45%,transparent);padding:1px}}
.cover .img img{{display:block;width:auto;max-width:100%;height:auto;max-height:94vh}}
.cover .img figcaption{{display:flex;justify-content:space-between;font-family:var(--mono);font-size:12px;color:var(--dim);padding:12px 2px 0}}
.cover .img figcaption b{{color:var(--gold);font-weight:500}}
.cover h1{{font-family:var(--disp);font-weight:400;font-size:clamp(52px,8vw,120px);line-height:.92;letter-spacing:-.02em;margin:0 0 20px;font-variation-settings:"opsz" 96}}
.cover h1 em{{font-style:italic;font-weight:500}}
.cover .meta{{font-family:var(--mono);font-size:12px;letter-spacing:.04em;color:var(--dim);display:grid;gap:4px;margin-bottom:28px}}
.cover .epi{{font-family:var(--disp);font-style:italic;font-size:clamp(20px,2vw,26px);line-height:1.35;max-width:36ch;margin:0 0 10px;color:var(--fg)}}
.cover cite{{font-style:normal;font-family:var(--mono);font-size:12px;color:var(--dim)}}
.cover .about{{font-size:16px;color:var(--dim);max-width:52ch;margin:28px 0 0}}
.cover .about b{{color:var(--fg);font-weight:500}}
/* chapters */
.chapter{{padding-block:clamp(56px,9vw,128px) 0;border-top:1px solid var(--rule);margin-top:clamp(56px,9vw,128px)}}
.plate{{background:var(--card);border:1px solid var(--rule);padding:clamp(10px,1.5vw,20px)}}
.plate .img{{background:#000;display:grid;place-items:center}}
.plate .img img{{display:block;width:100%;height:auto;max-height:80vh;object-fit:contain}}
.plate .img.capped{{padding:clamp(16px,3vw,48px) 0}}
.plate .img.capped img{{max-width:var(--aw)}}
.plate .img.bare{{background:var(--card);padding:clamp(16px,3vw,48px)}}
.plate .img.bare img{{max-width:1100px}}
.plate .img.two{{grid-template-columns:1fr 1fr;gap:2px;background:var(--rule)}}
.plate .img.two img{{max-height:none;background:#fff}}
.plate .img.type{{min-height:40vh}}
.plate .img.type span{{font-family:var(--disp);font-style:italic;font-size:clamp(180px,32vw,440px);line-height:.8;color:var(--gold);font-variation-settings:"opsz" 96}}
.cap{{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;font-family:var(--mono);font-size:12px;color:var(--dim);padding:12px 2px 0}}
.cap .n{{color:var(--gold)}}
/* motion: torn paper behind each headline, in the story's palette, settling slowly; cover letters lean from the cursor. */
.chead{{max-width:1000px;margin:clamp(32px,5vw,64px) auto 0;position:relative}}
.chead>*{{position:relative;z-index:1}}
.torn{{position:absolute;inset:-10% -4% -10% 40%;z-index:0!important;pointer-events:none;opacity:.22}}
.torn i{{position:absolute;animation:settle 20s ease-in-out infinite alternate}}
.torn i:nth-child(1){{right:6%;top:-6%;width:44%;height:70%;background:var(--a);clip-path:polygon(4% 0,96% 6%,100% 60%,88% 100%,10% 94%,0 40%);animation-delay:-3s}}
.torn i:nth-child(2){{right:30%;top:30%;width:38%;height:60%;background:var(--b);clip-path:polygon(0 12%,80% 0,100% 50%,92% 100%,18% 96%,4% 60%);animation-delay:-9s;animation-duration:24s}}
.torn i:nth-child(3){{right:0;bottom:-4%;width:26%;height:46%;background:var(--c);clip-path:polygon(10% 0,100% 10%,90% 100%,0 86%);animation-delay:-14s}}
.torn i:nth-child(4){{right:48%;top:0;width:16%;aspect-ratio:1;height:auto;background:var(--d);border-radius:50%;animation-duration:16s}}
@keyframes settle{{from{{transform:translate(0,0) rotate(0)}}to{{transform:translate(-1.5%,1.5%) rotate(1.5deg)}}}}
.cover h1 span{{display:inline-block;transition:transform .5s cubic-bezier(.2,.8,.2,1)}}
.cover h1 span.sp{{width:.22em}}
@media (prefers-reduced-motion:reduce){{.torn i{{animation:none}}.cover h1 span{{transition:none}}}}
@media (max-width:860px){{.torn{{display:none}}}}
.kicker{{font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--gold);margin:0 0 18px}}
.chead h2{{font-family:var(--disp);font-style:italic;font-weight:400;font-size:clamp(40px,6.4vw,92px);line-height:.98;letter-spacing:-.02em;margin:0 0 20px;text-wrap:balance;font-variation-settings:"opsz" 96}}
.dek{{font-size:clamp(20px,2vw,26px);font-weight:300;margin:0 0 10px;color:var(--dim)}}
.by{{font-family:var(--mono);font-size:12px;color:var(--dim);margin:0}}
.prose{{max-width:66ch;margin:clamp(32px,5vw,56px) auto 0;font-size:19px;line-height:1.62;font-weight:300}}
.prose p{{margin:0 0 1.2em;text-wrap:pretty}}
.prose h3{{font-family:var(--disp);font-style:italic;font-weight:500;font-size:28px;margin:2em 0 .6em;color:var(--fg)}}
.prose .pull{{margin:2em 0;padding:28px 0;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)}}
.prose .pull p{{font-family:var(--disp);font-style:italic;font-size:clamp(24px,2.6vw,34px);line-height:1.25;margin:0 0 12px;color:var(--rose)}}
.prose .pull cite{{font-style:normal;font-family:var(--mono);font-size:12px;color:var(--dim)}}
.prose .note{{font-family:var(--mono);font-size:13px;color:var(--dim);line-height:1.6;margin:2.4em 0}}
.prose .photo{{margin:2.2em 0;background:var(--card);border:1px solid var(--rule);padding:10px}}
.prose .photo.pair{{display:grid;grid-template-columns:1fr 1fr;gap:16px;max-width:none}}
.prose .photo.pair>div{{min-width:0}}
@media (min-width:1000px){{.prose .photo.pair{{width:calc(100% + 14rem);margin-left:-7rem}}}}
@media (max-width:640px){{.prose .photo.pair{{grid-template-columns:1fr}}}}
.prose .photo.small{{max-width:calc(var(--w) + 20px)}}
.prose .photo img{{display:block;width:100%;height:auto}}
.prose .photo figcaption{{font-family:var(--mono);font-size:12px;color:var(--dim);padding:10px 2px 0;line-height:1.5}}
.prose .qa{{font-family:var(--disp);font-style:italic;font-size:24px;line-height:1.3;color:var(--gold);margin:2em 0 .8em}}
.prose .ans b{{font-family:var(--mono);font-weight:500;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--dim);margin-right:.5em}}
.colophon{{max-width:1280px;margin:clamp(56px,9vw,128px) auto 0;{GUT}padding-block:40px 64px;border-top:1px solid var(--rule);font-family:var(--mono);font-size:12px;line-height:1.7;color:var(--dim)}}
a:focus-visible{{outline:2px solid var(--gold);outline-offset:3px}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
@media (max-width:860px){{.plate .img.two{{grid-template-columns:1fr}}}}
.chart{{margin:1.8em 0 2.2em;max-width:600px;--accent:var(--tint,var(--gold,#1b5e6b));--ink:var(--fg,#171614);--mute:var(--dim,var(--mute,#6d6962))}} .chart .ct{{font-size:13px;font-weight:600;margin:0 0 10px}} .chart .cn{{font-size:12px;margin:8px 0 0;opacity:.75}} .chart svg{{display:block;overflow:visible}}
.chart .cb,.chart .cdot,.chart .cseg.on,.chart .carea{{fill:var(--accent)}} .chart .cline,.chart .cbr{{fill:none;stroke:currentColor;opacity:.6;stroke-width:1.6}} .chart .carr{{fill:currentColor}} .chart .cpanel{{fill:none;stroke:var(--rule)}} .chart .cstrand{{fill:none;stroke:var(--accent);stroke-width:5}} .chart .cjoin{{stroke:var(--accent);stroke-width:16}} .chart .ghostline,.chart .ghost{{fill:transparent;stroke:transparent}} .chart .csq{{fill:none;stroke:var(--accent);stroke-width:2.5}} .chart .cdotm{{fill:currentColor;opacity:.5}} .chart .ctrack,.chart .cseg{{fill:var(--rule)}} .chart .cax,.chart .cstem{{stroke:var(--rule)}} .chart .ctick{{stroke:currentColor}}
.chart text{{font-size:12px;fill:currentColor}} .chart .cvin{{fill:#fff;font-weight:700}} .chart .cbig{{font-size:44px;font-weight:800}} .chart .cn2{{font-size:10.5px;opacity:.7}}
.chart .tl{{list-style:none;margin:12px 0 0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:6px 22px;font-size:12.5px}} .chart .tl li{{display:grid;grid-template-columns:3.2em 1fr;gap:8px}}
.figs{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px;margin:1.6em 0 2em}} .figs div{{border-top:3px solid var(--tint,var(--gold));padding-top:10px}} .figs b{{display:block;font-size:34px;line-height:1}} .figs span{{display:block;font-size:12.5px;margin-top:6px;opacity:.75}}
</style>
<div class="bar"><div class="in"><a class="brand" href="#top">The American Bahá'í</a><nav>{nav}</nav></div></div>
<main id="top">
<header class="cover wrap">
  <div>
    <h1>Plates from <em>the arts issue</em></h1>
    <div class="meta"><span>{esc(ISSUE["title"])}</span><span>{SUB}</span><span>{esc(ISSUE["date"])}</span><span>Cover painting by {esc(ISSUE["cover_artist"])}</span></div>
    <p class="epi">“{esc(ISSUE["epigraph"])}”</p>
    <cite>{esc(ISSUE["epigraph_src"])}</cite>
    <p class="about"><b>About this issue.</b> {esc(ISSUE["about"])}</p>
  </div>
  <figure class="img"><div class="mat"><img src="img/cover-paint.jpg" alt="Oil painting by Juliet Bogan: two figures in a flowering meadow look toward terraced green farmland and ochre mountains under a pale sky"></div><figcaption><b>Cover</b><span>Painting by {esc(ISSUE["cover_artist"])}</span><span>Oil on canvas</span></figcaption></figure>
</header>
<div class="wrap">{"".join(chapters)}</div>
<footer class="colophon">{esc(ISSUE["publisher"])}<br>Feature texts transcribed from the printed issue. Plate 3 reproduces the printed opener with its title as set in the magazine.</footer>
</main>
<script>
(function(){{
  if(matchMedia('(prefers-reduced-motion: reduce)').matches||!matchMedia('(hover: hover)').matches)return;
  var h=document.querySelector('.cover h1'); if(!h)return;
  var out=[]; h.childNodes.forEach(function(n){{
    var tag=n.nodeType===1?n.tagName.toLowerCase():null; var txt=n.textContent;
    txt.split('').forEach(function(ch){{var s=document.createElement('span');if(ch===' '){{s.className='sp';s.innerHTML='&nbsp;'}}else s.textContent=ch; if(tag){{var w=document.createElement(tag);w.appendChild(s);out.push(w)}}else out.push(s);}});
  }});
  h.textContent=''; out.forEach(function(x){{h.appendChild(x)}});
  var spans=[].slice.call(h.querySelectorAll('span'));
  h.addEventListener('mousemove',function(e){{spans.forEach(function(s){{var r=s.getBoundingClientRect();var dx=(r.left+r.width/2)-e.clientX;var k=Math.max(-1,Math.min(1,dx/180));s.style.transform='rotate('+(k*-5)+'deg) translateY('+(Math.abs(k)*-4)+'px)';}});}});
  h.addEventListener('mouseleave',function(){{spans.forEach(function(s){{s.style.transform=''}});}});
}})();
</script>
'''

# ------------------------------------------------------------------ READER (alternate, kept under alt/)
def build_reader():
    tints = {"gregory":"#e8532a","newyorkers":"#f05a7e","twoartists":"#b07a4a","abs":"#c9462c","endeavor":"#1b5e6b","comic":"#e9a21f"}
    arts = []
    for a in ARTICLES:
        t = tints[a["slug"]]
        if a.get("art"):
            if a["slug"] == "comic":
                art = f'<figure class="inset two"><img src="img/{a["art"]}" alt="{esc(a["art_alt"])}"><img src="img/{a["art2"]}" alt="{esc(a["art2_alt"])}"><figcaption>{esc(a["art_credit"])}</figcaption></figure>'
            else:
                art = f'<figure class="inset{" bare" if a.get("art_transparent") else ""}" style="max-width:{a.get("art_width") or 860}px"><img src="img/{a["art"]}" alt="{esc(a["art_alt"])}"><figcaption>{esc(a["art_credit"])}</figcaption></figure>'
        else:
            art = ""
        dek = f'<p class="dek">{esc(a["dek"])}</p>' if a.get("dek") else ""
        by = f'<span>{esc(a["byline"])}</span>' if a.get("byline") else ""
        arts.append(f'''<article class="story" id="{a["slug"]}" style="--tint:{t}">
  <header class="shead">
    <p class="kicker">{esc(a["kicker"])}</p>
    <h2>{esc(a["title"])}</h2>
    {dek}
    <p class="meta">{by}<span>Pages {a["pages"]}</span></p>
  </header>
  {art}
  <div class="prose">{body_html(a["body"])}</div>
</article>''')
    rail = "".join(f'<a href="#{a["slug"]}" style="--tint:{tints[a["slug"]]}"><span>{esc(a["short"])}</span><i class="fill"></i></a>' for a in ARTICLES)
    return f'''<title>{esc(ISSUE["title"])} Reader</title>
{SIDES}
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,300..800&family=Literata:ital,opsz,wght@0,7..72,300..600;1,7..72,300..600&display=swap">
<style>
/* Layout: a reading app. A rail on the left lists the features with the issue's own color tabs; the stories run on the right in a wide grotesque headline and a book-weight serif, art set inset at the column width. The rail becomes a strip across the top on phones. */
:root{{
  --bg:#fbfaf7; --fg:#171614; --mute:#6d6962; --rule:#e2ded6; --rail:#efede7; --tabon:#ffffff; --tint:#1b5e6b;
  --disp:"Bricolage Grotesque","Helvetica Neue",Arial,sans-serif; --text:"Literata",Georgia,serif;
}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#111110;--fg:#eceae4;--mute:#9f9a91;--rule:#2a2825;--rail:#161513;--tabon:#23211d;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#111110;--fg:#eceae4;--mute:#9f9a91;--rule:#2a2825;--rail:#161513;--tabon:#23211d;color-scheme:dark}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{margin:0;background:var(--bg);color:var(--fg);font-family:var(--text);font-size:18px;line-height:1.55}}
body::before{{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--rail)}}
.tabs{{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--rail);border-bottom:1px solid var(--rule)}}
.tabs .in{{max-width:1100px;margin:0 auto;{GUT}display:flex;align-items:stretch;gap:0;overflow-x:auto;scrollbar-width:none;position:relative}}
.tabs .brand{{font-family:var(--disp);font-weight:700;font-size:17px;letter-spacing:-.02em;color:var(--fg);text-decoration:none;white-space:nowrap;align-self:center;margin-right:28px}}
.tabs .brand small{{display:block;font-weight:400;font-size:11px;color:var(--mute);letter-spacing:.02em}}
.tabs nav{{display:flex;margin-left:auto}}
.tabs nav a{{position:relative;display:flex;align-items:flex-end;padding:18px 16px 0;border-bottom:4px solid var(--tint);color:var(--fg);text-decoration:none;font-family:var(--disp);font-weight:600;font-size:15px;letter-spacing:-.01em;white-space:nowrap}}
.tabs nav a span{{padding-bottom:12px}}
/* motion: the current tab's underline fills as the story is read; a thin dark line slides between tabs. */
.tabs nav a .fill{{position:absolute;left:0;bottom:-4px;height:4px;width:0;background:var(--fg);opacity:.9;transition:width .4s cubic-bezier(.2,.8,.2,1)}}
.tabs nav a.on .fill{{width:var(--p,0%)}}
.tabs .ind{{position:absolute;bottom:-1px;height:2px;background:var(--fg);transition:left .5s cubic-bezier(.2,.8,.2,1),width .5s cubic-bezier(.2,.8,.2,1)}}
@media (prefers-reduced-motion:reduce){{.tabs nav a .fill,.tabs .ind{{transition:none}}}}
.tabs nav a.on{{background:var(--tabon)}}
.tabs nav a:hover,.tabs nav a:focus-visible{{background:var(--tabon)}}
.pages{{{GUT}}}
.cover{{display:grid;grid-template-columns:minmax(0,1fr);gap:36px;padding-block:clamp(32px,5vw,72px) clamp(28px,4vw,56px);border-bottom:1px solid var(--rule);max-width:1100px;margin:0 auto}}
.cover h1{{font-family:var(--disp);font-weight:800;font-size:clamp(44px,6.6vw,96px);line-height:.92;letter-spacing:-.035em;margin:0 0 20px;font-variation-settings:"opsz" 96;text-wrap:balance}}
.cover .about{{max-width:50ch;font-size:16px;color:var(--mute);margin:0}}
.cover .about b{{color:var(--fg);font-weight:600}}
.cover figure{{margin:0 auto;width:fit-content;max-width:100%;border:1px solid var(--rule);padding:clamp(10px,1.4vw,18px);background:var(--rail);border-radius:6px}}
.cover figure .mat{{border:1px solid var(--rule);border-radius:3px;overflow:hidden}}
.cover img{{display:block;width:auto;max-width:100%;height:auto;max-height:92vh}}
.cover figcaption{{font-family:var(--disp);font-size:12px;color:var(--mute);margin-top:8px;letter-spacing:.02em}}
.story{{max-width:1100px;margin:0 auto;padding-block:clamp(56px,8vw,112px) 0}}
.story+.story{{border-top:1px solid var(--rule);margin-top:clamp(56px,8vw,112px)}}
.kicker{{font-family:var(--disp);font-size:12px;letter-spacing:.14em;text-transform:uppercase;font-weight:600;color:var(--tint);margin:0 0 16px}}
.shead h2{{font-family:var(--disp);font-weight:700;font-size:clamp(36px,5.4vw,72px);line-height:.98;letter-spacing:-.03em;margin:0 0 16px;max-width:20ch;text-wrap:balance;font-variation-settings:"opsz" 96}}
.dek{{font-family:var(--disp);font-weight:300;font-size:clamp(20px,2.2vw,28px);margin:0 0 14px;max-width:34ch}}
.meta{{display:flex;gap:20px;flex-wrap:wrap;font-family:var(--disp);font-size:13px;color:var(--mute);margin:0 0 32px}}
.inset{{margin:0 0 clamp(28px,4vw,48px);max-width:860px}}
.inset img{{display:block;width:100%;height:auto;border-radius:4px;border:1px solid var(--rule)}}
.inset.bare img{{border:0;border-radius:0}}
.inset.two{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.inset figcaption{{grid-column:1/-1;font-family:var(--disp);font-size:12px;color:var(--mute);margin-top:8px}}
.prose{{max-width:64ch;font-size:18.5px;line-height:1.62;font-variation-settings:"opsz" 18}}
.prose p{{margin:0 0 1.15em;text-wrap:pretty}}
.prose h3{{font-family:var(--disp);font-weight:700;font-size:22px;letter-spacing:-.01em;margin:2em 0 .6em}}
.prose .pull{{margin:1.8em 0;padding:4px 0 4px 20px;border-left:4px solid var(--tint)}}
.prose .pull p{{font-family:var(--disp);font-weight:500;font-size:clamp(21px,2.2vw,27px);line-height:1.25;letter-spacing:-.015em;margin:0 0 8px}}
.prose .pull cite{{font-style:normal;font-family:var(--disp);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}}
.prose .photo{{margin:2.4em 0;display:grid;grid-template-columns:minmax(0,1fr) 15ch;gap:14px 24px;align-items:end;max-width:none;width:min(58rem,calc(100vw - 32px))}}
.prose .photo>img{{display:block;width:100%;height:auto;border-radius:4px;grid-row:1;grid-column:1}}
.prose .photo.small{{grid-template-columns:minmax(0,var(--w)) 15ch;width:auto}}
.prose .photo>figcaption{{grid-column:2;grid-row:1;font-family:var(--disp);font-size:13px;line-height:1.5;color:var(--mute);padding-top:10px;border-top:3px solid var(--tint);align-self:end}}
.prose .photo>figcaption::before{{content:"Photograph";display:block;font-size:11px;letter-spacing:.12em;text-transform:uppercase;font-weight:700;color:var(--tint);margin-bottom:6px}}
.prose .photo.pair{{grid-template-columns:1fr 1fr;gap:22px;align-items:start;width:min(66rem,calc(100vw - 32px))}}
.prose .photo.pair>div{{min-width:0}}
.prose .photo.pair>div img{{display:block;width:100%;height:auto;border-radius:4px}}
.prose .photo.pair>div figcaption{{font-family:var(--disp);font-size:13px;line-height:1.5;color:var(--mute);margin-top:10px;padding-top:10px;border-top:3px solid var(--tint)}}
@media (max-width:640px){{.prose .photo,.prose .photo.pair{{grid-template-columns:1fr}} .prose .photo>figcaption{{grid-column:1;grid-row:2}}}}
.prose .note{{font-family:var(--disp);font-size:14px;color:var(--mute);background:var(--rail);padding:14px 16px;border-radius:4px;margin:2em 0}}
.prose .qa{{font-family:var(--disp);font-weight:700;font-size:20px;letter-spacing:-.01em;margin:1.8em 0 .6em}}
.prose .ans b{{font-family:var(--disp);font-weight:700;font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--tint);margin-right:.4em}}
.colophon{{max-width:1100px;margin:clamp(56px,8vw,112px) auto 0;padding-block:32px 64px;border-top:1px solid var(--rule);font-family:var(--disp);font-size:13px;line-height:1.6;color:var(--mute)}}
a:focus-visible{{outline:2px solid var(--fg);outline-offset:3px}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
@media (max-width:900px){{
  .tabs .brand small{{display:none}}
  .tabs nav{{margin-left:0}}
  .tabs nav a{{padding:14px 12px 0;font-size:14px}}
  .inset.two{{grid-template-columns:1fr}}
}}
.chart{{margin:1.8em 0 2.2em;max-width:600px;--accent:var(--tint,var(--gold,#1b5e6b));--ink:var(--fg,#171614);--mute:var(--dim,var(--mute,#6d6962))}} .chart .ct{{font-size:13px;font-weight:600;margin:0 0 10px}} .chart .cn{{font-size:12px;margin:8px 0 0;opacity:.75}} .chart svg{{display:block;overflow:visible}}
.chart .cb,.chart .cdot,.chart .cseg.on,.chart .carea{{fill:var(--accent)}} .chart .cline,.chart .cbr{{fill:none;stroke:currentColor;opacity:.6;stroke-width:1.6}} .chart .carr{{fill:currentColor}} .chart .cpanel{{fill:none;stroke:var(--rule)}} .chart .cstrand{{fill:none;stroke:var(--accent);stroke-width:5}} .chart .cjoin{{stroke:var(--accent);stroke-width:16}} .chart .ghostline,.chart .ghost{{fill:transparent;stroke:transparent}} .chart .csq{{fill:none;stroke:var(--accent);stroke-width:2.5}} .chart .cdotm{{fill:currentColor;opacity:.5}} .chart .ctrack,.chart .cseg{{fill:var(--rule)}} .chart .cax,.chart .cstem{{stroke:var(--rule)}} .chart .ctick{{stroke:currentColor}}
.chart text{{font-size:12px;fill:currentColor}} .chart .cvin{{fill:#fff;font-weight:700}} .chart .cbig{{font-size:44px;font-weight:800}} .chart .cn2{{font-size:10.5px;opacity:.7}}
.chart .tl{{list-style:none;margin:12px 0 0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:6px 22px;font-size:12.5px}} .chart .tl li{{display:grid;grid-template-columns:3.2em 1fr;gap:8px}}
.figs{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px;margin:1.6em 0 2em}} .figs div{{border-top:3px solid var(--tint,var(--gold));padding-top:10px}} .figs b{{display:block;font-size:34px;line-height:1}} .figs span{{display:block;font-size:12.5px;margin-top:6px;opacity:.75}}
</style>
<div class="tabs"><div class="in"><a class="brand" href="#top">The American Bahá'í<small>{SUB}</small></a><nav aria-label="Features">{rail}</nav><span class="ind" aria-hidden="true"></span></div></div>
<main class="pages" id="top">
<header class="cover">
  <div>
    <h1>Six features from the arts issue</h1>
    <p class="about"><b>About this issue.</b> {esc(ISSUE["about"])}</p>
  </div>
  <figure><div class="mat"><img src="img/cover-paint.jpg" alt="Oil painting by Juliet Bogan: two figures in a flowering meadow look toward terraced green farmland and ochre mountains under a pale sky"></div><figcaption>Cover painting by {esc(ISSUE["cover_artist"])} · Oil on canvas</figcaption></figure>
</header>
{"".join(arts)}
<footer class="colophon">{esc(ISSUE["publisher"])}<br>Feature texts transcribed from the printed issue.<br>“{esc(ISSUE["epigraph"])}” {esc(ISSUE["epigraph_src"])}</footer>
</main>
<script>
(function(){{
  var links=[].slice.call(document.querySelectorAll('.tabs nav a'));
  var secs=[].slice.call(document.querySelectorAll('article.story'));
  var ind=document.querySelector('.tabs .ind'), inn=document.querySelector('.tabs .in');
  var cur=null;
  function place(a){{if(!a||!ind)return;var r=a.getBoundingClientRect(),b=inn.getBoundingClientRect();ind.style.left=(r.left-b.left+inn.scrollLeft)+'px';ind.style.width=r.width+'px';}}
  var alias={{abiding:'huquq',fund:'huquq',rhythm:'huquq',books:'huquq',notices:'huquq'}};
  function tabFor(id){{return links.filter(function(l){{return l.getAttribute('href')==='#'+(alias[id]||id)}})[0];}}
  function progress(){{if(!cur)return;var a=tabFor(cur.id);if(!a)return;
    var r=cur.getBoundingClientRect();var top=r.top+scrollY, h=r.height;var p=(scrollY+innerHeight*0.4-top)/h;p=Math.max(0,Math.min(1,p));a.style.setProperty('--p',(p*100).toFixed(1)+'%');}}
  if('IntersectionObserver' in window){{
    var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(!e.isIntersecting)return;cur=e.target;
      var t=tabFor(e.target.id);links.forEach(function(a){{var on=a===t;a.classList.toggle('on',on);if(on)place(a);}});progress();}});}},{{rootMargin:'-30% 0px -60% 0px'}});
    secs.forEach(function(x){{io.observe(x)}});
  }}
  addEventListener('scroll',progress,{{passive:true}}); addEventListener('resize',function(){{place(document.querySelector('.tabs nav a.on'))}});
}})();
</script>
'''

for name, fn in [("tab", build_tab), ("plates", build_plates), ("reader", build_reader)]:
    with open(os.path.join(OUT, f"{name}.html"), "w") as f: f.write(fn())
with open(os.path.join(OUT, "member.html"), "w") as f: f.write(build_tab(member=True))

# ---------------------------------------------------------------- GitHub Pages site
SITE = os.path.join(HERE, "site")
def standalone(body):
    """Wrap an artifact page in a full HTML document; image paths become relative to site/img."""
    body = body.replace(SIDES, "").replace('src="img/', 'src="../img/').replace('url(img/', 'url(../img/')
    i = body.rfind("</style>")
    i = body.index("\n", i) + 1
    body = body[:i] + "</head>\n<body>\n" + body[i:]
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<link rel="icon" type="image/svg+xml" href="FAVICON">\n'
            '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}</style>\n'
            + body + '\n</body>\n</html>\n')
os.makedirs(SITE, exist_ok=True)
with open(os.path.join(SITE, "index.html"), "w") as f: f.write(standalone(build_tab()).replace('src="../img/', 'src="img/').replace('url(../img/', 'url(img/').replace('href="FAVICON"', 'href="favicon.svg"'))
shutil.copy(os.path.join(HERE, "favicon.svg"), os.path.join(SITE, "favicon.svg"))
os.makedirs(os.path.join(SITE, "member"), exist_ok=True)
with open(os.path.join(SITE, "member", "index.html"), "w") as f: f.write(standalone(build_tab(member=True)).replace('href="FAVICON"', 'href="../favicon.svg"'))
for d, fn in [("alt/plates", build_plates), ("alt/reader", build_reader)]:
    os.makedirs(os.path.join(SITE, d), exist_ok=True)
    with open(os.path.join(SITE, d, "index.html"), "w") as f: f.write(standalone(fn()).replace('src="../img/', 'src="../../img/').replace('href="FAVICON"', 'href="../../favicon.svg"'))
os.makedirs(os.path.join(SITE, "img"), exist_ok=True)
for f in os.listdir(os.path.join(OUT, "img")): shutil.copy(os.path.join(OUT, "img", f), os.path.join(SITE, "img", f))
open(os.path.join(SITE, ".nojekyll"), "w").close()
print("built out/ and site/")
