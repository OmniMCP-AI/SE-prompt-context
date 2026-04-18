# MaybeAI E-commerce Data Processing Pipeline

> Last updated: 2026-04-18
> Sources: `docs/ecommerce-ai-ux-solution.md`, `maibeiBI/website/index.html`, `fastestai-playground/src/fastestai_playground/excel/router/api.py`, `fastestai-playground/src/fastestai_playground/workflow/model.py`, `skillhub/ecomm_new_products/SKILL.md`

---

## Core Loop

The central UX principle and data processing driver:

```
Monitor → Investigate → Act → Automate → (back to Monitor)
```

Everything in the platform — sheets, workflows, AI assistant, segment cards — serves this loop.

---

## Layer 1: Data Source Configuration

Three ways to connect store data to 卖倍AI:

### 1.1 API 接入 (Platform ISV API) — Automated Sync

Long-term stable integration via platform partner APIs. Data syncs automatically on a schedule without manual intervention.

**Complete platform data source inventory** (from `e-comm-datapipeline-pattern.xlsx → datasource` sheet):

| Platform | Data Type | Data Source | API | Current Tool | API Needed |
|----------|-----------|-------------|-----|-------------|-----------|
| **Shopee** | 广告 (Ads) | 电商平台后台 | 1.获取广告列表 2.广告设置 3.每日表现 | 八爪鱼 (Octopus RPA) | 店铺申请/3rd开发者申请 |
| **Shopee** | 订单明细 | 电商平台后台 | 1.订单列表 2.订单基本信息 3.存管信息 4.物流号 5.附赠信息 | 八爪鱼 | 店铺申请/3rd开发者申请 |
| **Shopee** | 大盘数据 | 电商平台后台 | **无API — 需scraper/browser-use方案** | 八爪鱼 | WF+BS / 后台导出 |
| **Shopee** | 联盟转化报告 | 电商平台后台 | 联盟转化报告 | 手动+紫鸟 | 店铺申请/3rd开发者申请 |
| **千易ERP** | 订单毛利明细 | 千易ERP-dashboard | **无API — 需scraper/browser-use方案** | 影刀RPA+紫鸟 | WF+BS / 后台导出 |
| **千易ERP** | 库存 | 千易ERP | API | — | — |
| **Shopee** | 用户评论 | 电商平台前台 | API | 心舰 | — |
| **SHEIN** | 订单明细 | 电商平台后台 | 1.订单列表 2.订单详情 | 手动 | — |
| **SHEIN** | 销售 | 电商平台后台 | 1.订单列表 2.订单详情 | 手动 | — |
| **SHEIN** | 履约分析 | 电商平台后台 | 1.订单列表 2.订单基本信息 | 手动 | 之前有10天延时 |
| **SHEIN** | 经营流量分析 | 电商平台后台 | **无API，RPA无法获取（前端限制）** 初定：web API + cookies | 手动 | — |
| **SHEIN** | 商品图片 | 电商平台后台 | 电商平台后台 | 手动 | 低优先级 |
| **Amazon** | Business Report | 电商平台后台+OpenCLI | `developer-docs.amazon.com/sp-api` | 手动 | — |
| **Amazon** | 库存报告 | Amazon | TBD | 手动 | — |
| **Lazada** | 订单明细 | — | 1.订单列表(分页) 2.订单详情 3.商品明细/批量 | — | — |
| **Lazada** | 履约分析 | — | 1.订单列表 2.商品明细 3.物流轨迹 | — | — |

> ⚠️ **Critical:** 大盘数据 (performance/traffic data) and 千易ERP 订单毛利明细 have **no API available** — require scraper or RPA. This is the primary gap in the data pipeline.

**Shopee ERP authorization flow:**
1. User selects auth type (ERP / ADS / AMS)
2. System generates authorization link via `https://shopee.com.vn/partner/auth`
3. User completes OAuth on Shopee side
4. Callback handled at `/auth/shopee/callback`
5. Credentials stored, schedule sync initiated

**SHEIN authorization flow:**
1. App ID: `1523FCB22E801859E4894E04AD9B4`
2. Host: `openapi-sem.sheincorp.com`
3. Redirect to SHEIN open platform → `#/empower`
4. Callback at `window.location.origin + '/auth/shein/callback'`

