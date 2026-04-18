# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete

## [2026-04-18] create | Wiki initialized
- Domain: E-commerce data pipeline architecture
- Structure created with SCHEMA.md, index.md, log.md

## [2026-04-18] ingest | ecommerce-data-pipeline.md
- Created from: maibeiBI/website/index.html (data source config + Shopee/SHEIN auth), ecommerce-ai-ux-solution.md, codebase analysis of api.py and workflow/model.py
- Pages created: [[ecommerce-data-pipeline]]
- Topics covered: Core Monitor→Investigate→Act→Automate loop, 3 data source modes (API接入/文件上传/插件爬取), workflow node graph (6 nodes: Update Origin → Get Main Sku → Calcu Weekly → Calcu Linked → Calcu Team Category → Split Team Category), MCP server registry (ERP/Shopee/SHEIN), two-tier fetch pattern, error classification, weekly data API, field mappings (EN↔CN for business + affiliate), normalization rules, multi-dimensional reporting (by shop/team/category/product/order), segment cards, AI assistant modes, SkillHub, new product R&D workflow (9 steps), automation center, product architecture (卖倍AI), before/after efficiency comparison
- Sources: docs/ecommerce-ai-ux-solution.md, maibeiBI/website/index.html, fastestai-playground excel/router/api.py, workflow/model.py, skillhub/ecomm_new_products/SKILL.md
- Notes: Amazon/TikTok/TikTokShop MCPs not yet cloned — marked as WIP per user feedback (not essential to this doc); Google Docs source still requires OAuth; workflow JSON "69e30a8f" confirmed as 6-node weekly stats pipeline (七木-v5)