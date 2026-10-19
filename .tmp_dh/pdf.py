import sys, re, urllib.request, gzip, ssl, fitz
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

def dl(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
    try:
        r = urllib.request.urlopen(req, timeout=90)
    except Exception as e:
        if "CERTIFICATE_VERIFY_FAILED" not in str(e):
            raise
        ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
        r = urllib.request.urlopen(req, timeout=90, context=ctx)
    with r:
        d = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            d = gzip.decompress(d)
        return d

url = sys.argv[1]
mode = sys.argv[2] if len(sys.argv) > 2 else "head"
arg = sys.argv[3] if len(sys.argv) > 3 else "6000"
path = "doc.pdf"
open(path, "wb").write(dl(url))
doc = fitz.open(path)
pages = [p.get_text() for p in doc]
txt = "\n".join(pages)
txt = re.sub(r"[ \t]+", " ", txt)
print("PAGES:", len(pages), "CHARS:", len(txt), "URL:", url)
if mode == "head":
    print(txt[: int(arg)])
else:
    ctx = int(sys.argv[4]) if len(sys.argv) > 4 else 400
    n = 0
    for m in re.finditer(arg, txt, re.I):
        print("---")
        print(txt[max(0, m.start() - ctx): m.end() + ctx].replace("\n", " "))
        n += 1
        if n >= 10:
            break
    if not n:
        print("NO MATCH", arg)