### 1.2 上传文件导入 (File Upload) — Manual Export

Upload Shopee后台导出文件的 ZIP 压缩包. System auto-parses and aggregates all store data.

- **Supported formats:** `.zip` (max 50MB per upload)
- **Supported platforms:** Shopee, SHEIN, Lazada, Amazon, TikTok Shop
- **Processing time:** ~10 minutes after upload
- **Workflow:** Upload ZIP → Auto-parse → Aggregate → Generate report sheets

### 1.3 插件爬取汇总 (Browser Plugin Scraping)

Install MaybeAI Browser Scraper Chrome extension to automatically collect data from Shopee seller backend — no manual export needed.

- Extension: `maybeai-browserscraper-wei` on Chrome Web Store
- Installed → Enabled per store → Background scrape on schedule

### 1.4 Before vs After: Time Comparison

From `e-comm-datapipeline-pattern.xlsx → 以前步骤vs现在步骤`:

**Before (manual process):**

| 阶段 | 数据源 | 步骤 | 耗时 | 问题点 | 工具 |
|------|--------|------|------|--------|------|
| 原始数据准备 | 广告 | 开紫鸟浏览器 | 2分钟 | 下载20%概率出问题，需重试 | 影刀RPA+虎步RPA+紫鸟 |
| 原始数据准备 | 广告 | 选RPA模版，下载+重命名 | 5-10分钟 | RPA难维护，出错需人工介入 | 同上 |
| 数据处理 | Excel | 打开各种原始数据 | 30分钟/店铺 | RPA难维护，Excel操作复杂 | 影刀RPA |
| 数据处理 | Excel | 粘贴+VLOOKUP+Pivot Table | — | 异常需中断、调整、重试 | 同上 |
| 结果汇总 | — | 人工检查+汇总发群 | 30分钟 | — | — |
| | | **总计** | **≥60分钟/店铺** | | |

**After (MaybeAI workflow):**

| 阶段 | 数据源 | 步骤 | 耗时 | 工具 |
|------|--------|------|------|------|
| 原始数据准备 | 广告/订单/联盟报告 | API接入 | 1分钟 | API |
| 原始数据准备 | 大盘数据/ERP | 紫鸟浏览器+插件自动运行 | 2分钟 | 插件 |
| 数据处理 | Excel | 运行Excel workflow | 2分钟 | MaybeAI workflow |
| 结果汇总 | — | 程序检查异常+修复 | — | MaybeAI workflow |

**效率提升: 60+分钟 → ~5分钟 (6-12x faster)**

---

## Layer 2: E-commerce Workflow Steps

The core "七木-v5-多店铺周数据统计" (Nanmu-v5 Multi-store Weekly Data Statistics) workflow drives the entire data processing pipeline.

### Workflow JSON (from `wkly-sample-workflow.json`)

Real workflow ID: `69e30a8f38a1e3d944878f61` (title: 多店铺周数据统计, name: 七木-v5-多店铺周数据统计)

This is a **sequential orchestrator** — a parent workflow that calls 6 sub-workflows in order via `workflow_mcp__run_workflow`, each passing no variables (`variables: []`). Every node is a `tool_call` operation.

```json
{
  "id": "69e30a8f38a1e3d944878f61",
  "name": "七木-v5-多店铺周数据统计",
  "title": "多店铺周数据统计",
  "objective": "按顺序执行指定的workflow：69817458b46547413203d36b -> 697c99735c435e0365a2056a ->697c32247504e1e6b0b85e95",
  "task": "将 Split Team Category Data 改成 Calcu Team Category Data 之后在执行",
  "flows": [
    { "id": "update_origin_weekly_data",   "artifact_id": "699d66e656c5f49281dc07f2" },
    { "id": "get_main_sku",                "artifact_id": "699ed2485905005a1efe8563" },
    { "id": "calcu_weekly_data",           "artifact_id": "69ca4935f346358a5bcee49a" },
    { "id": "calcu_linked_data",           "artifact_id": "69c2a91a175471d3019c4466" },
    { "id": "calcu_team_category_data",    "artifact_id": "69ca4a13f346358a5bcee60d" },
    { "id": "split_team_category_data",    "artifact_id": "69a2917a1ee3f43a388c1853" }
  ],
  "result_tables": [],
  "output": ["workflow_result1", "workflow_result2", "workflow_result3", "workflow_result4", "workflow_result5"]
}
```

