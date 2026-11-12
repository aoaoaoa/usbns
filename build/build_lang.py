"""Translations live only under /magazine/lang/.
Run on the deploy tree after every copy of site/ into it (python3 build_lang.py /home/claude/usbns/magazine):
  1. moves the translations (es/, members/zh/, members/fa/) out of the public tree into lang/;
  2. strips every translation link from the public pages;
  3. mirrors the landing, the magazine and its pages, and the members edition into lang/, with the translation links shown.
Pages in lang/ link to one another; assets (img/, audio/, icons) stay at the magazine root and are referenced absolutely."""
import os, re, sys, shutil, posixpath

ROOT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/usbns/magazine"
LANG = os.path.join(ROOT, "lang")
BASE = "/usbns/magazine/"
TRANS = ["es", "members/zh", "members/fa"]
PAGES = ["", "landing", "members", "gregory", "newyorkers", "twoartists", "abs", "endeavor", "comic", "contact", "terms", "privacy"]
MIRRORED = set(PAGES) | set(TRANS) | {"es/" + p for p in ("gregory", "newyorkers", "twoartists", "abs", "endeavor")}

def strip_links(h):
    h = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', "", h)
    h = re.sub(r'<span class="lang"( hidden)?>.*?</span>(?=</div>)', "", h, flags=re.S)
    return h

L = "/usbns/magazine/lang/"
EDS = [("en", "English", L), ("es", "Español", L + "es/"), ("zh-Hans", "中文", L + "members/zh/"), ("fa", "فارسی", L + "members/fa/")]
def langs(skip, en=L):
    return '<span class="lang">' + " · ".join(f'<a href="{en if c == "en" else u}" hreflang="{c}" lang="{c}">{n}</a>' for c, n, u in EDS if c != skip) + "</span>"
BAND = ('<!-- langband --><style>.lgb{background:var(--card);border-block:1px solid var(--rule)}.lgb .wrap{padding-block:36px 40px}'
        '.lgb h2{font:700 12px/1 var(--ui);letter-spacing:.18em;text-transform:uppercase;color:var(--mute);margin:0 0 18px}'
        '.lgb ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}'
        '.lgb a{display:grid;gap:6px;height:100%;text-decoration:none;color:var(--ink);background:var(--paper);border:1px solid var(--rule);border-radius:4px;padding:18px 20px}'
        '.lgb a:hover,.lgb a:focus-visible{border-color:var(--ink)}.lgb b{font:700 24px/1.2 var(--text)}.lgb span{font:15px/1.45 var(--text);color:var(--mute)}'
        '.lgb i{font:600 14px var(--ui);font-style:normal;margin-top:4px}'
        '.lgb [lang=zh-Hans] b,.lgb [lang=zh-Hans] span{font-family:"Noto Serif SC",var(--text)}.lgb [lang=fa] b,.lgb [lang=fa] span,.lgb [lang=fa] i{font-family:"Vazirmatn",var(--ui)}</style>'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Vazirmatn:wght@400;700&display=swap">'
        '<section class="lgb" aria-labelledby="lg-h"><div class="wrap"><h2 id="lg-h">This issue in other languages</h2><ul>'
        f'<li><a href="{L}es/" hreflang="es" lang="es"><b>Español</b><span>Edición seleccionada: cinco reportajes de este número.</span><i>Leer el número →</i></a></li>'
        f'<li><a href="{L}members/zh/" hreflang="zh-Hans" lang="zh-Hans"><b>中文</b><span>完整版：五篇专题、一则漫画，以及总灵理会年中文告的印刷版中文译文。</span><i>阅读本期 →</i></a></li>'
        f'<li><a href="{L}members/fa/" hreflang="fa" lang="fa" dir="rtl"><b>فارسی</b><span>نسخهٔ کامل: پنج گزارش، یک داستان مصوّر، و ترجمهٔ فارسیِ چاپیِ پیام نیمه‌سالهٔ محفل روحانی ملّی.</span><i>خواندن این شماره ←</i></a></li>'
        '</ul></div></section><!-- /langband -->')
