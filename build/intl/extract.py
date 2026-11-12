import pymupdf,unicodedata,re,sys,json
d=pymupdf.open('src/mag.pdf')
def blocks(pages,keep,rtl=False,skip=()):
    out=[]
    for pn in pages:
        pg=d[pn-1];bs=[]
        for b in pg.get_text('blocks'):
            x0,y0,x1,y1,t=b[:5];t=unicodedata.normalize('NFKC',t)
            if not keep(t) or any(s in t for s in skip): continue
            bs.append([x0,y0,x1,y1,t])
        # cluster columns by x0
        cols=[]
        for b in sorted(bs,key=lambda b:b[0]):
            for c in cols:
                if abs(c[0]-b[0])<30: c[1].append(b);break
            else: cols.append([b[0],[b]])
        cols.sort(key=lambda c:-c[0] if rtl else c[0])
        for c in cols:
            for b in sorted(c[1],key=lambda b:b[1]): out.append((pn,round(b[0]),round(b[1]),b[4]))
    return out
if __name__=='__main__':
    lang=sys.argv[1]
    if lang=='zh':
        B=blocks(range(26,31),lambda t:len(re.findall(r'[一-鿿]',t))>=2)
    else:
        B=blocks(range(36,42),lambda t:len(re.findall(r'[؀-ۿ]',t))>=3,rtl=True)
    json.dump(B,open(f'intl/{lang}_blocks.json','w'),ensure_ascii=False,indent=0)
    for i,(pn,x,y,t) in enumerate(B): print(i,pn,x,y,'|',t.replace('\n','')[:70],'…',t.replace('\n','')[-25:])