### Node Dependency Graph (DAG)

```
update_origin_weekly_data          (artifact: 699d66e656c5f49281dc07f2)
        │
        ▼
    get_main_sku                    (artifact: 699ed2485905005a1efe8563)
        │
        ▼
   calcu_weekly_data                (artifact: 69ca4935f346358a5bcee49a)
        │
        ├──────────────────────────────┐
        ▼                              ▼
calcu_linked_data            calcu_team_category_data
(artifact: 69c2a91a...)              (artifact: 69ca4a13...)
        │                              │
        │                              ▼
        │                   split_team_category_data
        │                        (artifact: 69a2917a...)
        │                              │
        └──────────────────────────────┘
                        (converge → final output)
```

**Key observations:**
- `calcu_linked_data` and `calcu_team_category_data` run in **parallel** (both depend only on `calcu_weekly_data`)
- `split_team_category_data` depends only on `calcu_team_category_data` (not on `calcu_linked_data`)
- All tool calls use the same tool `workflow_mcp__run_workflow` with `artifact_id` + empty `variables[]`
- `result_tables: []` — no intermediate tables exposed as named outputs
- Final output: 5 scalar workflow results (`workflow_result1` through `workflow_result5`)

### Node Descriptions

| Node | artifact_id | Chinese | Description |
|------|-------------|---------|-------------|
| **update_origin_weekly_data** | `699d66e656c5f49281dc07f2` | 更新原始周数据 | Fetches raw weekly data from MCP sources (Shopee/SHEIN via ERP), handles pagination, error classification. No inputs, no dependencies. |
| **get_main_sku** | `699ed2485905005a1efe8563` | 获取大盘的主货号 | Identifies primary SKU/product identifiers from aggregated raw data. Normalizes across shops, extracts parent SKU hierarchy. Depends on ①. |
| **calcu_weekly_data** | `69ca4935f346358a5bcee49a` | 计算店铺相关周数据 | Computes per-shop weekly metrics (sales, orders, refund rate, fulfillment rate, margin). Groups by shop across all categories. Depends on ②. |
| **calcu_linked_data** | `69c2a91a175471d3019c4466` | 计算team&category相关周数据 | Computes team × category cross-dimensional metrics. Links shop performance to team structure. **Parallel with ⑤**, depends on ③. |
| **calcu_team_category_data** | `69ca4a13f346358a5bcee60d` | 计算team&category相关周数据 | Further aggregates team-level category performance. **Parallel with ④**, depends on ③. |
| **split_team_category_data** | `69a2917a1ee3f43a388c1853` | 分team计算category相关周数据 | Final split — separates by team, producing team-specific category sheets. Feeds Excel reporting. Depends on ⑤. |

### Dataflow Execution Model

Each node executes via `fastestai-api/src/fastestai/dataflow/`:

```python
User prompt → define_dataflow()  # LLM generates Dataflow JSON
                      ↓
          BasicDataflow executor
                      ↓
          FlowEvent stream (ToolCallFlow / MapFlow / FilterFlow / ApplyFlow / SwitchFlow / LoopFlow / ConfluenceFlow / HumanInteractionFlow)
```

**Flow types available:**
- `ToolCallFlow` — Call single MCP tool
- `MapFlow` — Parallel map over list
- `FilterFlow` — Filter by condition
- `ApplyFlow` — Transform each element
- `SwitchFlow` — Conditional branching
- `LoopFlow` — Iterative with convergence
- `ConfluenceFlow` — Merge multiple streams
- `HumanInteractionFlow` — Pause for approval

### Workflow Data Model

From `workflow/model.py`:

```python
Workflow
  ├── id, name, description, task
  ├── steps: List[WorkflowStep]         # Nodes in the graph
  │     └── WorkflowStep
  │           ├── id
  │           ├── content               # Human-readable description
  │           └── actions: List[WorkflowAction]
  │                 └── WorkflowAction
  │                       ├── id
  │                       ├── content
  │                       ├── tool: WorkflowTool | LLMTool
  │                       │     └── WorkflowTool: id, type=Mcp/Llm, default_arguments
  │                       ├── inputs: List[str]    # Output references from prior actions
  │                       └── outputs: List[str]   # Produced variables
  ├── variables: List[WorkflowVariable]  # Named inputs/outputs for the workflow
  ├── user_input: List[WorkflowVariable]  # User-provided at runtime
  └── config: WorkflowUserConfig         # Per-user configuration
```

