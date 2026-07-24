#!/usr/bin/env python3
"""
audit.py — Coleta determinística de fatores SEO mensuráveis.

Uso:
    python3 audit.py https://exemplo.com.br [--pages 8] [--output audit.json]

Busca a URL informada, amostra páginas internas e coleta fatores técnicos
de SEO. Gera JSON para ser interpretado e pontuado pela skill.
Usa apenas a biblioteca padrão do Python (sem dependências).
"""

import argparse
import json
import re
import sys
import time
import gzip
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

UA = "Mozilla/5.0 (compatible; SEORankAudit/1.0; +https://github.com/)"
TIMEOUT = 20


def fetch(url):
    """Retorna (status, html, elapsed_s, final_url, headers) ou (erro, None, ...)."""
    req = Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
    start = time.time()
    try:
        with urlopen(req, timeout=TIMEOUT) as resp:
            raw = resp.read()
            size = len(raw)  # bytes transferidos (comprimidos, se gzip)
            if resp.headers.get("Content-Encoding") == "gzip":
                raw = gzip.decompress(raw)
            elapsed = round(time.time() - start, 2)
            charset = resp.headers.get_content_charset() or "utf-8"
            html = raw.decode(charset, errors="replace")
            return resp.status, html, elapsed, resp.url, dict(resp.headers), size
    except HTTPError as e:
        return e.code, None, round(time.time() - start, 2), url, {}, 0
    except (URLError, Exception) as e:
        return f"erro: {e}", None, round(time.time() - start, 2), url, {}, 0


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self._in_title = False
        self.meta = {}
        self.headings = {"h1": [], "h2": [], "h3": []}
        self._in_heading = None
        self.canonical = None
        self.links = []
        self.images_total = 0
        self.images_no_alt = 0
        self.jsonld = []
        self._in_jsonld = False
        self._jsonld_buf = ""
        self.lang = None
        self.viewport = None
        self.og = {}
        self.hreflang = []
        self.text_parts = []
        self._skip_text = 0  # dentro de script/style

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            name = (a.get("name") or a.get("property") or "").lower()
            content = a.get("content", "")
            if name == "description":
                self.meta["description"] = content
            elif name == "robots":
                self.meta["robots"] = content
            elif name == "viewport":
                self.viewport = content
            elif name.startswith("og:"):
                self.og[name] = content
        elif tag == "link":
            rel = (a.get("rel") or "").lower()
            if rel == "canonical":
                self.canonical = a.get("href")
            if rel == "alternate" and a.get("hreflang"):
                self.hreflang.append(a.get("hreflang"))
        elif tag in ("h1", "h2", "h3"):
            self._in_heading = tag
            self.headings[tag].append("")
        elif tag == "a" and a.get("href"):
            self.links.append((a.get("href"), a.get("rel", "")))
        elif tag == "img":
            self.images_total += 1
            if not (a.get("alt") or "").strip():
                self.images_no_alt += 1
        elif tag == "script":
            if (a.get("type") or "").lower() == "application/ld+json":
                self._in_jsonld = True
                self._jsonld_buf = ""
            self._skip_text += 1
        elif tag == "style":
            self._skip_text += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag in ("h1", "h2", "h3"):
            self._in_heading = None
        elif tag in ("script", "style"):
            if self._skip_text > 0:
                self._skip_text -= 1
            if tag == "script" and self._in_jsonld:
                self._in_jsonld = False
                try:
                    data = json.loads(self._jsonld_buf)
                    items = data if isinstance(data, list) else [data]
                    for item in items:
                        t = item.get("@type") if isinstance(item, dict) else None
                        if t:
                            self.jsonld.append(t if isinstance(t, str) else str(t))
                except Exception:
                    self.jsonld.append("(JSON-LD inválido)")

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_heading:
            self.headings[self._in_heading][-1] += data.strip()
        if self._in_jsonld:
            self._jsonld_buf += data
        if self._skip_text == 0:
            self.text_parts.append(data)


