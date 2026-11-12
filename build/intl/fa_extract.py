import pymupdf,unicodedata,re,json,sys
MARKS=set('ًٌٍَُِّْٰٔ')
d=pymupdf.open('src/mag.pdf')
def fix_word(chars):
    # chars: list of (c,x0,x1). 1) lam-alef: zero-width alef followed by lam -> 'لا'
    out=[];i=0
    while i<len(chars):
        c,x0,x1=chars[i]
        if c=='ا' and abs(x1-x0)<0.05 and i+1<len(chars) and chars[i+1][0]=='ل':
            out.append(['ل',[]]);out.append(['ا',[]]);i+=2;continue
        if c in MARKS:
            if out: out[-1][1].append(c)
            i+=1;continue
        out.append([c,[]]);i+=1
    # 2) marks copied from the next letter: remove next letter's true marks from this letter's marks
    nxt=[]
    for k in range(len(out)-1,-1,-1):
        m=list(out[k][1])
        for x in nxt:
            if x in m: m.remove(x)
        out[k][1]=m;nxt=m
    return ''.join(c+''.join(m) for c,m in out)
def line_text(line):
    chars=[(c['c'],c['bbox'][0],c['bbox'][2]) for s in line['spans'] for c in s['chars']]
    words=[];cur=[]
    for ch in chars:
        if ch[0]==' ':
            if cur: words.append(fix_word(cur));cur=[]
            words.append(' ')
        else: cur.append(ch)
    if cur: words.append(fix_word(cur))
    return unicodedata.normalize('NFC',''.join(words))
def blocks(pages):
    out=[]
    for pn in pages:
        pg=d[pn-1];bs=[]
        for b in pg.get_text('rawdict')['blocks']:
            if 'lines' not in b: continue
            t='\n'.join(line_text(l) for l in b['lines'])
            if len(re.findall(r'[؀-ۿ]',t))<3: continue
            bs.append([b['bbox'][0],b['bbox'][1],b['bbox'][2],b['bbox'][3],t])
        cols=[]
        for b in sorted(bs,key=lambda b:-b[2]):
            for c in cols:
                if abs(c[0]-b[2])<30: c[1].append(b);break
            else: cols.append([b[2],[b]])
        cols.sort(key=lambda c:-c[0])
        for c in cols:
            for b in sorted(c[1],key=lambda b:b[1]): out.append((pn,round(b[2]),round(b[1]),b[4]))
    return out
B=blocks(range(36,42))
json.dump(B,open('intl/fa_blocks.json','w'),ensure_ascii=False,indent=0)
for i,(pn,x,y,t) in enumerate(B): print(i,pn,x,y,'|',t.replace('\n',' ')[:90],'…',t.replace('\n',' ')[-30:])
