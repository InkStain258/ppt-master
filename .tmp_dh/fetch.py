import sys, re, urllib.request, gzip, ssl
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

def get(url, timeout=45):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip", "Accept-Language": "en,zh;q=0.8"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
            if r.headers.get("Content-Encoding") == "gzip":
                data = gzip.decompress(data)
            return data, r.geturl(), r.status
    except Exception as e:
        if "CERTIFICATE_VERIFY_FAILED" not in str(e):
            raise
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            data = r.read()
            if r.headers.get("Content-Encoding") == "gzip":
                data = gzip.decompress(data)
            return data, r.geturl(), r.status

def to_text(html):
    import html as h
    html = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", html)
    html = re.sub(r"(?is)<!--.*?-->", " ", html)
    html = re.sub(r"(?i)</(p|div|li|h[1-6]|tr|section|article)>", "\n", html)
    html = re.sub(r"(?i)<br\s*/?>", "\n", html)
    html = re.sub(r"(?s)<[^>]+>", " ", html)
    html = h.unescape(html)
    html = re.sub(r"[ \t\r\f\v]+", " ", html)
    html = re.sub(r"\n\s*\n+", "\n", html)
    return html.strip()

def main():
    mode, url = sys.argv[1], sys.argv[2]
    try:
        data, final, status = get(url)
    except Exception as e:
        print("ERROR", url, e); return
    raw = data.decode("utf-8", "replace")
    txt = to_text(raw)
    print("URL:", final, "STATUS:", status, "CHARS:", len(txt))
    if mode == "get":
        n = int(sys.argv[3]) if len(sys.argv) > 3 else 12000
        print(txt[:n])
    elif mode == "grep":
        pat = sys.argv[3]
        ctx = int(sys.argv[4]) if len(sys.argv) > 4 else 300
        seen = 0
        for m in re.finditer(pat, txt, re.I):
            print("---")
            print(txt[max(0, m.start()-ctx):m.end()+ctx].replace("\n", " "))
            seen += 1
            if seen >= 10: break
        if not seen: print("NO MATCH", pat)
    elif mode == "raw":
        open(sys.argv[3], "wb").write(data); print("SAVED", sys.argv[3])

if __name__ == "__main__":
    main()