**Action dependency model:**
```python
ActionDependence
  ├── source: str   # Output variable name
  ├── target: str   # Input variable name of dependent action
  └── type: Required | Optional
```

---

## Layer 3: MCP Server Architecture

### MCP Server Registry

| Platform | MCP URL | Auth Method | Tools Available |
|----------|---------|------------|----------------|
| **ERP (Qianyi)** | `https://erp-mcp.maybe.ai/mcp` | Partner ID + User ID | `list_shops` + 26 others |
| **Shopee** | `https://shoppee-mcp.maybe.ai/mcp` | Via ERP MCP authorization | Category data, daily orders, product performance |
| **SHEIN** | `https://shein-mcp.maybe.ai/mcp` | App ID + OAuth | Product/listing data, activity analysis, traffic analysis |

### Two-Tier Fetch Pattern

```
ERP MCP (authorization + shop listing)
    │
    ├── partner_id / ads_partner_id / ams_partner_id
    ├── user_id: 6824bdc5964f92cba08e0219
    ├── Page size: 200 shops per request
    │
    ▼
Platform MCP (category-level data per shop)
    │
    ├── Shopee MCP via SSE proxy (SHOPEE_MCP_PROXY_SSE_URL)
    ├── SHEIN MCP direct
    │
    ▼
fastestai-playground API
    └── POST /api/v1/excel/process_weekly_data
```

### MCP Error Classification

All MCP tool calls classify errors into:

| Type | Retry? | Example |
|------|--------|---------|
| `transient_network` | ✅ With backoff | Timeout, connection reset |
| `auth` | ❌ | Invalid/expired token |
| `schema_validation` | ❌ | Unexpected response format |
| `business_empty_or_not_found` | ✅ But expected | No data for this shop/category |
| `unknown` | ⚠️ Manual review | Unclassified failures |

### Link Analysis Pattern (运营数据分析体系)

From `e-comm-datapipeline-pattern.xlsx → link-analysis-pattern`:

```
运营数据分析体系
│
├── 日常监控
│   ├── 销售额
│   ├── 单量
│   └── 营销占比（核心指标）
│
├── 营销占比异常
│   ├── 转化率下降？
│   │   ├── 点击率下降？→ 主图问题
│   │   ├── 缺货？
│   │   ├── 差评？
│   │   └── 流量不精准？
│   ├── 流量成本上升？→ ROI调整
│   └── 客单价下降？→ 清仓SKU？
│
├── 制定ToDo: 换图 / 调ROI / 控评 / 补货 / 优化详情页
├── 观察2-3天
└── 周复盘: 汇总同类 → 看趋势 → 看利润 → 是否值得推 → 下周目标

[开始] → 查看销售额/单量/营销占比
    ↓
营销占比是否异常？
├── 否 → 结束
└── 是
    ↓
拆解原因
    ↓
转化率下降？→ 是 → 检查点击率/库存/差评/流量
    ↓
流量成本上升？→ 是 → 调整ROI
    ↓
客单价下降？
    ↓
制定ToDo → 执行动作 → 观察2-3天
    ↓
是否改善？
├── 是 → 稳定/放大
└── 否 → 再归因 → [循环]
```

### 七木数据流 (Workflow References)

From `e-comm-datapipeline-pattern.xlsx → 七木数据流`:

| 流程 | URL |
|------|-----|
| 日数据总流程 | `https://www.maybe.ai/user/workflow/69b7f8279fc11af6a71ffd84` |
| 周数据总流程 | `https://www.maybe.ai/user/workflow/69ca4920f346358a5bcee480` |
| 日数据毛利表 | `https://www.maybe.ai/docs/spreadsheets/d/698da73a961db811bcfd2189?gid=41` |
| 周数据毛利表 | `https://www.maybe.ai/docs/spreadsheets/d/698a06cba56003ebf8667f72?gid=12` |
| 日数据链接数据 | `https://www.maybe.ai/docs/spreadsheets/d/698da73a961db811bcfd2189?gid=14` |
| 周数据链接数据 | `https://www.maybe.ai/docs/spreadsheets/d/698a06cba56003ebf8667f72?gid=14` |

