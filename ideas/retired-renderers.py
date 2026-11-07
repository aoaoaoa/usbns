# Renderers retired from build.py on 2026-11-07: no current data uses them.
# Each block was a branch of chart_html(c) or concept_html(c); paste back into the matching dispatcher to revive.

    elif c["kind"] in ("lifeyears", "ledger"):
        K = {"life": "Life", "teach": "Teaching journeys", "serve": "Service and institutions", "write": "Writings", "legacy": "Legacy"}
        kind = lambda y: c["kinds"].get(y, "legacy")
        key = '<p class="kkey">' + "".join(f'<span><i class="k-{k}"></i>{v}</span>' for k, v in K.items()) + '</p>'
        if c["kind"] == "lifeyears":
            by = {e[0]: e for e in c["events"]}; born, died = c["born"], c["died"]
            marks = {born: "Born", 1909: "Age 35", died: f"Age {died - born}", 1972: f"{1972 - died} years on", c["end"]: f"{c['end'] - died} years on"}
            cells = []
            for y in range(born, c["end"] + 1):
                e = by.get(y); cl = ("lv" if y <= died else "af") + (f" ev k-{kind(y)}" if e else "")
                m = f'<em{" class=r" if (y - born) % 26 > 20 else ""}>{marks[y]}</em>' if y in marks else ""
                cells.append(f'<span class="{cl}"{pop(f"{y}: {e[1]}", e[2]) if e else ""}>{m}</span>')
            svg = key + f'<div class="ages">{"".join(cells)}</div><p class="agecap"><span>{born}</span><span>{died} · {c["end"]}</span></p>'
        else:
            rows = []; prev = None
            for e in c["events"]:
                if prev and e[0] - prev >= 12: rows.append(f'<li class="gap"><span>{e[0] - prev} years</span></li>')
                rows.append(f'<li class="k-{kind(e[0])}"><b>{e[0]}</b><div><h4>{esc(e[1])}</h4><p>{esc(e[2])}</p></div></li>'); prev = e[0]
            svg = key + f'<ol class="ledger">{"".join(rows)}</ol>'

    elif c["kind"] == "ribbon":
        months = c["months"]; n = len(months); W = 620; GAP = 18; cw = (W - GAP) / n; parts = []
        for i, (name, mean) in enumerate(months):
            hue = (135 + 330 * i / (n - 1)) % 360; x = i * cw + (GAP if i == n - 1 else 0)
            base = c.get("starts", [None]*n)[i]; st = c.get("stories", {}).get(name, "")
            parts.append(f'<g class="hit"{pop(f"{name}, {mean}", month_body(c, i, name, base, st))}><rect x="{x+1:.1f}" y="26" width="{cw-2:.1f}" height="120" rx="3" style="fill:oklch(.62 .11 {hue:.0f})"/>'
                         f'<text x="{x+cw/2:.1f}" y="44" text-anchor="middle" class="cvin">{i+1}</text>'
                         f'<text transform="translate({x+cw/2+4:.1f},136) rotate(-90)" class="crib">{esc(mean)}</text></g>')
        xa = (n - 1) * cw + GAP / 2
        ah = "The intercalary days, four or five, before the last month: days of hospitality, charity and gift-giving."
        parts.append(f'<g class="hit"{pop("Ayyám-i-Há", ah)}><rect x="{xa-9:.1f}" y="26" width="18" height="120" class="ghost"/>' + "".join(f'<circle cx="{xa:.1f}" cy="{58 + k*18}" r="4.5" class="cayy"/>' for k in range(4)) + '</g>')
        parts.append(f'<text x="0" y="172" class="cn2">Naw-Rúz · March 21</text><text x="{xa:.1f}" y="172" text-anchor="middle" class="cn2">Ayyám-i-Há</text><text x="{W}" y="190" text-anchor="end" class="cn2">‘Alá’, the month of fasting</text>')
        svg = f'<svg viewBox="0 0 {W} 196" width="100%" role="img" aria-label="{esc(c["title"])}">{"".join(parts)}</svg>'

    elif c["kind"] == "pictogram":
        rows = c["rows"]; W = 600; parts = []; rowh = 40
        for r, row in enumerate(rows):
            lab, count, story = row[0], row[1], row[2] if len(row) > 2 else ""
            y = r * rowh
            dots = "".join(f'<circle cx="{170 + k*26}" cy="{y+18}" r="9" class="cdot"/>' for k in range(count))
            parts.append(f'<g class="hit"{pop(f"{lab}: {count}", story)}><rect x="0" y="{y}" width="{W}" height="{rowh}" class="ghost"/><text x="156" y="{y+22}" text-anchor="end" class="cl">{esc(lab)}</text>{dots}<text x="{170 + count*26 + 4}" y="{y+23}" class="cv">{count}</text></g>')
        svg = f'<svg viewBox="0 0 {W} {len(rows)*rowh}" width="100%" role="img" aria-label="{esc(c["title"])}">{"".join(parts)}</svg>'

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

    elif kind == "strands":
        st = c["strands"]; n = len(st); xj, yj = 360, 120; H = 240
        for i, (lab, story) in enumerate(st):
            y0 = 40 + i * 80
            P.append(f'<g class="hit"{pop(lab, story)}><path d="M200,{y0} C290,{y0} 300,{yj} {xj},{yj}" class="cstrand"/><path d="M200,{y0} C290,{y0} 300,{yj} {xj},{yj}" class="ghostline"/><circle cx="200" cy="{y0}" r="7" class="cdot"/>{lines(lab, 186, y0 + 5, "cv", "end")}</g>')
        jl, js = c["joined"]
        P.append(f'<g class="hit"{pop(jl.replace("|"," "), js)}><line x1="{xj}" y1="{yj}" x2="585" y2="{yj}" class="cjoin"/>{lines(jl, 472, yj + 34, "cv")}</g>')
