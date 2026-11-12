import json, importlib, sys, os
sys.path.insert(0, os.path.dirname(__file__))
segs = json.load(open("segs.json"))
FD = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
for lg in ("zh", "fa"):
    M = {}
    for i in range(12):
        t = importlib.import_module(f"t{i:02d}")
        for k, v in getattr(t, lg.upper()).items():
            pass
            M[segs[k]] = v
    miss = [i for i, s in enumerate(segs) if s not in M]
    print(lg, len(M), "missing", miss[:20], len(miss))
    json.dump(M, open(f"{lg}_map.json", "w"), ensure_ascii=False, indent=0)