---

## Layer 4: Data Processing

### Weekly Data API

`POST /api/v1/excel/process_weekly_data` — Main endpoint in `fastestai-playground/src/fastestai_playground/excel/router/api.py`

**Process:**
```
For each shop (from ERP list_shops):
  → _fetch_erp_shop_records()     # Paginated, 200/page
  → For each category in ACTIVE_SHOPEE_MCP_WEEKLY_CATEGORIES:
      → _fetch_weekly_shopee_mcp_worksheets()   # SSE proxy call
      → _extract_rows_from_shopee_mcp_payload()  # Parse JSON
      → _normalize_sheet_cell_value()            # Type conversion
      → _classify_shopee_mcp_error()             # Error categorization
      → _build_row_sample()                      # Sampling for AI analysis
  → Aggregate into Excel workbook
```

**Key constants from api.py:**
- `SHOPEE_MCP_PROXY_SSE_URL = "https://shoppee-mcp.maybe.ai/mcp"`
- `ERP_MCP_URL = "https://erp-mcp.maybe.ai/mcp"`
- `ERP_MCP_LIST_SHOPS_TOOL_NAME = "list_shops"`
- `ERP_MCP_PAGE_SIZE = 200`
- `SHEIN_MCP_URL = "https://shein-mcp.maybe.ai/mcp"`
- Site code aliases: `MY` (Malaysia), `TH` (Thailand)

### Field Mapping (Multi-language)

**Business Analysis fields (EN → CN):**
```python
"Item ID" → "商品编号"
"Product" → "商品"
"SKU" → "商品货号"
"Parent SKU" → "主商品货号"
"Product Visitors (Visit)" → "商品访客（访问）"
"Conversion Rate (Placed Order)" → "转化率（已下单）"
"Sales (Confirmed Order)" → "销售额（已确认订单）"
"Buyers (Confirmed Order)" → "买家数（已确认订单）"
```

**Affiliate/联盟 fields (EN → CN):**
```python
"Order id" → "订单编号"
"L1 Global Category" → "L1分类"
"Item Brand Commission" → "商品佣金"
"Order Brand Commission" → "订单佣金"
"Purchase Value" → "购买值"
"Refund Amount" → "退款金额"
```

### Data Normalization Rules

From `_normalize_sheet_cell_value()`:
- **Percentage strings** → float: regex `-?\d+(?:[.,]\d+)?%`
- **MongoDB URIs** → redacted via `_redact_mongo_uri()`
- **Site codes** → normalized (MY/TH mapping)
- **Decimal handling** → locale-aware (comma vs period decimal separator)

---

## Layer 5: Multi-Dimensional Reporting

### Reporting Dimensions

| Dimension | Granularity | Frequency | Sheet |
|-----------|-------------|-----------|-------|
| **By Shop** | Per store | Daily / Weekly | 店铺汇总 |
| **By Team** | Per team (MY/TH) | Weekly | team维度 |
| **By Category** | Category-level | Weekly | category维度 |
| **By Product** | SKU-level | Live | 商品表 |
| **By Order** | Order-level | Daily | 履约表 |

### Standard Report Sheets

| Sheet | Purpose |
|-------|---------|
| `商品表` | Product-level performance with KPI metrics |
| `核算表` | Financial accounting — margin, cost, profitability |
| `履约表` | Fulfillment tracking — orders, shipping, delivery status |

### Segment Cards (Business Filters)

Configurable alert cards on Overview page — instant filtering without page reload:

| Card | Rule | Color | Signal |
|------|------|-------|--------|
| 销量暴涨 | `sales_growth_7d > 30%` | Blue | KPI spike |
| 低利润 | `profit_rate < 5%` | Red | Margin risk |
| 高退款率 | `refund_rate > 10%` | Orange | Quality issue |
| 履约异常 | `fulfillment_rate < 95%` | Gold | Operation risk |