def show_links(h, rel):
    h = re.sub(r'<span class="lang"( hidden)?>.*?</span>(?=</div>)', "", h, flags=re.S)
    if rel == "":
        h = h.replace('<span>Curated edition</span></div>', '<span>Curated edition</span>' + langs("en") + '</div>', 1)
    if rel == "members":
        h = h.replace('<span><a href="../">Curated edition</a></span>', '<span><a href="../">Curated edition</a></span>' + langs("en"), 1)
    if rel == "landing" and "langband" not in h:
        i = h.find('<section class="band secin"')
        if i > 0: h = h[:i] + BAND + "\n" + h[i:]
    return h

def page_dir(t):  # the mirrored page a resolved path belongs to, or None
    t = t.strip("/")
    for p in sorted(MIRRORED, key=len, reverse=True):
        if t == p or t.startswith(p + "/") and not re.search(r"\.\w+$", t[len(p):]):
            return p
    return "" if t in ("", ".", "index.html") else None

def rebase(h, rel):
    """h is a page that lived at ROOT/rel/; it now lives at ROOT/lang/rel/."""
    h = re.sub(r'(?<![\w/.])(?:\.\./|\./)*(img|audio)/', BASE + r"\1/", h)
    h = re.sub(r'(?<![\w/.])(?:\.\./)*(favicon\.svg|icon-\d+\.png|apple-touch-icon\.png|manifest\.webmanifest)\b', BASE + r"\1", h)
    def ab(m):
        p = m.group(2)
        return m.group(1) + (BASE + "lang/" + p if page_dir(p) is not None else BASE + p)
    h = re.sub(r'(["\'])' + re.escape(BASE) + r'(?!lang/)([^"\'#?]*)', ab, h)
    def relink(m):
        a, u = m.group(1), m.group(2)
        if re.match(r"(?:[a-z]+:|#|/|data:)", u) or not u: return m.group(0)
        path, frag = (u.split("#", 1) + [""])[:2]
        t = posixpath.normpath(posixpath.join(rel or ".", path)) if path else rel
        if page_dir(t) is not None: return m.group(0)
        return f'{a}="{BASE}{t}{"/" if path.endswith("/") else ""}{"#" + frag if frag else ""}"'
    h = re.sub(r'\b(href|src|data-src|data-full|poster)="([^"]*)"', relink, h)
    h = h.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex">', 1) if 'name="robots"' not in h else h
    return h

def main():
    os.makedirs(LANG, exist_ok=True)
    for t in TRANS:  # 1
        src, dst = os.path.join(ROOT, t), os.path.join(LANG, t)
        if os.path.isdir(src):
            if os.path.isdir(dst): shutil.rmtree(dst)
            shutil.copytree(src, dst); shutil.rmtree(src)
    for dirpath, _, files in os.walk(ROOT):  # 2
        if dirpath.startswith(LANG): continue
        for f in files:
            if f.endswith(".html"):
                p = os.path.join(dirpath, f); h = open(p).read(); s = strip_links(h)
                if s != h: open(p, "w").write(s)
    n = 0
    for rel in PAGES:  # 3
        src = os.path.join(ROOT, rel, "index.html")
        if not os.path.exists(src): continue
        h = rebase(show_links(open(src).read(), rel), rel)
        os.makedirs(os.path.join(LANG, rel), exist_ok=True)
        open(os.path.join(LANG, rel, "index.html"), "w").write(h); n += 1
    for dirpath, _, files in os.walk(LANG):  # the translations, rebased one level deeper
        for f in files:
            if not f.endswith(".html"): continue
            rel = os.path.relpath(dirpath, LANG)
            if rel.split(os.sep)[0] in ("es",) or rel.startswith("members" + os.sep):
                p = os.path.join(dirpath, f); h = open(p).read()
                h = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', "", h)
                code = {"es": "es", "members/zh": "zh-Hans", "members/fa": "fa"}.get("/".join(rel.split(os.sep)[:2]) if rel.startswith("members") else "es")
                if f == "index.html" and rel in ("es", "members" + os.sep + "zh", "members" + os.sep + "fa"):
                    h = re.sub(r'<span class="lang"( hidden)?>.*?</span>(?=</div>)', lambda m: langs(code, L if code == "es" else L + "members/"), h, count=1, flags=re.S)
                h = rebase(h, rel.replace(os.sep, "/"))
                open(p, "w").write(h)
    print("lang:", n, "pages mirrored;", ", ".join(t for t in TRANS if os.path.isdir(os.path.join(LANG, t))))

if __name__ == "__main__":
    main()
