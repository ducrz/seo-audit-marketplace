# SEO Rank Audit

Skill open source para Claude Code que audita um site e atribui **notas de 0 a
100 por critério, separadas para Google e Bing**, com relatório priorizado de
correções.

📄 **Documentação completa:** https://www.cupomdescontos.com/ferramentas/auditoria-seo

## Instalação

```
/plugin marketplace add ducrz/seo-audit-marketplace
/plugin install seo-rank-audit
```

## Uso

```
audita o exemplo.com.br
por que essa página não ranqueia no Bing?
```

## O que coleta

- **Estrutura** — titles, metas, headings, canonical, schema, robots, sitemap,
  HTTPS, alt, links internos e atributos de link patrocinado (home + 5-10
  páginas internas)
- **Velocidade** — Core Web Vitals reais via API pública do PageSpeed Insights
  (sem chave, sem cadastro)
- **Bing Webmaster** *(opcional)* — tráfego, rastreamento e backlinks, para
  sites verificados na conta do próprio usuário

## Princípio

As notas refletem fatores **documentados** por Google e Bing, não o algoritmo
real. O que não pode ser medido é marcado como não verificado e sai da base de
cálculo — nunca vira chute nem zero.

## Licença

MIT — mantido por [Eduardo Monteiro](https://www.cupomdescontos.com/sobre),
que também toca o [CupomDescontos](https://www.cupomdescontos.com/). Construí
esta ferramenta para auditar meus próprios sites e resolvi abrir o código.
