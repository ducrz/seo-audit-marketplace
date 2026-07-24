🌐 [English](#english) · [Português](#português)

# English

## Privacy Policy — SEO Rank Audit

**Last updated: 2026-07-24**

SEO Rank Audit is a Claude Code skill that runs entirely on your own machine.
This tool does not collect, store, or transmit any personal data, and there
is no backend server operated by the maintainer that this tool reports to.

### What this tool does over the network

- **Target site being audited**: the collector script (`scripts/audit.py`)
  fetches the public pages of whatever site you ask it to audit — the same
  requests any browser or search engine crawler would make. No data from
  this is sent anywhere except back to you, in your own terminal/output file.
- **Google PageSpeed Insights API** (`scripts/pagespeed.py`): sends the
  target URL to Google's public, keyless API to retrieve Core Web Vitals.
  This call is made directly from your machine to Google — the maintainer
  never sees it. Subject to [Google's own privacy policy](https://policies.google.com/privacy)
  for that API.
- **Bing Webmaster Tools API** (`scripts/bing_wmt.py`, optional): only runs
  if you explicitly provide your own API key for a site verified in your own
  Bing Webmaster Tools account. The request goes directly from your machine
  to Microsoft using your credentials — the maintainer never sees your key
  or the data returned. Subject to
  [Microsoft's own privacy policy](https://privacy.microsoft.com/en-us/privacystatement).

### What this tool does NOT do

- No analytics, telemetry, or usage tracking of any kind.
- No account, signup, or login required for the core audit flow.
- No data is sent to the maintainer or to any server the maintainer operates.
- Generated reports (`.json`, `.html`) are written only to your local disk.

### Contact

Questions about this policy: ducatolico@gmail.com

---

# Português

## Política de Privacidade — SEO Rank Audit

**Última atualização: 24/07/2026**

O SEO Rank Audit é uma skill do Claude Code que roda inteiramente na sua
própria máquina. Esta ferramenta não coleta, armazena nem transmite nenhum
dado pessoal, e não existe servidor do mantenedor pro qual ela reporte algo.

### O que a ferramenta faz na rede

- **Site auditado**: o script coletor (`scripts/audit.py`) busca as páginas
  públicas do site que você pedir pra auditar — as mesmas requisições que
  qualquer navegador ou crawler de busca faria. Nenhum dado disso é enviado
  pra lugar nenhum além de volta pra você, no seu terminal/arquivo de saída.
- **API do Google PageSpeed Insights** (`scripts/pagespeed.py`): envia a URL
  auditada pra API pública e sem chave do Google, pra buscar Core Web
  Vitals. Essa chamada sai direto da sua máquina pro Google — o mantenedor
  nunca vê isso. Sujeito à
  [política de privacidade do próprio Google](https://policies.google.com/privacy)
  pra essa API.
- **API do Bing Webmaster Tools** (`scripts/bing_wmt.py`, opcional): só roda
  se você fornecer explicitamente sua própria chave de API de um site
  verificado na sua própria conta do Bing Webmaster Tools. A requisição sai
  direto da sua máquina pra Microsoft, usando suas credenciais — o
  mantenedor nunca vê sua chave nem os dados retornados. Sujeito à
  [política de privacidade da própria Microsoft](https://privacy.microsoft.com/pt-br/privacystatement).

### O que a ferramenta NÃO faz

- Nenhum tipo de analytics, telemetria ou rastreamento de uso.
- Nenhuma conta, cadastro ou login exigido pro fluxo principal de auditoria.
- Nenhum dado é enviado pro mantenedor ou pra qualquer servidor operado por ele.
- Os relatórios gerados (`.json`, `.html`) são gravados só no seu disco local.

### Contato

Dúvidas sobre esta política: ducatolico@gmail.com
