"""Give every published page its favicon and add-to-home-screen icons and name.
Run last, after every other step has written the pages:  python3 icons.py /home/claude/usbns /home/claude/labs
Each page gets one marked block; any older icon, manifest or app-name tags are removed first, so the step can run any number of times."""
import os, re, sys

M = "/usbns/magazine/"
TAB = dict(svg=M + "favicon.svg", touch=M + "apple-touch-icon.png", p192=M + "icon-192.png", p512=M + "icon-512.png", manifest=M + "manifest.webmanifest", theme="#222e4c")
AUD = "/labs/audience/"
AUDS = dict(svg=AUD + "favicon.svg", touch=AUD + "apple-touch-icon.png", p192=AUD + "icon-192.png", p512=AUD + "icon-512.png", manifest=AUD + "manifest.webmanifest", theme="#1b5e6b")
DIG = dict(TAB, manifest="/labs/digitab/manifest.webmanifest")

# (url prefix, icon set, home-screen name); the first match wins
RULES = [("/usbns/magazine/labs/", TAB, "TAB Labs"),
         ("/usbns/magazine/brief/", TAB, "TAB Brief"),
         ("/usbns/", TAB, "American Bahá’í"),
         ("/labs/audience/", AUDS, "Audiences"),
         ("/labs/digitab/", DIG, "TAB Brief")]

STRIP = [r'\n?<!-- icons -->.*?<!-- /icons -->\n?',
         r'<link rel="(?:icon|shortcut icon|apple-touch-icon|manifest|mask-icon)"[^>]*>\n?',
         r'<meta name="(?:application-name|apple-mobile-web-app-title|apple-mobile-web-app-capable|theme-color)"[^>]*>\n?']

def block(s, name):
    return (f'<!-- icons --><link rel="icon" href="{s["svg"]}" type="image/svg+xml"><link rel="icon" type="image/png" sizes="192x192" href="{s["p192"]}">'
            f'<link rel="apple-touch-icon" sizes="180x180" href="{s["touch"]}"><link rel="manifest" href="{s["manifest"]}">'
            f'<meta name="application-name" content="{name}"><meta name="apple-mobile-web-app-title" content="{name}"><meta name="theme-color" content="{s["theme"]}"><!-- /icons -->')

def url_of(root, path):
    rel = os.path.relpath(path, root).replace(os.sep, "/")
    return "/" + os.path.basename(root.rstrip("/")) + "/" + rel

def apply(root):
    n = 0
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x not in (".git", "build")]
        for f in files:
            if not f.endswith(".html"):
                continue
            p = os.path.join(d, f); u = url_of(root, p)
            rule = next((r for r in RULES if u.startswith(r[0])), None)
            if not rule:
                continue
            h = open(p, encoding="utf-8").read()
            if "<head" not in h and "<title" not in h:
                continue
            for rx in STRIP:
                h = re.sub(rx, "", h, flags=re.S)
            b = block(rule[1], rule[2])
            if "</title>" in h:
                h = h.replace("</title>", "</title>" + b, 1)
            elif "</head>" in h:
                h = h.replace("</head>", b + "</head>", 1)
            else:
                continue
            open(p, "w", encoding="utf-8").write(h); n += 1
    return n

if __name__ == "__main__":
    for r in sys.argv[1:]:
        print(r, apply(r))
