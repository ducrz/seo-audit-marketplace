# Critérios Google — pesos e pontuação

Baseado em fatores documentados publicamente pelo Google (Search Central, Helpful
Content, Search Quality Rater Guidelines). Não é o algoritmo real — é uma
aproximação auditável dos sinais confirmados.

Nota final Google = soma ponderada das 6 categorias (0–100).

## 1. Conteúdo útil e E-E-A-T — peso 25

Avaliação qualitativa (leia 2–3 páginas amostradas na íntegra):
- O conteúdo responde à intenção de busca ou só existe para ranquear? (10 pts)
- Sinais de experiência/expertise: autor identificado, informação original,
  profundidade além do óbvio, dados próprios (8 pts)
- Confiabilidade: página "sobre", contato, política de privacidade, ausência de
  claims exagerados, transparência sobre afiliados/publicidade (7 pts)

Penalize com força: conteúdo raso duplicado entre páginas, texto claramente
gerado em massa sem revisão, páginas doorway, excesso de anúncios acima da dobra.

## 2. Relevância on-page — peso 20

Do JSON do audit.py:
- `title`: único por página, 30–60 caracteres, palavra-chave no início (5 pts)
- `meta_description`: presente, 70–160 caracteres, com proposta de valor (3 pts)
- `h1_count` == 1 por página, coerente com o title (4 pts)
- Hierarquia h2/h3 presente e lógica (3 pts)
- `word_count`: adequado à intenção (páginas de conteúdo < 300 palavras são
  sinal fraco; não premie volume vazio) (5 pts)

## 3. Experiência de página — peso 15

Prioridade 1 — dados do pagespeed.py (CWV reais): CrUX p75 com LCP < 2,5s,
CLS < 0,1 e INP < 200ms = pontuação cheia; categoria AVERAGE = metade; SLOW =
zero nos 10 pts de velocidade. Sem CrUX, use a nota Lighthouse (>=90 ótimo,
50–89 parcial) e declare que é laboratório.

Prioridade 2 — só se o PSI falhar, proxies do audit.py (declare como proxies):
- `response_time_s`: < 0,8s ótimo; 0,8–2s aceitável; > 2s ruim (6 pts)
- `transfer_size_kb` (bytes transferidos): < 500 KB ótimo; 500–1500 aceitável; > 1500 ruim (4 pts)
- `content_encoding_gzip` e `cache_control` presentes (3 pts)
- `https` em todas as páginas, sem cadeias de redirect e sem mixed content
  (`mixed_content_refs` == 0) (2 pts)



## 4. Mobile — peso 10

- `viewport` presente em todas as páginas (6 pts)
- Sem indícios de conteúdo dependente de hover/Flash/larguras fixas (4 pts —
  avalie pelo HTML se necessário)

## 5. Técnica e rastreabilidade — peso 15

- `robots_txt.exists` e sem `disallow_all` (3 pts)
- `sitemap.exists` com `url_count` > 0 (3 pts)
- `canonical` presente e autorreferente nas páginas amostradas (3 pts)
- `meta_robots` sem noindex acidental (2 pts)
- `jsonld_types`: dados estruturados relevantes (Article, Product, Offer,
  FAQPage, BreadcrumbList...) (4 pts)

## 6. Links — peso 15

- `internal_links`: páginas importantes alcançáveis, âncoras descritivas,
  10–100 links internos/página é saudável (7 pts)
- `external_links` para fontes confiáveis quando faz sentido (3 pts)
- Links de afiliado com `nofollow`/`sponsored`/`ugc` (verifique
  `link_rel_counts`) (5 pts)

## Como reportar

Para cada categoria: nota, evidência concreta (cite a página e o dado), e a
correção com maior impacto. Não invente dados que o audit.py não coletou —
marque como "não verificado" o que não puder medir (backlinks externos,
Core Web Vitals reais, histórico de penalidades).
