🌐 [English](README.md) · [Português](README.pt-BR.md) · [Español](README.es.md) · [Français](README.fr.md) · [中文](README.zh-CN.md)

# SEO Rank Audit

Skill open source pour Claude Code qui audite un site et attribue des
**notes de 0 à 100 par critère, distinctes pour Google et Bing**, avec un
rapport de corrections priorisé.

📄 **Documentation complète :** https://www.cupomdescontos.com/ferramentas/auditoria-seo

## Installation

```
/plugin marketplace add ducrz/seo-audit-marketplace
/plugin install seo-rank-audit
```

## Utilisation

```
audite exemple.com
pourquoi cette page ne se positionne pas sur Bing ?
```

## Ce qu'elle analyse

- **Structure** — titles, balises meta, headings, canonical, schema, robots,
  sitemap, HTTPS, alt, liens internes et attributs de lien sponsorisé (page
  d'accueil + 5-10 pages internes)
- **Vitesse** — Core Web Vitals réels via l'API publique PageSpeed Insights
  (sans clé, sans inscription)
- **Bing Webmaster** *(optionnel)* — trafic, exploration et backlinks, pour
  les sites vérifiés sur le compte de l'utilisateur

## Principe

Les notes reflètent des facteurs **documentés** par Google et Bing, pas
l'algorithme réel. Ce qui ne peut pas être mesuré est marqué comme non
vérifié et retiré de la base de calcul — jamais transformé en supposition ni
en zéro.

## Licence

MIT — maintenu par [Eduardo Monteiro](https://www.cupomdescontos.com/sobre),
qui gère aussi [CupomDescontos](https://www.cupomdescontos.com/). J'ai
construit cet outil pour auditer mes propres sites et j'ai décidé d'en ouvrir
le code.
