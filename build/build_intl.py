"""Members-only editions in Chinese (/magazine/members/zh/) and Persian (/magazine/members/fa/).
Source: out/lite_{lang}.html, the members build with the six stories and the mid-year letter, the letter already set in the printed translation (intl/letter_{lang}.py).
Everything else is translated segment by segment from intl/{lang}_map.json, as build_es.py does for Spanish."""
import re, json, html, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "site", "magazine")
norm = lambda s: re.sub(r"\s+", " ", html.unescape(s).replace("'", "’")).strip()
KEEP_ATTR = ("alt", "aria-label", "title", "placeholder", "data-title", "data-name", "data-pt", "data-pb")
CFG = {
 "zh": dict(lang="zh-Hans", dir="ltr", name="中文", locale="zh_CN", clusters="{a}：{n}个联区", about="关于本期。",
            note='<p class="about"><b>关于本译本。</b>总灵理会的年中文告采用印刷版的中文译文。其余内容由英文版翻译而来；巴哈伊圣作与世界正义院文献的引文凡有正式出版译本的均予采用，其余为暂定译文。</p>',
            fonts="family=Noto+Serif+SC:wght@400;600;700;900&family=Noto+Sans+SC:wght@400;500;700",
            serif='"Noto Serif SC"', sans='"Noto Sans SC"'),
 "fa": dict(lang="fa", dir="rtl", name="فارسی", locale="fa_IR", clusters="{a}: {n} محدوده", about="دربارهٔ این شماره.",
            note='<p class="about"><b>دربارهٔ این ترجمه.</b> پیام نیمه‌سالهٔ محفل روحانی ملّی از ترجمهٔ فارسیِ نسخهٔ چاپی آمده است. باقی مطالب از نسخهٔ انگلیسی ترجمه شده است؛ آثار مبارکه و بیانات بیت‌العدل اعظم هر جا متن اصلی یا ترجمهٔ منتشرشده در دسترس بوده از آن نقل شده و در غیر این صورت ترجمه‌ای غیررسمی است.</p>',
            fonts="family=Vazirmatn:wght@300..800&family=Noto+Naskh+Arabic:wght@400..700",
            serif='"Noto Naskh Arabic"', sans='"Vazirmatn"'),
}
def load(lg):
    p = os.path.join(HERE, "intl", f"{lg}_map.json")
    M = json.load(open(p)) if os.path.exists(p) else {}
    return {norm(k): v for k, v in M.items()}
def load_js(lg):
    p = os.path.join(HERE, "intl", f"{lg}_js.json")
    return json.load(open(p)) if os.path.exists(p) else {}

def build(lg):
    C = CFG[lg]; MAP = load(lg); JS = load_js(lg); missing = []
    def tr(s, where):
        k = norm(s)
        if not k or not re.search(r"[A-Za-z]{2}", k): return None
        if k in MAP: return MAP[k]
        if k == "English": return None
        if re.search(r"[\u0600-\u06FF\u4e00-\u9fff]", k):
            m = re.fullmatch(r"(.+): (\d+) clusters?", k)
            return C["clusters"].format(a=m.group(1), n=m.group(2)) if m else None  # already in the edition's language
        m = re.fullmatch(r"(.+) · The American Bahá’í", k)
        if m and norm(m.group(1)) in MAP: return MAP[norm(m.group(1))] + " · The American Bahá’í"
        m = re.fullmatch(r"(\d+) min read", k)
        if m and "{n} min read" in MAP: return MAP["{n} min read"].replace("{n}", m.group(1))
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
        for a, b in JS.items(): s = s.replace(a, b)
        return s
    def fonts(css):  # put the script's own faces after each Latin face, so Latin keeps its type and the rest falls through
        css = re.sub(r'("(?:Literata|Newsreader|Libre Caslon Text|Fraunces|Bodoni Moda)")', r'\1,' + C["serif"], css)
        css = re.sub(r'("(?:Bricolage Grotesque|Barlow Condensed|Big Shoulders Display)")', r'\1,' + C["sans"], css)
        return css
    h = open(os.path.join(HERE, "out", f"lite_{lg}.html")).read()
    h = (h.replace('src="../img/', 'src="../../img/').replace('href="../img/', 'href="../../img/').replace('url(../img/', 'url(../../img/')
          .replace('href="FAVICON"', 'href="../../favicon.svg"').replace('data-src="audio/', 'data-src="../../audio/'))
    h = h.replace('<html lang="en"', f'<html lang="{C["lang"]}" dir="{C["dir"]}"', 1)
    out = []
    for part in re.split(r'(<script\b.*?</script>|<style\b.*?</style>|<[^>]+>)', h, flags=re.S | re.I):
        if not part: continue
        if part.startswith("<script"): out.append(script(part))
        elif part.startswith("<style"): out.append(fonts(part))
        elif part.startswith("<"): out.append(fonts(tag(part)) if 'style="' in part else tag(part))
        else: out.append(text_node(part))
    h = "".join(out).replace(">183 B.E.<", ">183 " + JS.get("B.E.", "B.E.") + "<").replace('"183 B.E."', '"183 ' + JS.get("B.E.", "B.E.") + '"')
    if lg == "fa": h = h.replace("183 بدیع", "۱۸۳ بدیع")
    h = re.sub(r'(<p class="about"><b>' + re.escape(C["about"]) + r'</b>.*?</p>)', lambda m: m.group(1) + "\n    " + C["note"], h, count=1, flags=re.S)
    link = f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{C["fonts"]}&display=swap">\n'
    h = h.replace("</head>", link + '<meta name="robots" content="noindex">\n' + (RTL_CSS if C["dir"] == "rtl" else ZH_CSS) + "\n</head>", 1)
    h = h.replace('<meta charset="utf-8">\n', f'<meta charset="utf-8">\n<meta property="og:locale" content="{C["locale"]}">\n', 1)
    h = h.replace("document.documentElement.dataset.base||", f"'https://aoaoaoa.github.io/usbns/magazine/members/{lg}/'||", 1)
    os.makedirs(os.path.join(SITE, "members", lg), exist_ok=True)
    open(os.path.join(SITE, "members", lg, "index.html"), "w").write(h)
    seen = set(); miss = [m for m in missing if not (m in seen or seen.add(m))]
    return miss

ZH_CSS = "<style>:lang(zh-Hans) .prose p,:lang(zh-Hans) .prose li{line-height:1.85;text-align:justify;text-justify:inter-character}:lang(zh-Hans) .pull p{text-align:start}:lang(zh-Hans) .kicker,:lang(zh-Hans) .kicker-top,:lang(zh-Hans) .k{letter-spacing:.06em}</style>"
RTL_CSS = "<style>[dir=rtl] .prose p,[dir=rtl] .prose li{line-height:2;text-align:justify}[dir=rtl] .pull p,[dir=rtl] .prose .pull p{text-align:start}[dir=rtl] .kicker,[dir=rtl] .kicker-top,[dir=rtl] .k{letter-spacing:0}</style>"

if __name__ == "__main__":
    for lg in (sys.argv[1:] or ["zh", "fa"]):
        if not os.path.exists(os.path.join(HERE, "out", f"lite_{lg}.html")): continue
        miss = build(lg)
        print(lg, "untranslated:", len(miss))
        if "-v" in sys.argv or len(miss) < 60:
            for w, k in miss[:2000]: print(" ", w, "|", k[:140])
        json.dump([k for w, k in miss], open(os.path.join(HERE, "intl", f"{lg}_missing.json"), "w"), ensure_ascii=False, indent=0)
