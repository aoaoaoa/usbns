"""Builds The American Bahá'í arts-issue site from data.py.

Outputs:
  out/tab.html, out/plates.html, out/reader.html   artifact pages (no html/head/body skeleton)
  site/                                            GitHub Pages tree: index.html (TAB), alt/plates, alt/reader, img/
Images are read from out/img/ (subfolders included) and mirrored to site/img/.
"""
import html, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import ISSUE, VOICES, ARTICLES
from footer import footer_html, FOOTER_CSS
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
    out = []; mark = None
    for b in blocks:
        k = b[0]
        if k == "p":
            t = qesc(b[1])
            if mark and mark[0] in t:  # the phrase a margin note answers
                t = t.replace(mark[0], f'<mark class="mnh" id="{mark[1]}">{mark[0]}</mark>', 1); mark = None
            out.append(f"<p>{t}</p>")
        elif k == "mnote":
            # ("mnote", quote, who, phrase in the next paragraph)
            mid = "mn-" + re.sub(r"[^a-z]+", "-", b[3].lower()).strip("-"); mark = (b[3], mid)
            out.append(f'<aside class="mnote" data-for="{mid}"><span class="mq">{qesc(b[1])}</span><span class="mw">{esc(b[2])}</span></aside>')
        elif k == "h": out.append(f"<h3>{esc(b[1])}</h3>")
        elif k == "q": out.append(f'<blockquote class="pull"><p>{esc(b[1])}</p><cite>{esc(b[2])}</cite></blockquote>')
        elif k == "note": out.append(f'<p class="note">{esc(b[1])}</p>')
        elif k == "qa": out.append(f'<p class="qa">{esc(b[1])}</p>')
        elif k == "a": out.append(f'<p class="ans"><b>{esc(b[1])}</b> {qesc(b[2])}</p>')
        elif k == "pair":
            w = next((x for x in b[1:] if isinstance(x, int)), None)
            prs = [x for x in b[1:] if isinstance(x, tuple)]
            st = f' style="max-width:{w}px"' if w else ""
            out.append(f'<figure class="photo pair{" capped" if w else ""}"{st}>' + "".join(f'<div style="flex:{IMGAR.get(f, 1):.3f} 1 12px"><img src="img/{f}" alt="{esc(c)}" loading="lazy"><figcaption>{esc(c)}</figcaption></div>' for f,c in prs) + '</figure>')
        elif k == "ext": out.append(f'<blockquote class="ext"><p>{qesc(b[1])}</p></blockquote>')
        elif k == "ext2": out.append(f'<blockquote class="ext ext2"><p>{qesc(b[1])}</p></blockquote>')
        elif k == "extw": out.append(f'<blockquote class="ext sacred"><p>{qesc(b[1])}</p></blockquote>')  # the Writings or the Universal House of Justice
        elif k == "list": out.append('<ul class="qs">' + "".join(f"<li>{qesc(x)}</li>" for x in b[1]) + "</ul>")
        elif k == "kv": out.append('<dl class="kv">' + "".join(f"<dt>{esc(x)}</dt><dd>{esc(y)}</dd>" for x,y in b[1]) + "</dl>")
        elif k == "chart": out.append(chart_html(b[1]))
        elif k == "concept": out.append(concept_html(b[1]))
        elif k == "figures": out.append('<div class="figs">' + "".join(f'<div{" class=has" if len(f) > 2 else ""}{pop(f[0] + " " + f[1], f[2] if len(f) > 2 else "")}><b{" class=wd" if len(f[0]) > 8 else ""}>{esc(f[0])}</b><span>{esc(f[1])}</span></div>' for f in b[1]) + "</div>")
        elif k == "verb":
            out.append(f'<blockquote class="verb vc" data-f="2"><p>“Neighboring has become a <em>verb.</em>”</p><span class="rl" aria-hidden="true"></span><cite>{esc(b[1])}</cite></blockquote>')
        elif k == "sentence":
            parts = b[1]; pops = b[2] if len(b) > 2 else {}
            out.append(f'<p class="figsent{" " + b[3] if len(b) > 3 else ""}">' + "".join((f'<b class="{"has" if pops.get(p) else ""}{" wd" if len(p) > 8 else ""}"{pop(p, pops.get(p, ""))}>{esc(p)}</b>' if i % 2 else esc(p)) for i, p in enumerate(parts)) + '</p>')
        elif k == "portraits":
            out.append('<div class="portraits">' + "".join(f'<figure class="{cl}"><img src="img/{f}" alt="{esc(cap)}" loading="lazy"><figcaption>{esc(cap)}</figcaption></figure>' for f, cap, cl in b[1]) + '</div>')
        elif k == "band":
            # full-bleed room: a toned wall or stage on which several photographs hang together
            c = b[1]; items = "".join(f'<figure class="bi {cl}"><img src="img/{f}" alt="{esc(cap)}" loading="lazy"><figcaption>{esc(cap)}</figcaption></figure>' for f, cap, cl in c["items"])
            lab = f'<p class="blab">{esc(c["label"])}</p>' if c.get("label") else ""
            out.append(f'<section class="band {c["tone"]}"><div class="bin">{lab}{items}</div></section>')
        elif k == "mount":
            # mounted print: a soft photograph shown at its sharp size on an off-white card
            f, cap, w = b[1], b[2], b[3]; side = b[4] if len(b) > 4 else ""
            out.append(f'<figure class="mountp {side}" style="--w:{w}px"><img src="img/{f}" alt="{esc(cap)}" loading="lazy"><figcaption>{esc(cap)}</figcaption></figure>')
        elif k == "img":
            w = b[3] if len(b) > 3 else None
            cls = "photo small" if w else "photo"
            st = f' style="--w:{w}px"' if w else ""
            out.append(f'<figure class="{cls}"{st}><img src="img/{b[1]}" alt="{esc(b[2])}" loading="lazy"><figcaption>{esc(b[2])}</figcaption></figure>')
    return "\n".join(out)

import json as _json
USMAP = _json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "usmap.json")))
USREG = _json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "usregions.json")))  # Bahá'í regions, merged from state lines

def _imgar():
    from PIL import Image as _I
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "img"); r = {}
    for f in os.listdir(d):
        try: w, h = _I.open(os.path.join(d, f)).size; r[f] = w / h
        except Exception: pass
    return r
IMGAR = _imgar()
def _dims(f):
    """width/height attributes so lazy images reserve their space before they load."""
    try:
        from PIL import Image as _I
        w, h = _I.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "img", f)).size
        return f' width="{w}" height="{h}"'
    except Exception: return ""

def pop(title, body):
    """Attributes that make an element open the shared popup."""
    if not body: return ""
    t = html.escape(title.replace("|", " "), quote=True)
    return f' tabindex="0" role="button" aria-label="{t}" data-pt="{t}" data-pb="{html.escape(body, quote=True)}"'

def size_cls(c):
    w = c.get("w"); return "" if not w else (" sized span" if w > 640 else " sized")
def size_sty(c):
    return f' style="--cw:{c["w"]}px"' if c.get("w") else ""

def month_body(c, i, name, base, st):
    import datetime as _dt
    n = len(c["months"]); starts = c.get("starts", [None]*n)
    if base is None and i == n - 1 and starts[i-1]:
        base = (_dt.datetime.strptime(starts[i-1], "%B %d, %Y") + _dt.timedelta(days=19 + 4)).strftime("%B %-d, %Y")
    lines = [f"Month {i+1} of 19."]
    if base:
        d0 = _dt.datetime.strptime(base, "%B %d, %Y")
        lines.append(f"Feast of {name}: {base}, the month's first day, beginning at sunset the evening before.")
        hd = c.get("holy", {}).get(name, [])
        if hd:
            lines.append("Holy Days: " + "; ".join(f"{h} ({(d0 + _dt.timedelta(days=day-1)).strftime('%B %-d')})" for day, h in hd) + ".")
    if st: lines.append(st)
    return "\n".join(lines)