**Source of truth:** Config table in sheet (Phase 1). Phase 2 → admin UI. Phase 3 → AI-assisted config ("create segment from prompt").

---

## Layer 6: AI Analysis & Automation

### AI Assistant Modes

Same brain, different surfaces:

```
[Ask]  [Analyze]  [Edit]  [Automate]
```

- **Ask:** "Why did fulfillment rate drop this week?" → reads data, explains
- **Analyze:** "Compare Thailand vs Malaysia low-margin SKUs" → cross-dimensional analysis
- **Edit:** "Add a column for margin band" → sheet manipulation
- **Automate:** "Monitor this segment every morning and notify ops" → creates workflow

### SkillHub Integration

Contextual entry points:
- From assistant suggestions
- From `Create automation`
- From a filtered segment
- From setup recommendations

### New Product R&D Workflow

From `skillhub/ecomm_new_products/SKILL.md` (9-step process):

```
Step 1 → Category Overview         Parse export, volume, seasonality, price distribution, top brands
Step 2 → Target Segment Deep Dive  Filter by price/positioning → identify opportunity zones
Step 3 → Competitor & Feature      Brand landscape + attribute extraction (functional/design/usage)
Step 4 → Market Gap Identification  Attribute gap / Positioning gap / Format gap / Trend gap
Step 5 → Product Definition        Per SKU: name, price, specs, variants, differentiation, margin
Step 6 → Sample Validation         Dimension + feature feasibility + scoring (1-5)
Step 7 → Social Proof Validation   Reddit, Google Trends, media signals
Step 8 → Keyword Advertising       Tier 1 (awareness) → Tier 2 (conversion) → Tier 3 (competitor)
Step 9 → Launch Timeline           Phase 1 test → Phase 2 optimize → Phase 3 expand
```

### Automation Center

- **First-class object:** Sheet ↔ Workflow = `Sheet 1 → N Workflows`
- **Header pattern:** `[AI Assistant] [Automation 2] [More]`
- **Drawer:** right-side panel showing linked workflows with trigger + last run
- **Deep link:** `/workspace?sheetId=<sheetId>&source=sheet`

---

## Data Flow Diagram (AI Automated Flow)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        BEFORE — 人工流程                                   │
│  手动导出文件 → 逐个店铺处理 → Excel汇总 → 人工核对 → 耗时长/易出错          │
└─────────────────────────────────────────────────────────────────────────────┘

                        ⬇ 效率提升 6x ⬇

┌─────────────────────────────────────────────────────────────────────────────┐
│                     AFTER — AI 自动化流程                                    │
│                                                                             │
│  [数据源配置]                                                               │
│    ├─ API接入 (Shopee ERP / SHEIN)  ───────────────────────────────┐       │
│    ├─ 上传文件导入 (ZIP)           ─────────────────────────────┐  │       │
│    └─ 插件爬取 (Browser Scraper)   ────────────────────────────┐  │  │       │
│                                                               │  │  │       │
│  [MCP数据获取] ──→ ERP MCP (授权/店铺列表)                      │  │  │       │
│                        │                                        │  │  │       │
│                        ▼                                        │  │  │       │
│                   Platform MCP                                  │  │  │       │
│                   (Shopee / SHEIN)                             │  │  │       │
│                        │                                        │  │  │       │
│                        ▼                                        ▼  │  │       │
│  [数据处理] ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←┘       │       │
│    │                                                                 │       │
│    ▼                                                                         │
│  [周数据统计 workflow]                                                       │
│    ① 更新原始周数据 → ② 获取主货号 → ③ 计算店铺数据 →                          │
│    ④ 计算team&category数据 → ⑤+⑥ 分team分category输出                        │
│    │                                                                            │
│    ▼                                                                            │
│  [报表输出]                                                                   │
│    商品表 / 核算表 / 履约表                                                   │
│    │                                                                            │
│    ▼                                                                            │
│  [AI分析层]                                                                   │
│    Segment Cards (销量暴涨/低利润/高退款率/履约异常)                          │
│    AI Assistant (Ask/Analyze/Edit/Automate)                                    │
│    SkillHub (workflow starter kit)                                            │
│    Automation Center (监控+通知)                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Product Architecture: 卖倍AI

Primary object: **Store / Seller Workspace**

