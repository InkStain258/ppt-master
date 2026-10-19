import sys, json, urllib.request, urllib.parse, ssl
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
def get(title, lang="en"):
    q = urllib.parse.urlencode({"action":"query","prop":"extracts","explaintext":"1","redirects":"1","format":"json","titles":title})
    url = f"https://{lang}.wikipedia.org/w/api.php?{q}"
    req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
    try:
        d = json.loads(urllib.request.urlopen(req, timeout=60, context=ctx).read().decode("utf-8"))
    except Exception as e:
        return f"ERR {e}"
    pages = d.get("query",{}).get("pages",{})
    for k,v in pages.items():
        return v.get("extract") or f"(no extract; missing={v.get('missing')})"
    return "(none)"
args = sys.argv[1:]
lang = "en"
if args and args[0].startswith("lang="):
    lang = args[0][5:]; args = args[1:]
mode = "head"; n = 1500; pats=[]
if args and args[0] in ("head","grep"):
    mode = args[0]; args = args[1:]
    if mode=="head" and args and args[0].isdigit():
        n = int(args[0]); args = args[1:]
    if mode=="grep":
        pats = args.pop(0).split("|")
        n = int(args[0]) if args and args[0].isdigit() else 200
        if args and args[0].isdigit(): args=args[1:]
for t in args:
    txt = get(t, lang)
    print(f"\n##### {t} ({lang}) len={len(txt)}")
    if mode=="head":
        print(txt[:n])
    else:
        import re
        sents = re.split(r"(?<=[.!?])\s+", txt)
        hits = [s for s in sents if any(re.search(p, s, re.I) for p in pats)]
        for s in hits[:n]:
            print("-", s.strip()[:400])
