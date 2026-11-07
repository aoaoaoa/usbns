# Banked from build.py chart_html: "A life in years" (and the two-column ledger, same data).
# Data: ("chart",{"kind":"lifeyears","w":760,"title":"A life in years","born":1874,"died":1951,"end":2026,
#                 "events":GREGORY_EVENTS,"kinds":GREGORY_KINDS})   # GREGORY_* live in data.py
# Kinds: life, teach, serve, write, legacy (any year not listed is legacy).

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

# CSS (inside the build.py f-string, so braces are doubled)
CSS = """
.chart{{--k-life:var(--ink);--k-teach:var(--accent);--k-serve:#265b76;--k-write:#9a6a12;--k-legacy:#8a8072}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]) .chart{{--k-serve:#7fb4d0;--k-write:#d9a94a}}}} :root[data-theme="dark"] .chart{{--k-serve:#7fb4d0;--k-write:#d9a94a}}
.chart .k-life{{--k:var(--k-life)}} .chart .k-teach{{--k:var(--k-teach)}} .chart .k-serve{{--k:var(--k-serve)}} .chart .k-write{{--k:var(--k-write)}} .chart .k-legacy{{--k:var(--k-legacy)}}
.chart .kkey{{display:flex;flex-wrap:wrap;gap:4px 16px;font-family:var(--ui);font-size:12px;color:var(--mute);margin:0 0 16px}} .chart .kkey i{{display:inline-block;width:9px;height:9px;border-radius:50%;background:var(--k);margin-right:6px}}
.chart .ages{{display:grid;grid-template-columns:repeat(26,1fr);gap:3px;margin-top:18px}}
.chart .ages span{{aspect-ratio:1;border-radius:2px;position:relative}} .chart .ages .lv{{background:color-mix(in oklab,var(--accent) 13%,var(--paper))}} .chart .ages .af{{border:1px solid var(--rule)}}
.chart .ages .ev{{background:var(--k);border:0;cursor:pointer}} .chart .ages .ev:hover,.chart .ages .ev:focus-visible{{outline:2px solid var(--ink);outline-offset:1px}}
.chart .ages em{{position:absolute;left:0;top:-15px;font-style:normal;font-family:var(--ui);font-size:10px;color:var(--mute);white-space:nowrap;pointer-events:none}}
.chart .ages em.r{{left:auto;right:0}} .chart .agecap{{display:flex;justify-content:space-between;font-family:var(--ui);font-size:12px;color:var(--mute);margin:8px 0 0}}
@media (max-width:560px){{.chart .ages{{grid-template-columns:repeat(16,1fr)}} .chart .ages em{{font-size:9px}}}}
.chart .ledger{{list-style:none;margin:0;padding:0;columns:2;column-gap:44px}}
.chart .ledger li{{break-inside:avoid;display:grid;grid-template-columns:3.1em 1fr;gap:0 16px;padding:0 0 16px;position:relative}}
.chart .ledger li::before{{content:"";position:absolute;left:calc(3.1em + 7px);top:0;bottom:0;width:1px;background:var(--rule)}}
.chart .ledger li b{{font-family:var(--disp);font-weight:600;font-size:24px;line-height:1;color:var(--k);text-align:right;font-variant-numeric:lining-nums;padding-top:3px}}
.chart .ledger li div{{padding-left:14px;position:relative}} .chart .ledger li div::before{{content:"";position:absolute;left:-3px;top:8px;width:9px;height:9px;border-radius:50%;background:var(--k);box-shadow:0 0 0 3px var(--paper)}}
.chart .ledger h4{{font-family:var(--ui);font-weight:600;font-size:15px;line-height:1.3;margin:2px 0 4px;color:var(--ink)}} .chart .ledger p{{margin:0;font-family:var(--text);font-size:14px;line-height:1.55;color:var(--ink);opacity:.82}}
.chart .ledger li.gap{{display:block;padding:0 0 16px calc(3.1em + 30px);font-family:var(--ui);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}}
.chart .ledger li.gap::before{{background:repeating-linear-gradient(var(--rule) 0 4px,transparent 4px 9px)}}
@media (max-width:760px){{.chart .ledger{{columns:1}}}}
"""
