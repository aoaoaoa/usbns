# Demos: /magazine/test/privacy/ (cleanup) and /magazine/test/contact/ (redesigns). Shares the shell and switcher with about_terms_demo.py.
import os, re
from about_terms_demo import shell, switch, SWITCH_CSS, SWITCH_JS, TERMS_CSS, SITE, NSA

# ------------------------------------------------------------------ PRIVACY (same substance as the live text, reorganized)
TOLL = "1-800-228-6483 (1-800-22 UNITE)"
STOPW = ["STOP", "QUIT", "END", "REVOKE", "OPT OUT", "CANCEL", "UNSUBSCRIBE"]
PG = [("Not tracked", "Visits are counted only in aggregate, never by person."),
      ("Only what you give us", "Personal details come only from forms you fill in."),
      ("Texts are your choice", "Opt in when you give your number; text STOP to end.")]
PV = [("visits", "Visits", "Visitors to this website are not tracked, except to produce aggregate statistical data which does not identify individual users."),
      ("cookies", "Cookies", "Where cookies are used to provide essential functionality, they are not used to track use of the website or to store personally identifiable information."),
      ("forms", "Information you give us", "We collect information that personally identifies you only when you provide it to us by filling in an online form. This may include your name, email address, address and telephone number. All identifiable personal information that you provide will be kept confidential and will only be used by authorized individuals to fulfill the purpose for which it was originally collected, or for a use consistent with that purpose."),
      ("sms", "Text messages", "When you provide your mobile number, you will be given the choice to opt in to SMS communications, including messages sent from our toll-free SMS number, " + TOLL + ". Mobile information collected, including information provided for receiving SMS messages sent via standard long-code numbers or via our toll-free number, will not be shared with third parties or affiliates for marketing or promotional purposes. Text messaging originator opt-in data and consent will not be shared with third parties."
              '<span class="sw">To opt out at any time, text ' + " · ".join(f"<kbd>{w}</kbd>" for w in STOPW) + "</span>"),
      ("security", "Security", "Steps have been taken to secure all information collected from unauthorized access, use or disclosure."),
      ("links", "Other websites", "This website may include links to websites with different privacy policies.")]
PRIV = ('<h1>Privacy policy</h1><p class="lede">This site collects personal information only when you give it to us, and uses it only for the purpose you gave it.</p>'
        '<div class="gl pg">' + "".join(f"<section><h3>{h}</h3><p>{x}</p></section>" for h, x in PG) + '</div>'
        '<ol class="cl">' + "".join(f'<li id="{i}"><b>{h}.</b> {x}</li>' for i, h, x in PV) + "</ol>")
PCHG = [("Two dense paragraphs", "split into six short, labeled sections: visits, cookies, information you give us, text messages, security, other websites."),
        ("Text messages", "the SMS sentences gathered in one place, in the order a reader meets them: opting in, what is shared, how to opt out. The opt-out words are set as keys."),
        ("Repetition", "“All the above categories exclude text messaging originator opt-in data and consent; this information will not be shared with third parties” shortened to “Text messaging originator opt-in data and consent will not be shared with third parties.”"),
        ("At a glance", "three plain-language points above the policy, marked as non-binding."),
        ("Not added", "a contact for privacy questions and a last-updated date. Both are usual on such pages; neither is in the current text.")]
PRIV_CSS = (".pg p{font:15px/1.45 var(--ui)!important;margin:0!important}.sw{display:block;margin-top:10px;font:14px/2 var(--ui)}"
            "kbd{font:700 12px var(--ui);border:1px solid var(--rule);border-bottom-width:2px;border-radius:4px;padding:2px 7px;background:var(--card)}")

