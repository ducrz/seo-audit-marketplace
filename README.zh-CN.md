🌐 [English](README.md) · [Português](README.pt-BR.md) · [Español](README.es.md) · [Français](README.fr.md) · [中文](README.zh-CN.md)

# SEO Rank Audit

面向 Claude Code 的开源 skill，可审计网站并按标准分别给出 **Google 和 Bing
的 0-100 分**，并附带按影响优先排序的修复建议报告。

📄 **完整文档：** https://www.cupomdescontos.com/ferramentas/auditoria-seo

## 环境要求

已安装 [Claude Code](https://docs.claude.com/en/docs/claude-code)（`npm install -g @anthropic-ai/claude-code`），并在终端中运行 —— `/plugin` 命令在 IDE 集成环境中不可用。

## 安装

```
/plugin marketplace add ducrz/seo-audit-marketplace
/plugin install seo-rank-audit
```

## 使用方法

```
审计 example.com
为什么这个页面在 Bing 上排名不好？
```

## 检测内容

- **页面结构** — 标题、meta 标签、标题层级、canonical、结构化数据、robots、
  sitemap、HTTPS、alt 文本、内部链接以及赞助链接属性（首页 + 5-10 个内部页面）
- **速度** — 通过 PageSpeed Insights 公共 API 获取真实的 Core Web Vitals
  数据（无需密钥，无需注册）
- **Bing Webmaster**（可选）— 针对用户账户中已验证的网站，提取流量、抓取和
  外链数据

## 原则

评分反映的是 Google 和 Bing **公开记录**的排名因素，而非真实算法。无法测量
的项目会标记为"未验证"并从计分基数中剔除——绝不会变成猜测或直接算作零分。

## 许可证

MIT — 由 [Eduardo Monteiro](https://www.cupomdescontos.com/sobre) 维护，他也
运营着 [CupomDescontos](https://www.cupomdescontos.com/)。这个工具最初是为了
审计自己的网站而开发的，后来决定开源。
