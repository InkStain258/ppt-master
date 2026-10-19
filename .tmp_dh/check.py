import sys, urllib.request, gzip
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
for url in sys.argv[1:]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
        with urllib.request.urlopen(req, timeout=25) as r:
            d = r.read()
            enc = r.headers.get("Content-Encoding")
            if enc == "gzip":
                d = gzip.decompress(d)
            print("OK", r.status, len(d), url)
    except Exception as e:
        print("FAIL", url, type(e).__name__, e)
