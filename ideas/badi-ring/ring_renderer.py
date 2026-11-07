# Badí‘ calendar as a ring of 19 months, from build.py chart_html (banked Nov 2026).
# Still live in build.py as kind="ring" for the full edition's "The year 183 B.E.".

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
            import datetime as _dt
            starts = c.get("starts", [None]*n)
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
            body = "\n".join(lines)
            hue = (135 + 330 * i / (n - 1)) % 360
            parts.append(f'<path d="{d}" class="cseg hit" style="fill:oklch(.62 .11 {hue:.0f})"{pop(f"{name}, {mean}", body)}/>')
            am = (a0 + a1) / 2; tx, ty = cx + 174*math.cos(am), cy + 174*math.sin(am)
            anchor = "start" if math.cos(am) > .15 else ("end" if math.cos(am) < -.15 else "middle")
            parts.append(f'<text x="{tx:.1f}" y="{ty+4:.1f}" text-anchor="{anchor}" class="cl">{esc(mean)}</text>')
            nx, ny = cx + (r0+r1)/2*math.cos(am), cy + (r0+r1)/2*math.sin(am)
            parts.append(f'<text x="{nx:.1f}" y="{ny+4:.1f}" text-anchor="middle" class="cvin">{i+1}</text>')
        parts.append(f'<text x="{cx}" y="{cy-6}" text-anchor="middle" class="cbig">19</text><text x="{cx}" y="{cy+18}" text-anchor="middle" class="cn2">months of 19 days</text><text x="{cx}" y="{cy+32}" text-anchor="middle" class="cn2">plus Ayyám-i-Há</text>')
        svg = f'<svg viewBox="-60 0 540 420" width="100%" role="img" aria-label="{esc(c["title"])}">{"".join(parts)}</svg>'
