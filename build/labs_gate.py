"""Password gate for pages published to the labs repo: the page body is encrypted (AES-GCM, key from PBKDF2-SHA256)
and opened in the browser with the shared password. The password is read from .labs_pw beside this file, never stored in source."""
import os, re, json, base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
ITER = 310000

def _pw():
    return open(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".labs_pw")).read().strip()

def seal(text):
    salt, iv = os.urandom(16), os.urandom(12)
    key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER).derive(_pw().encode())
    b = lambda x: base64.b64encode(x).decode()
    return json.dumps({"s": b(salt), "i": b(iv), "c": b(AESGCM(key).encrypt(iv, text.encode(), None)), "n": ITER})

CSS = """.lg{min-height:100vh;min-height:100dvh;display:grid;place-items:center;padding:24px max(16px,env(safe-area-inset-left,0px)) 24px max(16px,env(safe-area-inset-right,0px));background:#f5f1e8;color:#1d1a16}
.lg form{width:100%;max-width:420px;background:#fdfcf9;border:1px solid #d9d2c4;border-radius:14px;padding:32px;display:flex;flex-direction:column;gap:14px;font-family:"Bricolage Grotesque","Helvetica Neue",Arial,sans-serif}
.lg .k{margin:0;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#6a635a}.lg h1{margin:4px 0 6px;font:800 34px/1 "Bricolage Grotesque","Helvetica Neue",Arial,sans-serif;letter-spacing:-.03em}
.lg label{font-weight:600;font-size:14px}.lg input{font:16px inherit;font-family:inherit;min-height:48px;border-radius:10px;border:1.5px solid #d9d2c4;background:#f5f1e8;color:#1d1a16;padding:0 14px;width:100%;box-sizing:border-box}
.lg input:focus-visible,.lg button:focus-visible{outline:2px solid #1b5e6b;outline-offset:2px}.lg button{min-height:48px;border-radius:999px;border:0;background:#1d1a16;color:#fdfcf9;font:700 15px inherit;font-family:inherit;cursor:pointer}
.lg .err{margin:0;font-size:14px;color:#8a3a1e;min-height:1.2em}"""

JS = r"""var G=document.querySelector('.lg'),Fm=G.querySelector('form'),In=G.querySelector('input'),Er=G.querySelector('.err'),Bt=G.querySelector('button');
function b64(s){var b=atob(s),a=new Uint8Array(b.length);for(var i=0;i<b.length;i++)a[i]=b.charCodeAt(i);return a}
function open_(pw){return crypto.subtle.importKey('raw',new TextEncoder().encode(pw),'PBKDF2',false,['deriveKey']).then(function(k){
 return crypto.subtle.deriveKey({name:'PBKDF2',salt:b64(P.s),iterations:P.n,hash:'SHA-256'},k,{name:'AES-GCM',length:256},false,['decrypt'])}).then(function(key){
 return crypto.subtle.decrypt({name:'AES-GCM',iv:b64(P.i)},key,b64(P.c))}).then(function(buf){return new TextDecoder().decode(buf)})}
function show(h,pw){try{sessionStorage.setItem('labs-pw',pw)}catch(e){}var m=document.getElementById('lg-main');m.innerHTML=h;G.remove();m.hidden=false;
 if(location.hash){var t=document.getElementById(location.hash.slice(1));t&&t.scrollIntoView()}}
Fm.onsubmit=function(e){e.preventDefault();Er.textContent='';Bt.disabled=true;var pw=In.value;
 open_(pw).then(function(h){show(h,pw)}).catch(function(){Er.textContent='That password did not work. Try again.';Bt.disabled=false;In.select()})};
var saved=null;try{saved=sessionStorage.getItem('labs-pw')}catch(e){}
if(saved)open_(saved).then(function(h){show(h,saved)}).catch(function(){In.focus()});else In.focus();"""

def gate(page, title, kicker="The American Bahá’í"):
    """Encrypt everything inside <body>; scripts in it are not run, so gate only pages whose body needs none."""
    head, rest = page.split("<body>", 1)
    body = rest.rsplit("</body>", 1)[0]
    assert "<script" not in body, "gated body must hold no scripts"
    ui = (f'<div class="lg"><form><p class="k">{kicker}</p><h1>{title}</h1><label for="lg-pw">Password</label>'
          f'<input id="lg-pw" type="password" autocomplete="current-password" required><p class="err" role="alert"></p>'
          f'<button type="submit">Open</button></form></div><noscript><p style="padding:24px">This page needs JavaScript to open.</p></noscript><div id="lg-main" hidden></div>')
    return head.replace("</head>", f"<style>{CSS}</style></head>", 1) + f"<body>{ui}<script>(function(){{var P={seal(body)};{JS}}})();</script></body>" + rest.rsplit("</body>", 1)[1]
