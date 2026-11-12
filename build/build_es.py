"""Spanish curated edition at /magazine/es/: the English build, translated segment by segment from es_map.json."""
import re, json, html, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "site", "magazine")
M = json.load(open(os.path.join(HERE, "es_map.json")))
norm = lambda s: re.sub(r"\s+", " ", html.unescape(s).replace("'", "’")).strip()
MAP = {norm(k): v for k, v in M.items()}
# fragments that read differently in different places, by order of appearance
OCC = {norm("Bahá’í Studies"): ["Estudios Bahá’ís", "Bahá’í Studies"]}
KEEP_ATTR = ("alt", "aria-label", "title", "placeholder", "data-title", "data-name", "data-pt", "data-pb")
JS = [("'en-US'", "'es-US'"), ("'The month of '", "'Mes de '"), ("'Today'", "'Hoy'"), ("'Tomorrow'", "'Mañana'"),
      ("'In '+dd+' days'", "'En '+dd+' días'"), ('">Next</span>', '">Próximamente</span>'), ("<h4>With the next issue</h4>", "<h4>Con el próximo número</h4>"),
      ("Each issue carries the Holy Days and Feasts ahead.", "Cada número incluye los próximos Días Sagrados y Fiestas."),
      ('"Anniversary of the Birth of the Báb"', '"Natalicio del Báb"'), ('"Anniversary of the Birth of Bahá\'u\'lláh"', '"Natalicio de Bahá’u’lláh"'),
      ('"Day of the Covenant"', '"Día de la Alianza"'), ('"Ascension of ‘Abdu\'l-Bahá"', '"Ascensión de ‘Abdu’l-Bahá"'),
      ('"Feast of ', '"Fiesta de '), ("'Audio not yet added'", "'Audio aún no disponible'"), ("'Link copied'", "'Enlace copiado'"),
      ("'Pause':'Play'", "'Pausa':'Reproducir'"), ("'Photographs from '", "'Fotografías de '"), ("'View larger: '", "'Ver más grande: '"),
      ('aria-label="Contents" title="Contents"', 'aria-label="Contenido" title="Contenido"'),
      ('B.E.', 'E.B.')]
MEAN = {"Splendor": "Esplendor", "Glory": "Gloria", "Beauty": "Belleza", "Grandeur": "Grandeza", "Light": "Luz", "Mercy": "Misericordia", "Words": "Palabras",
        "Perfection": "Perfección", "Names": "Nombres", "Might": "Fuerza", "Will": "Voluntad", "Knowledge": "Conocimiento", "Power": "Poder", "Speech": "Habla",
        "Questions": "Preguntas", "Honor": "Honor", "Sovereignty": "Soberanía", "Dominion": "Dominio", "Loftiness": "Sublimidad"}
NUDGE = {"Share your ideas to shape the magazine\\u2019s future.": "Comparte tus ideas para dar forma al futuro de la revista.",
         "Takes 5 minutes.": "Toma 5 minutos.", "Have the next stories sent to you.": "Recibe las próximas historias.",
         "By email, as they\\u2019re published.": "Por correo electrónico, a medida que se publiquen.", "Know a story like these?": "¿Conoces una historia como estas?",
         "Send story ideas, photos and field notes from where you live.": "Envía ideas para historias, fotos y notas de campo desde donde vives.",
         "What do you enjoy reading most?": "¿Qué es lo que más te gusta leer?", "Which stories, ideas and resources matter to you?": "¿Qué historias, ideas y recursos te importan?",
         "What should we write about next?": "¿Sobre qué deberíamos escribir después?"}
DESC = {"Earlier this year, the Bahá’ís of the United States addressed a message titled": "A principios de este año, los bahá’ís de Estados Unidos dirigieron un mensaje titulado “Un esfuerzo común” a toda alma que lleva “la promesa de Estados Unidos en su corazón”…",
        "How can the arts bring neighbors together": "¿Cómo pueden las artes unir a los vecinos y crear espacios para una conexión más profunda y para la resolución colectiva de problemas?",
        "At an exhibition during this year’s Los Angeles Design Weekend": "En una exposición durante el Los Angeles Design Weekend de este año, la artista visual Maya Mansour escuchó al curador explicar el calendario bahá’í a los visitantes…",
        "In the months since the National Spiritual Assembly shared": "En los meses transcurridos desde que la Asamblea Espiritual Nacional compartió “Un esfuerzo común”, los bahá’ís han ido creando oportunidades para presentar el mensaje a sus amigos y vecinos…"}
NOTE = ('<p class="about"><b>Sobre esta traducción.</b> Esta edición traduce al español la edición seleccionada en inglés. '
        'Los pasajes de los Escritos bahá’ís y de la Casa Universal de Justicia se citan de traducciones publicadas cuando existen; '
        'los demás se ofrecen en traducción provisional.</p>')
missing = []
def tr(s, where):
    k = norm(s)
    if not k or not re.search(r"[A-Za-z]{2}", k): return None
    if k in OCC and OCC[k]: return OCC[k].pop(0)
    if k in MAP: return MAP[k]
    if k == "English": return None
    for en, es in DESC.items():
        if k.startswith(en): return es
    if k == "The full Arts Issue": return "Todo el número de las artes"
    m = re.fullmatch(r"(.+) · The American Bahá’í", k)
    if m and norm(m.group(1)) in MAP: return MAP[norm(m.group(1))] + " · The American Bahá’í"
    m = re.fullmatch(r"(\d+) min read", k)
    if m: return m.group(1) + " min de lectura"
    missing.append((where, k)); return None
