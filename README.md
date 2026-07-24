🌐 [English](README.md) · [Português](README.pt-BR.md) · [Español](README.es.md) · [Français](README.fr.md) · [中文](README.zh-CN.md)

# SEO Rank Audit

Open source skill for Claude Code that audits a site and assigns **scores from
0 to 100 per criterion, separated for Google and Bing**, with a prioritized
report of fixes.

📄 **Full documentation:** https://www.cupomdescontos.com/ferramentas/auditoria-seo

## Requirements

[Claude Code](https://docs.claude.com/en/docs/claude-code) installed (`npm install -g @anthropic-ai/claude-code`), running in a terminal — the `/plugin` command isn't available in IDE integrations.

## Installation

```
/plugin marketplace add ducrz/seo-audit-marketplace
/plugin install seo-rank-audit
```

## Usage

```
audit example.com
why isn't this page ranking on Bing?
```

## What it collects

- **Structure** — titles, meta tags, headings, canonical, schema, robots,
  sitemap, HTTPS, alt text, internal links and sponsored-link attributes
  (home + 5-10 internal pages)
- **Speed** — real Core Web Vitals via the public PageSpeed Insights API
  (no API key, no signup)
- **Bing Webmaster** *(optional)* — traffic, crawling and backlinks, for
  sites verified in the user's own account

## Principle

Scores reflect **documented** ranking factors from Google and Bing, not the
real algorithm. Anything that can't be measured is marked as unverified and
removed from the score base — it never becomes a guess or a zero.

## License

MIT — maintained by [Eduardo Monteiro](https://www.cupomdescontos.com/sobre),
who also runs [CupomDescontos](https://www.cupomdescontos.com/). Built this
tool to audit my own sites and decided to open source it.