def analyze_page(url, base_netloc):
    status, html, elapsed, final_url, headers, size = fetch(url)
    page = {"url": url, "status": status, "response_time_s": elapsed,
            "transfer_size_kb": round(size / 1024, 1)}
    if not html:
        page["error"] = str(status)
        return page, []

    p = PageParser()
    try:
        p.feed(html)
    except Exception as e:
        page["parse_error"] = str(e)

    text = " ".join(" ".join(p.text_parts).split())
    words = len(text.split())

    internal, external = [], 0
    rel_counts = {"nofollow": 0, "sponsored": 0, "ugc": 0}
    for href, rel in p.links:
        absu = urljoin(final_url, href)
        parsed = urlparse(absu)
        if parsed.scheme not in ("http", "https"):
            continue
        relset = (rel or "").lower().split()
        for r in rel_counts:
            if r in relset:
                rel_counts[r] += 1
        if parsed.netloc == base_netloc:
            internal.append(absu.split("#")[0])
        else:
            external += 1

    title = p.title.strip()
    desc = p.meta.get("description", "")
    page.update({
        "https": urlparse(final_url).scheme == "https",
        "redirected_to": final_url if final_url != url else None,
        "title": title,
        "title_length": len(title),
        "meta_description": desc,
        "meta_description_length": len(desc),
        "meta_robots": p.meta.get("robots"),
        "canonical": p.canonical,
        "lang": p.lang,
        "viewport": p.viewport,
        "h1_count": len([h for h in p.headings["h1"] if h]),
        "h1": [h for h in p.headings["h1"] if h][:3],
        "h2_count": len(p.headings["h2"]),
        "h3_count": len(p.headings["h3"]),
        "word_count": words,
        "images_total": p.images_total,
        "images_no_alt": p.images_no_alt,
        "internal_links": len(internal),
        "external_links": external,
        "link_rel_counts": rel_counts,
        "mixed_content_refs": (len(re.findall(r'(?:src|href)=["\']http://', html))
                               if urlparse(final_url).scheme == "https" else 0),
        "jsonld_types": p.jsonld,
        "og_tags": list(p.og.keys()),
        "hreflang": p.hreflang,
        "cache_control": headers.get("Cache-Control"),
        "content_encoding_gzip": headers.get("Content-Encoding") == "gzip",
    })
    return page, internal


def check_infra(base):
    """robots.txt e sitemap."""
    infra = {}
    status, body, _, _, _, _ = fetch(urljoin(base, "/robots.txt"))
    infra["robots_txt"] = {"status": status, "exists": status == 200}
    sitemap_url = None
    if body:
        m = re.search(r"(?im)^sitemap:\s*(\S+)", body)
        if m:
            sitemap_url = m.group(1)
        infra["robots_txt"]["disallow_all"] = bool(
            re.search(r"(?im)^user-agent:\s*\*\s*[\r\n]+disallow:\s*/\s*$", body))
    if not sitemap_url:
        sitemap_url = urljoin(base, "/sitemap.xml")
    s_status, s_body, _, _, _, _ = fetch(sitemap_url)
    locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", s_body) if s_body else []
    lastmods = re.findall(r"<lastmod>\s*([^<\s]+)\s*</lastmod>", s_body) if s_body else []
    infra["sitemap"] = {"url": sitemap_url, "status": s_status,
                        "exists": s_status == 200,
                        "url_count": len(locs),
                        "lastmod_count": len(lastmods),
                        "latest_lastmod": max(lastmods) if lastmods else None}
    return infra, locs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--pages", type=int, default=8,
                    help="máximo de páginas internas a amostrar (padrão 8)")
    ap.add_argument("--output", default="audit.json")
    args = ap.parse_args()

    start_url = args.url if args.url.startswith("http") else "https://" + args.url
    base_netloc = urlparse(start_url).netloc
    base = f"{urlparse(start_url).scheme}://{base_netloc}"

    print(f"Analisando {start_url} ...", file=sys.stderr)
    infra, sitemap_urls = check_infra(base)
    home, internal_links = analyze_page(start_url, base_netloc)
    if str(home.get("status")) == "403":
        print("AVISO: 403 — o site pode estar bloqueando bots (WAF/Cloudflare). "
              "Siga o fallback descrito no SKILL.md.", file=sys.stderr)

    # Amostra de páginas internas: únicas, sem a própria home, distribuídas
    seen, sample = {start_url, start_url.rstrip("/")}, []
    for link in internal_links:
        if link not in seen and not re.search(r"\.(jpg|png|gif|css|js|pdf|xml|ico|svg|webp)$", link, re.I):
            seen.add(link)
            sample.append(link)
    step = max(1, len(sample) // args.pages) if sample else 1
    sample = sample[::step][:args.pages]
    # Complementa com URLs do sitemap se a home rendeu poucos links
    for u in sitemap_urls:
        if len(sample) >= args.pages:
            break
        if urlparse(u).netloc == base_netloc and u not in seen:
            seen.add(u)
            sample.append(u)

    pages = []
    for u in sample:
        print(f"  → {u}", file=sys.stderr)
        pg, _ = analyze_page(u, base_netloc)
        pages.append(pg)

    all_pages = [home] + pages
    titles = [pg.get("title") for pg in all_pages if pg.get("title")]
    descs = [pg.get("meta_description") for pg in all_pages if pg.get("meta_description")]
    dup = lambda xs: sorted({x for x in xs if xs.count(x) > 1})
    result = {
        "site": base,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "infra": infra,
        "homepage": home,
        "sampled_pages": pages,
        "sample_size": len(pages),
        "summary": {
            "duplicate_titles": dup(titles),
            "duplicate_meta_descriptions": dup(descs),
        },
    }
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"OK — resultado salvo em {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
