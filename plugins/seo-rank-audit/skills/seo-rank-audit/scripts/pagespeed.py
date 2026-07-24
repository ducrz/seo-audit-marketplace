#!/usr/bin/env python3
"""
pagespeed.py — Core Web Vitals reais via API do PageSpeed Insights (gratuita).

Uso:
    python3 pagespeed.py https://exemplo.com.br [--strategy mobile|desktop|both]
                         [--key CHAVE_API] [--output pagespeed.json]

Funciona SEM chave (padrão). A cota sem chave é limitada por IP; este
script pausa entre chamadas para respeitá-la. Se a cota estourar, o erro
orienta as alternativas (aguardar, Lighthouse local ou chave opcional).

Retorna, por estratégia:
- Nota de performance do Lighthouse (0-100) — dado de laboratório
- LCP, CLS, INP e FCP do CrUX — dados reais de usuários (quando o site
  tem tráfego suficiente para aparecer no CrUX)
"""

import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from urllib.error import HTTPError

API = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"


def _is_quota_error(http_error):
    """Distingue cota da API sem chave estourada de outro motivo pro 403/429
    (ex: bloqueio de rede/proxy/firewall) — checa o corpo JSON do erro em vez
    de assumir cota sempre que o código HTTP é 403."""
    try:
        body = http_error.read().decode("utf-8", errors="replace")
        data = json.loads(body)
        status = (data.get("error", {}) or {}).get("status", "")
        message = (data.get("error", {}) or {}).get("message", "")
        text = f"{status} {message}".lower()
        return "resource_exhausted" in text or "quota" in text or "rate limit" in text
    except Exception:
        # corpo não é o JSON de erro esperado da API do Google (ex: página
        # HTML de um proxy/firewall) — não é cota, é outra coisa.
        return False


def run(url, strategy, key):
    params = {"url": url, "strategy": strategy,
              "category": "performance"}
    if key:
        params["key"] = key
    full = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(full, headers={"User-Agent": "SEORankAudit/1.1"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.load(resp)

    out = {"strategy": strategy}
    lh = data.get("lighthouseResult", {})
    perf = lh.get("categories", {}).get("performance", {}).get("score")
    out["lighthouse_performance"] = round(perf * 100) if perf is not None else None

    audits = lh.get("audits", {})
    for k, label in [("largest-contentful-paint", "lab_lcp"),
                     ("cumulative-layout-shift", "lab_cls"),
                     ("total-blocking-time", "lab_tbt"),
                     ("first-contentful-paint", "lab_fcp"),
                     ("speed-index", "lab_speed_index")]:
        a = audits.get(k, {})
        out[label] = a.get("displayValue")

    # CrUX — dados reais de campo (28 dias); pode não existir p/ sites pequenos
    field = data.get("loadingExperience", {})
    metrics = field.get("metrics", {})
    crux = {}
    for k, label in [("LARGEST_CONTENTFUL_PAINT_MS", "lcp_ms"),
                     ("CUMULATIVE_LAYOUT_SHIFT_SCORE", "cls_x100"),
                     ("INTERACTION_TO_NEXT_PAINT", "inp_ms"),
                     ("FIRST_CONTENTFUL_PAINT_MS", "fcp_ms")]:
        m = metrics.get(k)
        if m:
            crux[label] = {"p75": m.get("percentile"),
                           "category": m.get("category")}  # FAST/AVERAGE/SLOW
    out["crux_field_data"] = crux or None
    out["crux_overall"] = field.get("overall_category")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--strategy", default="both",
                    choices=["mobile", "desktop", "both"])
    ap.add_argument("--key", default=os.environ.get("PSI_API_KEY"))
    ap.add_argument("--output", default="pagespeed.json")
    args = ap.parse_args()

    url = args.url if args.url.startswith("http") else "https://" + args.url
    strategies = ["mobile", "desktop"] if args.strategy == "both" else [args.strategy]

    results = {"url": url, "results": []}
    for i, strat in enumerate(strategies):
        if i > 0:
            time.sleep(3)  # respeita a cota sem chave
        print(f"PSI ({strat}) — pode levar ~30s ...", file=sys.stderr)
        try:
            results["results"].append(run(url, strat, args.key))
        except HTTPError as e:
            if e.code in (403, 429) and _is_quota_error(e):
                msg = ("cota da API sem chave estourada — alternativas: "
                       "(1) aguarde alguns minutos; "
                       "(2) rode Lighthouse local sem chave: "
                       "npx lighthouse URL --only-categories=performance --output=json; "
                       "(3) opcional: chave gratuita via PSI_API_KEY")
            elif e.code == 403:
                msg = (f"HTTP 403 da API do PageSpeed Insights, mas o corpo da resposta não "
                       f"indica cota estourada — provável bloqueio de rede/proxy/firewall "
                       f"entre esta máquina e a API do Google, não limite de uso. Confira a "
                       f"conexão (proxy, VPN, firewall corporativo) antes de esperar cota "
                       f"liberar. Detalhe: {e.reason}")
            else:
                msg = str(e)
            results["results"].append({"strategy": strat, "error": msg})
            print(f"  erro: {msg}", file=sys.stderr)
        except Exception as e:
            results["results"].append({"strategy": strat, "error": str(e)})
            print(f"  erro: {e}", file=sys.stderr)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"OK — resultado salvo em {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
