"""Typographic apostrophes in text nodes only (never inside tags, scripts or styles)."""
import re
_SKIP = re.compile(r'(<script\b.*?</script>|<style\b.*?</style>|<[^>]+>)', re.S | re.I)
_L = r"[^\W_]"
def _fix(t):
    t = re.sub(r"(?<=" + _L + r")'(?=" + _L + r")", "\u2019", t)     # Bahá'í, Abdu'l
    t = re.sub(r"(?:(?<=^)|(?<=[\s(\[\u201c\u2014\u2013-]))'(?=\d)", "\u2019", t)  # '90s
    t = re.sub(r"(?:(?<=^)|(?<=[\s(\[\u201c\u2014\u2013-]))'(?=" + _L + r")", "\u2018", t)  # 'Abdu'l-Bahá, opening quote
    t = re.sub(r"(?<=[^\W_]|[.,!?;:])'", "\u2019", t)                 # closing / possessive
    return t
def curl(h):
    out = []
    for part in _SKIP.split(h):
        if not part: continue
        out.append(part if part.startswith('<') else _fix(part))
    return "".join(out)