def text_node(t):
    r = tr(t, "text")
    if r is None: return t
    lead = re.match(r"\s*", t).group(0); trail = re.search(r"\s*$", t).group(0)
    return lead + html.escape(r, quote=False) + trail
def tag(t):
    def at(m):
        a, v = m.group(1), m.group(2)
        r = tr(v, "@" + a)
        return m.group(0) if r is None else f' {a}="{html.escape(r)}"'
    t = re.sub(r'\s(' + "|".join(KEEP_ATTR) + r')="([^"]*)"', at, t)
    if t.startswith("<meta") and re.search(r'(name="description"|property="og:(title|description|image:alt)")', t):
        t = re.sub(r'\s(content)="([^"]*)"', at, t)
    return t
def script(s):
    for a, b in JS: s = s.replace(a, b)
    for en, es in MEAN.items(): s = s.replace(f'"{en}"', f'"{es}"')
    for en, es in NUDGE.items(): s = s.replace(f'"{en}"', '"' + es + '"').replace(f"'{en}'", "'" + es + "'")
    return s
def translate(h, depth):
    h = h.replace('<i>T</i>wo', '<i>D</i>wo')
    up = "../" * depth
    h = (h.replace('<html lang="en"', '<html lang="es"').replace('src="img/', f'src="{up}img/').replace('href="img/', f'href="{up}img/')
          .replace('url(img/', f'url({up}img/').replace('href="favicon.svg"', f'href="{up}favicon.svg"').replace('data-src="audio/', f'data-src="{up}audio/'))
    h = h.replace('<span class="lang" hidden><a href="es/" hreflang="es" lang="es">Español</a></span>', '<span class="lang"><a href="../" hreflang="en" lang="en">English</a></span>')
    h = h.replace("Edición seleccionada</span>", "Edición seleccionada</span>")
    out = []
    for part in re.split(r'(<script\b.*?</script>|<style\b.*?</style>|<[^>]+>)', h, flags=re.S | re.I):
        if not part: continue
        if part.startswith("<script"): out.append(script(part))
        elif part.startswith("<style"): out.append(part.replace('"183 B.E."', '"183 E.B."'))
        elif part.startswith("<"): out.append(tag(part))
        else: out.append(re.sub(r"(?<=\d),(?=\d{3}\b)", "", text_node(part)).replace("B.E.", "E.B."))
    h = "".join(out)
    h = h.replace("</head>", "<style>.nyo .n2{font-size:16.8cqw;margin-left:4%}</style>\n</head>", 1)
    h = re.sub(r'(<p class="about"><b>Sobre este número\.</b>.*?</p>)', lambda m: m.group(1) + "\n    " + NOTE, h, count=1, flags=re.S)
    return h
if __name__ == "__main__":
    src = open(os.path.join(SITE, "index.html")).read()
    es = translate(src, 1)
    es = es.replace('<meta property="og:url" content="https://aoaoaoa.github.io/usbns/magazine/">', '<meta property="og:url" content="https://aoaoaoa.github.io/usbns/magazine/es/">')
    es = es.replace('<meta charset="utf-8">\n', '<meta charset="utf-8">\n<meta property="og:locale" content="es_US">\n<link rel="alternate" hreflang="en" href="https://aoaoaoa.github.io/usbns/magazine/">\n', 1)
    es = es.replace("document.documentElement.dataset.base||", "'https://aoaoaoa.github.io/usbns/magazine/es/'||", 1)
    os.makedirs(os.path.join(SITE, "es"), exist_ok=True)
    open(os.path.join(SITE, "es", "index.html"), "w").write(es)
    _en = open(os.path.join(SITE, "index.html")).read()
    if 'hreflang="es"' not in _en.split("</head>")[0]:
        open(os.path.join(SITE, "index.html"), "w").write(_en.replace('<meta charset="utf-8">\n', '<meta charset="utf-8">\n<link rel="alternate" hreflang="es" href="https://aoaoaoa.github.io/usbns/magazine/es/">\n', 1))
    # story pages in Spanish
    for slug in ("gregory", "newyorkers", "twoartists", "abs", "endeavor"):
        p = os.path.join(SITE, slug, "index.html")
        if not os.path.exists(p): continue
        s = translate(open(p).read().replace('src="../img/', 'src="img/').replace('href="../img/', 'href="img/').replace('url(../img/', 'url(img/').replace('href="../favicon.svg"', 'href="favicon.svg"').replace('data-src="../audio/', 'data-src="audio/'), 2)
        s = s.replace(f'https://aoaoaoa.github.io/usbns/magazine/{slug}/', f'https://aoaoaoa.github.io/usbns/magazine/es/{slug}/')
        s = s.replace("document.documentElement.dataset.base||", "'https://aoaoaoa.github.io/usbns/magazine/es/'||", 1)
        os.makedirs(os.path.join(SITE, "es", slug), exist_ok=True)
        open(os.path.join(SITE, "es", slug, "index.html"), "w").write(s)
    seen = set(); miss = [m for m in missing if not (m in seen or seen.add(m))]
    print("untranslated:", len(miss))
    for w, k in miss[:80]: print(" ", w, "|", k[:110])
