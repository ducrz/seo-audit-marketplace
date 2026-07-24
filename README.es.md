🌐 [English](README.md) · [Português](README.pt-BR.md) · [Español](README.es.md) · [Français](README.fr.md) · [中文](README.zh-CN.md)

# SEO Rank Audit

Skill de código abierto para Claude Code que audita un sitio y asigna
**puntuaciones de 0 a 100 por criterio, separadas para Google y Bing**, con un
informe priorizado de correcciones.

📄 **Documentación completa:** https://www.cupomdescontos.com/ferramentas/auditoria-seo

## Instalación

```
/plugin marketplace add ducrz/seo-audit-marketplace
/plugin install seo-rank-audit
```

## Uso

```
audita ejemplo.com
¿por qué esta página no posiciona en Bing?
```

## Qué analiza

- **Estructura** — titles, metaetiquetas, headings, canonical, schema, robots,
  sitemap, HTTPS, alt, enlaces internos y atributos de enlace patrocinado
  (home + 5-10 páginas internas)
- **Velocidad** — Core Web Vitals reales vía la API pública de PageSpeed
  Insights (sin clave, sin registro)
- **Bing Webmaster** *(opcional)* — tráfico, rastreo y backlinks, para sitios
  verificados en la cuenta del propio usuario

## Principio

Las puntuaciones reflejan factores **documentados** por Google y Bing, no el
algoritmo real. Lo que no se puede medir se marca como no verificado y se
excluye de la base de cálculo — nunca se convierte en una suposición ni en
cero.

## Licencia

MIT — mantenido por [Eduardo Monteiro](https://www.cupomdescontos.com/sobre),
quien también dirige [CupomDescontos](https://www.cupomdescontos.com/).
Construí esta herramienta para auditar mis propios sitios y decidí abrir el
código.