# ------------------------------------------------------------------ CONTACT (same contacts as the live page, three layouts)
SURVEY = "https://form.typeform.com/to/NfIWSbQl"
CT = {
 "submit": ("Submit a story or photographs", "Online, with your Bahá’í Online Services account (BOSA)", "link.bahai.us/TAB_submit", "https://link.bahai.us/TAB_submit"),
 "editors": ("Write to the editors", "Questions, leads, or a story idea in a few lines", "TAB@usbnc.org", "mailto:TAB@usbnc.org"),
 "feedback": ("Share your experience of the site", "What worked, what didn’t, and what you’d like to see", "research@bahai.us", "mailto:research@bahai.us"),
 "survey": ("Take the reader survey", "Share your ideas to shape the magazine’s future", "5 minutes", SURVEY),
 "subs": ("Bahá’í Subscriber Service", "Subscriptions to the magazines and periodicals of the National Spiritual Assembly", "1.800.999.9019 · subscription@usbnc.org", "mailto:subscription@usbnc.org"),
 "back": ("Back issues", "$3 + shipping/handling, from the Bahá’í Distribution Service", "1.800.999.9019 · bahaibookstore.com", "https://www.bahaibookstore.com"),
 "media": ("Office of Public Affairs", "For editors, journalists, and other media professionals", "(202) 833-8990 · usnsa-opa@usbnc.org", "mailto:usnsa-opa@usbnc.org"),
 "nc": ("Bahá’í National Center offices", "1233 Central St., Evanston, IL 60201", "(847) 733-3400", "tel:+18477333400"),
}
STAFF2 = ('<p><b>Editor</b> Neena Rouhani · <a href="mailto:nrouhani@usbnc.org">nrouhani@usbnc.org</a></p>'
          '<p><b>Designer</b> Luthando Mazibuko · <a href="mailto:lmazibuko@usbnc.org">lmazibuko@usbnc.org</a></p>'
          '<p class="ph">Photography by license or by permission of community members.</p>')
MH = f'<section class="mh2"><p class="wm"><small>The</small>American Bahá’í</p>{STAFF2}</section>'
def card(k):
    h, d, v, u = CT[k]; ext = ' target="_blank" rel="noopener"' if u.startswith("https") else ""
    return f'<a class="c" href="{u}"{ext}><b>{h}</b><span class="d">{d}</span><span class="v">{v} <span aria-hidden="true">→</span></span></a>'
ROUTES = [("I have a story or photographs", ["submit", "editors"]), ("I have feedback on the site", ["feedback", "survey"]),
          ("I want the magazine", ["subs", "back"]), ("I’m a journalist", ["media"]), ("I need the National Center", ["nc"])]
DIR = [("Stories and photographs", ["submit", "editors"]), ("Feedback", ["feedback", "survey"]), ("Subscriptions", ["subs", "back"]), ("Media", ["media"]), ("National Center", ["nc"])]
c1 = ('<h1>How can we help?</h1><div class="rt">' + "".join(f'<button type="button" aria-pressed="{str(k == 0).lower()}" data-k="{k}">{q}</button>' for k, (q, _) in enumerate(ROUTES)) + "</div>"
      + "".join(f'<div class="rp" data-k="{k}"{"" if k == 0 else " hidden"}>{"".join(card(x) for x in L)}</div>' for k, (_, L) in enumerate(ROUTES)) + MH)
rows = ""
for g, L in DIR:
    for j, x in enumerate(L):
        th = f'<th rowspan="{len(L)}" scope="rowgroup">{g}</th>' if j == 0 else ""
        rows += f'<tr>{th}<td><b>{CT[x][0]}</b><span>{CT[x][1]}</span></td><td><a href="{CT[x][3]}">{CT[x][2]}</a></td></tr>'
c2 = f'<h1>Contacts</h1><table class="dir"><tbody>{rows}</tbody></table>' + MH
c3 = (f'<div class="sp"><aside class="mh2 stk"><p class="wm"><small>The</small>American Bahá’í</p>{STAFF2}<p class="pub2">Published by the {NSA}.</p></aside><div>'
      '<h1>Contacts</h1>' + "".join(f'<h2>{g}</h2><div class="g2">{"".join(card(x) for x in L)}</div>' for g, L in DIR) + "</div></div>")
