#!/usr/bin/env python3
"""
bing_wmt.py — Dados do Bing Webmaster Tools via API oficial (sites próprios).

Uso:
    python3 bing_wmt.py https://seusite.com --key SUA_CHAVE [--output bing.json]

A chave sai do Bing Webmaster Tools: Configurações → Acesso de API.
Só funciona para sites VERIFICADOS na sua conta — não audita sites de
terceiros. Se um método falhar, o erro fica registrado no JSON e os demais
continuam (nem toda conta tem todos os métodos liberados).

Coleta: tráfego de busca (impressões/cliques), estatísticas de crawl,
problemas de crawl, contagem de backlinks e cota do URL Submission.
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

BASE = "https://ssl.bing.com/webmaster/api.svc/json/"

METHODS = [
    ("GetRankAndTrafficStats", "trafego_busca"),
    ("GetCrawlStats", "crawl_stats"),
    ("GetCrawlIssues", "problemas_crawl"),
    ("GetLinkCounts", "backlinks"),
    ("GetUrlSubmissionQuota", "cota_submissao"),
]


def call(method, site, key):
    qs = urllib.parse.urlencode({"apikey": key, "siteUrl": site})
    req = urllib.request.Request(BASE + method + "?" + qs,
                                 headers={"User-Agent": "SEORankAudit/1.3"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.load(resp)
    return data.get("d", data)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("site")
    ap.add_argument("--key", default=os.environ.get("BING_WMT_KEY"),
                    help="chave da API (ou variável BING_WMT_KEY)")
    ap.add_argument("--output", default="bing.json")
    args = ap.parse_args()

    if not args.key:
        sys.exit("Erro: informe --key ou defina BING_WMT_KEY. "
                 "A chave está em Bing Webmaster Tools → Configurações → Acesso de API.")

    site = args.site if args.site.startswith("http") else "https://" + args.site
    result = {"site": site, "fonte": "Bing Webmaster API"}

    for method, label in METHODS:
        print(f"  → {method} ...", file=sys.stderr)
        try:
            result[label] = call(method, site, args.key)
        except Exception as e:
            result[label] = {"erro": str(e)}
            print(f"    falhou: {e}", file=sys.stderr)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"OK — resultado salvo em {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