```
卖倍AI (MaibeiBI)
│
├── Overview                    # Business health, anomalies, recommended actions
│   └── Segment Cards: [销量暴涨 71] [低利润 6] [高退款率 4] [履约异常 12]
│
├── Data Sources                # Live control center (not just onboarding)
│   ├── Store Connections        # API接入 (Shopee/SHEIN authorization)
│   ├── Upload History           # ZIP上传记录
│   └── Sync Health             # Monitor sync status, failed syncs
│
├── Operations                   # Instant in-place filtering (no page jump)
│   ├── Orders                   # 履约数据
│   ├── Ads                      # 广告数据
│   ├── ERP                      # ERP汇总
│   ├── Weekly Summary           # 周报
│   └── Influencer / Live        # 网红/直播
│
├── Sheets                       # Investigation workspace
│   ├── 商品表                   # Product table (Live, linked to 2 workflows)
│   ├── 核算表                   # Accounting table
│   └── 履约表                   # Fulfillment table
│
├── Automations                  # First-class, accessible everywhere
│   ├── Automation Center        # Deep management
│   ├── Workflow Templates       # Starter kits
│   └── Run History              # Execution log
│
└── AI                           # Control layer, not utility panel
    ├── Assistant [Ask/Analyze/Edit/Automate]
    └── SkillHub                 # Capability marketplace
```

### UX Principles

1. **Business-first language:** 低margin SKUs, ad ROI anomaly, fulfillment risk — not workflow/trigger/spreadsheet terms
2. **In-place update over page jump:** Click segment card → table filters instantly, header/filters/context stay stable
3. **Visible relationships:** Every page exposes linked objects (sheet page shows workflows, workflow shows source sheet)

---

## Key File Reference

| File | Purpose |
|------|---------|
| `fastestai-playground/src/fastestai_playground/excel/router/api.py` | Main Excel API + `process_weekly_data` (~13,863 lines). Contains all MCP URLs, field mappings, error classification, normalization logic. |
| `fastestai-playground/src/fastestai_playground/workflow/model.py` | Workflow data model — `Workflow`, `WorkflowStep`, `WorkflowAction`, `WorkflowTool`, `WorkflowVariable` |
| `fastestai-playground/src/fastestai_playground/workflow/server/workflow_server.py` | `WorkflowServer` — CRUD, MongoDB collection `workflow` |
| `fastestai-api/src/fastestai/dataflow/dataflow.py` | LLM-driven workflow execution engine — `define_dataflow()`, `BasicDataflow` |
| `fastestai-api/src/fastestai/dataflow/models.py` | Pydantic flow types — `ToolCallFlow`, `MapFlow`, `FilterFlow`, `ApplyFlow`, `SwitchFlow`, `LoopFlow`, `ConfluenceFlow`, `HumanInteractionFlow` |
| `maibeiBI/website/index.html` | Data source configuration UI — API接入, 文件上传, 插件爬取. Shopee/SHEIN auth flows. |
| `docs/ecommerce-ai-ux-solution.md` | Product UX architecture — core loop, information architecture, journey patterns |
| `skillhub/ecomm_new_products/SKILL.md` | New product R&D 9-step workflow |

---

## Environment & Config

| Service | Detail |
|---------|--------|
| **MongoDB** | 3 instances: main playground, ai_qa, omnimcp_be |
| **Redis** | Session management, rate limiting, quota tracking |
| **MaybeAI API** | `https://www.maybe.ai` |
| **ERP MCP** | `https://erp-mcp.maybe.ai/mcp` |
| **Shopee MCP Proxy** | `https://shoppee-mcp.maybe.ai/mcp` |
| **SHEIN MCP** | `https://shein-mcp.maybe.ai/mcp` |
| **Cloud Storage** | Tencent COS — `maybe-static-1317942802` bucket, `ap-singapore` region |

---

## Next Steps

- [ ] Clone missing MCPs (amazon-mcp, tiktok-mcp, tiktokshop-mcp) from `github.com/OmniMCP-AI/` if needed
- [ ] Implement Phase 2 segment card management UI
- [ ] Add AI-assisted segment configuration ("create segment from prompt")
- [ ] Build cross-team comparison view (MY vs TH)
- [ ] Extend new product R&D workflow with live competitor monitoring