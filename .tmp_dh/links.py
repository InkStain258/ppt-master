import re, sys, urllib.request, gzip, ssl
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
url = sys.argv[1]
pat = sys.argv[2] if len(sys.argv) > 2 else r"\.pdf"
req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
try:
    r = urllib.request.urlopen(req, timeout=40)
except Exception as e:
    if "CERTIFICATE_VERIFY_FAILED" not in str(e):
        raise
    ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
    r = urllib.request.urlopen(req, timeout=40, context=ctx)
with r:
    d = r.read()
    if r.headers.get("Content-Encoding") == "gzip":
        d = gzip.decompress(d)
h = d.decode("utf-8", "replace")
for m in sorted(set(re.findall(r'href="([^"]*' + pat + r'[^"]*)"', h))):
    print(m)
