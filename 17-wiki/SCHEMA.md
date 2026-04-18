# Wiki Schema

## Domain
E-commerce data pipeline architecture — MaybeAI platform covering Shopee, SHEIN, Amazon, TikTok, TikTokShop integration with ERP, Excel reporting, AI analysis, and automation workflows.

## Conventions
- File names: lowercase, hyphens, no spaces (e.g., `ecommerce-data-pipeline.md`)
- Every wiki page starts with YAML frontmatter
- Use `[[wikilinks]]` to link between pages (minimum 2 outbound links per page)
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`

## Frontmatter
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [from taxonomy below]
sources: [raw/...]
---
```

## Tag Taxonomy
- **Platforms**: shopee, shein, amazon, tiktok, tiktokshop, erp
- **Components**: mcp, api, dataflow, excel, automation, skill
- **Business**: reporting, analytics, product-research, launch
- **Meta**: architecture, pipeline, integration, comparison

## Page Thresholds
- **Create a page** when an entity/concept appears in 2+ sources OR is central to one source
- **Add to existing page** when a source mentions something already covered
- **DON'T create a page** for passing mentions, minor details, or things outside the domain
- **Split a page** when it exceeds ~200 lines

## Update Policy
When new information conflicts with existing content:
1. Check the dates — newer sources generally supersede older ones
2. If genuinely contradictory, note both positions with dates and sources
3. Mark the contradiction in frontmatter: `contradictions: [page-name]`
4. Flag for user review in the lint report