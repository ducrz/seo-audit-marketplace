# Critérios Bing — pesos e pontuação

Baseado nas Bing Webmaster Guidelines. O Bing difere do Google em pontos
relevantes: dá mais peso a correspondência exata de palavras-chave, sinais
explícitos on-page, autoridade de domínio estabelecida e adoção do IndexNow.

Nota final Bing = soma ponderada das 5 categorias (0–100).

## 1. Relevância e correspondência — peso 25

O Bing é mais literal que o Google:
- Palavra-chave exata no `title`, `h1` e URL pesa mais (10 pts)
- `meta_description` com o termo-alvo (5 pts)
- Termo presente nos primeiros parágrafos do conteúdo (5 pts)
- URLs curtas, legíveis, com hífens (5 pts)

## 2. Qualidade e credibilidade — peso 25

- Autoridade percebida: quem publica, credenciais visíveis, site "sobre" e
  contato claros (10 pts)
- Conteúdo completo e sem clickbait; o Bing pune títulos que prometem o que a
  página não entrega (8 pts)
- Transparência de monetização (afiliados sinalizados) (7 pts)

## 3. Frescor — peso 15

- Datas de publicação/atualização visíveis e recentes onde faz sentido
  (cupons e ofertas são conteúdo perecível — datas desatualizadas em páginas
  de oferta são penalidade forte aqui) (10 pts)
- Sitemap com `lastmod` (`infra.sitemap.lastmod_count` > 0) e `latest_lastmod`
  recente (5 pts)

## 4. Velocidade e experiência — peso 15

- CWV reais do pagespeed.py quando disponíveis; senão `response_time_s` e
  `transfer_size_kb` (mesmos limiares do google.md) (10 pts)
- `https`, `viewport`, sem interstitiais agressivos (5 pts)

## 5. Técnica — peso 20

- `robots_txt` e `sitemap` válidos (5 pts)
- Dados estruturados: o Bing lê JSON-LD e também microdata/RDFa (5 pts)
- Uso de IndexNow (verifique se há chave em /indexnow ou pergunte ao usuário;
  se não der para verificar, marque "não verificado" e recomende — é
  diferencial forte de indexação no Bing) (5 pts)
- Bing Webmaster Tools configurado — verificável via bing_wmt.py quando o
  usuário fornece a chave (site próprio); senão pergunte (5 pts)

Quando o bing_wmt.py rodou com sucesso, use os problemas de crawl
reportados pelo próprio Bingbot como evidência primária da Técnica — eles
valem mais que qualquer inferência externa.

## Como reportar

Mesma regra do google.md: nota + evidência + correção prioritária por
categoria. Destaque no relatório as divergências Google vs Bing — ex.: uma
página pode pontuar bem no Google (conteúdo profundo) e mal no Bing (sem
palavra-chave exata no title, sem IndexNow).