def chart_html(c):
    """Small inline SVG charts drawn to scale from the record's numbers."""
    def money(v): return f"${v:,.0f}"
    fmt = money if c.get("fmt") == "money" else (lambda v: f"{v:,}")
    title = (f'<p class="cno">No. {c["no"]}</p>' if c.get("no") else "") + f'<p class="ct">{esc(c["title"])}</p>'; note = f'<p class="cn">{esc(c["note"])}</p>' if c.get("note") else ""
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
    elif c["kind"] == "timeline" and c.get("style") == "steps":
        import textwrap as _tw
        ev = c["events"]; n = len(ev); W = 640; cw = W / n; parts = [f'<line x1="0" y1="58" x2="{W}" y2="58" class="cax"/>']; mx = 0
        for i, e in enumerate(ev):
            y, lab = e[0], e[1]; story = e[2] if len(e) > 2 else ""; x = i * cw
            ws = _tw.wrap(lab, max(12, int(cw / 7.4)))[:9]; mx = max(mx, len(ws))
            txt = "".join(f'<text x="{x:.1f}" y="{86 + 16*k}" class="cstep">{esc(w)}</text>' for k, w in enumerate(ws))
            parts.append(f'<g class="hit"{pop(f"{y}: {lab}", story)}><rect x="{x:.1f}" y="0" width="{cw-6:.1f}" height="{90 + 16*9}" class="ghost"/>'
                         f'<text x="{x:.1f}" y="40" class="cyr">{y}</text><circle cx="{x+6:.1f}" cy="58" r="{6.5 if story else 5}" class="cdot"/>{txt}</g>')
        svg = f'<svg viewBox="0 0 {W} {80 + 16*mx + 8}" width="100%" role="img" aria-label="{esc(c["title"])}">{"".join(parts)}</svg>'
    elif c["kind"] == "timeline" and c.get("break"):
        # two scales: the life stretched across most of the width, the later years folded behind a break mark;
        # year labels fan out on leader lines in two tiers so every year can be read
        ev = c["events"]; y0, y1 = c["start"], c["end"]; b0, b1 = c["break"]; W = 760; pad = 14; BR = 26; split = c.get("split", .76)
        lw = (W - 2*pad - BR) * split; gw = (W - 2*pad - BR) - lw
        X = lambda y: pad + lw * (y - y0) / (b0 - y0) if y <= b0 else pad + lw + BR + gw * (y - b1) / (y1 - b1)
        kind = (lambda y: c["kinds"].get(y, "legacy")) if c.get("kinds") else (lambda y: "teach")
        LY = 46; T = (86, 102, 118); SP = 38
        parts = [f'<line x1="{pad}" y1="{LY}" x2="{pad+lw:.1f}" y2="{LY}" class="cax"/><line x1="{pad+lw+BR:.1f}" y1="{LY}" x2="{W-pad}" y2="{LY}" class="cax"/>',
                 f'<path d="M{pad+lw+7:.1f} {LY+8} l5 -16 M{pad+lw+14:.1f} {LY+8} l5 -16" class="cbrk"/>']
        for a, bb, lab in c.get("eras", []):
            parts.append(f'<rect x="{X(a):.1f}" y="{LY-5}" width="{X(bb)-X(a):.1f}" height="10" rx="5" class="cera"/><text x="{(X(a)+X(bb))/2:.1f}" y="10" text-anchor="middle" class="cn2">{esc(lab)}</text>')
        for t in [t for t in range((y0 // 10) * 10, b0 + 1, 10)] + [t for t in (1970, 2000, 2030) if b1 <= t <= y1]:
            parts.append(f'<text x="{X(t):.1f}" y="30" text-anchor="middle" class="cn2">{t}</text>')
        xs = [X(e[0]) for e in ev]; lx = [0.0] * len(ev)
        for tier in range(len(T)):  # place each tier's labels left to right, then pull back from the right edge
            idx = [i for i in range(len(ev)) if i % len(T) == tier]
            for n, i in enumerate(idx): lx[i] = max(xs[i], lx[idx[n-1]] + SP if n else pad + 12)
            for n in range(len(idx) - 1, -1, -1):
                i = idx[n]; lim = lx[idx[n+1]] - SP if n < len(idx) - 1 else W - pad - 12
                if lx[i] > lim: lx[i] = lim
        rows = []; eras = c.get("eras", [])
        for i, e in enumerate(ev):
            y, lab = e[0], e[1]; story = e[2] if len(e) > 2 else ""; x = xs[i]; ty = T[i % len(T)]; k = kind(y)
            parts.append(f'<path d="M{x:.1f} {LY+6} V{LY+12} L{lx[i]:.1f} {ty-16} V{ty-12}" class="cfan"/>')
            parts.append(f'<g class="k-{k}"><circle cx="{x:.1f}" cy="{LY}" r="5.5" class="cdotk"/><circle cx="{x:.1f}" cy="{LY}" r="11" class="ghost hit"{pop(f"{y}: {lab}", story)}/><text x="{lx[i]:.1f}" y="{ty}" text-anchor="middle" class="cvk"{pop(f"{y}: {lab}", story)}>{y}</text></g>')
            if i == 0 and eras: rows.append(f'<li class="era">{esc(eras[0][2])} · {ev[0][0]}–{max(e[0] for e in ev if e[0] < b0)}</li>')
            if len(eras) > 1 and y > b0 and ev[i-1][0] < b0: rows.append(f'<li class="era e2">{esc(eras[1][2])} · {y}–{ev[-1][0]}</li>')
            rows.append(f'<li class="k-{k}{" has" if story else ""}" data-y="{y}"{pop(f"{y}: {lab}", story)}><b>{y}</b><span>{esc(lab)}</span></li>')
        K = {"life": "Life", "teach": "Teaching journeys", "serve": "Service and institutions", "write": "Writings", "legacy": "Legacy"}
        used = {kind(e[0]) for e in ev}
        key = ('<p class="kkey">' + "".join(f'<span><i class="k-{k}"></i>{v}</span>' for k, v in K.items() if k in used) + '</p>') if c.get("kinds") else ""
        def row(evs, a, z, ticks, era, T):
            # phone row: one span at the phone's width, labels fanned in T rows
            RW = 358; rp = 12; RY = 30; RSP = 34; Xr = lambda y: rp + (RW - 2*rp) * (y - a) / (z - a)
            q = [f'<line x1="{rp}" y1="{RY}" x2="{RW-rp}" y2="{RY}" class="cax"/>']
            if era: q.append(f'<rect x="{Xr(era[0]):.1f}" y="{RY-4}" width="{Xr(era[1])-Xr(era[0]):.1f}" height="8" rx="4" class="cera"/>')
            q += [f'<text x="{Xr(t):.1f}" y="{RY-12}" text-anchor="middle" class="cn2">{t}</text>' for t in ticks]
            rx = [Xr(e[0]) for e in evs]; rl = rx[:]
            for tier in range(len(T)):
                idx = [i for i in range(len(evs)) if i % len(T) == tier]
                for n, i in enumerate(idx): rl[i] = max(rx[i], rl[idx[n-1]] + RSP if n else rp + 10)
                for n in range(len(idx) - 1, -1, -1):
                    i = idx[n]; lim = rl[idx[n+1]] - RSP if n < len(idx) - 1 else RW - rp - 10
                    if rl[i] > lim: rl[i] = lim
            for i, e in enumerate(evs):
                ty = T[i % len(T)]; k = kind(e[0]); story = e[2] if len(e) > 2 else ""
                q.append(f'<path d="M{rx[i]:.1f} {RY+5} V{RY+10} L{rl[i]:.1f} {ty-13} V{ty-10}" class="cfan"/>')
                q.append(f'<g class="k-{k}"><circle cx="{rx[i]:.1f}" cy="{RY}" r="4" class="cdotk"/><circle cx="{rx[i]:.1f}" cy="{RY}" r="9" class="ghost hit"{pop(f"{e[0]}: {e[1]}", story)}/><text x="{rl[i]:.1f}" y="{ty}" text-anchor="middle" class="cvk"{pop(f"{e[0]}: {e[1]}", story)}>{e[0]}</text></g>')
            return f'<svg viewBox="0 0 {RW} {T[-1] + 6}" width="100%" aria-hidden="true">{"".join(q)}</svg>'
        eras = c.get("eras", [])
        life = [e for e in ev if e[0] <= b0]; later = [e for e in ev if e[0] > b0]
        rows2 = (f'<div class="tlrows"><p class="tlrl">{esc(eras[0][2]) if eras else ""}, {life[0][0]}–{life[-1][0]}</p>' + row(life, (y0 // 10) * 10, b0 + 3, [t for t in range(1880, b0, 20)], eras[0][:2] if eras else None, (62, 78, 94, 110))
                 + f'<p class="tlrl">{esc(eras[1][2]) if len(eras) > 1 else ""}, {later[0][0]}–{later[-1][0]}</p>' + row(later, later[0][0] - 6, y1, [t for t in (1960, 1980, 2000, 2020) if later[0][0] - 6 < t < y1], (later[0][0], later[-1][0]), (62, 78)) + '</div>') if later else ""
        svg = key + f'<svg viewBox="0 0 {W} 124" width="100%" role="img" aria-label="{esc(c["title"])}" class="tl2">{"".join(parts)}</svg>{rows2}<ol class="tl tlx">{"".join(rows)}</ol>'
    elif c["kind"] == "timeline":
        ev = c["events"]; y0 = c.get("start", ev[0][0]); y1 = c.get("end", ev[-1][0]); W = 600; pad = 14
        X = lambda y: pad + (W - 2*pad) * (y - y0) / (y1 - y0)
        parts = [f'<line x1="{pad}" y1="30" x2="{W-pad}" y2="30" class="cax"/>']
        for era in c.get("eras", []):
            a, b, lab = era; parts.append(f'<rect x="{X(a):.1f}" y="24" width="{X(b)-X(a):.1f}" height="12" class="cera"/><text x="{(X(a)+X(b))/2:.1f}" y="16" text-anchor="middle" class="cn2">{esc(lab)}</text>')
        rows = []; edge = [-1e9, -1e9]; labs = []; LW = 44  # year labels take two rows; a crowded year keeps its dot and popup, and the list below names it
        for i, e in enumerate(ev):
            y, lab = e[0], e[1]; story = e[2] if len(e) > 2 else ""
            x = X(y); anc = "start" if x < 40 else ("end" if x > W - 40 else "middle")
            l = x - 6 if anc == "start" else x - LW - 6 if anc == "end" else x - LW/2
            r = next((k for k in (0, 1) if l > edge[k] + 4), None)
            parts.append(f'<circle cx="{x:.1f}" cy="30" r="4.5" class="cdot"/><circle cx="{x:.1f}" cy="30" r="11" class="ghost hit"{pop(f"{y}: {lab}", story)}/>')
            if r is not None:
                edge[r] = l + LW; ly = 56 + 16 * r; labs.append((r, x, l, ly))
                parts.append(f'<text x="{x - 6 if anc == "start" else x + 6 if anc == "end" else x:.1f}" y="{ly}" text-anchor="{anc}" class="cv">{y}</text>')
            rows.append(f'<li{" class=has" if story else ""}{pop(f"{y}: {lab}", story)}><b>{y}</b><span>{esc(lab)}</span></li>')
        for r, x, l, ly in labs:  # a lower label's stem stops short rather than cut through an upper label
            cut = r and any(l0 - 2 < x < l0 + LW + 2 for r0, x0, l0, _ in labs if r0 == 0)
            parts.append(f'<line x1="{x:.1f}" y1="35" x2="{x:.1f}" y2="{40 if cut else ly-10}" class="cstem"/>')
        for t in c.get("ticks", []):
            parts.append(f'<text x="{X(t):.1f}" y="92" text-anchor="middle" class="cn2">{t}</text>')
        svg = f'<svg viewBox="0 0 {W} 96" width="100%" role="img" aria-label="{esc(c["title"])}">{"".join(parts)}</svg><ol class="tl">{"".join(rows)}</ol>'
    elif c["kind"] == "ring":
        import math
        months = c["months"]; n = len(months); cx = cy = 210; r0, r1 = 118, 160
        parts = []
        for i, (name, mean) in enumerate(months):
            a0 = -math.pi/2 + 2*math.pi*i/n + .012; a1 = -math.pi/2 + 2*math.pi*(i+1)/n - .012
            p = lambda r, a: f"{cx + r*math.cos(a):.1f},{cy + r*math.sin(a):.1f}"
            d = f"M{p(r1,a0)} A{r1},{r1} 0 0 1 {p(r1,a1)} L{p(r0,a1)} A{r0},{r0} 0 0 0 {p(r0,a0)} Z"
            st = c.get("stories", {}).get(name, "")
            base = c.get("starts", [None]*n)[i]
            body = month_body(c, i, name, base, st)
            hue = (135 + 330 * i / (n - 1)) % 360
            parts.append(f'<path d="{d}" class="cseg hit" style="fill:oklch(.62 .11 {hue:.0f})"{pop(f"{name}, {mean}", body)}/>')
            am = (a0 + a1) / 2; tx, ty = cx + 174*math.cos(am), cy + 174*math.sin(am)
            anchor = "start" if math.cos(am) > .15 else ("end" if math.cos(am) < -.15 else "middle")
            parts.append(f'<text x="{tx:.1f}" y="{ty+4:.1f}" text-anchor="{anchor}" class="cl">{esc(mean)}</text>')
            nx, ny = cx + (r0+r1)/2*math.cos(am), cy + (r0+r1)/2*math.sin(am)
            parts.append(f'<text x="{nx:.1f}" y="{ny+4:.1f}" text-anchor="middle" class="cvin">{i+1}</text>')
        parts.append(f'<text x="{cx}" y="{cy-6}" text-anchor="middle" class="cbig">19</text><text x="{cx}" y="{cy+18}" text-anchor="middle" class="cn2">months of 19 days</text><text x="{cx}" y="{cy+32}" text-anchor="middle" class="cn2">plus Ayyám-i-Há</text>')
        svg = f'<svg viewBox="-60 0 540 420" width="100%" role="img" aria-label="{esc(c["title"])}">{"".join(parts)}</svg>'
    elif c["kind"] == "map":
        import math
        M = USMAP; W, H = M["w"], M["h"]
        items = [dict(name=n, x=M["places"][n][0], y=M["places"][n][1], story=st, feat=False) for n, st in c.get("reports", [])]
        for pl in c["places"]:
            x, y = M["places"][pl[0]]
            items.append(dict(name=pl[0], x=x, y=y, story=pl[2] if len(pl) > 2 else "", feat=True, lab=pl[1], side=pl[3] if len(pl) > 3 else ("end" if x > W * .6 else "start")))
        def cluster(its, R):
            cs = []
            for it in sorted(its, key=lambda t: not t["feat"]):
                for cl in cs:
                    if math.hypot(it["x"] - cl[0]["x"], it["y"] - cl[0]["y"]) < R: cl.append(it); break
                else: cs.append([it])
            return cs
        def body(cl): return "\n\n".join(f'{m["name"]}. {m["story"]}' for m in cl) if len(cl) > 1 else cl[0]["story"]
        def draw(cl, X, Y, lab=False):
            head = cl[0]; x, y = X(head["x"]), Y(head["y"]); n = len(cl)
            if head["feat"]:
                dx = -9 if head["side"] == "end" else 9
                t = head["lab"] + (f" and {n-1} nearby" if n > 1 else "")
                badge = f'<text x="{x}" y="{y+3.6}" text-anchor="middle" class="ccnt">{n}</text>' if n > 1 else ""
                return f'<g class="hit pin"{pop(t, body(cl))}><circle cx="{x:.1f}" cy="{y:.1f}" r="13" class="ghost"/><circle cx="{x:.1f}" cy="{y:.1f}" r="{9.6 if n > 1 else 8}" class="cdot big"/>{badge}<text x="{x+dx*(1.4 if n > 1 else 1.15):.0f}" y="{y+4:.0f}" text-anchor="{head["side"]}" class="cl on">{esc(head["lab"])}</text></g>'
            short = lambda m: m["name"].split(",")[0].replace(" County", " Co.")
            if n == 1:
                tl = (f'<text x="{x-10.5:.1f}" y="{y+4:.1f}" text-anchor="end" class="cil">' if x > lab else f'<text x="{x+10.5:.1f}" y="{y+4:.1f}" class="cil">') + esc(short(head)) + '</text>' if lab else ""
                return f'<g class="hit pin rep"{pop(head["name"], head["story"])}><circle cx="{x:.1f}" cy="{y:.1f}" r="9" class="ghost"/><circle cx="{x:.1f}" cy="{y:.1f}" r="6" class="crep"/>{tl}</g>'
            cx = sum(X(m["x"]) for m in cl) / n; cy = sum(Y(m["y"]) for m in cl) / n; r = 8.1 + 2.2 * math.sqrt(n)
            return f'<g class="hit pin rep"{pop(f"{n} communities", body(cl))}><circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r+4:.1f}" class="ghost"/><circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" class="cclu"/><text x="{cx:.1f}" y="{cy+3.8:.1f}" text-anchor="middle" class="ccnt">{n}</text>{(f'<text x="{cx-r-5:.1f}" y="{cy+4:.1f}" text-anchor="end" class="cil">' if cx > lab else f'<text x="{cx+r+5:.1f}" y="{cy+4:.1f}" class="cil">') + esc(" · ".join(short(m) for m in cl)) + '</text>' if lab else ""}</g>'
        I = lambda v: v
        regs = "".join(f'<path d="{r["d"]}" class="rf hit t{r["tone"]}" data-click{pop(r["name"] + " region", ", ".join(r["states"]) + ".")}/>' for r in USREG["regions"])
        rnames = "".join(f'<text x="{r["label"][0]}" y="{r["label"][1]}" class="rn">{esc(r["name"])}</text>' for r in USREG["regions"])
        parts = ['<use href="#usmap"/>', f'<g class="creg">{regs}<path d="{USMAP["states"]}" class="cstate"/><path d="{USREG["inner"]}" class="rb"/>{rnames}</g>']; insets = c.get("insets", []); used = set(); panels = []
        PW, PH, GAP, TOP = 290, 170, 20, H + 34
        for j, (ititle, names) in enumerate(insets):
            mem = [it for it in items if it["name"] in names]; used |= {m["name"] for m in mem}
            xs = [m["x"] for m in mem]; ys = [m["y"] for m in mem]
            bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys); cxm, cym = (bx0 + bx1) / 2, (by0 + by1) / 2
            MW = 168; k = min((MW - 30) / max(bx1 - bx0, 1), (PH - 56) / max(by1 - by0, 1), 60)
            hw, hh = PW / 2 / k, PH / 2 / k
            px = j * (PW + GAP); py = TOP
            parts.append(f'<rect x="{cxm-hw:.1f}" y="{cym-hh:.1f}" width="{2*hw:.1f}" height="{2*hh:.1f}" class="cibox"/>')
            parts.append(f'<path d="M{cxm-hw:.1f},{cym+hh:.1f} L{px:.1f},{py:.1f} M{cxm+hw:.1f},{cym+hh:.1f} L{px+PW:.1f},{py:.1f}" class="cilead"/>')
            X = lambda v, cxm=cxm, k=k, px=px: px + MW / 2 + (v - cxm) * k
            Y = lambda v, cym=cym, k=k, py=py: py + PH / 2 + (v - cym) * k
            g = [f'<clipPath id="ci{j}"><rect x="{px}" y="{py}" width="{PW}" height="{PH}"/></clipPath><g clip-path="url(#ci{j})"><rect x="{px}" y="{py}" width="{PW}" height="{PH}" class="cipanel"/><use href="#usmap" transform="translate({px + MW/2 - cxm*k:.2f},{py + PH/2 - cym*k:.2f}) scale({k:.3f})" class="cizoom"/>']
            mem = sorted(mem, key=lambda m: (m["y"], m["x"]))
            P2 = [[X(m["x"]), Y(m["y"])] for m in mem]
            for _ in range(60):
                for a_ in range(len(P2)):
                    for b_ in range(a_ + 1, len(P2)):
                        ddx = P2[b_][0] - P2[a_][0]; ddy = P2[b_][1] - P2[a_][1]; dd = math.hypot(ddx, ddy) or .01
                        if dd < 15: f_ = (15 - dd) / 2 / dd; P2[a_][0] -= ddx * f_; P2[a_][1] -= ddy * f_; P2[b_][0] += ddx * f_; P2[b_][1] += ddy * f_
            for q, m in enumerate(mem):
                x, y = P2[q]
                g.append(f'<g class="hit pin rep"{pop(m["name"], m["story"])}><circle cx="{x:.1f}" cy="{y:.1f}" r="9" class="ghost"/><circle cx="{x:.1f}" cy="{y:.1f}" r="7.8" class="cclu"/><text x="{x:.1f}" y="{y+3.4:.1f}" text-anchor="middle" class="ccnt cn9">{q+1}</text></g>'
                         f'<g class="hit"{pop(m["name"], m["story"])}><rect x="{px+MW}" y="{py+34+q*14.5:.1f}" width="{PW-MW-6}" height="14" class="ghost"/><text x="{px+MW+4}" y="{py+45+q*14.5:.1f}" class="cil"><tspan class="cin9">{q+1}</tspan> {esc(m["name"].split(",")[0].replace("County South", "South").replace(" County", " Co."))}</text></g>')
            g.append(f'</g><rect x="{px}" y="{py}" width="{PW}" height="{PH}" class="ciframe"/><text x="{px+10}" y="{py+20}" class="cit">{esc(ititle)}</text>')
            panels.append("".join(g))
        LBL = c.get("labels", {})
        for cl in cluster([it for it in items if it["name"] not in used], 15):
            parts.append(draw(cl, I, I))
            hd = cl[0]
            if hd["feat"]: continue
            key = hd["name"]; t, side = LBL.get(key, (None, None)) if isinstance(LBL.get(key), (list, tuple)) else (LBL.get(key), None)
            if t is None: continue
            n = len(cl); cx = sum(m["x"] for m in cl) / n; cy = sum(m["y"] for m in cl) / n
            r = (8.1 + 2.2 * math.sqrt(n)) if n > 1 else 6
            side = side or ("end" if cx > W * .62 else "start")
            if side in ("above", "below"): tx, ty, anc = cx, (cy - r - 5 if side == "above" else cy + r + 12), "middle"
            else: tx, ty, anc = cx + (-(r + 5) if side == "end" else (r + 5)), cy + 4, side
            parts.append(f'<text x="{tx:.1f}" y="{ty:.1f}" text-anchor="{anc}" class="cml">{esc(t)}</text>')
        tot = TOP + PH + 6 if insets else H + 10
        svg = f'<svg viewBox="-10 -6 {W + 20} {tot + 6}" width="100%" role="img" aria-label="{esc(c["title"])}">{"".join(parts)}{"".join(panels)}</svg>'
        if c.get("reports"): svg += '<p class="key"><span><i></i>In this issue</span><span><i class="g"></i>Reported to the National Assembly</span></p>'
    hint = ""
    return f'<figure class="chart{size_cls(c)}"{size_sty(c)}>{title}{svg}{note}{hint}</figure>'

def concept_html(c):
    """Diagrams for ideas rather than numbers. Every part can open the shared popup."""
    import math
    kind = c["form"]; W = 600; P = []
    if kind == "ring":
        import math as _m
        st = c["steps"]; n = len(st); R = 170; SW = 52; gap = 6; lo = .22; lw = .4
        def pt(r, deg): t = _m.radians(deg - 90); return 300 + r * _m.cos(t), 300 + r * _m.sin(t)
        P2 = []
        for i, (l, _) in enumerate(st):
            a0, a1 = i * 360 / n + gap / 2, (i + 1) * 360 / n - gap / 2
            (x0, y0), (x1, y1) = pt(R, a0), pt(R, a1)
            on = f'<animate attributeName="opacity" dur="16s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;{i/n:.4f};{(i+1)/n:.4f}" values="{lo};1;{lo}"/>' if i else f'<animate attributeName="opacity" dur="16s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;{1/n:.4f}" values="1;{lo}"/>'
            seg = f'M{x0:.1f},{y0:.1f} A{R},{R} 0 0,1 {x1:.1f},{y1:.1f}'
            P2.append(f'<path d="{seg}" class="wseg" opacity="{lo}"/>')
            k0, k1 = i / n, (i + 1) / n
            if i == 0:
                vis = f'<animate attributeName="opacity" dur="16s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;{k1:.4f}" values="1;0"/>'
                dash = f'<animate attributeName="stroke-dashoffset" dur="16s" repeatCount="indefinite" keyTimes="0;{k1:.4f};1" values="1;0;0"/>'
            else:
                vis = f'<animate attributeName="opacity" dur="16s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;{k0:.4f};{k1:.4f}" values="0;1;0"/>'
                dash = f'<animate attributeName="stroke-dashoffset" dur="16s" repeatCount="indefinite" keyTimes="0;{k0:.4f};{k1:.4f};1" values="1;1;0;0"/>'
            P2.append(f'<path d="{seg}" pathLength="1" class="wseg wfill" stroke-dasharray="1 1" stroke-dashoffset="{0 if i == 0 else 1}" opacity="{1 if i == 0 else 0}">{vis}{dash}</path>')
            mid = (a0 + a1) / 2; tx, ty = pt(R + SW / 2 + 22, mid); anc = "start" if 0 < mid < 180 else "end"
            nx, ny = pt(R, (a0 + a1) / 2)
            onw = on.replace(f'values="{lo};1;{lo}"', f'values="{lw};1;{lw}"').replace(f'values="1;{lo}"', f'values="1;{lw}"')
            P2.append(f'<text x="{tx:.1f}" y="{ty + 13:.1f}" text-anchor="{anc}" class="wword" opacity="{lw}">{esc(l)}{onw}</text>')

        P2.append(f'<circle cx="300" cy="300" r="{R-SW/2-14}" class="whair"/>')
        ring = f'<svg class="rsvg" viewBox="-70 70 740 460" aria-hidden="true">{"".join(P2)}</svg>'
        cols = "".join(f'<li{" class=on" if i == 0 else ""}><h5>{esc(l)}</h5><p>{esc(t)}</p></li>' for i, (l, t) in enumerate(st))
        return f'<figure class="chart concept ringf{size_cls(c)}"{size_sty(c)}><p class="ct">{esc(c["title"])}</p><div class="rwrap">{ring}<ol class="rcols">{cols}</ol></div></figure>'
    arrow = '<defs><marker id="ah{i}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" class="carr"/></marker></defs>'.format(i=id(c) % 100000)
    mk = f'url(#ah{id(c) % 100000})'
    arrow += '<defs><marker id="aa{i}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10z" class="cb"/></marker></defs>'.format(i=id(c) % 100000)
    mka = f'url(#aa{id(c) % 100000})'
    def lines(txt, x, y, cls="cl", anchor="middle", lh=17):
        return "".join(f'<text x="{x}" y="{y + k*lh}" text-anchor="{anchor}" class="{cls}">{esc(t)}</text>' for k, t in enumerate(txt.split("|")))
    H = 300
    if kind == "rings":
        rs = c["rings"]; n = len(rs); cx, cy = 300, 175; step = 160 / n; H = 350
        for i in range(n - 1, -1, -1):
            lab, story = rs[i]; R = step * (i + 1)
            P.append(f'<circle cx="{cx}" cy="{cy}" r="{R:.1f}" class="carea hit cringf" style="fill:color-mix(in oklab,var(--accent) {100 - i*(78/max(1,n-1)):.0f}%,var(--paper))"{pop(lab, story)}/>')
        for i, (lab, story) in enumerate(rs):
            R0 = step * i; R1 = step * (i + 1); y = cy if i == 0 else cy - (R0 + R1)/2
            P.append(lines(lab, cx, y + (4 if i == 0 else 5) - (8 if "|" in lab else 0), "cring cin" if i == 0 else "cring", lh=15))
    elif kind == "arches":
        rs = c["rings"]; n = len(rs); cols = c.get("colors", []); cx, base = 300, 262; W = 600; H = 280
        for i in range(n - 1, -1, -1):
            lab, story = rs[i]; r = 78 + i * 72; col = cols[i] if i < len(cols) else "var(--accent)"
            P.append(f'<path d="M{cx-r},{base} A{r},{r} 0 0 1 {cx+r},{base} Z" class="hit" style="fill:{col}"{pop(lab, story)}/>')
        for i, (lab, story) in enumerate(rs):
            r = 78 + i * 72; y = base - (r * .45 if i == 0 else r - 34)
            P.append(lines(lab, cx, y, "cring" + (" cin" if i == 0 else ""), lh=15))
        P.append(f'<line x1="{cx-300}" y1="{base}" x2="{cx+300}" y2="{base}" class="cground"/>')
    elif kind == "stepper":
        st = c["steps"]; n = len(st); thr = c.get("threshold"); W = 600; gap = 66; H = 30 + n * gap
        P.append(f'<line x1="56" y1="26" x2="56" y2="{30 + (n-1)*gap}" class="cspine"/>')
        for i, s_ in enumerate(st):
            lab, story = s_[0], s_[1]; y = 30 + i * gap; past = thr is not None and i >= thr
            P.append(f'<g class="hit"{pop(lab.replace("|", " "), story)}><rect x="20" y="{y-24}" width="560" height="{gap-6}" class="ghost"/>'
                     f'<circle cx="56" cy="{y}" r="{14 if past else 11}" class="{"cdot" if past else "cdotm"}"/><text x="56" y="{y+4.5}" text-anchor="middle" class="cvin">{i+1}</text>'
                     f'<text x="90" y="{y+6}" class="cstl{" on" if past else ""}">{esc(lab.replace("|", " "))}</text></g>')
            if thr is not None and i == thr - 1:
                yy = y + gap / 2
                P.append(f'<line x1="20" y1="{yy}" x2="580" y2="{yy}" class="cthr"/><text x="580" y="{yy+16}" text-anchor="end" class="cthrl">{esc(c.get("threshold_label","threshold"))}</text>')
        H = 30 + (n - 1) * gap + 30
    elif kind == "overlap":
        st = c["strands"]; W = 600; H = 300; cs = [(250, 105), (350, 105), (300, 192)]
        for (x, y), (lab, story) in zip(cs, st):
            P.append(f'<circle cx="{x}" cy="{y}" r="88" class="carea hit cven"{pop(lab.replace("|"," "), story)}/>')
        for (x, y), (lab, _), (dx, dy) in zip(cs, st, [(-62, -30), (62, -30), (0, 48)]):
            P.append(lines(lab, x + dx, y + dy, "cring", lh=15))
        jl, js = c["joined"]
        P.append(f'<g class="hit"{pop(jl.replace("|"," "), js)}><circle cx="300" cy="134" r="30" class="ghost"/>{lines(jl, 300, 130, "cv", lh=16)}</g>')
    elif kind == "chevrons":
        st = c["steps"]; n = len(st); W = 620; cw = W / n; H = 110
        for i, s_ in enumerate(st):
            lab, story = s_[0], s_[1]; x = i * cw
            d = f"M{x+(0 if i == 0 else 0)},10 h{cw-20} l20,45 l-20,45 h{-(cw-20)}" + (" l20,-45 Z" if i else " Z")
            P.append(f'<g class="hit"{pop(lab.replace("|"," "), story)}><path d="{d}" class="carea" style="opacity:{.38 + .62*i/max(1,n-1):.2f}"/>{lines(lab, x + cw/2 + (8 if i else 0), 52 - (8 if "|" in lab else 0), "cring cin", lh=16)}</g>')
    elif kind == "twoway":
        # one band between people and technology; which way the weight runs is the difference
        W = 600; H = 230; P2 = []
        uid = id(c) % 100000
        P2.append(f'<defs><marker id="tw{uid}" viewBox="0 0 10 10" refX="2" refY="5" markerWidth="28" markerHeight="28" markerUnits="userSpaceOnUse" orient="auto"><path d="M0 0L10 5L0 10z" class="cb"/></marker>'
                  f'<marker id="tx{uid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="9" markerHeight="9" markerUnits="userSpaceOnUse" orient="auto"><path d="M0 0L10 5L0 10z" class="carr"/></marker></defs>')
        for k, (title, story, sub) in enumerate(c["panels"]):
            y = 26 + k * 112
            fwd = k == 1
            big = f'<line x1="{160 if fwd else 440}" y1="{y+38}" x2="{420 if fwd else 180}" y2="{y+38}" class="twb" marker-end="url(#tw{uid})"/>'
            small = f'<line x1="{450 if fwd else 150}" y1="{y+64}" x2="{150 if fwd else 450}" y2="{y+64}" class="cline{"" if fwd else " twd"}" marker-end="url(#tx{uid})"/>'
            P2.append(f'<g class="hit"{pop(title, story)}><rect x="0" y="{y-14}" width="{W}" height="104" class="ghost"/>'
                      f'<text x="40" y="{y}" class="twk">{esc(title)}</text>'
                      f'<text x="40" y="{y+44}" class="cv">People</text><text x="{W-40}" y="{y+44}" text-anchor="end" class="cv">Technology</text>'
                      f'{big}{small}<text x="{W/2}" y="{y+86}" text-anchor="middle" class="cl">{esc(sub)}</text></g>')
        P.extend(P2)
    elif kind == "contrast":
        H = (326 if any(len(p) > 3 and len(p[3]) > 2 for p in c["panels"]) else 262) if any(len(p) > 3 for p in c["panels"]) or c.get("arrows") else 250
        for k, panel in enumerate(c["panels"]):
            title, story, sch = panel[:3]; ox = k * 310; cx, cy = ox + 145, 100
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
                    if c.get("arrows"):
                        L = math.hypot(dx, dy); ux, uy = dx/L, dy/L
                        g.append(f'<line x1="{cx+dx+ux*30:.1f}" y1="{cy+dy+uy*30:.1f}" x2="{cx+dx+ux*56:.1f}" y2="{cy+dy+uy*56:.1f}" class="cpull" marker-end="{mka}"/>')
                g.append(f'<line x1="{cx-40}" y1="{cy-10}" x2="{cx-12}" y2="{cy+18}" class="cline" marker-start="{mk}" marker-end="{mk}"/><line x1="{cx+40}" y1="{cy-10}" x2="{cx+12}" y2="{cy+18}" class="cline" marker-start="{mk}" marker-end="{mk}"/>')
            elif sch == "whole":
                g.append(f'<circle cx="{cx}" cy="{cy}" r="80" class="carea" style="opacity:.25"/>')
                if c.get("arrows"):
                    for dx, dy in [(-34,-18),(0,32),(34,-18)]:
                        L = math.hypot(dx, dy); ux, uy = dx/L, dy/L
                        g.append(f'<line x1="{cx+ux*112:.1f}" y1="{cy+uy*112:.1f}" x2="{cx+ux*86:.1f}" y2="{cy+uy*86:.1f}" class="cpull" marker-end="{mka}"/>')
                for dx, dy in [(-34,-18),(0,32),(34,-18)]: g.append(f'<circle cx="{cx+dx}" cy="{cy+dy}" r="30" class="carea" style="opacity:.6"/>')
            elif sch == "oneway":
                g.append(f'<rect x="{cx-110}" y="{cy-26}" width="80" height="52" class="carea" style="opacity:.6"/><line x1="{cx-24}" y1="{cy}" x2="{cx+60}" y2="{cy}" class="cline" marker-end="{mk}"/><circle cx="{cx+78}" cy="{cy}" r="10" class="cdot"/>')
            elif sch == "loop":
                pts = [(cx + 62*math.cos(t), cy + 62*math.sin(t)) for t in [-math.pi/2, 0, math.pi/2, math.pi]]
                for i in range(4):
                    a = pts[i]; b = pts[(i+1) % 4]
                    g.append(f'<path d="M{a[0]+(b[0]-a[0])*.22:.1f},{a[1]+(b[1]-a[1])*.22:.1f} Q{cx+(a[0]+b[0]-2*cx)*.9:.1f},{cy+(a[1]+b[1]-2*cy)*.9:.1f} {a[0]+(b[0]-a[0])*.78:.1f},{a[1]+(b[1]-a[1])*.78:.1f}" class="cline" marker-end="{mk}"/>')
                for x, y in pts: g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="10" class="cdot"/>')
            word = panel[3] if len(panel) > 3 else None
            label = (f'<text x="{cx}" y="22" text-anchor="middle" class="cpre">{esc(word[0])}</text><text x="{cx}" y="84" text-anchor="middle" class="cword{" hollow" if k == 0 else ""}">{esc(word[1])}</text>' + (f'<text x="{cx}" y="112" text-anchor="middle" class="csubw">{esc(word[2])}</text>' if len(word) > 2 else '')) if word else lines(title, cx, 238 if c.get("arrows") else 206, "cv")
            P.append(f'<g class="hit"{pop(title.replace("|"," "), story)}><rect x="{ox}" y="0" width="290" height="{H}" class="cpanel"/>{(f'<g transform="translate(0 112)">' + "".join(g) + '</g>') if word else "".join(g)}{label}</g>')
    elif kind == "spectrum":
        pts = c["points"]; n = len(pts); x0, x1 = 60, 560; y = 40; H = 120
        P.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" class="cline" marker-end="{mk}"/>')
        for i, (lab, story) in enumerate(pts):
            x = x0 + (x1 - x0 - 70) * i / (n - 1); on = i == n - 1
            P.append(f'<g class="hit"{pop(lab.replace("|"," "), story)}><circle cx="{x:.1f}" cy="{y}" r="20" class="ghost"/><circle cx="{x:.1f}" cy="{y}" r="{12 if on else 8}" class="{"cdot" if on else "cdotm"}"/>{lines(lab, round(x,1), y + 36, "cv" if on else "cl")}</g>')
    svg = f'<svg viewBox="0 -10 {W} {H + 10}" width="100%" role="img" aria-label="{esc(c["title"])}">{arrow}{"".join(P)}</svg>'
    title = (f'<p class="cno">No. {c["no"]}</p>' if c.get("no") else "") + f'<p class="ct">{esc(c["title"])}</p>'; note = f'<p class="cn">{esc(c["note"])}</p>' if c.get("note") else ""
    return f'<figure class="chart concept{size_cls(c)}"{size_sty(c)}>{title}{svg}{note}</figure>'

def after_first(h, extra):
    """Place a block right after the first paragraph of a story."""
    i = h.find("</p>")
    return h[:i + 4] + extra + h[i + 4:] if i >= 0 else extra + h

def first_para_dropcap(h):
    return h.replace("<p>", '<p class="first">', 1)

# ------------------------------------------------------------------ TAB (the published site)
SHARE_ICONS = {
 "copy": '<path d="M10 14a4 4 0 0 0 5.66 0l3-3a4 4 0 0 0-5.66-5.66l-1.2 1.2M14 10a4 4 0 0 0-5.66 0l-3 3a4 4 0 0 0 5.66 5.66l1.2-1.2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
 "facebook": '<path d="M13.4 21v-7.6h2.6l.4-3h-3V8.5c0-.9.3-1.5 1.5-1.5h1.6V4.3c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4v2.2H7.7v3h2.6V21z"/>',
 "x": '<path d="M4 4h4.6l3.9 5.3L17.2 4h2.3l-6 6.9L20.2 20h-4.6l-4.2-5.7L6.3 20H4l6.4-7.3zm3 1.4 9.6 13.2h1.3L8.4 5.4z"/>',
 "linkedin": '<circle cx="6.2" cy="6.2" r="1.9"/><path d="M4.6 9.2h3.2V20H4.6zM10 9.2h3.1v1.5c.5-.9 1.6-1.8 3.3-1.8 3.4 0 4 2.2 4 5V20h-3.2v-5.4c0-1.3 0-2.9-1.8-2.9s-2.1 1.4-2.1 2.8V20H10z"/>',
 "whatsapp": '<path d="M12 3.6a8.4 8.4 0 0 0-7.2 12.7L3.7 20.3l4.1-1.1A8.4 8.4 0 1 0 12 3.6z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><path d="M9.3 7.9c.2 0 .4 0 .6.4l.8 1.9c.1.2 0 .4-.1.6l-.5.6c-.1.2-.2.3 0 .6.5.9 1.5 2 2.8 2.6.3.1.4.1.6-.1l.6-.8c.2-.2.4-.2.6-.1l1.8.9c.3.1.4.3.4.4 0 .6-.3 1.4-1 1.8-.7.4-1.8.5-3.6-.3-2.2-1-3.7-3.2-4-3.6-.3-.4-1-1.5-1-2.8 0-1.2.7-1.8 1-2.1.2-.1.4-.1.6-.1z"/>',
 "telegram": '<path d="M20.6 4.2 2.9 11c-.9.4-.9 1.4 0 1.7l4.4 1.4 1.7 5.3c.2.7 1 .8 1.5.4l2.5-2.1 4.7 3.4c.6.4 1.4.1 1.5-.6l2.9-14.3c.2-.8-.6-1.4-1.5-1zM9.6 14.4l8.3-6.9-6.6 7.7-.3 3.1z"/>',
 "email": '<rect x="3.5" y="5.5" width="17" height="13" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="m4 7 8 6 8-6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>',
}
def share(a):
    """Opens the shared share sheet for this feature."""
    return (f'<button class="sharebtn" type="button" data-share="{a["slug"]}" data-title="{esc(a["title"])}" aria-haspopup="dialog">'
            '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v12M7.5 7.5 12 3l4.5 4.5M5 12v7.5h14V12" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
            '<span>Share this story</span></button>')
SHARE_HTML = ('<dialog class="sharedlg" aria-labelledby="share-h"><div class="shd"><p class="shk">Share</p><h2 id="share-h"></h2>'
    '<button class="shx" type="button" aria-label="Close"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button></div><ul class="shl">'
    + "".join(f'<li><{"button type=button" if k == "copy" else "a target=_blank rel=noopener"} class="sho" data-k="{k}"><span class="shi"><svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor">{p}</svg></span><span class="shn">{n}</span></{"button" if k == "copy" else "a"}></li>'
              for k, n, p in [(k, n, SHARE_ICONS[k]) for k, n in [("copy","Copy link"),("facebook","Facebook"),("x","X"),("linkedin","LinkedIn"),("whatsapp","WhatsApp"),("telegram","Telegram"),("email","Email")]])
    + '</ul><p class="shst" role="status" aria-live="polite"></p></dialog>')
SHARE_JS = r"""<script>
(function(){var d=document.querySelector('.sharedlg');if(!d||!d.showModal)return;var h=d.querySelector('#share-h'),st=d.querySelector('.shst'),url='',title='',opener=null;
  var mk={facebook:function(u,t){return 'https://www.facebook.com/sharer/sharer.php?u='+u},x:function(u,t){return 'https://x.com/intent/post?url='+u+'&text='+t},
    linkedin:function(u){return 'https://www.linkedin.com/sharing/share-offsite/?url='+u},whatsapp:function(u,t){return 'https://wa.me/?text='+t+'%20'+u},
    telegram:function(u,t){return 'https://t.me/share/url?url='+u+'&text='+t},email:function(u,t){return 'mailto:?subject='+t+'&body='+t+'%0A%0A'+u}};
  document.addEventListener('click',function(e){var b=e.target.closest('.sharebtn');if(!b)return;opener=b;
    url=location.href.split('#')[0]+'#'+b.dataset.share;title=b.dataset.title+' · The American Bahá’í';h.textContent=b.dataset.title;st.textContent='';
    var u=encodeURIComponent(url),t=encodeURIComponent(title);[].forEach.call(d.querySelectorAll('a.sho'),function(a){a.href=mk[a.dataset.k](u,t);if(a.dataset.k==='email')a.removeAttribute('target')});
    d.showModal();});
  d.querySelector('.shx').addEventListener('click',function(){d.close()});
  d.addEventListener('click',function(e){if(e.target===d)d.close()});
  d.addEventListener('close',function(){if(opener)opener.focus()});
  d.querySelector('[data-k=copy]').addEventListener('click',function(){var done=function(){st.textContent='Link copied'};
    if(navigator.clipboard)navigator.clipboard.writeText(url).then(done,function(){st.textContent=url});else st.textContent=url;});
})();
</script>"""

SURVEY_FORM = "https://form.typeform.com/to/NfIWSbQl"
SVY_HTML = ('<dialog class="svydlg" aria-labelledby="svy-h"><div class="svh"><div><p class="shk">Reader survey</p><h2 id="svy-h">Shape the future of The American Bahá’í</h2></div>'
    '<button class="shx" type="button" aria-label="Close the survey"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button></div>'
    '<div class="svf"><iframe title="TAB Reader Survey" allow="camera; microphone; autoplay; encrypted-media; fullscreen" data-src="' + SURVEY_FORM + '?typeform-medium=embed-snippet"></iframe></div></dialog>')
SVY_JS = r"""<script>
(function(){var d=document.querySelector('.svydlg');if(!d||!d.showModal)return;var f=d.querySelector('iframe'),opener=null;
  function open(o){opener=o||null;if(!f.src)f.src=f.dataset.src;if(!d.open)d.showModal();}
  document.addEventListener('click',function(e){var b=e.target.closest('[data-survey]');if(!b)return;e.preventDefault();open(b);});
  d.querySelector('.shx').addEventListener('click',function(){d.close()});
  d.addEventListener('click',function(e){if(e.target===d)d.close()});
  d.addEventListener('close',function(){if(location.hash==='#survey')history.replaceState(null,'',location.pathname+location.search);if(opener)opener.focus()});
  function hash(){if(location.hash==='#survey')open();}
  addEventListener('hashchange',hash);hash();
})();
</script>"""

ASK_Q = ["What do you enjoy reading most?", "Which stories, ideas and resources matter to you?", "What should we write about next?"]
_ns = {}
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "nsadd.py")).read(), _ns)  # the landing's Badí‘ calendar, shared
CAL_HTML = _ns["calendar_html"]()
_c = _ns["CSS_ADD"]; _i = _c.index("/* dateline above the header */"); CAL_CSS = (_c[_i:_c.index("/*", _i + 10)] + ".dl .wrap{max-width:1120px}@media (max-width:1023px){.head .in>.dl{order:2;margin-left:auto}.head .rh{order:1}.head .rht{order:3}}.head .in>nav{min-width:0;flex:0 1 auto;overflow-x:auto;scrollbar-width:none}.head .in>nav::-webkit-scrollbar{display:none}@media (max-width:1180px){.head .in>.dl .bd{font-size:0}.head .in>.dl .bd b{font-size:13px}}.head .dl,.rhd .dl{position:static;background:none;border:0;flex:none;margin-left:14px;font-size:12.5px}.dl summary .dr{display:inline-flex;padding:0!important;max-width:none;min-height:0;gap:6px;width:auto;justify-content:flex-start}.head .dl{align-self:center}.head .dl .gd,.head .dl .nx,.rhd .dl .gd,.rhd .dl .nx{display:none}.dl .bd{font:400 13px var(--ui);letter-spacing:0;text-transform:none;color:var(--ink)}.dl .tg{font-size:0;gap:0;margin-left:0!important}.dl .bd{margin-right:0!important}.dl .tg svg{width:12px;height:12px}.dl summary{display:inline-block;border-radius:999px;padding:5px 10px;border:1px solid var(--rule)}.dl summary:hover{border-color:var(--ink)}.dl .panel{position:fixed;left:0;right:0;top:58px;z-index:40;background:var(--bar)!important;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);box-shadow:0 18px 36px -18px rgba(29,26,22,.35);text-transform:none;letter-spacing:0}.rhd .r{align-items:center}@media (max-width:700px){.rhd .r .n{display:none}.dl .bd{font-size:0}.dl .bd b{font-size:12.5px}.dl summary{padding:4px 8px}.head .dl,.rhd .dl{margin-left:6px}.dl .panel{top:55px;max-height:calc(100dvh - 55px);overflow:auto}}\n").replace("var(--card)", "var(--bar)")
CHIP_JS = "<script>(function(){var D=document.querySelector('.head .dl');if(!D)return;var HP=D.parentNode,HA=D.nextSibling,H=document.documentElement;\nfunction mv(){var R=document.querySelector('.rhd .r');if(!R)return;var rh=R.parentNode;rh.removeAttribute('aria-hidden');var want=H.classList.contains('rhon')?R:HP;if(D.parentNode!==want){D.open=false;if(want===R)R.insertBefore(D,R.firstChild);else HP.insertBefore(D,HA)}}\nvar q=0;addEventListener('scroll',function(){if(!q){q=1;requestAnimationFrame(function(){q=0;mv()})}},{passive:true});\ndocument.addEventListener('click',function(e){if(D.open&&!D.contains(e.target))D.open=false});\ndocument.addEventListener('keydown',function(e){if(e.key==='Escape'&&D.open){D.open=false;D.querySelector('summary').focus()}});mv()})();</script>"
FI2_CSS = ".fih{margin:40px 0 14px;color:var(--mem)}.fi2{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:6px 28px}.fi2 a{display:grid;gap:3px;padding:12px 0 14px;border-top:2px solid var(--mem);text-decoration:none;color:inherit}.fi2 .kk{font:600 14.5px/1.25 var(--ui);color:var(--ink)}.fi2 .t{font:italic 300 16px/1.35 var(--text);color:var(--mute)}.fi2 a:hover .kk,.fi2 a:focus-visible .kk{color:var(--mem)}@media (max-width:600px){.fi2{grid-template-columns:1fr}}\n"
from endasks import END_CSS, SUB_SECTION
END_ASKS_CSS = ".edask{--card:var(--bar,#fdfcf9);--soft:color-mix(in oklab,var(--ink) 82%,var(--paper))}" + END_CSS + ".edask.sbm{background:var(--bar,#fdfcf9)!important;border-top:0!important}.edask.sbx{background:var(--paper)!important;border-top:1px solid var(--rule)}.edask .wrap{max-width:1120px}"
MAST_CSS = ('.cover .mast .the{font:italic 400 clamp(22px,2.6vw,34px)/1 "Literata",Georgia,serif;letter-spacing:0;margin:0 0 -.12em .06em;color:#b8782e;text-shadow:0 1px 0 rgba(255,255,255,.85),0 -1px 1px rgba(0,0,0,.35)}'
    '.cover h1{color:#25201b;text-shadow:0 1.5px 0 rgba(255,255,255,.85),0 -1px 1px rgba(0,0,0,.45),0 -2px 5px rgba(0,0,0,.08)}'
    '.cover .mast .sub{text-shadow:0 1px 0 rgba(255,255,255,.8)}'
    '@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .cover h1{color:var(--ink);text-shadow:0 1px 0 rgba(0,0,0,.6),0 -1px 1px rgba(255,255,255,.12)}:root:not([data-theme="light"]) .cover .mast .the,:root:not([data-theme="light"]) .cover .mast .sub{text-shadow:none}}'
    ':root[data-theme="dark"] .cover h1{color:var(--ink);text-shadow:0 1px 0 rgba(0,0,0,.6)}:root[data-theme="dark"] .cover .mast .the,:root[data-theme="dark"] .cover .mast .sub{text-shadow:none}')
L_CSS = '\n/* one issue: story color, chapter frames, running head (curated) */\n.story{--ac2:color-mix(in oklab,var(--accent) 55%,#1d1a16)}\n:root[data-theme="dark"] .story{--ac2:color-mix(in oklab,var(--accent) 60%,#fff)}\n@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .story{--ac2:color-mix(in oklab,var(--accent) 60%,#fff)}}\n.story .torn{--a:var(--accent)!important;--b:color-mix(in oklab,var(--accent) 45%,#fff)!important;--c:var(--ac2)!important;--d:color-mix(in oklab,var(--accent) 25%,#fff)!important}\n.story .shead h2{color:var(--ink)}\n.story .prose .pull{border-left-color:var(--accent)}.story .prose .pull p{color:var(--ac2)}\n.story .plate figcaption,.story .prose .photo figcaption{border-left:3px solid var(--accent);padding-left:10px}\n.wrap>.chap+.story{padding-top:0!important}.chap+.story .margin .kicker,.chap+.story .margin .pp{display:none}.chap+.story .margin{row-gap:14px}.chap+.story .margin .by{flex-basis:100%;margin:0!important}\n.index.nb a{display:grid;grid-template-columns:56px minmax(0,1fr);align-items:baseline;gap:4px 14px;font-style:normal}\n.index.nb .nm{grid-row:1/3;font:800 44px/.8 var(--disp);letter-spacing:-.04em;color:var(--c)}\n.index.nb .kk{font:600 11.5px var(--ui);letter-spacing:.14em;text-transform:uppercase;color:var(--c)}\n.index.nb .t{font-family:var(--text);font-style:italic;font-weight:300}\n@media (prefers-color-scheme:dark){:root:not([data-theme=\"light\"]) .index.nb a{--c2:color-mix(in oklab,var(--c) 60%,#fff)}}\n:root[data-theme=\"dark\"] .index.nb a{--c2:color-mix(in oklab,var(--c) 60%,#fff)}\n.index.nb .nm,.index.nb .kk{color:var(--c2,var(--c))}\n.index.nb a:hover .t,.index.nb a:focus-visible .t{color:var(--c)}\n@media (max-width:600px){.index.nb a{grid-template-columns:40px minmax(0,1fr);gap:4px 10px}.index.nb .nm{font-size:34px}}\n.chap{margin-top:clamp(48px,8vw,112px);display:grid;grid-template-columns:auto 1fr auto;align-items:end;gap:6px 22px;border-top:6px solid var(--accent);padding-top:16px;margin:0 0 clamp(28px,4vw,48px);font:600 12px var(--ui);letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}\n.chap .n{font:800 clamp(64px,9vw,120px)/.78 var(--disp);letter-spacing:-.05em;color:var(--accent);grid-row:1/3}\n.chap .k{color:var(--ink);grid-row:1/3;align-self:end}.chap .of{grid-column:3;grid-row:1/3;align-self:end}\n.rhd{position:fixed;top:0;left:0;right:0;z-index:6;height:58px;display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:16px;padding:0 max(20px,env(safe-area-inset-right,0px)) 0 max(20px,env(safe-area-inset-left,0px));background:var(--bar);border-bottom:1px solid var(--barrule,var(--rule));font:600 12px var(--ui);letter-spacing:.12em;text-transform:uppercase;color:var(--mute);visibility:hidden;opacity:0;transition:opacity .25s,visibility .25s}\nhtml.rhon .rhd{visibility:visible;opacity:1}html.rhon .head{visibility:hidden}\n.rhd a{color:inherit;text-decoration:none}.rhd .w{font:700 15px var(--disp);letter-spacing:-.01em;text-transform:none;color:var(--ink)}\n.rhd .t{color:var(--ink);text-transform:none;letter-spacing:0;font:600 14px var(--ui);max-width:56vw;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}\n.rhd .r{justify-self:end;display:flex;gap:16px}.rhd .r a.ci{width:34px;height:34px;display:grid;place-items:center;border-radius:50%;color:var(--ink)}.rhd .r a.ci:hover{background:var(--paper);color:var(--ink)}.rhd .r a.ci svg{width:22px;height:22px;display:block}.rhd .r a:hover,.rhd .w:hover{color:var(--accent)}\n.rhd i{position:absolute;left:0;bottom:-1px;height:3px;width:var(--p,0);background:var(--c,var(--accent))}\n@media (max-width:700px){.rhd{height:55px;grid-template-columns:minmax(0,1fr) auto}.rhd .w{display:none}.rhd .t{max-width:none}}\n@media (prefers-reduced-motion:reduce){.rhd{transition:none}}\n'
NB_CSS = "".join(l + "\n" for l in L_CSS.split("\n") if ".index.nb" in l)
L_JS = '<script>(function(){var S=[].slice.call(document.querySelectorAll(\'article.story\'));if(!S.length)return;var r=document.createElement(\'div\');r.className=\'rhd\';r.setAttribute(\'aria-hidden\',\'true\');\nr.innerHTML=\'<a class="w" href="#top" tabindex="-1">The American Bahá’í</a><span class="t"></span><span class="r"><a class="ci" href="#front" tabindex="-1" aria-label="Contents" title="Contents"><svg viewBox="0 0 24 24" aria-hidden="true"><path stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" fill="none" d="M12 6.5C10 5 7 4.6 3.5 5v13c3.5-.4 6.5 0 8.5 1.5 2-1.5 5-1.9 8.5-1.5V5C17 4.6 14 5 12 6.5zM12 6.5v13"/></svg></a></span><i></i>\';document.body.appendChild(r);\nvar T=r.querySelector(\'.t\'),N=r.querySelector(\'.n\'),H=document.documentElement,q=0;\nfunction u(){q=0;var y=70,c=-1;S.forEach(function(s,i){if(s.getBoundingClientRect().top<y)c=i});var on=c>=0&&S[c].getBoundingClientRect().bottom>y;H.classList.toggle(\'rhon\',on);if(!on)return;\nvar s=S[c],b=s.getBoundingClientRect();T.textContent=s.querySelector(\'.shead h2\').textContent;r.style.setProperty(\'--c\',s.style.getPropertyValue(\'--accent\'));r.style.setProperty(\'--p\',Math.min(100,Math.max(0,(y-b.top)/b.height*100))+\'%\')}\naddEventListener(\'scroll\',function(){if(!q){q=1;requestAnimationFrame(u)}},{passive:true});addEventListener(\'resize\',u);u()})();</script>'
ASK_HTML = ('<div class="askw"><section class="ask" aria-labelledby="ask-h"><div class="askq"><h2 class="askb" id="ask-h">Reader <b>Survey</b></h2>'
    '<p class="askr" aria-live="off">' + ASK_Q[0] + '</p>'
    '<div class="askc">' + "".join(f'<a href="{SURVEY_FORM}" data-survey target="_blank" rel="noopener">{t}</a>' for t in ("Stories", "Ideas", "Resources", "Future topics")) + '</div>'
    f'<div class="askg"><a class="askbtn" href="{SURVEY_FORM}" data-survey target="_blank" rel="noopener">Give feedback</a><span class="askm">Takes 5 minutes</span></div></div>'
    '<div class="aski"><img src="img/motif/m08.webp" alt="" loading="lazy"></div></section></div>')
NUDGE_LINES = [("Tell us what you enjoy reading and share your ideas for future topics.", "Takes 5 minutes."),
               ("Know a story like these?", "Send story ideas, photos and field notes from where you live."),
               ("Have the next stories sent to you.", "By email, as they’re published.")]
NUDGE_HTML = ('<div class="nudge" hidden role="complementary" aria-label="Take part"><span class="ndot"><img src="img/motif/dot03.webp" alt="" loading="lazy"></span>'
    f'<span class="ntx" aria-live="polite"><b>{NUDGE_LINES[0][0]}</b><span class="nl">{NUDGE_LINES[0][1]}</span></span>'
    f'<span class="n3"><a class="on" data-k="0" href="{SURVEY_FORM}" data-survey target="_blank" rel="noopener">Reader survey</a><a data-k="1" href="#" data-submit>Contribute</a><a data-k="2" href="/usbns/magazine/landing/#subscribe" data-subscribe>Subscribe</a></span>'
    '<button class="nx" type="button" aria-label="Dismiss"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 7l10 10M17 7 7 17" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button></div>')
ASK_JS = r"""<script>
(function(){var el=document.querySelector('.askr');if(el&&!matchMedia('(prefers-reduced-motion:reduce)').matches){var Q=""" + __import__("json").dumps(ASK_Q) + r""",i=0;
  setInterval(function(){el.style.opacity=0;setTimeout(function(){i=(i+1)%Q.length;el.textContent=Q[i];el.style.opacity=1},400)},3400);}
  var n=document.querySelector('.nudge');if(!n||!('IntersectionObserver' in window))return;var K='tab-takepart-x',off=false;
  try{off=!!sessionStorage.getItem(K)}catch(e){}if(off)return;
  function stop(){off=true;n.classList.remove('on');setTimeout(function(){n.hidden=true},300);try{sessionStorage.setItem(K,'1')}catch(e){}}
  n.querySelector('.nx').addEventListener('click',stop);var L=""" + __import__("json").dumps(NUDGE_LINES) + r""",C=[].slice.call(n.querySelectorAll('.n3 a')),B=n.querySelector('.ntx b'),S=n.querySelector('.ntx .nl'),cur=0,held=false;function show(k){if(k===cur)return;cur=k;B.textContent=L[k][0];S.textContent=L[k][1];C.forEach(function(c,i){c.classList.toggle('on',i===k)})}C.forEach(function(c,i){c.addEventListener('mouseenter',function(){held=true;show(i)});c.addEventListener('focus',function(){held=true;show(i)});c.addEventListener('mouseleave',function(){held=false});c.addEventListener('blur',function(){held=false})});if(!matchMedia('(prefers-reduced-motion:reduce)').matches)setInterval(function(){if(!held&&n.classList.contains('on'))show((cur+1)%3)},5000);
  var dock=document.getElementById('dock');function place(){var h=(dock&&!dock.hidden&&dock.classList.contains('on'))?dock.querySelector('.dk').getBoundingClientRect().height+14:0;n.style.setProperty('--dh',h+'px')}
  var arts=[].slice.call(document.querySelectorAll('article.story:not(.dept):not(.letter)')),q=0;
  function chk(){q=0;if(off)return;var vh=innerHeight,show=false;arts.forEach(function(a){var r=a.getBoundingClientRect();if(r.height&&r.bottom-r.height*.25<vh*.9&&r.bottom>-vh*.6)show=true});
    place();if(show){if(n.hidden){n.hidden=false;requestAnimationFrame(function(){n.classList.add('on')})}else n.classList.add('on')}else n.classList.remove('on')}
  addEventListener('scroll',function(){if(!q){q=1;requestAnimationFrame(chk)}},{passive:true});addEventListener('resize',chk);chk();
})();
</script>"""

def listen(a):
    """Launcher for a feature's audio reading; playback runs in the docked player."""
    if not a.get("audio"): return ""
    by = f'<span class="lby">Read by {esc(a["audio_reader"])}</span>' if a.get("audio_reader") else ""
    return f'''<button class="listen" type="button" data-src="{a["audio"]}" data-title="{esc(a["title"])}" aria-label="Listen to this story">
      <span class="lp"><svg class="ic-play" viewBox="0 0 16 16" aria-hidden="true"><path d="M4 2.5v11l9-5.5z"/></svg><svg class="ic-pause" viewBox="0 0 16 16" aria-hidden="true"><path d="M3.5 2.5h3.2v11H3.5zM9.3 2.5h3.2v11H9.3z"/></svg></span>
      <span class="lt">Listen to this story</span><span class="ltime">Audio reading</span>{by}
    </button>'''

LBX_CSS = r'''
/* photo lightbox: the story's own color, its photographs in sequence, then back into the text */
.lbx-t{cursor:zoom-in}
.lbx-t:focus-visible{outline:3px solid var(--accent);outline-offset:3px}
.lbx{position:fixed;inset:0;z-index:60;background:color-mix(in oklab,var(--lc,#1b5e6b) 26%,#0a0705);color:#f3ece2;display:flex;flex-direction:column;font-family:var(--ui)}
.lbx[hidden]{display:none}
.lbx [hidden]{display:none!important}
.lbx .vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.lbx-bar{display:flex;align-items:center;gap:12px;padding:max(10px,env(safe-area-inset-top,0px)) 14px 10px}
.lbx-n{margin:0;font-family:"Literata",var(--text),serif;font-size:19px;font-variant-numeric:lining-nums}
.lbx-n span{opacity:.7}
.lbx button{font:inherit;color:inherit;cursor:pointer}
.lbx-x,.lbx-nav{display:grid;place-items:center;width:48px;height:48px;border-radius:50%;border:0;background:rgba(255,255,255,.1)}
.lbx-x{margin-left:auto}
.lbx-x:hover,.lbx-nav:hover{background:rgba(255,255,255,.18)}
.lbx :focus-visible{outline:3px solid #f3ece2;outline-offset:3px}
.lbx-stage{flex:1;min-height:0;position:relative;display:flex;align-items:center;justify-content:center;padding:0 72px 18px;touch-action:pan-y}
.lbx-fig{margin:0;display:flex;flex-direction:column;align-items:center;max-height:100%;transition:opacity .3s}
.lbx-fig img{display:block;max-width:100%;max-height:calc(100dvh - 210px);width:auto;height:auto;object-fit:contain}
.lbx-fig figcaption{max-width:62ch;margin-top:14px;font-family:var(--text);font-size:16px;line-height:1.55;text-align:center;color:#eadfd1}
.lbx-nav{position:absolute;top:50%;transform:translateY(-50%)}
.lbx-prev{left:12px}.lbx-next{right:12px}
.lbx-end{width:min(680px,100%);max-height:100%;overflow-y:auto;padding:4px 2px 18px}
.lbx-k{margin:0 0 10px;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:color-mix(in oklab,var(--lc,#1b5e6b) 45%,#fff)}
.lbx-para{margin:0;font-family:var(--text);font-size:clamp(19px,2.4vw,24px);line-height:1.55}
.lbx-back{margin-top:22px;min-height:48px;padding:0 24px;border-radius:999px;border:0;background:#f3ece2;color:color-mix(in oklab,var(--lc,#1b5e6b) 30%,#0a0705)!important;font-weight:600;font-size:15px}
.lbx-th{margin:30px 0 10px;font-size:12px;letter-spacing:.14em;text-transform:uppercase;font-weight:600;color:color-mix(in oklab,var(--lc,#1b5e6b) 45%,#fff)}
.lbx-tiles{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(84px,1fr));gap:8px}
.lbx-tiles button{display:block;width:100%;aspect-ratio:1;padding:3px;border:0;background:#2f5a2a;border-radius:2px}
.lbx-tiles img{display:block;width:100%;height:100%;object-fit:cover}
.lbx-tiles button[aria-current="true"]{outline:2px solid #f3ece2;outline-offset:2px}
@media (max-width:640px){.lbx-stage{padding:0 14px 14px}.lbx-nav{display:none}.lbx-fig img{max-height:calc(100dvh - 230px)}}
.lbx-hl{animation:lbxhl 2.6s ease-out}
.prose p[tabindex="-1"]:focus{outline:none}
@keyframes lbxhl{0%,30%{background:color-mix(in oklab,var(--accent) 22%,transparent)}100%{background:transparent}}
@media (prefers-reduced-motion:reduce){.lbx-fig{transition:none}.lbx-hl{animation:none;background:color-mix(in oklab,var(--accent) 16%,transparent)}}
'''
LBX_HTML = '''<div class="lbx" id="lbx" role="dialog" aria-modal="true" aria-labelledby="lbx-h" hidden>
<h2 id="lbx-h" class="vh">Photographs</h2>
<div class="lbx-bar"><p class="lbx-n" aria-live="polite"></p><button type="button" class="lbx-x" aria-label="Close photographs"><svg width="18" height="18" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 3l10 10M13 3L3 13" fill="none" stroke="currentColor" stroke-width="1.7"/></svg></button></div>
<div class="lbx-stage">
<button type="button" class="lbx-nav lbx-prev" aria-label="Previous photograph"><svg width="18" height="18" viewBox="0 0 16 16" aria-hidden="true"><path d="M10 2L4 8l6 6" fill="none" stroke="currentColor" stroke-width="1.7"/></svg></button>
<figure class="lbx-fig"><img alt=""><figcaption></figcaption></figure>
<section class="lbx-end" aria-label="Back to the story" hidden><p class="lbx-k"></p><p class="lbx-para"></p><button type="button" class="lbx-back">Back to the story</button><h3 class="lbx-th">The photographs of this story</h3><ul class="lbx-tiles"></ul></section>
<button type="button" class="lbx-nav lbx-next" aria-label="Next photograph"><svg width="18" height="18" viewBox="0 0 16 16" aria-hidden="true"><path d="M6 2l6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.7"/></svg></button>
</div>
</div>'''
LBX_JS = r'''<script>
(function(){
  var box=document.getElementById('lbx'); if(!box)return;
  var rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
  var nEl=box.querySelector('.lbx-n'), fig=box.querySelector('.lbx-fig'), im=fig.querySelector('img'), cap=fig.querySelector('figcaption'),
      end=box.querySelector('.lbx-end'), para=box.querySelector('.lbx-para'), kick=box.querySelector('.lbx-k'), tiles=box.querySelector('.lbx-tiles'),
      prevB=box.querySelector('.lbx-prev'), nextB=box.querySelector('.lbx-next'), head=box.querySelector('#lbx-h'), stage=box.querySelector('.lbx-stage');
  var set=[], cur=0, from=null, ending=false, story=null, opener=null;
  function capOf(img){var c=img.closest('.bi,.pair>div,figure');var f=c&&c.querySelector('figcaption');var t=f&&f.textContent.trim();
    if(!t||c.querySelectorAll('img').length>1)t=img.alt;return t||img.alt||'';}
  function nextPara(img){var p=img.closest('.prose');var blk=img.closest('.prose>*');
    if(!p)return (img.closest('article')||document).querySelector('.prose p');
    for(var e=blk&&blk.nextElementSibling;e;e=e.nextElementSibling){if(e.tagName==='P')return e;var q=e.querySelector&&e.querySelector('p');if(q&&e.tagName!=='FIGURE'&&!e.classList.contains('chart'))return q;}
    return blk;}
  var stories=[].slice.call(document.querySelectorAll('article.story'));
  stories.forEach(function(a){var imgs=[].slice.call(a.querySelectorAll('img')).filter(function(i){return !i.closest('.chart,.torn,.blooms,.listen')});
    imgs.forEach(function(img,k){img.classList.add('lbx-t');img.setAttribute('tabindex','0');img.setAttribute('role','button');
      img.setAttribute('aria-label','View larger: '+(img.alt||capOf(img))+'. Photograph '+(k+1)+' of '+imgs.length);
      img.addEventListener('click',function(){open(a,imgs,k,img)});
      img.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();open(a,imgs,k,img)}});});
    [].forEach.call(a.querySelectorAll('a[data-lbx]'),function(l){l.addEventListener('click',function(e){var t=document.getElementById(l.getAttribute('data-lbx'));var k=imgs.indexOf(t);if(k<0)return;e.preventDefault();open(a,imgs,k,l)})});});
  [].forEach.call(document.querySelectorAll('.mnote'),function(n){var m=document.getElementById(n.getAttribute('data-for'));if(!m)return;
    n.addEventListener('mouseenter',function(){m.classList.add('on')});n.addEventListener('mouseleave',function(){m.classList.remove('on')});});
  function title(a){var h=a.querySelector('.shead h2');return h?h.textContent.trim():'';}
  function show(){var n=set.length;
    if(ending){fig.hidden=true;end.hidden=false;prevB.hidden=false;nextB.hidden=true;nEl.innerHTML='<span>Back to the story</span>';
      [].forEach.call(tiles.querySelectorAll('button'),function(b,k){b.setAttribute('aria-current',k===from?'true':'false')});
      end.querySelector('.lbx-back').focus();return;}
    end.hidden=true;fig.hidden=false;prevB.hidden=cur===0;nextB.hidden=false;
    var img=set[cur];im.src=img.currentSrc||img.src;im.alt=img.alt;cap.textContent=capOf(img);
    nEl.innerHTML=(cur+1)+' <span>/ '+n+'</span><span class="vh"> photographs</span>';}
  function open(a,imgs,k,img){story=a;set=imgs;cur=k;from=k;ending=false;opener=img;
    box.style.setProperty('--lc',getComputedStyle(a).getPropertyValue('--accent').trim()||'#1b5e6b');
    head.textContent='Photographs from '+title(a);kick.textContent=title(a)+' · continues';
    var np=nextPara(img);para.textContent=np?np.textContent.trim():'';
    tiles.innerHTML='';imgs.forEach(function(t,j){var li=document.createElement('li'),b=document.createElement('button'),ti=document.createElement('img');
      b.type='button';b.setAttribute('aria-label','Photograph '+(j+1)+' of '+imgs.length+': '+(t.alt||capOf(t)));ti.src=t.currentSrc||t.src;ti.alt='';ti.loading='lazy';
      b.appendChild(ti);b.addEventListener('click',function(){ending=false;cur=j;show();box.querySelector('.lbx-x').focus()});li.appendChild(b);tiles.appendChild(li);});
    [].forEach.call(document.body.children,function(c){if(c!==box&&c.tagName!=='SCRIPT'){c.setAttribute('data-lbx-inert','');c.inert=true}});
    document.documentElement.style.overflow='hidden';box.hidden=false;show();box.querySelector('.lbx-x').focus();}
  function close(){var target=nextPara(set[from])||null;box.hidden=true;document.documentElement.style.overflow='';
    [].forEach.call(document.querySelectorAll('[data-lbx-inert]'),function(c){c.inert=false;c.removeAttribute('data-lbx-inert')});
    var trg=ending?target:set[cur];
    if(ending&&target){target.scrollIntoView({block:'center',behavior:rm?'auto':'smooth'});target.classList.remove('lbx-hl');void target.offsetWidth;target.classList.add('lbx-hl');
      setTimeout(function(){target.classList.remove('lbx-hl')},2800);target.setAttribute('tabindex','-1');target.focus({preventScroll:true});}
    else if(trg){trg.scrollIntoView({block:'center',behavior:'auto'});trg.focus({preventScroll:true});}
    ending=false;}
  function next(){if(ending){close();return}if(cur<set.length-1){cur++;show()}else{ending=true;show()}}
  function prev(){if(ending){ending=false;cur=set.length-1;show();return}if(cur>0){cur--;show()}}
  nextB.addEventListener('click',next);prevB.addEventListener('click',prev);
  box.querySelector('.lbx-x').addEventListener('click',function(){ending=false;close()});
  box.querySelector('.lbx-back').addEventListener('click',function(){ending=true;close()});
  box.addEventListener('keydown',function(e){
    if(e.key==='Escape'){e.preventDefault();close();return}
    if(e.key==='ArrowRight'){e.preventDefault();next()} if(e.key==='ArrowLeft'){e.preventDefault();prev()}
    if(e.key==='Tab'){var f=[].slice.call(box.querySelectorAll('button:not([hidden]),[href]')).filter(function(x){return x.offsetParent!==null});
      if(!f.length)return;var a=f[0],z=f[f.length-1];if(e.shiftKey&&document.activeElement===a){e.preventDefault();z.focus()}else if(!e.shiftKey&&document.activeElement===z){e.preventDefault();a.focus()}}});
  var sx=null,sy=null;stage.addEventListener('touchstart',function(e){sx=e.touches[0].clientX;sy=e.touches[0].clientY},{passive:true});
  stage.addEventListener('touchend',function(e){if(sx===null)return;var dx=e.changedTouches[0].clientX-sx,dy=e.changedTouches[0].clientY-sy;sx=null;
    if(Math.abs(dx)>48&&Math.abs(dx)>Math.abs(dy)){dx<0?next():prev()}else if(dy>90&&Math.abs(dy)>Math.abs(dx)){close()}},{passive:true});
})();
</script>'''
DOCK = '''<div class="dock" id="dock" role="region" aria-label="Audio player" hidden>
  <div class="dk">
    <button class="dp" type="button" aria-label="Pause"><svg class="ic-play" viewBox="0 0 16 16" aria-hidden="true"><path d="M4 2.5v11l9-5.5z"/></svg><svg class="ic-pause" viewBox="0 0 16 16" aria-hidden="true"><path d="M3.5 2.5h3.2v11H3.5zM9.3 2.5h3.2v11H9.3z"/></svg></button>
    <button class="ds" type="button" aria-label="Playback speed">1×</button>
    <button class="dj" type="button" data-j="-15" aria-label="Back 15 seconds"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5V2L7 6l5 4V7a6 6 0 1 1-6 6H4a8 8 0 1 0 8-8z"/><text x="12" y="16.2" text-anchor="middle">15</text></svg></button>
    <button class="dj" type="button" data-j="15" aria-label="Forward 15 seconds"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5V2l5 4-5 4V7a6 6 0 1 0 6 6h2a8 8 0 1 1-8-8z"/><text x="12" y="16.2" text-anchor="middle">15</text></svg></button>
    <a class="dt" href="#" tabindex="-1" aria-label="Story being read"></a>
    <span class="dtime">0:00 / 0:00</span>
    <div class="dbar" role="slider" tabindex="0" aria-label="Seek" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><i></i><b></b></div>
    <button class="dx" type="button" aria-label="Close player"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3.5 3.5l9 9M12.5 3.5l-9 9"/></svg></button>
  </div>
</div>'''

def _star9(cx, cy, R, r, rot=-90):
    import math
    return " ".join(f"{cx+(R if i%2==0 else r)*math.cos(math.radians(rot+i*20)):.2f},{cy+(R if i%2==0 else r)*math.sin(math.radians(rot+i*20)):.2f}" for i in range(18))

def prayer_html(pr):
    """An illuminated prayer: a gilt rosette above, a lapis versal, and each sentence on its own line."""
    import re as _r
    text, src = pr
    rose = (f'<svg class="rose" viewBox="0 0 120 120" aria-hidden="true"><polygon points="{_star9(60,60,56,40)}" fill="none" stroke="var(--gilt)" stroke-width="1.2"/>'
            f'<polygon points="{_star9(60,60,46,33,-70)}" fill="var(--gilt)" opacity=".22"/><polygon points="{_star9(60,60,38,27)}" fill="none" stroke="var(--gilt)" stroke-width="1"/>'
            f'<circle cx="60" cy="60" r="16" fill="var(--lap)"/><polygon points="{_star9(60,60,13,7)}" fill="var(--gilt2)"/></svg>')
    first, rest = text[0], text[1:]
    versal = (f'<span class="vbox" aria-hidden="true"><svg viewBox="0 0 100 100"><rect x="2" y="2" width="96" height="96" fill="var(--lap)" stroke="var(--gilt)" stroke-width="2.5"/>'
              f'<rect x="8" y="8" width="84" height="84" fill="none" stroke="var(--gilt2)" stroke-width=".8"/><polygon points="{_star9(50,52,40,28)}" fill="none" stroke="var(--gilt)" stroke-width=".8" opacity=".55"/>'
              f'<text x="50" y="72" text-anchor="middle" font-family="Literata,serif" font-weight="600" font-size="72" fill="var(--gilt2)">{esc(first)}</text></svg></span>')
    lines = [x.strip() for x in _r.split(r"(?<=[.])\s+", rest)]
    body = "".join(f'<span class="ln">{esc(x)}</span>' for x in lines)
    corner = lambda n: f'<svg class="jc jc{n}" viewBox="0 0 40 40" aria-hidden="true"><polygon points="{_star9(20,20,18,11)}" fill="var(--gilt)"/><circle cx="20" cy="20" r="5" fill="var(--lap)"/></svg>'
    return f'<blockquote class="passage prayer illum">{"".join(corner(n) for n in range(1,5))}{rose}<p class="lines">{versal}<span class="vh">{esc(first)}</span>{body}</p><cite>{esc(src)}</cite></blockquote>'

def build_tab(member=False, menu="contents"):
    tints = {"gregory":"#e8532a","newyorkers":"#f05a7e","twoartists":"#b07a4a","abs":"#c9462c","endeavor":"#1b5e6b","comic":"#e9a21f"}
    secs = []
    bands = ["#1b5e6b", "#8a3a1e", "#3b3f7a", "#5c2a4e", "#2f5d3a", "#8b6a1a"]
    for i, a in enumerate(ARTICLES):
        art = ""
        if a.get("art"):
            if a["slug"] == "comic":
                art = ('<div class="csplash" aria-hidden="true"><div class="burst"></div><div class="k">Adventures in pioneering · Indianapolis</div><div class="tt">Sparkling spirits!</div></div>')
                below = f'''<figure class="plate comic"><img src="img/{a["art"]}" alt="{esc(a["art_alt"])}"{_dims(a["art"])} loading="lazy"><img src="img/{a["art2"]}" alt="{esc(a["art2_alt"])}"{_dims(a["art2"])} loading="lazy"><figcaption>{esc(a["art_credit"])}</figcaption></figure>'''
            else:
                cls = "plate bare" if a.get("art_transparent") else "plate"
                if a.get("art_width"): cls += " capped"
                cap = f'<figcaption>{a.get("art_credit_html") or esc(a["art_credit"])}</figcaption>' if a.get("art_credit") else ""
                ov = a.get("art_overlay")
                ov_open = f'<div class="ovw {ov.get("cls","")}" style="--ar:{ov["ar"]}">' if ov else ""
                ov_close = f'<div class="ov" aria-hidden="true">{ov["html"]}</div></div>' if ov else ""
                art = f'''<figure class="{cls}" style="--aw:{a.get("art_width",0)}px">{ov_open}<img src="img/{a["art"]}" alt="{esc(a["art_alt"])}"{_dims(a["art"])}{"" if a is ARTICLES[0] else ' loading="lazy" decoding="async"'}>{ov_close}{cap}</figure>'''
                if a.get("art_extra"):  # seen only in the lightbox, opened from a link in the caption
                    x = a["art_extra"]
                    art += f'<figure class="lbx-only" hidden><img id="{x["id"]}" src="img/{x["file"]}" alt="{esc(x["alt"])}" loading="lazy"><figcaption>{esc(x["caption"])}</figcaption></figure>'
        else:
            art = ('<div class="fnote" role="img" aria-label="50 years: the Association for Bahá\'í Studies, founded in 1975"><div class="fbig" aria-hidden="true"><span>50</span><sup>1</sup></div><div class="frule" aria-hidden="true"></div>'
                   '<p class="fnt" aria-hidden="true"><sup>1</sup> Years since the founding of the <i>Association for Bahá\'í Studies</i>, 1975.</p></div>')
        dek = f'<p class="dek">{esc(a["dek"])}</p>' if a.get("dek") else ""
        by = (f'<p class="by{" nob" if a["byline"].startswith(("Adapted","Story")) else ""}">{esc(a["byline"])}</p>') if a.get("byline") else ""
        blooms = '<div class="blooms" aria-hidden="true"><i></i><i></i><i></i></div>' if a["slug"] == "newyorkers" else ""
        pal = {"gregory":("#f26b2b","#2448c8","#f05a7e","#f3c623"),"newyorkers":("#2448c8","#f05a7e","#f3c623","#5f8f3a"),"twoartists":("#b07a4a","#e9a21f","#2f6a4a","#f26b2b"),"abs":("#c9462c","#1b5e6b","#e9a21f","#2448c8"),"endeavor":("#1b5e6b","#e9a21f","#9ec3cc","#f26b2b"),"comic":("#f3c623","#2448c8","#f26b2b","#5f8f3a")}[a["slug"]]
        torn = f'<div class="torn" data-v="{i % 6}" aria-hidden="true" style="--a:{pal[0]};--b:{pal[1]};--c:{pal[2]};--d:{pal[3]}"><i></i><i></i><i></i><i></i></div>'
        margin = f'''<aside class="margin">
    <p class="kicker">{esc(a["kicker"])}</p>
    {by}
    {f'<p class="pp">{"Print pages" if "–" in str(a["pages"]) else "Print page"} {a["pages"]}</p>' if member else ""}
    {share(a)}
    {listen(a)}
  </aside>'''
        _feat = [x for x in ARTICLES if x["slug"] != "comic"]
        chap = "" if member or a["slug"] == "comic" else (f'<div class="chap" aria-hidden="true" style="--accent:{tints[a["slug"]]}"><span class="n">{_feat.index(a) + 1}</span><span class="k">{esc(a["kicker"])}</span>'
                f'<span class="of">{_feat.index(a) + 1} of {len(_feat)}</span></div>')
        story = chap + f'''<article class="story" id="{a["slug"]}" style="--accent:{tints[a["slug"]]}">{blooms}
  {art}
  <header class="shead{"" if dek else " nodek"}">{torn}
    <h2>{esc(a["title"])}</h2>
    {dek}
  </header>
  {"" if a["slug"] == "comic" else margin}
  <div class="prose">{margin + after_first(first_para_dropcap(body_html(a["body"])), below) if a["slug"] == "comic" else first_para_dropcap(body_html(a["body"]))}</div>
</article>'''
        if a["slug"] == "comic":  # the comic lives in the full edition, among the departments
            comic_story = story; comic_rec = a; continue
        secs.append(story)
        if i < len(VOICES):
            v = VOICES[i]
            secs.append(f'''</div><aside class="voice" style="--band:{bands[i % len(bands)] if member else "color-mix(in oklab," + tints[a["slug"]] + " 58%,#1d1a16)"}"><div class="vin"><p>{esc(v[0])}</p><cite>{esc(v[1])}</cite></div></aside><div class="wrap">''')
    FEAT = [a for a in ARTICLES if a["slug"] != "comic"]
    head = "".join(f'<a href="#{a["slug"]}" style="--tint:{tints[a["slug"]]}"><span>{esc(a["short"])}</span><i class="fill"></i></a>' for a in FEAT)
    index = "".join(f'<li><a href="#{a["slug"]}"><span class="t">{esc(a["title"])}</span><span class="pg">{a["pages"].split("–")[0]}</span></a></li>' for a in FEAT)
    if True:
        index = "".join(f'<li><a href="#{a["slug"]}" style="--c:{tints[a["slug"]]}"><span class="nm" aria-hidden="true">{n}</span><span class="kk">{esc(a["kicker"])}</span><span class="t">{esc(a["title"])}</span></a></li>' for n, a in enumerate(FEAT, 1))
    lead = ""; depts = ""; dindex = ""; dhead = ""
    rows = [(a["slug"], a["short"], a["pages"].split("–")[0], tints[a["slug"]], a["kicker"], a["title"]) for a in FEAT]
    if member:
        from member_data import LETTER, HUQUQ, ABIDING, FUND, RHYTHM, BOOKS, NOTICES
        L = LETTER
        lead = f'''<article class="story letter members" id="{L["slug"]}">
  <header class="shead"><p class="kicker-top">{esc(L["kicker"])}</p><h2>{esc(L["title"])}</h2><p class="dek">{esc(L["dek"])}</p></header>
  <aside class="margin"><p class="kicker">Mid-year letter</p><p class="pp">{"Print pages" if "–" in str(L["pages"]) else "Print page"} {L["pages"]}</p></aside>
  <div class="prose"><p class="salute">{esc(L["salutation"])}</p>{first_para_dropcap(body_html(L["body"]))}<p class="sign">{esc(L["closing"][0])}<br><b>{esc(L["closing"][1])}</b></p></div>
</article>'''
        def dept_open(d):
            dek = f'<p class="dek">{esc(d["dek"])}</p>' if d.get("dek") else ""
            return f'''<article class="story dept members" id="{d["slug"]}">
  <header class="shead"><p class="kicker-top">{esc(d["kicker"])}</p><h2>{esc(d["title"])}</h2>{dek}</header>
  <aside class="margin"><p class="kicker">{esc(d["kicker"])}</p><p class="pp">{"Print pages" if "–" in str(d["pages"]) else "Print page"} {d["pages"]}</p></aside>'''
        huq = dept_open(HUQUQ) + f'<div class="prose">{first_para_dropcap(body_html(HUQUQ["body"]))}</div></article>'
        qs = "".join(f'<section class="qblock"><h3>{esc(q)}</h3>' + "".join(f'<blockquote class="passage"><p>{esc(t)}</p><cite>{esc(c)}</cite></blockquote>' for t,c in items) + '</section>' for q,items in ABIDING["questions"])
        abide = dept_open(ABIDING) + f'''<div class="prose compilation"><blockquote class="passage lead"><p>{esc(ABIDING["epigraph"][0])}</p><cite>{esc(ABIDING["epigraph"][1])}</cite></blockquote>{qs}</div></article>'''
        fund = dept_open(FUND) + f'<div class="prose">{first_para_dropcap(body_html(FUND["body"]))}</div></article>'
        R = RHYTHM
        hd = "".join(f'<li><b>{esc(n)}</b><span>{esc(w)}</span></li>' for n,w in R["holydays"])
        fs = "".join(f'<li><b>{esc(n)}</b><i>{esc(m)}</i><span>{esc(d)}</span></li>' for n,m,d in R["feasts"])
        rhythm = dept_open(R) + f'''<div class="prose calendar">
  <div class="cal"><div><h3>Holy Days</h3><ul class="hd">{hd}</ul></div><div><h3>Upcoming Feasts</h3><ul class="feast">{fs}</ul></div></div>
  <p class="note">{esc(R["note"])}</p>
</div></article>'''
        B = BOOKS
        def book(it):
            t, sub, desc, price = it[:4]; url = it[4] if len(it) > 4 else None
            h = f'<a href="{url}" target="_blank" rel="noopener">{esc(t)}</a>' if url else esc(t)
            buy = f' <a class="buy" href="{url}" target="_blank" rel="noopener">View at the Bahá\'í Bookstore</a>' if url else ""
            return f'<li><h3>{h}</h3>{("<p class=sub>"+esc(sub)+"</p>") if sub else ""}<p>{esc(desc)}</p>{("<p class=price>"+esc(price)+buy+"</p>") if price else ""}</li>'
        bk = "".join(book(it) for it in B["items"])
        books = dept_open(B) + f'<div class="prose shelf"><ul class="books">{bk}</ul><p class="note">{esc(B["contact"])}</p></div></article>'
        nt = "".join(f'''<li{' class="svn"' if "1052" in n["src"] else ""}>{('<img src="img/'+n["img"]+'" alt="'+esc(n.get("alt") or n["title"]+" cover")+'" loading="lazy">') if n.get("img") else ""}{('<a class="svm" href="'+SURVEY_FORM+'" data-survey target="_blank" rel="noopener" aria-label="Take the reader survey"><img src="img/motif/m09.webp" alt="" loading="lazy"></a>') if "1052" in n["src"] else ""}<p class="k">{esc(n["kicker"])}</p><h3>{esc(n["title"])}</h3><p>{esc(n["text"])}</p>{('<a class="svb" href="'+SURVEY_FORM+'" data-survey target="_blank" rel="noopener">Take the survey here</a>') if "1052" in n["src"] else ""}<cite>{esc(n["src"])}</cite></li>''' for n in NOTICES)
        notices = f'''<article class="story dept members" id="notices"><header class="shead"><p class="kicker-top">Announcements</p><h2>Notices</h2></header><aside class="margin"><p class="kicker">Notices</p><p class="pp">Print pages 40–48</p></aside><div class="prose"><ul class="notices">{nt}</ul></div></article>'''
        depts = '<h2 class="reg members" id="members">The full issue<small>The National Spiritual Assembly\'s mid-year letter and the departments of the printed issue</small></h2>' + lead + abide + huq + comic_story + fund + rhythm + books + notices + f'<section class="story dept members visit" id="visitation" aria-label="From the Tablet of Visitation"><div class="prose">{prayer_html(RHYTHM["prayer"])}</div></section>'
        lead = ""
        D = [("abiding","Abiding in God's Law","32"),("huquq","Ḥuqúqu'lláh","30"),("comic",comic_rec["short"],comic_rec["pages"].split("–")[0]),("fund","Bahá'í Fund","42"),("rhythm","Rhythm of Bahá'í Life","39"),("books","Bookstore","36"),("notices","Notices","40")]
        import member_data as _md
        _sub = {"abiding": _md.ABIDING, "huquq": _md.HUQUQ, "fund": _md.FUND, "rhythm": _md.RHYTHM, "books": _md.BOOKS}
        _rows = [("letter", L["kicker"], L["title"])] + [(s_, (_sub[s_]["kicker"] if s_ in _sub else t_), (_sub[s_]["title"] if s_ in _sub else ("Adventures in pioneering: " + comic_rec["title"] if s_ == "comic" else "Announcements" if s_ == "notices" else ""))) for s_, t_, p_ in D]
        dindex = '<h2 class="fih">The full issue</h2><ol class="fi2">' + "".join(f'<li><a href="#{s_}"><span class="kk">{esc(k_)}</span><span class="t">{esc(t_)}</span></a></li>' for s_, k_, t_ in _rows) + '</ol>'
        shorts = {"gregory":"Gregory","newyorkers":"New Yorkers","twoartists":"Two artists","abs":"ABS","endeavor":"Endeavor","comic":"Comic"}
        dhead = "".join(f'<a href="#{a["slug"]}" style="--tint:{tints[a["slug"]]}"><span>{shorts[a["slug"]]}</span><i class="fill"></i></a>' for a in FEAT) + '<a href="#letter" class="mem more" style="--tint:var(--mem)"><span>Letter</span><i class="fill"></i></a><a href="#huquq" class="mem" style="--tint:var(--mem)"><span>Departments</span><i class="fill"></i></a>'
        head = dhead
        recs = {"huquq": HUQUQ, "comic": comic_rec, "abiding": ABIDING, "fund": FUND, "rhythm": RHYTHM, "books": BOOKS}
        rows += [("letter", "Letter", "2", "var(--mem)", L["kicker"], L["title"])] + [(s, t, p, "var(--mem)", recs[s]["kicker"] if s in recs else "Announcements", t) for s, t, p in D]
    import re as _re
    vol = _re.sub(r"Volume (\d+), Number (\d+)", r"Vol. \1 · No. \2", ISSUE["vol"]); ms = _re.findall(r"[A-Z][a-z]+", ISSUE["date"]); yr = _re.findall(r"\d{4}", ISSUE["date"])
    when = f'{ms[0][:3]}–{ms[-1][:3]} {yr[-1]}' if ms and yr else ISSUE["date"]
    if menu == "bands":
        light = {"#e9a21f", "#f05a7e"}
        sheet = ('<div class="rhs rhs-b" role="navigation" id="rhs" aria-label="Contents">' + f'<p class="rhi">{esc(ISSUE["theme"])}</p>'
                 + "".join(f'<a href="#{s}" style="--tint:{t}" class="{"dk" if t in light else ""}" data-name="{esc(n)}"><span class="cur">Reading</span><span class="nm">{esc(n)}</span><span class="pp">p.&#8201;{p}</span><i class="bar"></i></a>' for s, n, p, t, k, ti in rows)+ '</div>')
    else:
        sheet = ('<div class="rhs rhs-c" role="navigation" id="rhs" aria-label="Contents">' + f'<div class="rhm"><span>{vol}</span><span>{when}</span></div><p class="rhtt">{esc(ISSUE["theme"])}</p>'
                 + "".join(f'<a href="#{s}" style="--tint:{t}" data-name="{esc(n)}"><span class="pn">{p}</span><span class="rx"><span class="k">{esc(k)}</span><span class="tt">{esc(ti)}</span><span class="rd" aria-hidden="true"><i></i></span></span></a>' for s, n, p, t, k, ti in rows)
                 + '<div class="rhf"><a href="#top">Back to the cover</a></div></div>')
    title = esc(ISSUE["title"]) + (" Full Edition" if member else "")
    return f'''<title>{title}</title>
{SIDES}
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@300;400;700&family=Newsreader:ital,opsz,wght@0,6..72,400;1,6..72,400&family=Bricolage+Grotesque:opsz,wght@12..96,300..800&family=Literata:ital,opsz,wght@0,7..72,300..700;1,7..72,300..700&family=Pinyon+Script&family=Big+Shoulders+Display:wght@800..900&family=Fraunces:opsz,wght@9..144,300..600&{"family=Bangers&" if member else ""}family=Reenie+Beanie&family=Libre+Caslon+Text:ital@0;1&display=swap">
<style>
/* Layout: one long page. Running head with color tabs; masthead with the framed cover painting; index and front matter; each feature on a three-column field (margin, text, open) opened by its art; a colored band between features carries one passage from the issue's pages on the arts. */
:root{{
  --paper:#f5f1e8; --ink:#1d1a16; --mute:#6a635a; --rule:#d9d2c4; --accent:#1b5e6b; --cream:#f7f2ea; --bar:#fdfcf9; --tabon:#f5f1e8; --barrule:#d9d2c4; --tabon-white:#ffffff; --mem:#5b4a8a;
  --disp:"Bricolage Grotesque","Helvetica Neue",Arial,sans-serif; --text:"Literata",Georgia,serif; --ui:"Bricolage Grotesque","Helvetica Neue",Arial,sans-serif;
}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--paper:#15130f;--ink:#efe9dd;--mute:#a39b8e;--rule:#2f2a22;--accent:#7fc0c9;--cream:#1c1915;--bar:#221e19;--tabon:#15130f;--barrule:#2f2a22;--tabon-white:#1f1c17;--mem:#b3a3e0;color-scheme:dark}}}}
:root[data-theme="dark"]{{--paper:#15130f;--ink:#efe9dd;--mute:#a39b8e;--rule:#2f2a22;--accent:#7fc0c9;--cream:#1c1915;--bar:#221e19;--tabon:#15130f;--barrule:#2f2a22;--tabon-white:#1f1c17;--mem:#b3a3e0;color-scheme:dark}}
*{{box-sizing:border-box}}
:where(img){{height:auto}}
html{{scroll-behavior:smooth}}
[tabindex="-1"]:focus:not(:focus-visible){{outline:none}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
html{{overflow-x:clip}}
body{{margin:0;overflow-x:clip;background:var(--paper);color:var(--ink);font-family:var(--text);font-size:18px;line-height:1.55}}
.story,#top{{scroll-margin-top:calc(env(safe-area-inset-top,0px) + 64px)}}
.wrap{{max-width:1120px;margin:0 auto;{GUT}}}
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
.cover h1{{position:relative;isolation:isolate}}.stroke{{position:absolute;left:-2%;top:.28em;width:min(760px,80%);height:.62em;z-index:-1;pointer-events:none}}
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
.chart .cdot.big{{stroke:var(--paper);stroke-width:3}}
.chart .cpanel{{fill:transparent;stroke:transparent}}
.chart .cringf{{stroke:var(--paper);stroke-width:2.5}} .chart text.cin{{fill:#fff}} .chart .cring{{font-family:var(--ui);font-weight:600;font-size:13.5px;fill:var(--ink)}} .chart circle.carea.hit:hover{{filter:brightness(1.08)}}
.chart .ghost{{fill:transparent}} .chart .hit{{cursor:pointer;outline:none}}
.chart .hit:hover .cb,.chart .hit:focus-visible .cb,.chart rect.hit:hover,.chart path.hit:hover{{filter:brightness(1.12)}}
.chart path.hit:focus-visible,.chart rect.hit:focus-visible,.chart .hit:focus-visible .cdot{{stroke:var(--ink);stroke-width:2}}
.chart .pin:hover .cdot,.chart .pin:focus-visible .cdot{{r:10.2}}
.cland{{fill:var(--cream);stroke:var(--rule);stroke-width:1}} .cstate{{fill:none;stroke:var(--rule);stroke-width:.6}}
.creg .rf{{stroke:none;opacity:.85;transition:opacity .2s}} .chart .creg .rf.hit:hover,.chart .creg .rf.hit:focus-visible{{opacity:1;filter:saturate(1.6) brightness(.97)}} .creg .cstate,.creg .rb{{pointer-events:none}} .creg .ta{{fill:#efe4d0}} .creg .tb{{fill:#e3eadb}} .creg .tc{{fill:#f1ddd5}} .creg .td{{fill:#dde6ee}}
.creg .rb{{fill:none;stroke:color-mix(in oklab,var(--ink) 45%,transparent);stroke-width:1.6;stroke-linejoin:round;vector-effect:non-scaling-stroke}}
.chart .creg text.rn{{font-family:"Literata",serif;font-size:11px;font-weight:600;font-style:italic;letter-spacing:.02em;fill:color-mix(in oklab,var(--ink) 62%,transparent);text-anchor:middle;paint-order:stroke;stroke:var(--paper);stroke-width:3px;stroke-linejoin:round}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]) .creg .ta{{fill:#2c251b}} :root:not([data-theme="light"]) .creg .tb{{fill:#1e2720}} :root:not([data-theme="light"]) .creg .tc{{fill:#2d201c}} :root:not([data-theme="light"]) .creg .td{{fill:#1b232b}}}}
:root[data-theme="dark"] .creg .ta{{fill:#2c251b}} :root[data-theme="dark"] .creg .tb{{fill:#1e2720}} :root[data-theme="dark"] .creg .tc{{fill:#2d201c}} :root[data-theme="dark"] .creg .td{{fill:#1b232b}} .chart text{{pointer-events:none}}
.chart .tl li.has,.figs div.has{{cursor:pointer}} .chart .tl li.has span{{text-decoration:underline dotted;text-underline-offset:3px;text-decoration-color:var(--rule)}}
.figs div.has b::after{{content:"+";font-size:.45em;vertical-align:super;margin-left:3px;color:var(--accent)}}
.figs div.has:focus-visible,.chart .tl li.has:focus-visible{{outline:2px solid var(--accent);outline-offset:4px}}
.popup{{position:fixed;z-index:30;max-width:min(340px,calc(100vw - 32px));background:var(--tabon-white);color:var(--ink);border:1px solid var(--rule);border-top:3px solid var(--pa,var(--accent));box-shadow:0 10px 30px rgba(30,25,15,.16);padding:14px 16px 14px;font-family:var(--ui);font-size:14px;line-height:1.5;opacity:0;transform:translateY(4px);transition:opacity .15s,transform .15s;pointer-events:none}}
.popup.show{{opacity:1;transform:none;pointer-events:auto}}
.popup b{{display:block;font-family:var(--disp);font-weight:700;font-size:15.5px;letter-spacing:-.01em;margin:0 18px 6px 0}}
.popup p{{margin:0;color:var(--ink);white-space:pre-line}}
.popup button{{position:absolute;top:6px;right:6px;border:0;background:none;font-size:18px;line-height:1;color:var(--mute);cursor:pointer;padding:4px 6px}}
@media (prefers-reduced-motion:reduce){{.popup{{transition:none}}}}
.chart .cax{{stroke:var(--rule);stroke-width:2}} .chart .cdot{{fill:var(--accent)}} .chart .cstem{{stroke:var(--rule);stroke-width:1}} .chart .cera{{fill:var(--accent);opacity:.18}}
.chart .cseg{{fill:var(--rule)}} .chart .cseg.on{{fill:var(--accent)}} .chart .cl.on{{fill:var(--ink);font-weight:600}} .chart .cbig{{font-family:var(--disp);font-weight:800;font-size:48px;fill:var(--ink)}}
.chart .cvin{{font-family:var(--disp);font-weight:700;font-size:12px;fill:#fff}}
.chart .tl{{list-style:none;margin:12px 0 0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:6px 22px}}
.chart .tl li{{display:grid;grid-template-columns:3.4em 1fr;gap:10px;font-family:var(--ui);font-size:14px;line-height:1.45;color:var(--mute)}} .chart .tl b{{color:var(--ink);font-variant-numeric:tabular-nums}}
.prose .chart.wide{{max-width:none}}
.prose .chart{{margin:1.8em 0 2.2em;max-width:600px}}
.prose .chart.sized{{max-width:var(--cw)}} .prose>.chart:not(.span){{max-width:min(var(--cw,520px),520px)}} .letter .prose>.chart:not(.span){{max-width:580px}}
/* infographic refresh */
.chart .hit:hover rect[style]{{filter:brightness(1.08)}}
.chart text.cyr{{font-family:"Literata",var(--text),serif;font-weight:600;font-size:22px;fill:var(--ink)}} .chart text.cstep{{font-family:var(--ui);font-size:12.5px;fill:var(--mute)}}
.chart .cground{{stroke:var(--rule);stroke-width:2}}
.chart .cspine{{stroke:var(--rule);stroke-width:3}} .chart text.cstl{{font-family:var(--ui);font-size:15.5px;fill:var(--mute)}} .chart text.cstl.on{{fill:var(--ink);font-weight:700}}
.chart .cthr{{stroke:var(--accent);stroke-width:2;stroke-dasharray:6 6}} .chart text.cthrl{{font-family:var(--ui);font-size:11px;letter-spacing:.14em;text-transform:uppercase;fill:var(--accent)}}
.chart .cven{{opacity:.26}} .chart .cven:hover{{opacity:.4}}
.chart .cpull{{stroke:var(--accent);stroke-width:2.5;fill:none}}
.chart text.csubw{{font-family:var(--text);font-style:italic;font-size:15px;fill:var(--mute)}} .chart text.cpre{{font-family:var(--ui);font-size:11px;letter-spacing:.16em;text-transform:uppercase;fill:var(--mute)}}
.chart text.cword{{font-family:"Literata",var(--text),serif;font-weight:600;font-size:72px;fill:var(--accent)}} .chart text.cword.hollow{{fill:none;stroke:var(--accent);stroke-width:1.6}}
.prose>.verb{{grid-column:2;margin:clamp(28px,4vw,48px) 0;padding:0 0 0 .1em}}
.prose>.verb p{{margin:0;max-width:none}} .verb .vw{{font-family:"Literata",var(--text),serif;font-variation-settings:"opsz" 72;font-size:clamp(34px,4.6vw,60px);line-height:1;font-weight:700;letter-spacing:-.025em;cursor:pointer;user-select:none;-webkit-tap-highlight-color:transparent}}
.verb .sx{{display:inline-block;color:var(--accent);font-style:italic}} .verb .s2{{display:inline-block;transition:opacity .35s,transform .45s cubic-bezier(.2,.8,.2,1)}}
.verb:not([data-f="2"]) .s2{{opacity:0;transform:translateX(-.15em)}}
.verb .pos{{display:inline-flex;flex-direction:column;gap:.15em;vertical-align:top;margin:.12em 0 0 .5em;font-family:var(--ui);font-size:clamp(11px,1.1vw,13px);font-style:normal;letter-spacing:.14em;text-transform:uppercase;line-height:1.1;color:var(--mute)}}
.verb .pn{{text-decoration:none;position:relative}} .verb .pn::after{{content:"";position:absolute;left:-2px;right:-2px;top:52%;height:1.5px;background:currentColor;transform:scaleX(var(--k,1));transform-origin:left;transition:transform .4s cubic-bezier(.5,.1,.4,1)}}
.verb .pv{{font-weight:600;color:var(--accent);transition:opacity .35s .15s,transform .35s .15s}}
.verb[data-f="0"] .pn{{--k:0}} .verb[data-f="0"] .pv{{opacity:0;transform:translateY(-.3em)}}
.verb .vq{{margin-left:-.42em;display:inline-block;width:.42em}}
.verb .vr{{font-family:"Literata",var(--text),serif;font-variation-settings:"opsz" 36;font-size:clamp(19px,2.2vw,27px);line-height:1.15;margin-top:.1em;transition:opacity .5s,transform .5s}}
.verb cite{{display:block;font-family:var(--ui);font-style:normal;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--mute);margin-top:1em;transition:opacity .5s .15s}}
.verb:not([data-f="2"]) .vr{{opacity:.18;transform:translateY(.15em)}} .verb:not([data-f="2"]) cite{{opacity:0}}
@media (max-width:760px){{.prose>.verb{{grid-column:auto}} .verb .vq{{margin-left:0;width:auto}}}}
/* display, centered, in Newsreader */
.verb.vc{{text-align:center;margin-left:auto;margin-right:auto;max-width:560px}}
.verb.vc p{{font-family:"Newsreader",var(--text),serif;font-optical-sizing:auto;font-weight:400;font-size:clamp(28px,3.6vw,44px);line-height:1.1;letter-spacing:-.005em;margin:0 0 16px;text-wrap:balance;color:var(--ink)}}
.verb.vc em{{font-style:italic;color:var(--accent)}}
.verb.vc .rl{{display:block;width:80px;height:3px;background:#b8782e;margin:0 auto 14px}}
.verb.vc cite{{margin:0}}
.vh{{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}}
.prose>.mnote{{grid-column:1;grid-row:span 2;align-self:start;margin:.3em 0 1.6em;max-width:24ch;transform:rotate(var(--mr,-1.5deg));color:#2c4a72;cursor:default}}
.prose>.mnote:nth-of-type(even){{--mr:1.2deg}}
.mnote .mq{{display:block;font-family:"Reenie Beanie",cursive;font-size:clamp(25px,2.3vw,31px);line-height:1}}
.mnote .mw{{display:block;font-family:var(--ui);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--mute);margin-top:6px;line-height:1.45}}
.mnh{{background:none;color:inherit;background-image:linear-gradient(color-mix(in oklab,#e7b84a 70%,transparent),color-mix(in oklab,#e7b84a 70%,transparent));background-repeat:no-repeat;background-position:0 92%;background-size:100% .3em;transition:background-size .7s,background-position .3s}}
.mnh.on{{background-size:100% 1.1em;background-position:0 70%}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]) .prose>.mnote{{color:#a9c4e8}}}} :root[data-theme="dark"] .prose>.mnote{{color:#a9c4e8}}
@media (max-width:760px){{.prose>.mnote{{grid-column:auto;grid-row:auto;margin:0 0 1.4em 1em;max-width:none}}}}
@media (prefers-reduced-motion:no-preference){{
.ovready .mnote .mq{{clip-path:inset(0 100% 0 0)}} .ovready .mnote .mw{{opacity:0}}
.ovready .mnote.go .mq{{clip-path:inset(0 0 0 0);transition:clip-path 1.4s cubic-bezier(.5,.1,.4,1)}} .ovready .mnote.go .mw{{opacity:1;transition:opacity .5s .9s}}
.ovready .mnh{{background-size:0 .3em}} .ovready .mnh.go{{background-size:100% .3em;transition:background-size .7s .5s}} .ovready .mnh.go.on{{background-size:100% 1.1em;transition:background-size .4s,background-position .3s}}
}}
/* A common endeavor: postmarks on the quilt */
.evo .ov{{text-shadow:none}}
.evo svg{{position:absolute;inset:0;width:100%;height:100%;filter:drop-shadow(0 1px 1.5px rgba(10,30,40,.85)) drop-shadow(0 0 6px rgba(10,30,40,.5))}}
.evo .adr text{{font-family:"Reenie Beanie",cursive;font-size:74px;font-weight:400;fill:#fbf3e2}}
.evo .ttl{{font-family:var(--ui);font-size:22px;letter-spacing:5px;fill:#fbf3e2}}
.evo .pm circle,.evo .pm .wv{{fill:none;stroke:#fbf3e2;stroke-width:3}}
.evo .pm text{{fill:#fbf3e2;font-family:var(--ui);font-weight:700}} .evo .pmt{{font-size:14px;letter-spacing:2px}} .evo .pms{{font-size:21px}} .evo .pmy{{font-size:13px}}
@media (prefers-reduced-motion:no-preference){{
.ovready .evo .pm{{opacity:0}} .ovready .evo .pmi{{transform:scale(1.7)}}
.ovready .evo.go .pm{{opacity:1;transition:opacity .15s;transition-delay:var(--d)}}
.ovready .evo.go .pmi{{transform:none;transition:transform .25s cubic-bezier(.3,1.4,.5,1);transition-delay:var(--d)}}
.ovready .evo .adr{{clip-path:inset(0 100% 0 0)}} .ovready .evo.go .adr{{clip-path:inset(0 0 0 0);transition:clip-path 1.8s cubic-bezier(.5,.1,.4,1) .2s}}
.ovready .evo .ttl{{opacity:0}} .ovready .evo.go .ttl{{opacity:1;transition:opacity .8s 2s}}
}}
.prose>.figsent{{font-family:var(--text);font-size:clamp(21px,2vw,26px);line-height:1.45;margin:1.6em 0 1.8em;text-wrap:pretty}}
.figsent b{{font-family:"Literata",var(--text),serif;font-weight:600;font-size:1.55em;line-height:1;color:var(--accent);letter-spacing:-.01em}}
.prose>.figsent.lg{{font-size:clamp(26px,2.9vw,36px);line-height:1.35}} .figsent b.wd{{font-size:1.15em}} .figsent b.has{{cursor:pointer;text-decoration:underline dotted;text-decoration-thickness:1px;text-underline-offset:6px;text-decoration-color:color-mix(in oklab,var(--accent) 50%,transparent)}}

/* photo frames: a thin border cut from the cover painting */
.prose .photo.pair{{display:flex!important;gap:20px;align-items:flex-start}} .prose .photo.pair>div{{min-width:0}}
@media (max-width:640px){{.prose .photo.pair{{flex-direction:column}}}}
.prose .photo img,.prose .portraits img,.band .bi img,.prose .mountp img{{box-sizing:border-box;padding:6px;background:#2f5a2a url(img/motif-uhj.jpg) center/cover;border-radius:0!important}}

/* CARS wheel: four phases, each filling in turn */
.chart.ringf .ct{{font-family:"Literata",var(--text),serif;font-weight:500;font-size:clamp(19px,1.75vw,24px);line-height:1.25;letter-spacing:-.005em;max-width:34ch;margin-bottom:18px;font-variation-settings:"opsz" 48}}
.rwrap{{display:grid;gap:clamp(20px,3vw,44px)}}
.rsvg{{display:block;width:100%;max-width:350px;height:auto;overflow:visible;margin:0 auto}}
.wseg{{fill:none;stroke:var(--accent);stroke-width:52;stroke-linecap:butt}}
.wword{{font-family:"Literata",var(--text),serif;font-weight:500;font-size:34px;letter-spacing:-.01em;fill:var(--ink);font-variation-settings:"opsz" 48}}
.whair{{fill:none;stroke:var(--rule);stroke-width:1}}
.rcols{{list-style:none;margin:8px 0 0;padding:0;display:grid;grid-template-columns:repeat(4,1fr);gap:20px 26px}}
.rcols li{{border-top:2px solid var(--rule);padding-top:10px;opacity:.5;transition:opacity .5s,border-color .5s}} .rcols li.on{{opacity:1;border-color:var(--accent)}}
.rcols h5{{font-family:"Literata",var(--text),serif;font-weight:500;font-size:24px;margin:2px 0 6px;color:var(--ink);transition:color .5s}} .rcols li.on h5{{color:var(--accent)}}
.rcols p{{font-family:var(--ui);font-size:13.5px;line-height:1.45;color:var(--mute);margin:0}}
@media (max-width:760px){{.rcols{{grid-template-columns:1fr 1fr}}}}

/* mounted prints */
.prose>.mountp{{grid-column:2;justify-self:start;width:calc(var(--w) + 44px);max-width:100%;box-sizing:border-box;margin:2.2em 0;background:#fdfcf9;border:1px solid var(--rule);padding:20px 20px 14px;position:relative;box-shadow:0 10px 24px -18px rgba(40,25,10,.35)}}
.prose>.mountp.right{{justify-self:end}}
.mountp img{{display:block;width:100%;height:auto}}
.mountp figcaption{{font-family:var(--ui);font-size:12.5px;line-height:1.45;color:var(--mute);margin-top:12px;padding-bottom:6px;text-wrap:pretty}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]) .prose>.mountp{{background:#1f1c17}}}} :root[data-theme="dark"] .prose>.mountp{{background:#1f1c17}}

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
.portraits .q1{{grid-column:2/7}} .portraits .q2{{grid-column:7/12;margin-top:clamp(60px,9vw,140px)}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]) .band.wall{{background:#4a3436;color:#ecd6d8}}}}
:root[data-theme="dark"] .band.wall{{background:#4a3436;color:#ecd6d8}}
@media (max-width:760px){{.band .bin>.bi,.portraits>figure{{grid-column:1/-1!important;grid-row:auto!important;margin-top:0!important;transform:none!important}}}}

@media (min-width:981px){{.prose>.chart.span{{grid-column:2/4}}}}
.chart .cclu{{fill:color-mix(in oklab,var(--mute) 70%,var(--paper));stroke:var(--paper);stroke-width:1.5}} .chart text.ccnt{{font-family:var(--ui);font-weight:700;font-size:10.5px;fill:#fff}} .chart .rep:hover .cclu{{fill:var(--ink)}}
.chart .cibox{{fill:none;stroke:var(--ink);stroke-width:.8;opacity:.5}} .chart .cilead{{fill:none;stroke:var(--ink);stroke-width:.6;opacity:.3}} .chart .cipanel{{fill:var(--paper)}} .chart .ciframe{{fill:none;stroke:var(--rule);stroke-width:1}} .chart text.ccnt.cn9{{font-size:8.5px}} .chart .cin9{{font-weight:700;fill:var(--ink)}} .chart .twb{{stroke:var(--accent);stroke-width:14}} .chart .twd{{stroke-dasharray:3 5}} .chart text.twk{{font-family:var(--ui);font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;fill:var(--mute)}}
.chart text.cml{{font-family:var(--ui);font-size:11.5px;fill:var(--mute);pointer-events:none}} .chart text.cil{{font-family:var(--ui);font-size:10.5px;fill:var(--mute)}} .chart text.cit{{font-family:var(--ui);font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;fill:var(--mute)}} .cizoom .cland,.cizoom .cstate{{vector-effect:non-scaling-stroke}}
.chart .crep{{fill:var(--mute);stroke:var(--paper);stroke-width:1.5;opacity:.9;transition:opacity .15s}} .chart .rep:hover .crep,.chart .rep:focus-visible .crep{{opacity:1;r:7}}
.chart .key{{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--ui);font-size:13px;color:var(--mute);margin:10px 0 0}} .chart .key i{{display:inline-block;width:9px;height:9px;border-radius:50%;background:var(--accent);margin-right:6px;vertical-align:0}} .chart .key i.g{{background:var(--mute);opacity:.9;width:10px;height:10px;box-shadow:0 0 0 1.5px var(--paper),0 0 0 2.5px var(--rule)}}
.chart .ct{{font-family:var(--ui);font-weight:600;font-size:15px;letter-spacing:.04em;margin:0 0 10px;color:var(--ink)}}
.chart{{--k-life:var(--ink);--k-teach:var(--accent);--k-serve:#265b76;--k-write:#9a6a12;--k-legacy:#8a8072}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]) .chart{{--k-serve:#7fb4d0;--k-write:#d9a94a}}}} :root[data-theme="dark"] .chart{{--k-serve:#7fb4d0;--k-write:#d9a94a}}
/* the chronology under the two-scale timeline: a card that reads down, linked to the line */
.chart .tlx{{display:block;columns:3 240px;column-gap:34px;column-rule:1px solid color-mix(in oklab,var(--rule) 70%,transparent);background:var(--tlcard);border:1px solid var(--rule);border-radius:6px;padding:16px 22px 18px;margin-top:18px;box-shadow:0 1px 0 rgba(0,0,0,.03),0 8px 24px -16px rgba(40,30,20,.25)}}
.chart{{--tlcard:#fffdf9}} @media (prefers-color-scheme:dark){{:root:not([data-theme="light"]) .chart{{--tlcard:#1f1c17}}}} :root[data-theme="dark"] .chart{{--tlcard:#1f1c17}}
.chart .tlx li{{break-inside:avoid;border-radius:4px;margin:0 -8px;padding:5px 8px;transition:background .15s}}
.chart .tlx li b{{display:flex;align-items:baseline;gap:6px;color:var(--ink)}} .chart .tlx li b::before{{content:"";width:6px;height:6px;border-radius:50%;background:var(--k,var(--ink));flex:none;position:relative;top:-1px}}
.chart .tlx li.has span{{text-decoration:none;color:var(--ink)}} .chart .tlx li.has span::after{{content:" +";color:var(--mute);font-size:.85em}}
.chart .tlx li.k-legacy span{{color:var(--mute)}}
.chart .tlx li.era{{display:block;column-span:all;margin:0 0 6px;padding:2px 0 8px;border-radius:0;border-bottom:1px solid var(--rule);font-size:11px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--mute)}} .chart .tlx li.era.e2{{margin-top:14px}}
.chart .tlx li.lit{{background:color-mix(in oklab,var(--accent) 12%,transparent)}}
.chart svg.tl2 .lit{{stroke:var(--accent)!important;stroke-width:3px!important}} .chart svg.tl2 text.lit{{fill:var(--accent)!important;stroke:none!important}}
.chart .tlrows{{display:none}} .chart .tlrl{{font-family:var(--ui);font-size:12px;color:var(--mute);margin:10px 0 0}}
@media (max-width:600px){{.chart svg.tl2{{display:none}} .chart .tlrows{{display:block}} .chart .tlrows svg+.tlrl{{margin-top:4px}}}}
.chart .cdotk{{fill:var(--k)}} .chart text.cvk[data-pb]{{pointer-events:auto;cursor:pointer}} .chart text.cvk[data-pb]:hover,.chart text.cvk[data-pb]:focus-visible{{text-decoration:underline;outline:none}} .chart .cvk{{font-family:var(--ui);font-weight:700;font-size:12px;fill:var(--k);stroke:var(--paper);stroke-width:3px;paint-order:stroke;stroke-linejoin:round;font-variant-numeric:tabular-nums}} .chart .cfan{{fill:none;stroke:var(--rule);stroke-width:1}} .chart .cbrk{{stroke:var(--mute);stroke-width:1.5;fill:none}}
.chart .hit:hover+.cvk,.chart g:hover .cdotk{{stroke:var(--paper);stroke-width:2}}
.chart .k-life{{--k:var(--k-life)}} .chart .k-teach{{--k:var(--k-teach)}} .chart .k-serve{{--k:var(--k-serve)}} .chart .k-write{{--k:var(--k-write)}} .chart .k-legacy{{--k:var(--k-legacy)}}
.chart .kkey{{display:flex;flex-wrap:wrap;gap:4px 16px;font-family:var(--ui);font-size:12px;color:var(--mute);margin:0 0 16px}} .chart .kkey i{{display:inline-block;width:9px;height:9px;border-radius:50%;background:var(--k);margin-right:6px}}
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
/* The mid-year letter: graphics a size larger, with stronger color */
.letter{{--accent:#46347e;--acc2:#b8862e}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]) .letter{{--accent:#a993ea;--acc2:#e2b85c}}}} :root[data-theme="dark"] .letter{{--accent:#a993ea;--acc2:#e2b85c}}
.letter .prose>.chart{{grid-column:2/4;max-width:580px;background:var(--tabon-white,#fff);border:1px solid var(--rule);border-top:3px solid var(--accent);padding:clamp(18px,2.4vw,28px) clamp(18px,2.6vw,32px) clamp(14px,2vw,22px);margin:2.4em 0}}
.letter .prose>.chart.sized{{max-width:580px}}
.letter .chart .ct{{font-size:17px;color:var(--ink);margin-bottom:14px}}
.letter .chart .cn{{color:color-mix(in oklab,var(--ink) 70%,var(--mute))}}
.letter .chart text.cl{{fill:var(--ink)}}
.letter .chart g.hit:first-of-type .cb{{fill:color-mix(in oklab,var(--accent) 35%,var(--rule))}}
.letter .chart .ctrack{{fill:color-mix(in oklab,var(--accent) 16%,var(--rule))}} .letter .chart .ctick{{stroke:var(--acc2);stroke-width:2.5}}
.letter .chart .cthr{{stroke:var(--acc2)}} .letter .chart .cdotm{{opacity:.85}}
.letter .figsent b{{color:var(--accent)}} .letter .figsent{{grid-column:2/4;max-width:760px}}
.prose .salute{{font-style:italic;margin-bottom:1.2em}}
.prose .sign{{margin-top:2em;font-style:italic}} .prose .sign b{{font-style:normal;font-family:var(--ui);font-size:12px;letter-spacing:.12em;text-transform:uppercase;font-weight:600;color:var(--accent)}}
.prose .ext{{margin:1.4em 0 1.6em;padding:0 0 0 20px;border-left:2px solid var(--rule);font-size:.94em}}
.prose .ext p{{margin:0}} .prose .ext2{{margin-left:20px}}
.prose .qs{{margin:0 0 1.4em;padding-left:1.2em}} .prose .qs li{{margin:0 0 .6em;text-wrap:pretty}}
.prose .kv{{margin:1.2em 0 1.8em;display:grid;grid-template-columns:minmax(10ch,14ch) 1fr;gap:8px 18px;font-size:15.5px;line-height:1.5}}
.prose .kv dt{{font-family:var(--ui);font-weight:600;font-size:12.5px;letter-spacing:.04em;color:var(--accent);padding-top:2px}} .prose .kv dd{{margin:0}}
.prose .figs{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:18px;margin:1.8em 0 2.2em}}
.prose .figs div{{border-top:3px solid var(--accent);padding-top:10px;min-width:0}} .prose .figs b.wd{{font-size:clamp(22px,2.2vw,28px);line-height:1.1;letter-spacing:-.02em}}
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
/* Illumination: passages from the Writings and the Universal House of Justice in the full edition */
.members{{--gilt:#a47628;--gilt2:#d9b562;--star:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 48 48'%3E%3Cpath fill='%23b8893a' d='M22.0121%2012.0305L23.9836%208.64366L25.9552%2012.0305L27.4999%2014.6878L30.3894%2013.6493L34.0717%2012.3258L33.4077%2016.1878L32.8894%2019.2183L35.7688%2020.2839L39.4375%2021.6414L36.4531%2024.1731L34.1089%2026.1584L35.6333%2028.8292L37.5744%2032.233L33.6618%2032.25L30.5927%2032.2636L30.0473%2035.2907L29.3529%2039.1459L26.3447%2036.6414L23.9836%2034.6731L21.6225%2036.6414L18.6144%2039.1459L17.92%2035.2907L17.3746%2032.2636L14.3055%2032.25L10.3929%2032.233L12.334%2028.8292L13.8583%2026.1584L11.5142%2024.1731L8.52977%2021.6414L12.2018%2020.2839L15.0812%2019.2183L14.5629%2016.1878L13.899%2012.3258L17.5812%2013.6493L20.4708%2014.6878L22.0155%2012.0305H22.0121ZM18.523%209.3733L8.32652%205.70475L10.1626%2016.4016L0%2020.1584L8.26894%2027.1697L2.89294%2036.5905L13.7262%2036.638L15.6537%2047.3179L23.9836%2040.3778L32.3136%2047.3179L34.241%2036.638L45.0743%2036.5905L39.6983%2027.1697L47.9673%2020.1584L37.8047%2016.4016L39.6408%205.70475L29.4443%209.3733L23.9803%200L18.523%209.3767V9.3733Z'/%3E%3C/svg%3E")}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]) .members{{--gilt:#d4b062;--gilt2:#f0d690}}}} :root[data-theme="dark"] .members{{--gilt:#d4b062;--gilt2:#f0d690}}
.members .passage,.members .ext.sacred{{position:relative;border:0;padding:2px 0 0 24px;margin:0 0 1.9em}}
.members .passage::before,.members .ext.sacred::before{{content:"";position:absolute;left:0;top:.4em;bottom:.2em;width:1.5px;background:linear-gradient(var(--gilt2),var(--gilt) 55%,transparent)}}
.members .passage p::first-letter,.members .ext.sacred p::first-letter{{float:left;font-family:"Literata",serif;font-weight:600;font-size:2.6em;line-height:.82;margin:.1em .1em 0 0;color:var(--gilt);font-variation-settings:"opsz" 72}}
.members .passage cite{{display:flex;align-items:center;gap:10px;margin-top:10px}} .members .passage cite::before{{content:"";flex:none;width:18px;height:1px;background:var(--gilt)}}
.members .passage.lead,.members .passage.prayer{{padding:46px clamp(18px,5vw,48px) 30px;margin:0 0 2.4em;text-align:center;background:radial-gradient(120% 90% at 50% 0,color-mix(in oklab,var(--gilt2) 16%,transparent),transparent 70%);border-top:1px solid color-mix(in oklab,var(--gilt) 55%,transparent);border-bottom:1px solid color-mix(in oklab,var(--gilt) 55%,transparent)}}
.members .passage.lead::before,.members .passage.prayer::before{{left:50%;top:-11px;bottom:auto;width:22px;height:22px;margin-left:-11px;background:var(--paper) var(--star) center/18px no-repeat;border-radius:50%}}
.members .passage.lead p::first-letter,.members .passage.prayer p::first-letter{{float:none;font-size:1.5em;line-height:1;margin:0}}
.members .passage.lead cite,.members .passage.prayer cite{{justify-content:center}} .members .passage.lead cite::after,.members .passage.prayer cite::after{{content:"";flex:none;width:18px;height:1px;background:var(--gilt)}}
.members .passage.prayer p{{font-size:20px}}
.members{{--lap:#23406f}} @media (prefers-color-scheme:dark){{:root:not([data-theme="light"]) .members{{--lap:#2c4c80}}}} :root[data-theme="dark"] .members{{--lap:#2c4c80}}
.members .passage.prayer.illum{{position:relative;background:var(--tabon-white,#fdfcf9);text-align:left;margin:2.4em 0;padding:40px clamp(26px,5vw,52px) 36px;border:3px solid var(--gilt);box-shadow:inset 0 0 0 4px var(--tabon-white,#fdfcf9),inset 0 0 0 6px var(--lap),inset 0 0 0 9px var(--tabon-white,#fdfcf9),inset 0 0 0 10px var(--ver)}}
.members{{--ver:#b5452c}} @media (prefers-color-scheme:dark){{:root:not([data-theme="light"]) .members{{--ver:#d8735a}}}} :root[data-theme="dark"] .members{{--ver:#d8735a}}
.members .passage.prayer.illum .jc{{position:absolute;width:30px;height:30px}} .members .passage.prayer.illum .jc1{{left:-16px;top:-16px}} .members .passage.prayer.illum .jc2{{right:-16px;top:-16px}} .members .passage.prayer.illum .jc3{{left:-16px;bottom:-16px}} .members .passage.prayer.illum .jc4{{right:-16px;bottom:-16px}}
.members .passage.prayer.illum::before{{content:none}}
.visit{{padding-top:0!important;margin-top:clamp(40px,6vw,72px)}} .visit .prose{{grid-row:1}} .members .passage.prayer.illum .rose{{display:block;width:84px;height:84px;margin:0 auto 22px}}
.members .passage.prayer.illum p::first-letter{{all:unset}}
.members .passage.prayer.illum .vbox{{float:left;width:5em;height:5em;margin:.35em .9em .2em 0}} .members .passage.prayer.illum .vbox svg{{display:block;width:100%;height:100%}}
.members .passage.prayer.illum .vh{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}}
.members .passage.prayer.illum .ln{{display:block;margin:0 0 .55em}}
.members .passage.prayer.illum cite{{justify-content:center;clear:both;padding-top:8px}}
.members.compilation h3::before,.members .compilation h3::before{{content:"";display:block;width:16px;height:16px;margin:0 0 12px;background:var(--star) center/contain no-repeat}}

.shelf .books{{list-style:none;margin:0 0 1.6em;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:22px 28px}}
.shelf .books li{{border-top:1px solid var(--rule);padding-top:12px}}
.shelf li h3{{font-family:var(--disp);font-weight:700;font-size:18px;letter-spacing:-.015em;text-transform:none;color:inherit;padding-top:0;border-top:0;line-height:1.6;margin:0 0 4px}}
.shelf .sub{{font-family:var(--ui);font-size:12.5px;color:var(--mute);margin:0 0 8px}}
.shelf .books p{{font-size:15px;line-height:1.5;margin:0 0 8px}}
.shelf .price{{font-family:var(--ui);font-size:12.5px;font-weight:600;color:var(--accent)}}
.shelf li h3 a{{color:inherit;text-decoration:none;background-image:linear-gradient(var(--accent),var(--accent));background-size:100% 1px;background-repeat:no-repeat;background-position:0 100%}}
.shelf li h3 a:hover,.shelf li h3 a:focus-visible{{color:var(--accent)}}
.shelf .buy{{display:block;margin-top:4px;font-weight:500;color:var(--accent)}}
.notices{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:28px}}
.dept .prose:has(.notices){{grid-column:2/4;display:block;max-width:none}}
.notices li{{border-top:3px solid var(--accent);padding-top:14px}}
.notices img{{display:block;width:120px;height:auto;border:1px solid var(--rule);margin:0 0 12px}}
.notices .k{{font-family:var(--ui);font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--mute);margin:0 0 6px}}
.notices li h3{{font-family:var(--disp);font-weight:700;font-size:20px;letter-spacing:-.02em;text-transform:none;color:inherit;padding-top:0;border-top:0;line-height:1.6;margin:0 0 8px}}
.notices p{{font-size:15.5px;line-height:1.55;margin:0 0 8px}}
.notices cite{{font-style:normal;font-family:var(--ui);font-size:12.5px;color:var(--accent)}}
.prose>.shelf,.prose>.calendar{{grid-column:2/4}}
.dept .prose.shelf,.dept .prose.calendar{{grid-column:1/-1;display:block;max-width:none}}
.dept .prose.calendar{{max-width:72ch;grid-column:2/4}}
.dept .prose.shelf{{grid-column:2/4}}
#rhythm,#books{{zoom:.85}}
.dept .margin,.letter .margin{{grid-row:2}}
.dept .prose,.letter .prose{{grid-row:2}}
.dept .shead,.letter .shead{{grid-row:1}}

.head.member nav a{{padding:18px 13px 0;font-size:14.5px}}
@media (max-width:980px){{.calendar .cal{{grid-template-columns:1fr}}}}
/* running head */
body::before{{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--paper)}}
.head{{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:color-mix(in oklab,var(--bar) 94%,transparent);backdrop-filter:blur(10px);border-bottom:1px solid var(--barrule)}}
.head .in{{max-width:1120px;margin:0 auto;{GUT}display:flex;align-items:stretch;gap:0;overflow-x:auto;scrollbar-width:none;position:relative}}
.head .brand{{font-family:var(--disp);font-size:17px;font-weight:700;letter-spacing:-.02em;color:var(--ink);text-decoration:none;white-space:nowrap;align-self:center;position:relative;padding-right:28px;margin-right:4px}}
.head .brand::after{{content:"";position:absolute;right:0;top:12%;bottom:12%;width:1px;background:var(--barrule)}}
.head .brand b{{font-family:var(--text);font-weight:600;font-size:18.5px;letter-spacing:-.015em;font-variation-settings:"opsz" 24}}
.head .brand .sc{{font-style:normal;font-variant-caps:all-small-caps;letter-spacing:.06em;font-weight:500}}
.head .brand .star path{{transition:fill .5s}} .head .brand.tinted .star path{{fill:var(--sc)}}
.head .brand .star{{transform:translateY(-1px) rotate(var(--rot,0deg));transition:transform .4s cubic-bezier(.2,.8,.2,1)}}
@media (prefers-reduced-motion:reduce){{.head .brand .star{{transform:translateY(-1px)!important}}}}
.head .brand .bn{{display:inline-flex;align-items:center;gap:6px}}
.head .brand .star{{width:17px;height:17px;flex:none}}
.head .brand small{{display:block;font-weight:400;font-size:11px;color:var(--mute);letter-spacing:.02em}}
.head nav{{display:flex;margin-left:auto}}
.head nav a{{display:flex;align-items:flex-end;position:relative;padding:18px 16px 0;border-bottom:4px solid var(--tint);color:var(--ink);text-decoration:none;font-family:var(--disp);font-weight:600;font-size:15px;letter-spacing:-.01em;white-space:nowrap}}
.head nav a span{{padding-bottom:12px}}
.head nav a.on,.head nav a:hover,.head nav a:focus-visible{{background:var(--tabon)}}
.head nav a .fill{{position:absolute;left:0;bottom:-4px;height:4px;width:0;background:var(--ink);opacity:.9;transition:width .4s cubic-bezier(.2,.8,.2,1)}}
.head nav a.on .fill{{width:var(--p,0%)}}
.head .ind{{position:absolute;bottom:-1px;height:2px;background:var(--ink);transition:left .5s cubic-bezier(.2,.8,.2,1),width .5s cubic-bezier(.2,.8,.2,1)}}
@media (prefers-reduced-motion:reduce){{.head nav a .fill,.head .ind{{transition:none}}}}
.head .rh,.head .rht,.head .rhp,.head .rhs{{display:none}}
@media (max-width:700px){{
.head .in{{overflow:visible;align-items:center;min-height:54px}} .head nav,.head .ind{{display:none}}
.head .brand{{padding-right:0;margin-right:10px}} .head .brand::after,.head .brand b{{display:none}} .head .brand .star{{width:20px;height:20px}}
.head .rh{{display:flex;flex:1;min-width:0;flex-direction:column;gap:1px;background:none;border:0;padding:6px 0;text-align:left;color:var(--ink);cursor:pointer;font:inherit}}
.head .rh small{{font-family:var(--text);font-size:11.5px;color:var(--mute);line-height:1.2}}
.head .rh b{{font-family:var(--ui);font-weight:600;font-size:15.5px;display:flex;align-items:center;gap:7px;line-height:1.25;min-width:0}} .head .rh b span{{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.head .rh b i{{width:8px;height:8px;border-radius:50%;background:var(--rt,transparent);flex:none}} .head:not(.inside) .rh b i{{display:none}}
.head .rht{{display:grid;place-items:center;width:44px;height:44px;margin-right:-10px;border:0;background:none;color:var(--ink);cursor:pointer}} .head .rht svg{{transition:transform .25s}} .head.open .rht svg{{transform:rotate(180deg)}}
.head .rhp{{display:block;position:absolute;left:0;bottom:-1px;height:3px;width:var(--rp,0%);background:var(--rt,transparent);transition:width .15s}}
.head .rhs{{display:block;position:absolute;left:0;right:0;top:100%;max-height:calc(100dvh - 70px);overflow-y:auto;background:var(--bar);border-bottom:1px solid var(--barrule);box-shadow:0 14px 24px rgb(0 0 0/.12);opacity:0;visibility:hidden;transform:translateY(-6px);transition:opacity .18s,transform .18s,visibility 0s .18s}}
.head.open .rhs{{opacity:1;visibility:visible;transform:none;transition:opacity .18s,transform .18s}}
.head .rhs-c{{padding:16px 18px 6px}}
.head .rhs-c .rhm{{display:flex;justify-content:space-between;font-family:"Literata",var(--text),serif;font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--mute);border-bottom:1px solid var(--ink);padding-bottom:8px}}
.head .rhs-c .rhtt{{font-family:"Literata",var(--text),serif;font-weight:500;font-size:29px;line-height:1.1;margin:10px 0 10px;color:var(--ink)}}
.head .rhs-c a[data-name]{{display:grid;grid-template-columns:44px 1fr;gap:12px;align-items:baseline;padding:12px 0;border-top:1px solid var(--barrule);color:var(--ink);text-decoration:none}}
.head .rhs-c .pn{{font-family:"Literata",var(--text),serif;font-weight:600;font-size:25px;line-height:1;color:var(--tint);font-variant-numeric:lining-nums}}
.head .rhs-c .k{{display:block;font-family:var(--ui);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--mute);margin-bottom:2px}}
.head .rhs-c .tt{{display:block;font-family:var(--text);font-size:16px;line-height:1.3}}
.head .rhs-c .rd{{display:none;height:3px;background:var(--barrule);margin-top:8px;border-radius:2px;overflow:hidden}} .head .rhs-c .rd i{{display:block;height:100%;width:var(--rp,0%);background:var(--tint)}}
.head .rhs-c a.on .tt{{font-weight:600}} .head .rhs-c a.on .rd{{display:block}}
.head .rhs-c .rhf{{display:flex;justify-content:space-between;gap:12px;border-top:1px solid var(--ink);margin-top:2px;padding:12px 0 8px;font-family:var(--ui);font-size:13.5px}}
.head .rhs-c .rhf a{{color:var(--mute);min-height:32px;display:flex;align-items:center}}

.head .rhs-b{{padding:10px;background:var(--paper)}}
.head .rhs-b .rhi{{font-family:"Literata",var(--text),serif;font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--mute);margin:4px 6px 8px}}
.head .rhs-b a[data-name]{{position:relative;overflow:hidden;display:flex;align-items:center;flex-wrap:wrap;gap:0 12px;min-height:54px;margin-bottom:6px;padding:0 16px;border-radius:8px;background:var(--tint);color:#fff;text-decoration:none}}
.head .rhs-b a.dk{{color:#1d1a16}}
.head .rhs-b .nm{{font-family:var(--ui);font-weight:700;font-size:19px}}
.head .rhs-b .pp{{margin-left:auto;font-family:var(--ui);font-size:13px;opacity:.9}}
.head .rhs-b .cur{{display:none;width:100%;font-family:var(--ui);font-size:10.5px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;opacity:.9}}
.head .rhs-b .bar{{position:absolute;left:0;bottom:0;height:4px;width:var(--rp,0%);background:currentColor;opacity:.85;display:none}}
.head .rhs-b a.on{{min-height:84px;align-content:center;background:var(--tint)}} .head .rhs-b a.on .cur,.head .rhs-b a.on .bar{{display:block}}
.head .rhs a:focus-visible{{outline:2px solid var(--ink);outline-offset:-2px}}
.head .rhs a small{{margin-left:auto;flex:none;font-family:var(--ui);font-size:11.5px;color:var(--mute);font-variant-numeric:tabular-nums}} .head .rhs a.on{{background:var(--tabon)}}
}}
@media (prefers-reduced-motion:reduce){{.head .rhs,.head .rhp,.head .rht svg{{transition:none}}}}
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
.plate:has(.ovw:not(.nyo):not(.gro):not(.evo)){{background:#1a0f0b;border-color:#1a0f0b}}
/* New Yorkers: the print title set beneath the brush-stroke cut */
.ovw.nyo{{padding-bottom:0}}
.nyo .ov{{text-shadow:none;color:var(--accent)}}
.nyo .ov .nyb{{position:absolute;left:40%;top:auto;bottom:1.5%;width:58%;height:auto;container-type:inline-size}}
.nyo .ov span{{position:relative;display:block;white-space:nowrap}}
.nyo .n1{{font-family:"Bricolage Grotesque",sans-serif;font-weight:300;font-size:22.6cqw;line-height:.74;letter-spacing:-.045em;margin-left:9.4%;font-variation-settings:"opsz" 96,"wdth" 75;transform:scaleX(.86);transform-origin:left}}
.nyo .n2{{font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:22.6cqw;line-height:.74;letter-spacing:-.03em;margin:.06em 0 0 6.2%;font-variation-settings:"opsz" 96}}
.nyo .n3{{font-family:"Literata",Georgia,serif;font-style:italic;font-weight:400;font-size:4.3cqw;line-height:1;color:var(--ink);margin-top:.75em;text-shadow:0 0 3px var(--paper),0 0 8px var(--paper),0 0 14px var(--paper);letter-spacing:-.005em}}
.nyo .n3 b{{font-weight:800}}
.ovw{{position:relative;width:min(100%,calc(92vh * var(--ar)));margin:0 auto;container-type:inline-size}}
.ovw img{{max-height:none;background:none}}
.ov{{position:absolute;inset:0;color:#fff;pointer-events:none;text-shadow:0 1px 2px rgba(20,6,2,.35),0 6px 28px rgba(30,10,5,.55)}}
.ov span{{position:absolute;white-space:nowrap;line-height:.9}}
.ov .t1{{left:2%;top:18.25%;font-family:"Literata",serif;font-weight:500;font-size:20cqw;letter-spacing:-.03em;font-variation-settings:"opsz" 48}}
.ov .t1 i{{font-style:italic}}
.ov .t2{{left:36%;top:27.25%;font-family:"Pinyon Script",cursive;font-size:17cqw}}
.ov .t3{{right:8%;top:36.25%;font-family:"Literata",serif;font-weight:500;font-size:15.5cqw;letter-spacing:-.035em;font-variation-settings:"opsz" 48}}
.ov .byl{{left:9%;top:58%;font-family:"Literata",serif;font-weight:600;font-size:3.2cqw;letter-spacing:.02em;font-variation-settings:"opsz" 11}}
.ov .sub{{right:1.5%;top:52%;font-family:"Literata",serif;font-style:italic;font-weight:400;font-size:4.8cqw;line-height:1.12;text-align:right;white-space:normal;width:48%;font-variation-settings:"opsz" 18}}
@media (prefers-reduced-motion:no-preference){{.ov span:not(.nyb){{animation:ovin 1.6s cubic-bezier(.2,.7,.2,1) both}} .nyo .n2{{animation-delay:.25s}} .nyo .n3{{animation-delay:.5s}} .ov .t2{{animation-delay:.25s}} .ov .t3{{animation-delay:.45s}} .ov .byl,.ov .sub{{animation-delay:.7s}}}}
@keyframes ovin{{from{{opacity:0;filter:blur(6px)}}}}
/* New Yorkers: the two words drift apart a few pixels as the image scrolls past; the bold words wash in with the story color */
.nyo .n3 b{{color:var(--accent);text-shadow:none}}
@media (prefers-reduced-motion:no-preference){{
.ovready .nyo .n3 b{{background:linear-gradient(90deg,var(--accent) 0 50%,var(--ink) 50% 100%);background-size:200% 100%;background-position:100% 0;-webkit-background-clip:text;background-clip:text;color:transparent}}
.ovready .nyo.go .n3 b{{background-position:0 0;transition:background-position 1.3s cubic-bezier(.4,.1,.2,1) .9s}} .ovready .nyo.go .n3 b+b{{transition-delay:1.5s}}
}}
.nyo .n1{{transform:translateX(calc(var(--dr,0) * -1px)) scaleX(.86)}} .nyo .n2{{transform:translateX(calc(var(--dr,0) * 1px))}}
/* Two artists: the script is traced by pen, then inked; a band of warm light crosses the lettering once */
.ov .t2{{display:none}}
.ov .pen{{position:absolute;inset:0;width:100%;height:100%;overflow:visible;filter:drop-shadow(0 1px 2px rgba(20,6,2,.35)) drop-shadow(0 6px 22px rgba(30,10,5,.5))}}
.ov .pen text{{font-family:"Pinyon Script",cursive;font-size:170px;fill:#fff;stroke:#fff;stroke-width:0;stroke-linejoin:round}}
.ov .sweep{{position:absolute;inset:0;pointer-events:none;background:linear-gradient(105deg,transparent 40%,rgba(255,214,150,0) 44%,rgba(255,214,150,.55) 50%,rgba(255,214,150,0) 56%,transparent 60%);background-size:250% 100%;background-position:120% 0;mix-blend-mode:soft-light}}
@media (prefers-reduced-motion:no-preference){{
.ovready .ov .pen{{clip-path:inset(0 63% 0 0)}} .ovready .ov .pen text{{fill-opacity:0;stroke-width:1.6;stroke-dasharray:420;stroke-dashoffset:420}}
.ovready .ovw.go .ov .pen{{animation:penclip 2.2s cubic-bezier(.5,.1,.4,1) .3s forwards}}
.ovready .ovw.go .ov .pen text{{animation:pendraw 2.6s cubic-bezier(.45,.05,.3,1) .3s forwards,penfill .9s ease-out 2.2s forwards}}
.ovready .ovw.go .ov .sweep{{animation:sweep 1.8s cubic-bezier(.4,.1,.3,1) 2.3s both}}
}}
@keyframes penclip{{to{{clip-path:inset(0 0 0 0)}}}} @keyframes pendraw{{to{{stroke-dashoffset:0}}}} @keyframes penfill{{to{{fill-opacity:1;stroke-width:0}}}}
@keyframes sweep{{from{{background-position:120% 0}}to{{background-position:-20% 0}}}}
/* ABS at 50: a footnote, as in a scholarly paper */
.fnote{{margin:0 0 clamp(28px,4vw,48px);color:var(--ink)}}
.fbig{{font-family:"Fraunces",var(--text),serif;font-weight:300;font-size:clamp(140px,26vw,330px);line-height:.8;letter-spacing:-.04em;color:var(--accent);font-variation-settings:"opsz" 144}}
.fbig sup{{font-size:.22em;vertical-align:top;position:relative;top:.35em;margin-left:.06em;font-weight:500}}
.frule{{width:min(28%,220px);height:1.5px;background:var(--ink);margin:clamp(18px,3vw,32px) 0 10px;transform-origin:left}}
.fnt{{font-family:"Fraunces",var(--text),serif;font-size:clamp(15px,1.6vw,18px);line-height:1.5;max-width:52ch;margin:0;font-variation-settings:"opsz" 12}}
.fnt sup{{font-size:.7em}}
@media (prefers-reduced-motion:no-preference){{
.ovready .fbig span{{display:inline-block;opacity:0;transform:translateY(.12em)}} .ovready .fbig sup,.ovready .fnt{{opacity:0}} .ovready .frule{{transform:scaleX(0)}}
.ovready .fnote.go .fbig span{{opacity:1;transform:none;transition:opacity .9s,transform .9s cubic-bezier(.2,.8,.2,1)}}
.ovready .fnote.go .fbig sup{{opacity:1;transition:opacity .6s 1s}} .ovready .fnote.go .frule{{transform:none;transition:transform .6s 1.4s}} .ovready .fnote.go .fnt{{opacity:1;transition:opacity .8s 1.8s}}
}}
/* Comic: splash page */
@media (max-width:600px){{.story>.csplash{{aspect-ratio:16/7}}}}
.csplash{{position:relative;overflow:hidden;container-type:inline-size;aspect-ratio:16/5;background:#f0b429;display:grid;place-items:center;margin:0 0 clamp(16px,2.4vw,28px);border-radius:4px}}
.csplash .burst{{position:absolute;inset:-20%;background:repeating-conic-gradient(from 0deg,rgba(255,255,255,.42) 0 6deg,transparent 6deg 18deg)}}
.csplash .tt{{position:relative;text-align:center;font-family:"Bangers",var(--disp),cursive;color:#fff;-webkit-text-stroke:.4cqw #1d1a16;paint-order:stroke fill;text-shadow:.6cqw .6cqw 0 #1d1a16;font-size:9cqw;line-height:1;white-space:nowrap;margin-top:3cqw;letter-spacing:.04em;transform:rotate(-4deg)}}
.csplash .k{{position:absolute;left:4cqw;top:4cqw;background:#fff6c9;color:#1d1a16;border:.3cqw solid #1d1a16;padding:.8cqw 1.4cqw;font-family:"Bangers",var(--disp),cursive;font-size:max(11px,1.9cqw);letter-spacing:.08em}}
@media (prefers-reduced-motion:no-preference){{
.ovready .csplash .burst{{transform:rotate(-40deg) scale(.6);opacity:0}} .ovready .csplash .tt{{transform:scale(.4) rotate(-6deg);opacity:0}} .ovready .csplash .k{{opacity:0}}
.ovready .csplash.go .burst{{transform:none;opacity:1;transition:transform 1.6s cubic-bezier(.2,.8,.2,1),opacity .6s}}
.ovready .csplash.go .tt{{transform:rotate(-4deg);opacity:1;transition:transform .7s cubic-bezier(.3,1.6,.5,1) .5s,opacity .3s .5s}}
.ovready .csplash.go .k{{opacity:1;transition:opacity .4s 1.2s}}
}}
/* Louis Gregory: a broadside, the name pressed in letter by letter */
.gro .ov{{text-shadow:none;color:#1d1a16}}
.gro .ov span{{animation:none!important}}
.gro .gbs{{position:absolute;right:2.5%;top:4%;width:auto;white-space:normal;line-height:1;background:rgba(247,242,234,.62);-webkit-backdrop-filter:blur(3px);backdrop-filter:blur(3px);padding:1.2cqw 1.4cqw;box-shadow:0 .4cqw 1.6cqw rgba(0,0,0,.12)}}
.gro .gbs span{{position:relative;white-space:normal}} .gro .gbs .gnm{{white-space:nowrap}}
.gro .gnm{{display:block;font-family:"Big Shoulders Display",sans-serif;font-weight:900;font-size:5.8cqw;line-height:.86;text-transform:uppercase;white-space:nowrap}}
.gro .gl{{display:inline-block}}
.gro .gyr{{display:flex;justify-content:space-between;font-family:"Libre Caslon Text",serif;font-size:2.2cqw;margin:.35em 0 .2em;border-bottom:.25cqw solid #1d1a16;padding-bottom:.25em;font-variant-numeric:oldstyle-nums}}
@media (prefers-reduced-motion:no-preference){{
.ovready .gro .gl{{transform:scale(1.12);opacity:0;filter:blur(1.5px)}} .ovready .gro .gyr{{opacity:0}}
.ovready .gro.go .gl{{transform:none;opacity:1;filter:none;transition:transform .5s cubic-bezier(.2,.9,.2,1) var(--d),opacity .35s var(--d),filter .5s var(--d)}}
.ovready .gro.go .gyr{{opacity:1;transition:opacity .8s .9s}}
}}

.plate.bare{{background:transparent;border:0}}
.plate.bare img{{max-height:none;object-fit:contain;max-width:1000px}}
.plate.bare figcaption{{padding-left:0}}
.prose>.plate.comic{{grid-column:1/-1;margin:0 0 clamp(28px,4vw,44px)}}
.plate figcaption a{{color:inherit;text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:3px}} .plate figcaption a:hover{{text-decoration-thickness:2px}}
.plate.comic{{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--rule)}}
.plate.comic img{{max-height:none;background:#fff}}
.plate.comic figcaption{{grid-column:1/-1;background:var(--cream)}}
.plate figcaption{{font-family:var(--ui);font-size:12px;letter-spacing:.06em;color:var(--mute);padding:10px 14px}}
/* article grid: a 3-column field. Margin column at left holds kicker, byline, pages; the headline spans the field; prose sits in the middle column with air on both sides; pull quotes hang into the left margin, photographs span margin and text. */
.story{{display:grid;grid-template-columns:minmax(200px,26ch) minmax(0,64ch) minmax(0,1fr);column-gap:clamp(24px,4vw,56px)}}
.story>.plate,.story>.fnote,.story>.csplash{{grid-column:1/-1}}
.story>.plate:has(.evo){{justify-self:center;width:min(100%,800px)}}
/* the quilt as a paper envelope, tilted */
.ovw.evo{{background:#fffdf6;padding:14px;box-sizing:content-box;width:min(calc(100% - 28px),calc(92vh * var(--ar)));transform:rotate(-1.4deg);box-shadow:0 2px 3px rgba(0,0,0,.08),0 18px 36px rgba(29,26,22,.22);margin:10px auto 18px}}
.ovw.evo>img{{display:block;width:100%;height:auto}}
.ovw.evo .ov{{inset:14px}}
.ovw.evo::after{{content:"";position:absolute;left:14px;right:14px;top:14px;height:46%;z-index:2;pointer-events:none;background:linear-gradient(to bottom right,transparent 49.5%,rgba(255,253,246,.7) 50%,transparent 50.8%) left/50% 100% no-repeat,linear-gradient(to bottom left,transparent 49.5%,rgba(255,253,246,.7) 50%,transparent 50.8%) right/50% 100% no-repeat}}
.ovw.evo::before{{content:"183 B.E.";position:absolute;top:28px;right:28px;z-index:3;width:clamp(52px,10cqw,84px);aspect-ratio:84/112;box-sizing:border-box;padding:6px 6px 0;display:flex;align-items:flex-end;justify-content:center;white-space:nowrap;font:700 clamp(7px,1.2cqw,10px)/1.6 "Barlow Condensed","Arial Narrow",sans-serif;letter-spacing:.08em;color:#222e4c;
  background:url(img/motif/m12.webp) center 6px/calc(100% - 12px) calc(100% - 26px) no-repeat,#fffdf6;filter:drop-shadow(0 2px 3px rgba(0,0,0,.25));--r:3.5px;
  -webkit-mask:radial-gradient(var(--r),#0000 97%,#000) round calc(-1.5*var(--r)) calc(-1.5*var(--r))/calc(3*var(--r)) calc(3*var(--r)),linear-gradient(#000 0 0) calc(1.5*var(--r)) calc(1.5*var(--r))/calc(100% - 3*var(--r)) calc(100% - 3*var(--r)) no-repeat;
  mask:radial-gradient(var(--r),#0000 97%,#000) round calc(-1.5*var(--r)) calc(-1.5*var(--r))/calc(3*var(--r)) calc(3*var(--r)),linear-gradient(#000 0 0) calc(1.5*var(--r)) calc(1.5*var(--r))/calc(100% - 3*var(--r)) calc(100% - 3*var(--r)) no-repeat}}
@media (prefers-reduced-motion:reduce){{.ovw.evo{{transform:none}}}} .story>.plate:has(.gro){{justify-self:center;width:min(100%,960px)}} .story>.plate:has(.nyo){{justify-self:center;width:min(100%,750px)}}
.shead{{grid-column:1/-1;margin:0 0 clamp(40px,6vw,88px);position:relative}}
.shead.nodek{{margin-bottom:clamp(20px,2.6vw,36px)}}
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
.prose>.margin{{grid-row:1;grid-column:1;padding-bottom:clamp(24px,3vw,40px)}}
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
.sharebtn{{display:inline-flex;align-items:center;gap:8px;margin-top:16px;min-height:40px;padding:0 14px 0 10px;border:1px solid var(--rule);border-radius:999px;background:transparent;color:var(--ink);font:inherit;font-family:var(--ui);font-size:13px;letter-spacing:0;text-transform:none;cursor:pointer}}
.sharebtn:hover{{border-color:var(--accent);color:var(--accent)}} .sharebtn:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}} .sharebtn svg{{width:18px;height:18px}}
@media (max-width:980px){{.sharebtn{{margin-top:0}}}}
.sharedlg{{border:0;border-radius:14px;padding:22px 22px 18px;width:min(440px,calc(100vw - 32px));background:var(--bar);color:var(--ink);box-shadow:0 24px 60px rgba(20,16,10,.28)}}
.sharedlg::backdrop,.svydlg::backdrop{{background:rgba(20,16,10,.38)}}
.svydlg{{border:0;border-radius:14px;padding:0;width:min(760px,calc(100vw - 32px));height:min(720px,calc(100dvh - 48px));background:var(--bar);color:var(--ink);box-shadow:0 24px 60px rgba(20,16,10,.28);overflow:hidden}}
.svydlg[open]{{display:flex;flex-direction:column}}
.svydlg .svh{{display:flex;justify-content:space-between;align-items:start;gap:12px;padding:18px 18px 14px 22px;border-bottom:1px solid var(--rule)}}
.svydlg .shk{{margin:0;font-family:var(--ui);font-size:11px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--mute)}}
.svydlg h2{{margin:0;font-family:var(--disp);font-size:20px;line-height:1.2;letter-spacing:-.01em}}
.svydlg .shx{{flex:none;width:40px;height:40px;border-radius:50%;border:0;background:transparent;color:var(--mute);cursor:pointer}} .svydlg .shx svg{{width:20px;height:20px}} .svydlg .shx:hover{{background:var(--tabon)}}
.svydlg .svf{{flex:1;min-height:0}} .svydlg iframe{{display:block;width:100%;height:100%;border:0;background:#fff}}
@media (max-width:640px){{.svydlg{{width:100vw;max-width:100vw;height:100dvh;max-height:100dvh;border-radius:0;margin:0}} .svydlg .svh{{padding-top:max(14px,env(safe-area-inset-top,0px))}}}}
.notices .svb{{display:flex;width:max-content;text-decoration:none;align-items:center;gap:8px;margin:6px 0 12px;padding:9px 16px;border:0;border-radius:999px;background:var(--accent);color:var(--paper);font:600 14px/1 var(--ui);cursor:pointer}}
.notices .svb:hover{{filter:brightness(1.08)}}
.notices li.svn .svm{{display:block;aspect-ratio:1;overflow:hidden;margin:0 0 14px;border-radius:2px}} .notices li.svn .svm img{{width:100%;height:100%;object-fit:cover;border:0;margin:0}}
.ask{{--navy:#222e4c;--blush:#f2cfc6;display:grid;grid-template-columns:1.15fr .85fr;background:var(--blush);color:var(--navy);margin:8px 0 56px;border-radius:4px;overflow:hidden}}
.ask .askq{{padding:clamp(24px,4vw,48px);min-width:0}}
.ask .askb{{font-family:"Barlow Condensed","Arial Narrow",var(--ui),sans-serif;font-weight:300;font-size:clamp(32px,3.6vw,46px);line-height:1;letter-spacing:0;text-transform:none;margin:0 0 14px;padding:0;border:0;color:inherit}} .ask .askb b{{font-weight:700}}
.ask .askr{{font-family:"Literata",var(--text),serif;font-style:italic;font-size:clamp(22px,2.4vw,30px);line-height:1.25;min-height:2.6em;margin:0 0 18px;transition:opacity .4s}}
.ask .askc{{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 22px}}
.ask .askc a{{font-family:"Barlow Condensed","Arial Narrow",var(--ui),sans-serif;font-size:18px;text-decoration:none;color:var(--navy);border:1.5px solid var(--navy);border-radius:999px;padding:5px 14px}}
.ask .askc a:hover,.ask .askc a:focus-visible{{background:var(--navy);color:var(--blush)}}
.ask .askg{{display:flex;flex-wrap:wrap;align-items:center;gap:10px 16px}}
.ask .askbtn,.nudge .nbtn{{font-family:"Barlow Condensed","Arial Narrow",var(--ui),sans-serif;font-weight:700;font-size:20px;letter-spacing:.02em;text-transform:uppercase;text-decoration:none;background:var(--navy);color:var(--blush);padding:10px 22px;border-radius:3px;white-space:nowrap;transition:transform .2s,box-shadow .2s}}
.ask .askbtn:hover{{transform:translateY(-2px);box-shadow:0 6px 16px rgba(0,0,0,.18)}}
.ask .askm{{font-family:"Barlow Condensed","Arial Narrow",var(--ui),sans-serif;font-size:17px}}
.ask .aski{{min-height:280px;position:relative}} .ask .aski img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
@media (max-width:720px){{.ask{{grid-template-columns:1fr}} .ask .aski{{min-height:0;aspect-ratio:16/9;order:-1}}}}
.front>div:first-child{{display:flex;flex-direction:column}}
.front .askw{{margin:32px 0 0;padding:12px;background:var(--bar);border:1px solid var(--rule);filter:drop-shadow(0 10px 18px rgba(29,26,22,.10));
  clip-path:polygon(0 1.5%,3% 0,7% 1.2%,12% .2%,18% 1.4%,25% .3%,31% 1.1%,38% 0,45% 1.3%,52% .2%,59% 1.2%,66% 0,73% 1.4%,80% .3%,87% 1.2%,93% 0,97% 1.3%,100% .4%,99.4% 8%,100% 16%,99.3% 25%,100% 34%,99.5% 43%,100% 52%,99.3% 61%,100% 70%,99.4% 79%,100% 88%,99.5% 96%,100% 100%,94% 99%,88% 100%,81% 98.8%,74% 100%,67% 99%,60% 100%,53% 98.7%,46% 100%,39% 99%,32% 100%,25% 98.9%,18% 100%,11% 99%,5% 100%,0 99%,.6% 90%,0 80%,.7% 70%,0 60%,.5% 50%,0 40%,.7% 30%,0 20%,.6% 10%)}}
.front .ask{{margin:0;border-radius:0;grid-template-columns:minmax(0,1fr) 36%}}
.front .ask .askq{{padding:24px 24px 26px}}
.front .ask .askb{{font-size:32px;margin-bottom:10px}}
.front .ask .askr{{font-size:20px;min-height:2.5em;margin-bottom:14px}}
.front .ask .askc{{margin-bottom:16px;gap:6px}} .front .ask .askc a{{font-size:16px;padding:4px 11px}}
.front .ask .askbtn{{font-size:18px;padding:9px 18px}}
.front .ask .aski{{min-height:0}}
@media (max-width:720px){{.front .ask{{grid-template-columns:1fr}} .front .ask .aski{{aspect-ratio:16/7}}}}
.nudge{{--navy:#222e4c;--blush:#f2cfc6;position:fixed;z-index:9;left:50%;bottom:calc(max(14px,env(safe-area-inset-bottom,0px)) + var(--dh,0px));transform:translate(-50%,24px);opacity:0;transition:transform .3s,opacity .3s,bottom .3s;
  display:flex;align-items:center;gap:12px;width:max-content;max-width:calc(100vw - 32px);background:var(--navy);color:var(--blush);border-radius:999px;padding:7px 8px 7px 7px;box-shadow:0 10px 26px rgba(0,0,0,.25)}}
.nudge.on{{transform:translate(-50%,0);opacity:1}}
.nudge .ndot{{width:48px;height:48px;border-radius:50%;overflow:hidden;flex:none}} .nudge .ndot img{{width:100%;height:100%;object-fit:cover;display:block}}
.nudge .ntx{{font-family:"Barlow Condensed","Arial Narrow",var(--ui),sans-serif;font-size:18px;line-height:1.15;min-width:0}} .nudge .ntx b{{display:block;font-size:20px}}
.nudge .ntx{{width:min(36ch,46vw);min-height:3.4em;display:flex;flex-direction:column;justify-content:center}} .nudge .ntx b{{font-size:17px;line-height:1.15}} .nudge .nl{{display:block;font:13px/1.35 var(--ui);opacity:.8;margin-top:2px}} .nudge .n3{{display:flex;gap:6px;flex:none}} .nudge .n3 a{{font-family:"Barlow Condensed","Arial Narrow",var(--ui),sans-serif;font-weight:700;font-size:15px;letter-spacing:.04em;text-transform:uppercase;text-decoration:none;color:var(--blush);border:1px solid rgba(242,207,198,.45);padding:8px 13px;border-radius:999px;white-space:nowrap;transition:background .2s,color .2s}} .nudge .n3 a.on,.nudge .n3 a:hover{{background:var(--blush);color:var(--navy);border-color:var(--blush)}}
.nudge .nx{{flex:none;width:32px;height:32px;border-radius:50%;border:0;background:transparent;color:var(--blush);cursor:pointer;display:grid;place-items:center}} .nudge .nx svg{{width:18px;height:18px}} .nudge .nx:hover{{background:rgba(255,255,255,.12)}}
.nudge a:focus-visible,.nudge button:focus-visible,.ask a:focus-visible{{outline:2px solid var(--accent,#1b5e6b);outline-offset:3px}}
@media (max-width:640px){{.nudge{{flex-wrap:wrap;gap:8px 10px;border-radius:22px;padding:10px 8px 10px 10px;width:calc(100vw - 24px)}} .nudge .ndot{{width:36px;height:36px}} .nudge .ntx{{flex:1 1 0;width:auto}} .nudge .ntx b{{font-size:15.5px}} .nudge .nl{{font-size:12px}} .nudge .ntx{{min-height:5.6em}} .nudge .n3{{order:3;flex-basis:100%;justify-content:space-between;gap:5px}} .nudge .n3 a{{flex:1 1 0;min-width:0;text-align:center;font-size:13px;letter-spacing:.02em;padding:8px 3px}}}}
@media (prefers-reduced-motion:reduce){{.nudge,.ask .askbtn{{transition:none}}}} .notices .svb:focus-visible{{outline:3px solid var(--accent);outline-offset:3px}}
.sharedlg .shd{{display:grid;grid-template-columns:1fr auto;align-items:start;gap:2px 12px;margin-bottom:18px}}
.sharedlg .shk{{grid-column:1;margin:0;font-family:var(--ui);font-size:11px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--mute)}}
.sharedlg h2{{grid-column:1;margin:0;font-family:var(--disp);font-size:20px;line-height:1.2;letter-spacing:-.01em}}
.sharedlg .shx{{grid-column:2;grid-row:1/3;width:40px;height:40px;border-radius:50%;border:0;background:transparent;color:var(--mute);cursor:pointer}} .sharedlg .shx svg{{width:20px;height:20px}}
.sharedlg .shx:hover{{background:var(--tabon)}}
.sharedlg .shl{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,1fr);gap:18px 8px}}
.sharedlg .sho{{display:flex;flex-direction:column;align-items:center;gap:8px;width:100%;padding:4px 0;border:0;background:none;color:var(--ink);text-decoration:none;font:inherit;font-family:var(--ui);font-size:13px;cursor:pointer;border-radius:10px}}
.sharedlg .shi{{display:grid;place-items:center;width:56px;height:56px;border-radius:50%;background:color-mix(in oklab,var(--ink) 8%,transparent);transition:background .15s,transform .15s}}
.sharedlg .shi svg{{width:24px;height:24px}}
.sharedlg .sho:hover .shi,.sharedlg .sho:focus-visible .shi{{background:color-mix(in oklab,var(--ink) 14%,transparent);transform:translateY(-1px)}}
.sharedlg .sho:focus-visible{{outline:2px solid var(--ink);outline-offset:2px}}
.sharedlg .shst{{min-height:1.2em;margin:14px 0 0;text-align:center;font-family:var(--ui);font-size:13px;color:var(--mute);word-break:break-all}}
@media (max-width:420px){{.sharedlg .shl{{grid-template-columns:repeat(3,1fr)}}}}
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
/* Illuminated initial: the quote bands and the front epigraph */
:root{{--gl:#e6c983;--gilt-c:#a47628;--star-l:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 48 48'%3E%3Cpath fill='%23d9b562' d='M22.0121%2012.0305L23.9836%208.64366L25.9552%2012.0305L27.4999%2014.6878L30.3894%2013.6493L34.0717%2012.3258L33.4077%2016.1878L32.8894%2019.2183L35.7688%2020.2839L39.4375%2021.6414L36.4531%2024.1731L34.1089%2026.1584L35.6333%2028.8292L37.5744%2032.233L33.6618%2032.25L30.5927%2032.2636L30.0473%2035.2907L29.3529%2039.1459L26.3447%2036.6414L23.9836%2034.6731L21.6225%2036.6414L18.6144%2039.1459L17.92%2035.2907L17.3746%2032.2636L14.3055%2032.25L10.3929%2032.233L12.334%2028.8292L13.8583%2026.1584L11.5142%2024.1731L8.52977%2021.6414L12.2018%2020.2839L15.0812%2019.2183L14.5629%2016.1878L13.899%2012.3258L17.5812%2013.6493L20.4708%2014.6878L22.0155%2012.0305H22.0121ZM18.523%209.3733L8.32652%205.70475L10.1626%2016.4016L0%2020.1584L8.26894%2027.1697L2.89294%2036.5905L13.7262%2036.638L15.6537%2047.3179L23.9836%2040.3778L32.3136%2047.3179L34.241%2036.638L45.0743%2036.5905L39.6983%2027.1697L47.9673%2020.1584L37.8047%2016.4016L39.6408%205.70475L29.4443%209.3733L23.9803%200L18.523%209.3767V9.3733Z'/%3E%3C/svg%3E");--star-d:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 48 48'%3E%3Cpath fill='%23a47628' d='M22.0121%2012.0305L23.9836%208.64366L25.9552%2012.0305L27.4999%2014.6878L30.3894%2013.6493L34.0717%2012.3258L33.4077%2016.1878L32.8894%2019.2183L35.7688%2020.2839L39.4375%2021.6414L36.4531%2024.1731L34.1089%2026.1584L35.6333%2028.8292L37.5744%2032.233L33.6618%2032.25L30.5927%2032.2636L30.0473%2035.2907L29.3529%2039.1459L26.3447%2036.6414L23.9836%2034.6731L21.6225%2036.6414L18.6144%2039.1459L17.92%2035.2907L17.3746%2032.2636L14.3055%2032.25L10.3929%2032.233L12.334%2028.8292L13.8583%2026.1584L11.5142%2024.1731L8.52977%2021.6414L12.2018%2020.2839L15.0812%2019.2183L14.5629%2016.1878L13.899%2012.3258L17.5812%2013.6493L20.4708%2014.6878L22.0155%2012.0305H22.0121ZM18.523%209.3733L8.32652%205.70475L10.1626%2016.4016L0%2020.1584L8.26894%2027.1697L2.89294%2036.5905L13.7262%2036.638L15.6537%2047.3179L23.9836%2040.3778L32.3136%2047.3179L34.241%2036.638L45.0743%2036.5905L39.6983%2027.1697L47.9673%2020.1584L37.8047%2016.4016L39.6408%205.70475L29.4443%209.3733L23.9803%200L18.523%209.3767V9.3733Z'/%3E%3C/svg%3E")}}
.voice p::before{{content:none}} .voice p::first-letter{{float:left;font-size:2.7em;line-height:.8;margin:.06em .1em 0 0;color:var(--gl);font-weight:600}}
.uhj p::first-letter{{color:var(--gilt-c);font-size:1.45em;font-style:normal;font-weight:600}}
.uhj cite{{display:flex;align-items:center;gap:10px;color:var(--gilt-c)}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--gilt-c:#d4b062;--star-d:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 48 48'%3E%3Cpath fill='%23d4b062' d='M22.0121%2012.0305L23.9836%208.64366L25.9552%2012.0305L27.4999%2014.6878L30.3894%2013.6493L34.0717%2012.3258L33.4077%2016.1878L32.8894%2019.2183L35.7688%2020.2839L39.4375%2021.6414L36.4531%2024.1731L34.1089%2026.1584L35.6333%2028.8292L37.5744%2032.233L33.6618%2032.25L30.5927%2032.2636L30.0473%2035.2907L29.3529%2039.1459L26.3447%2036.6414L23.9836%2034.6731L21.6225%2036.6414L18.6144%2039.1459L17.92%2035.2907L17.3746%2032.2636L14.3055%2032.25L10.3929%2032.233L12.334%2028.8292L13.8583%2026.1584L11.5142%2024.1731L8.52977%2021.6414L12.2018%2020.2839L15.0812%2019.2183L14.5629%2016.1878L13.899%2012.3258L17.5812%2013.6493L20.4708%2014.6878L22.0155%2012.0305H22.0121ZM18.523%209.3733L8.32652%205.70475L10.1626%2016.4016L0%2020.1584L8.26894%2027.1697L2.89294%2036.5905L13.7262%2036.638L15.6537%2047.3179L23.9836%2040.3778L32.3136%2047.3179L34.241%2036.638L45.0743%2036.5905L39.6983%2027.1697L47.9673%2020.1584L37.8047%2016.4016L39.6408%205.70475L29.4443%209.3733L23.9803%200L18.523%209.3767V9.3733Z'/%3E%3C/svg%3E")}}}} :root[data-theme="dark"]{{--gilt-c:#d4b062;--star-d:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 48 48'%3E%3Cpath fill='%23d4b062' d='M22.0121%2012.0305L23.9836%208.64366L25.9552%2012.0305L27.4999%2014.6878L30.3894%2013.6493L34.0717%2012.3258L33.4077%2016.1878L32.8894%2019.2183L35.7688%2020.2839L39.4375%2021.6414L36.4531%2024.1731L34.1089%2026.1584L35.6333%2028.8292L37.5744%2032.233L33.6618%2032.25L30.5927%2032.2636L30.0473%2035.2907L29.3529%2039.1459L26.3447%2036.6414L23.9836%2034.6731L21.6225%2036.6414L18.6144%2039.1459L17.92%2035.2907L17.3746%2032.2636L14.3055%2032.25L10.3929%2032.233L12.334%2028.8292L13.8583%2026.1584L11.5142%2024.1731L8.52977%2021.6414L12.2018%2020.2839L15.0812%2019.2183L14.5629%2016.1878L13.899%2012.3258L17.5812%2013.6493L20.4708%2014.6878L22.0155%2012.0305H22.0121ZM18.523%209.3733L8.32652%205.70475L10.1626%2016.4016L0%2020.1584L8.26894%2027.1697L2.89294%2036.5905L13.7262%2036.638L15.6537%2047.3179L23.9836%2040.3778L32.3136%2047.3179L34.241%2036.638L45.0743%2036.5905L39.6983%2027.1697L47.9673%2020.1584L37.8047%2016.4016L39.6408%205.70475L29.4443%209.3733L23.9803%200L18.523%209.3767V9.3733Z'/%3E%3C/svg%3E")}}
{FOOTER_CSS}
.colo{{margin-top:clamp(48px,8vw,112px)}}
a:focus-visible{{outline:2px solid var(--accent);outline-offset:3px}}
@media (max-width:980px){{
  .story{{grid-template-columns:minmax(0,1fr)}}
  .shead,.margin,.prose{{grid-column:1}}
  .margin{{grid-row:auto;position:static;display:flex;gap:18px;flex-wrap:wrap;margin-bottom:28px}}
  .dept .margin,.letter .margin,.dept .prose,.letter .prose{{grid-row:auto}} .dept .prose.shelf,.dept .prose.calendar,.dept .prose:has(.notices){{grid-column:1}}
  .margin .listen{{flex-basis:100%}}
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
{LBX_CSS}
{(NB_CSS + FI2_CSS if member else L_CSS + MAST_CSS) + CAL_CSS + END_ASKS_CSS}
</style>
<div class="head{" member" if member else ""}"><div class="in"><a class="brand" href="#top"><span class="bn"><svg class="star" viewBox="0 0 48 48" aria-hidden="true"><defs><linearGradient id="star-g" x1="26" y1="1" x2="26" y2="48.4" gradientUnits="userSpaceOnUse"><stop stop-color="#73E4C4"/><stop offset=".19" stop-color="#54ADA5"/><stop offset=".47" stop-color="#357686"/><stop offset=".79" stop-color="#265B76"/><stop offset="1" stop-color="#255875"/></linearGradient></defs><path d="M22.0121 12.0305L23.9836 8.64366L25.9552 12.0305L27.4999 14.6878L30.3894 13.6493L34.0717 12.3258L33.4077 16.1878L32.8894 19.2183L35.7688 20.2839L39.4375 21.6414L36.4531 24.1731L34.1089 26.1584L35.6333 28.8292L37.5744 32.233L33.6618 32.25L30.5927 32.2636L30.0473 35.2907L29.3529 39.1459L26.3447 36.6414L23.9836 34.6731L21.6225 36.6414L18.6144 39.1459L17.92 35.2907L17.3746 32.2636L14.3055 32.25L10.3929 32.233L12.334 28.8292L13.8583 26.1584L11.5142 24.1731L8.52977 21.6414L12.2018 20.2839L15.0812 19.2183L14.5629 16.1878L13.899 12.3258L17.5812 13.6493L20.4708 14.6878L22.0155 12.0305H22.0121ZM18.523 9.3733L8.32652 5.70475L10.1626 16.4016L0 20.1584L8.26894 27.1697L2.89294 36.5905L13.7262 36.638L15.6537 47.3179L23.9836 40.3778L32.3136 47.3179L34.241 36.638L45.0743 36.5905L39.6983 27.1697L47.9673 20.1584L37.8047 16.4016L39.6408 5.70475L29.4443 9.3733L23.9803 0L18.523 9.3767V9.3733Z" fill="url(#star-g)"/></svg><b><em class="sc">The</em> American Bahá'í</b></span><small>{SUB}</small></a><nav aria-label="Features">{head}</nav><span class="ind" aria-hidden="true"></span>{CAL_HTML if member else CAL_HTML.replace(" · work is not to be suspended", "").replace(" · work is to be suspended", "")}<button class="rh" type="button" aria-expanded="false" aria-controls="rhs"><small>The American Bahá'í</small><b><i></i><span>{esc(ISSUE["theme"])}</span></b></button><button class="rht" type="button" aria-label="Contents" aria-expanded="false" aria-controls="rhs"><svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 6l5 5 5-5" fill="none" stroke="currentColor" stroke-width="1.8"/></svg></button></div><i class="rhp" aria-hidden="true"></i>{sheet}</div>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><g id="usmap"><path d="{USMAP["nation"]}" class="cland" vector-effect="non-scaling-stroke"/><path d="{USMAP["states"]}" class="cstate" vector-effect="non-scaling-stroke"/></g></defs></svg>
<div class="popup" role="dialog" aria-modal="false" aria-live="polite" hidden><button type="button" aria-label="Close">×</button><b></b><p></p></div>
<div class="terraces" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
<header class="cover wrap" id="top">
  <div class="mast">
    <p class="the">The</p>
    <h1><svg class="stroke" viewBox="0 0 720 90" preserveAspectRatio="none" aria-hidden="true"><path d="M20 55 C 160 20, 300 80, 440 45 S 640 30, 700 50"/><path d="M40 70 C 200 40, 380 90, 560 55 S 660 50, 690 62"/></svg>American Bahá’í</h1>
    <p class="sub">{SUB}</p>
    <div class="line"><span>{esc(ISSUE["date"])}</span><span>{"Full edition" if member else "Curated edition"}</span>{'<span><a href="../">Curated edition</a></span>' if member else ''}</div>
  </div>
  <figure class="painting"><div class="mat"><img src="img/cover-paint.jpg" alt="Oil painting by Juliet Bogan: two figures in a flowering meadow look toward terraced green farmland and ochre mountains under a pale sky"></div><figcaption><span>Cover painting by {esc(ISSUE["cover_artist"])}</span><span>Oil on canvas</span></figcaption></figure>
</header>
<main>
<div class="wrap">
<section class="front" id="front">
  <div>
    <h2>Features</h2>
    <ol class="index nb">{index}</ol>
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
</div>
</main>
{_ns["submit_html"]("", "#").replace('<section class="sbm sbc"', '<section class="sbm sbc edask"', 1).replace('src="img/', 'src="img/')}{SUB_SECTION.replace('class="sbx"', 'class="sbx edask"', 1)}
{footer_html("https://aoaoaoa.github.io/usbns/magazine/landing/")}
{DOCK}
{LBX_HTML}
{SHARE_HTML}
{SVY_HTML}
{SHARE_JS}
{SVY_JS}
{NUDGE_HTML}
{ASK_JS}
{("" if member else L_JS) + CHIP_JS}
{LBX_JS}
<script>
(function(){{ /* opening lettering: play once in view; New Yorkers drifts with scroll */
  var rm=matchMedia('(prefers-reduced-motion: reduce)').matches; document.documentElement.classList.add('ovready');
  (function(){{var V=[].slice.call(document.querySelectorAll('.verb:not(.vc)'));if(!V.length||matchMedia('(prefers-reduced-motion:reduce)').matches)return;
    V.forEach(function(v){{v.dataset.f='0';v.querySelector('.vw').addEventListener('click',function(){{v.dataset.hold=1;v.dataset.f=String((+v.dataset.f+1)%3)}})}});
    function tick(){{V.forEach(function(v){{if(v.dataset.hold)return;var r=v.getBoundingClientRect(),h=innerHeight;var p=(h*0.8-r.top)/(h*0.4);v.dataset.f=String(Math.max(0,Math.min(2,Math.floor(p*3))))}})}}
    addEventListener('scroll',tick,{{passive:true}});addEventListener('resize',tick);tick();}})();
  [].forEach.call(document.querySelectorAll('.chart ol.tlx'),function(ol){{var svg=ol.parentNode.querySelector('svg.tl2');if(!svg)return;
    function lit(li,on){{li.classList.toggle('lit',on);[].forEach.call(svg.querySelectorAll('[data-pt^="'+li.dataset.y+':"]'),function(e){{e.classList.toggle('lit',on)}})}}
    [].forEach.call(ol.querySelectorAll('li[data-y]'),function(li){{['mouseenter','focus'].forEach(function(t){{li.addEventListener(t,function(){{lit(li,true)}})}});['mouseleave','blur'].forEach(function(t){{li.addEventListener(t,function(){{lit(li,false)}})}})}});}});
  /* play each piece when it reaches the reading band (above the lowest quarter of the screen);
     a piece scrolled past before it had time to finish resets, and plays again when the reader returns */
  var W=[].slice.call(document.querySelectorAll('.ovw,.fnote,.csplash,.mnote'));
  function mark(n,on){{if(!n.classList.contains('mnote'))return;var m=document.getElementById(n.getAttribute('data-for'));if(m)m.classList.toggle('go',on)}}
  if('IntersectionObserver' in window&&!rm){{var t0=new WeakMap(),FULL=2600;
    var io=new IntersectionObserver(function(es){{es.forEach(function(e){{var el=e.target;
      if(e.isIntersecting){{if(!el.classList.contains('go')){{el.classList.add('go');mark(el,true);t0.set(el,performance.now())}}}}
      else if(el.classList.contains('go')&&!el.dataset.done){{if(performance.now()-t0.get(el)<FULL){{el.classList.remove('go');mark(el,false)}}else el.dataset.done=1}}
      if(el.classList.contains('go')&&performance.now()-(t0.get(el)||0)>=FULL)el.dataset.done=1;}})}},{{rootMargin:'0px 0px -25% 0px',threshold:.2}});
    W.forEach(function(w){{io.observe(w)}});
    setInterval(function(){{W.forEach(function(w){{if(w.classList.contains('go')&&!w.dataset.done&&performance.now()-t0.get(w)>=FULL){{w.dataset.done=1;io.unobserve(w)}}}})}},500);}}
  else W.forEach(function(w){{w.classList.add('go');mark(w,true)}});
  /* looping diagrams start from their first step when they come into view */
  if('IntersectionObserver' in window&&!rm){{var rio=new IntersectionObserver(function(es){{es.forEach(function(e){{if(!e.isIntersecting)return;var v=e.target;if(v.setCurrentTime)v.setCurrentTime(0);rio.unobserve(v)}})}},{{rootMargin:'0px 0px -25% 0px',threshold:.3}});[].forEach.call(document.querySelectorAll('.rsvg'),function(v){{rio.observe(v)}});}}
  var ny=document.querySelector('.ovw.nyo'); if(ny&&!rm){{var tick=function(){{var r=ny.getBoundingClientRect(),p=(innerHeight-r.top)/(innerHeight+r.height);p=Math.max(0,Math.min(1,p))-.5;ny.style.setProperty('--dr',(p*24).toFixed(1))}};addEventListener('scroll',tick,{{passive:true}});tick();}}
}})();
(function(){{[].forEach.call(document.querySelectorAll('figure.ringf'),function(f){{var v=f.querySelector('.rsvg'),li=[].slice.call(f.querySelectorAll('.rcols li'));if(!v||!v.getCurrentTime)return;var last=-1;setInterval(function(){{var k=Math.floor((v.getCurrentTime()%16)/4);if(k!==last){{last=k;li.forEach(function(x,i){{x.classList.toggle('on',i===k)}});}}}},150);}});}})();
(function(){{var R=[].slice.call(document.querySelectorAll('.rsvg'));var rm=matchMedia('(prefers-reduced-motion: reduce)').matches;R.forEach(function(v){{if(rm&&v.pauseAnimations){{v.pauseAnimations();v.setCurrentTime(3.9);}}var f=v.closest('figure');f.addEventListener('mouseenter',function(){{v.pauseAnimations&&v.pauseAnimations()}});f.addEventListener('mouseleave',function(){{if(!rm&&v.unpauseAnimations)v.unpauseAnimations()}});}});}})();
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
  var cur=null, brand=document.querySelector('.head .brand');
  var hd=document.querySelector('.head'), rhs=[].slice.call(document.querySelectorAll('.head .rhs a[data-name]')), rhn=document.querySelector('.head .rh span'); var RH0=rhn.textContent;
  function rhSet(id){{var l=rhs.filter(function(x){{return x.getAttribute('href')==='#'+id}})[0]||rhs.filter(function(x){{return x.getAttribute('href')==='#'+(alias[id]||id)}})[0];
    rhs.forEach(function(x){{x.classList.toggle('on',x===l);if(x===l)x.setAttribute('aria-current','location');else x.removeAttribute('aria-current')}});hd.classList.toggle('inside',!!l);rhn.textContent=l?l.dataset.name:RH0;if(l)hd.style.setProperty('--rt',l.style.getPropertyValue('--tint'));}}
  function rhOpen(o){{hd.classList.toggle('open',o);var on=o&&document.querySelector('.head .rhs a.on');if(on)on.parentNode.scrollTop=on.offsetTop-on.parentNode.clientHeight/3;[].forEach.call(document.querySelectorAll('.head .rh,.head .rht'),function(b){{b.setAttribute('aria-expanded',o)}});}}
  [].forEach.call(document.querySelectorAll('.head .rh,.head .rht'),function(b){{b.addEventListener('click',function(){{rhOpen(!hd.classList.contains('open'))}})}});
  [].forEach.call(document.querySelectorAll('.head .rhs a'),function(x){{x.addEventListener('click',function(){{rhOpen(false)}})}});
  // late-loading content above a target can push it down mid-jump; settle on it, for in-page links and for links arriving from outside
  var sIv=null;function settle(id){{var t=id&&document.getElementById(id);if(!t||id==='survey')return;clearInterval(sIv);
    var n=0,stop=function(){{clearInterval(sIv);removeEventListener('wheel',stop);removeEventListener('touchstart',stop);removeEventListener('keydown',stop)}};
    addEventListener('wheel',stop,{{passive:true}});addEventListener('touchstart',stop,{{passive:true}});addEventListener('keydown',stop);
    sIv=setInterval(function(){{var d=t.getBoundingClientRect().top-hd.offsetHeight;if(++n>24||Math.abs(d)<3&&n>4){{stop();return}}if(n>1&&Math.abs(d)>=3)scrollTo({{top:scrollY+d,behavior:'auto'}});}},250);}}
  // in-page links glide: eased, duration grows gently with distance, target re-measured each frame so late layout never causes a jump
  var gRaf=0;function glide(t){{var H=document.documentElement,rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
    var off=function(){{var m=parseFloat(getComputedStyle(t).scrollMarginTop)||0;return Math.max(0,t.getBoundingClientRect().top+scrollY-Math.max(hd.offsetHeight+8,m))}};
    cancelAnimationFrame(gRaf);if(rm){{scrollTo(0,off());return}}
    var y0=scrollY,d0=Math.abs(off()-y0),dur=Math.min(1100,Math.max(450,350+Math.sqrt(d0)*4)),st=performance.now(),sb=H.style.scrollBehavior;H.style.scrollBehavior='auto';
    var stop=function(){{cancelAnimationFrame(gRaf);H.style.scrollBehavior=sb;removeEventListener('wheel',stop);removeEventListener('touchstart',stop);removeEventListener('keydown',stop)}};
    addEventListener('wheel',stop,{{passive:true}});addEventListener('touchstart',stop,{{passive:true}});addEventListener('keydown',stop);
    (function step(now){{var q=Math.min(1,(now-st)/dur),e=q<.5?4*q*q*q:1-Math.pow(-2*q+2,3)/2;scrollTo(0,y0+(off()-y0)*e);if(q<1)gRaf=requestAnimationFrame(step);else stop()}})(st)}}
  document.addEventListener('click',function(e){{if(e.defaultPrevented||e.button||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;var x=e.target.closest('a[href^="#"]');if(!x)return;var id=x.getAttribute('href').slice(1);if(!id)return;
    var t=document.getElementById(decodeURIComponent(id));if(!t||!t.getClientRects().length||id==='survey'){{if(t)settle(id);return}}
    e.preventDefault();if(location.hash!=='#'+id)history.pushState(null,'','#'+id);glide(t);if(!t.hasAttribute('tabindex'))t.setAttribute('tabindex','-1');t.focus({{preventScroll:true}})}});
  if(location.hash.length>1)settle(decodeURIComponent(location.hash.slice(1)));
  document.addEventListener('keydown',function(e){{if(e.key==='Escape')rhOpen(false)}});
  document.addEventListener('click',function(e){{if(!e.target.closest('.head'))rhOpen(false)}});
  function place(a){{if(!a||!ind)return;var r=a.getBoundingClientRect(),b=inn.getBoundingClientRect();ind.style.left=(r.left-b.left+inn.scrollLeft)+'px';ind.style.width=r.width+'px';}}
  var alias={{abiding:'huquq',fund:'huquq',rhythm:'huquq',books:'huquq',notices:'huquq'}};
  function tabFor(id){{return links.filter(function(l){{return l.getAttribute('href')==='#'+(alias[id]||id)}})[0];}}
  function progress(){{if(!cur)return;var a=tabFor(cur.id);if(!a)return;
    var r=cur.getBoundingClientRect();var top=r.top+scrollY, h=r.height;var p=(scrollY+innerHeight*0.4-top)/h;p=Math.max(0,Math.min(1,p));a.style.setProperty('--p',(p*100).toFixed(1)+'%');hd.style.setProperty('--rp',(p*100).toFixed(1)+'%');if(brand)brand.style.setProperty('--rot',(p*40).toFixed(1)+'deg');}}
  if('IntersectionObserver' in window){{
    var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(!e.isIntersecting)return;cur=e.target;
      var t=tabFor(e.target.id);links.forEach(function(a){{var on=a===t;a.classList.toggle('on',on);if(on)place(a);}});rhSet(e.target.id);if(brand){{var c=t&&getComputedStyle(t).getPropertyValue('--tint').trim();brand.classList.toggle('tinted',!!c);if(c)brand.style.setProperty('--sc',c);}}progress();}});}},{{rootMargin:'-30% 0px -60% 0px'}});
    secs.forEach(function(x){{io.observe(x)}});
  }}
  function home(){{if(brand&&secs[0]&&secs[0].getBoundingClientRect().top>innerHeight*.4){{brand.classList.remove('tinted');brand.style.setProperty('--rot','0deg');hd.classList.remove('inside');hd.style.setProperty('--rp','0%');rhn.textContent=RH0;rhs.forEach(function(x){{x.classList.remove('on')}});}}}}
  addEventListener('scroll',function(){{progress();home();}},{{passive:true}}); addEventListener('resize',function(){{place(document.querySelector('.head nav a.on'))}});
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
  document.addEventListener('mouseover',function(e){{if(!hov||pinned)return;var el=e.target.closest('[data-pb]');if(el&&el.hasAttribute('data-click'))el=null;if(el&&el!==cur)show(el);}});
  document.addEventListener('mouseout',function(e){{if(!hov||pinned)return;var el=e.target.closest('[data-pb]');if(el&&!el.contains(e.relatedTarget)&&!box.contains(e.relatedTarget))hide();}});
  document.addEventListener('click',function(e){{var el=e.target.closest('[data-pb]');if(el){{e.preventDefault();(cur===el&&pinned)?hide():show(el,true);return;}}
    if(e.target.closest('.popup button')||!box.contains(e.target))hide();}});
  document.addEventListener('keydown',function(e){{if(e.key==='Escape'&&cur){{var c=cur;hide();c.focus();return;}}
    var el=e.target.closest&&e.target.closest('[data-pb]');if(el&&(e.key==='Enter'||e.key===' ')){{e.preventDefault();show(el,true);}}}});
  document.addEventListener('focusin',function(e){{var el=e.target.closest&&e.target.closest('[data-pb]');if(el&&!pinned&&!(hov&&el.hasAttribute('data-click')&&e.target.matches(':hover')))show(el);}});
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
    <div class="cap"><span class="n">Plate {n}</span><span>{esc(a["art_credit"] or "Set in type")}</span></div>
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Literata:ital,opsz,wght@0,7..72,300..700;1,7..72,300..700&family=Source+Serif+4:ital,opsz,wght@0,8..60,300..600;1,8..60,300..600&family=DM+Mono:wght@400;500&display=swap">
<style>
/* Layout: a dark gallery. Each feature is hung as a plate on a charcoal wall, its illustration at full width with a caption strip in mono; the headline follows in Literata italic, and the text runs in one lit column. One deliberate theme. */
:root{{
  --wall:#141312; --card:#1c1a18; --fg:#f1ebe0; --dim:#a69d8e; --rule:#2c2926; --gold:#d6b25e; --rose:#e8a3a3;
  --disp:"Literata",Georgia,serif; --text:"Source Serif 4",Georgia,serif; --mono:"DM Mono","SF Mono",Menlo,monospace;
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
.chart .cb,.chart .cdot,.chart .cseg.on,.chart .carea{{fill:var(--accent)}} .chart .cline{{fill:none;stroke:currentColor;opacity:.6;stroke-width:1.6}} .chart .carr{{fill:currentColor}} .chart .cpanel{{fill:none;stroke:var(--rule)}} .chart .cstrand{{fill:none;stroke:var(--accent);stroke-width:5}} .chart .cjoin{{stroke:var(--accent);stroke-width:16}} .chart .ghostline,.chart .ghost{{fill:transparent;stroke:transparent}} .chart .csq{{fill:none;stroke:var(--accent);stroke-width:2.5}} .chart .cdotm{{fill:currentColor;opacity:.5}} .chart .ctrack,.chart .cseg{{fill:var(--rule)}} .chart .cax,.chart .cstem{{stroke:var(--rule)}} .chart .ctick{{stroke:currentColor}}
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
    <p class="meta">{by}</p>
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
.chart .cb,.chart .cdot,.chart .cseg.on,.chart .carea{{fill:var(--accent)}} .chart .cline{{fill:none;stroke:currentColor;opacity:.6;stroke-width:1.6}} .chart .carr{{fill:currentColor}} .chart .cpanel{{fill:none;stroke:var(--rule)}} .chart .cstrand{{fill:none;stroke:var(--accent);stroke-width:5}} .chart .cjoin{{stroke:var(--accent);stroke-width:16}} .chart .ghostline,.chart .ghost{{fill:transparent;stroke:transparent}} .chart .csq{{fill:none;stroke:var(--accent);stroke-width:2.5}} .chart .cdotm{{fill:currentColor;opacity:.5}} .chart .ctrack,.chart .cseg{{fill:var(--rule)}} .chart .cax,.chart .cstem{{stroke:var(--rule)}} .chart .ctick{{stroke:currentColor}}
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

_DIMS = {}
def _add_dims(page):
    """Give every local raster image its width/height so lazy loading never shifts the page under a reader."""
    def fix(m):
        tag, f = m.group(0), m.group(1)
        if " width=" in tag or f.endswith(".svg"): return tag
        if f not in _DIMS: _DIMS[f] = _dims(f)
        return tag[:-1] + _DIMS[f] + ">" if _DIMS[f] else tag
    return re.sub(r'<img src="img/([^"]+)"[^>]*>', fix, page)
_build_tab = build_tab
AUDIO_DIR = "/home/claude/usbns/magazine/audio"
def _audio(h):
    """Point every reading without its own file at audio/placeholder.mp3 (the A Common Endeavor letter reading, for now)."""
    return re.sub(r'audio/([a-z0-9-]+)\.mp3', lambda m: m.group(0) if os.path.exists(os.path.join(AUDIO_DIR, m.group(1) + ".mp3")) else "audio/placeholder.mp3", h)
def build_tab(*a, **k): return _audio(_add_dims(_build_tab(*a, **k)))

for name, fn in [("tab", build_tab), ("plates", build_plates), ("reader", build_reader)]:
    with open(os.path.join(OUT, f"{name}.html"), "w") as f: f.write(fn())
with open(os.path.join(OUT, "member.html"), "w") as f: f.write(build_tab(member=True))

# ---------------------------------------------------------------- GitHub Pages site
SITE = os.path.join(HERE, "site", "magazine")
def standalone(body):
    """Wrap an artifact page in a full HTML document; image paths become relative to site/img."""
    body = body.replace(SIDES, "").replace('src="img/', 'src="../img/').replace('href="img/', 'href="../img/').replace('url(img/', 'url(../img/')
    i = body.rfind("</style>")
    i = body.index("\n", i) + 1
    body = body[:i] + "</head>\n<body>\n" + body[i:]
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<link rel="icon" type="image/svg+xml" href="FAVICON">\n'
            '<link rel="apple-touch-icon" href="/usbns/magazine/apple-touch-icon.png">\n<meta name="apple-mobile-web-app-title" content="American Bahá’í">\n'
            '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}</style>\n'
            + body + '\n</body>\n</html>\n')
os.makedirs(SITE, exist_ok=True)
with open(os.path.join(SITE, "index.html"), "w") as f: f.write(standalone(build_tab()).replace('src="../img/', 'src="img/').replace('href="../img/', 'href="img/').replace('url(../img/', 'url(img/').replace('href="FAVICON"', 'href="favicon.svg"'))
shutil.copy(os.path.join(HERE, "favicon.svg"), os.path.join(SITE, "favicon.svg"))
shutil.copy(os.path.join(HERE, "apple-touch-icon.png"), os.path.join(SITE, "apple-touch-icon.png"))
os.makedirs(os.path.join(SITE, "members"), exist_ok=True)
with open(os.path.join(SITE, "members", "index.html"), "w") as f: f.write(standalone(build_tab(member=True)).replace('href="FAVICON"', 'href="../favicon.svg"').replace('data-src="audio/', 'data-src="../audio/'))
# the colour-index menu variant: same build, so it follows every change to the main pages
# /test/: the curated edition as it stands, with trial treatments layered on (masthead: story-color stripes in "Bahá’í", gold italic "The", letterpress)
TEST_CSS = ('<style>/* test */.cover .mast .the{font:italic 400 clamp(22px,2.6vw,34px)/1 "Literata",Georgia,serif;letter-spacing:0;margin:0 0 -.12em .06em;color:#b8782e;text-shadow:0 1px 0 rgba(255,255,255,.85),0 -1px 1px rgba(0,0,0,.35)}'
    '.cover h1{color:#25201b;text-shadow:0 1.5px 0 rgba(255,255,255,.85),0 -1px 1px rgba(0,0,0,.45),0 -2px 5px rgba(0,0,0,.08)}'
    '.cover h1 .fl{position:relative;background:repeating-linear-gradient(115deg,#e8532a 0 34px,#f05a7e 34px 68px,#b07a4a 68px 102px,#c9462c 102px 136px,#1b5e6b 136px 170px);-webkit-background-clip:text;background-clip:text;color:transparent;text-shadow:none;filter:drop-shadow(0 1.5px 0 rgba(255,255,255,.9)) drop-shadow(0 -1px .6px rgba(0,0,0,.55))}'
    '.cover .mast .sub{text-shadow:0 1px 0 rgba(255,255,255,.8)}'
    '@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .cover h1{color:var(--ink);text-shadow:0 1px 0 rgba(0,0,0,.6),0 -1px 1px rgba(255,255,255,.12)}:root:not([data-theme="light"]) .cover h1 .fl{filter:none}}'
    ':root[data-theme="dark"] .cover h1{color:var(--ink);text-shadow:0 1px 0 rgba(0,0,0,.6)}:root[data-theme="dark"] .cover h1 .fl{filter:none}</style>')
def build_test():
    h = standalone(build_tab()).replace('href="FAVICON"', 'href="../favicon.svg"').replace('data-src="audio/', 'data-src="../audio/')
    h = h.replace("Bahá’í</h1>", '<span class="fl">Bahá’í</span></h1>', 1).replace('</head>', TEST_CSS + '<meta name="robots" content="noindex"></head>', 1)
    return h
os.makedirs(os.path.join(SITE, "test"), exist_ok=True)
with open(os.path.join(SITE, "test", "index.html"), "w") as f: f.write(build_test())
if os.path.exists(os.path.join(SITE, "alt", "index.html")): os.remove(os.path.join(SITE, "alt", "index.html"))
os.makedirs(os.path.join(SITE, "members", "alt"), exist_ok=True)
with open(os.path.join(SITE, "members", "alt", "index.html"), "w") as f: f.write(standalone(build_tab(member=True, menu="bands")).replace('data-src="audio/', 'data-src="../../audio/').replace('src="../img/', 'src="../../img/').replace('href="../img/', 'href="../../img/').replace('url(../img/', 'url(../../img/').replace('href="FAVICON"', 'href="../../favicon.svg"'))
for d, fn in [("alt/plates", build_plates), ("alt/reader", build_reader)]:
    os.makedirs(os.path.join(SITE, d), exist_ok=True)
    with open(os.path.join(SITE, d, "index.html"), "w") as f: f.write(standalone(fn()).replace('src="../img/', 'src="../../img/').replace('href="../img/', 'href="../../img/').replace('url(../img/', 'url(../../img/').replace('href="FAVICON"', 'href="../../favicon.svg"'))
os.makedirs(os.path.join(SITE, "img"), exist_ok=True)
# out/img is the source of truth: mirror it into site/img, dropping anything no longer there
shutil.rmtree(os.path.join(SITE, "img")); shutil.copytree(os.path.join(OUT, "img"), os.path.join(SITE, "img"))
open(os.path.join(SITE, ".nojekyll"), "w").close()
print("built out/ and site/")
