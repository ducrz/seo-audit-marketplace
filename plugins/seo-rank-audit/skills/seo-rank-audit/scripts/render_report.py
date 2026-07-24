#!/usr/bin/env python3
"""
render_report.py — Injeta os dados da auditoria no template e gera o HTML final.

Uso:
    python3 render_report.py --data relatorio.json --output auditoria-site.html

O JSON segue o esquema abaixo. Só `site`, `generated_at`, `sample_size`,
`engines` e `overall` são obrigatórios; o resto é opcional e some do relatório
quando ausente.

{
  "site": "exemplo.com.br",
  "generated_at": "2026-07-24",
  "sample_size": 8,
  "collection_note": "texto se a coleta foi parcial, senão null",
  "engines": {
    "google": {"total": 73, "categories": [
        {"name": "Conteúdo e E-E-A-T", "score": 19, "max": 25},
        {"name": "Backlinks", "verified": false}
    ]},
    "bing": {"total": 78, "categories": [...]}
  },
  "overall": 76,
  "renormalized_note": "X pts saíram da base por não serem verificáveis.",
  "divergences": "parágrafo",
  "strengths": "parágrafo",
  "priorities": [{"title": "...", "impact": "alto", "detail": "..."}],
  "details": [{"category": "...", "evidence": "...", "fix": "..."}],
  "unverified": ["item — como checar"]
}
"""

import argparse
import json
import os
import sys

START = "/*__DATA_START__*/"
END = "/*__DATA_END__*/"
REQUIRED = ["site", "generated_at", "sample_size", "engines", "overall"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="JSON com os dados da auditoria")
    ap.add_argument("--output", required=True, help="caminho do HTML final")
    ap.add_argument("--template", default=None,
                    help="padrão: assets/report-template.html ao lado deste script")
    args = ap.parse_args()

    tpl_path = args.template or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "assets", "report-template.html")

    with open(args.data, encoding="utf-8") as f:
        data = json.load(f)

    missing = [k for k in REQUIRED if k not in data]
    if missing:
        sys.exit(f"Erro: faltam campos obrigatórios no JSON: {', '.join(missing)}")

    with open(tpl_path, encoding="utf-8") as f:
        tpl = f.read()

    if START not in tpl or END not in tpl:
        sys.exit("Erro: template sem os marcadores de dados.")

    head, rest = tpl.split(START, 1)
    _, tail = rest.split(END, 1)

    payload = json.dumps(data, ensure_ascii=False, indent=2)
    # </script> dentro de string quebraria o bloco <script> do template
    payload = payload.replace("</", "<\\/")

    html = f"{head}{START}\nconst DATA = {payload};\n{END}{tail}"

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"OK — relatório gerado em {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