CON_CSS = ("main{max-width:980px!important}"
 ".c{display:grid;gap:6px;align-content:start;text-decoration:none;color:var(--ink)!important;background:var(--card);border:1px solid var(--rule);border-top:4px solid #222e4c;padding:18px}.c:hover{border-color:var(--ink)}"
 ".c b{font:700 19px/1.25 var(--text)}.c .d{font:14px/1.5 var(--ui);color:var(--mute)}.c .v{font:700 15px var(--ui);color:var(--link)}"
 ".rt{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 20px}.rt button{font:600 15px var(--ui);border:1px solid var(--rule);background:var(--card);color:var(--ink);border-radius:999px;padding:10px 16px;cursor:pointer}.rt button[aria-pressed=true]{background:#222e4c;color:#f2cfc6;border-color:#222e4c}"
 ".rp{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}.rp[hidden]{display:none}"
 ".mh2{margin:40px 0 0;background:var(--card);border:1px solid var(--rule);overflow:hidden}.mh2 .wm{margin:0 0 14px!important;background:#222e4c;color:#fff;font:400 30px/1 var(--text)!important;padding:16px 20px}.mh2 .wm small{display:block;font:italic 14px var(--text);color:#f2cfc6}"
 ".mh2 p{font:15px/1.5 var(--ui)!important;margin:0 20px 8px!important}.mh2 p b{display:inline-block;min-width:80px;color:var(--mute)}.mh2 .ph{color:var(--mute);margin-bottom:18px!important}"
 ".dir{width:100%;border-collapse:collapse;font:15px/1.45 var(--ui)}.dir th{text-align:left;vertical-align:top;font:700 12px var(--ui);letter-spacing:.14em;text-transform:uppercase;color:#b8782e;padding:16px 16px 16px 0;width:22%;border-top:1px solid var(--rule)}"
 ".dir td{border-top:1px solid var(--rule);padding:14px 16px 14px 0;vertical-align:top}.dir td b{display:block;font:700 17px var(--text)}.dir td span{color:var(--mute);font-size:14px}.dir td:last-child{white-space:nowrap}"
 ".sp{display:grid;grid-template-columns:280px minmax(0,1fr);gap:40px;align-items:start}.stk{position:sticky;top:60px;margin:0}.pub2{color:var(--mute);font-size:13px!important;margin-bottom:18px!important}"
 ".g2{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}"
 "@media (max-width:760px){.sp{grid-template-columns:1fr}.stk{position:static}.dir,.dir tbody,.dir tr,.dir th,.dir td{display:block;width:auto}.dir th{padding-bottom:4px}.dir td{border:0;padding:4px 0}.dir td:last-child{white-space:normal;padding-bottom:14px;border-bottom:1px solid var(--rule)}}")
CON_JS = ("(function(){var B=[].slice.call(document.querySelectorAll('.rt button')),P=[].slice.call(document.querySelectorAll('.rp'));"
          "B.forEach(function(b){b.onclick=function(){B.forEach(function(x){x.setAttribute('aria-pressed',x===b)});P.forEach(function(p){p.hidden=p.dataset.k!==b.dataset.k})}})})();")

def cur(slug): return re.search(r"<main>(.*)</main>", open(os.path.join(SITE, slug, "index.html")).read(), re.S).group(1)
def write(d, h):
    os.makedirs(os.path.join(SITE, "test", d), exist_ok=True); open(os.path.join(SITE, "test", d, "index.html"), "w").write(h)

if __name__ == "__main__":
    prop = PRIV + '<aside class="chg"><h2>What changed</h2><ul>' + "".join(f"<li><b>{a}:</b> {b}</li>" for a, b in PCHG) + "</ul></aside>"
    bar, vv = switch("Privacy page", [("Proposed", prop), ("Current", cur("privacy"))])
    write("privacy", shell("privacy", "Privacy Page Study", vv, SWITCH_CSS + TERMS_CSS + PRIV_CSS, SWITCH_JS).replace('<header class="pt">', bar + '<header class="pt">', 1))
    bar, vv = switch("Contact page", [("Ask a question", c1), ("Directory", c2), ("Masthead beside", c3), ("Current", cur("contact"))])
    write("contact", shell("contact", "Contact Page Studies", vv, SWITCH_CSS + CON_CSS, SWITCH_JS + CON_JS).replace('<header class="pt">', bar + '<header class="pt">', 1))
    print("ok")
