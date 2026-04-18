# Sheet × Workflow × AI — UX Design Solution

> Product: 卖倍AI (MaybeAI for ecommerce)
> Date: 2026-03-20
> Scope: clawAI app, sheet view, automation panel, AI copilot, sidebar restructure

---

## 1. Product Position

> **卖倍AI is an AI-native ecommerce workspace.**
> Not a BI tool. Not a chatbot. Not a spreadsheet. All three, unified.

```
YOUR DATA in sheets     →  tree nav, live sync, filter chips
YOUR AUTOMATION         →  ⚡ badges on sheets, workflow panel, ⊙ dashboard nodes
YOUR AI ASSISTANT       →  context-aware copilot (web + Discord unified)
```

Target users: Chinese ecommerce sellers on Shopee / SHEIN / TikTok Shop / Lazada.

---

## 2. Core Architecture — 3 Surfaces, One Workspace

```
Web (clawAI)                Discord (openclaw)         AI Engine
┌──────────────────┐        ┌──────────────────────┐   ┌──────────────┐
│ Tree nav         │        │ OpenClaw gateway      │   │ fastestai-api│
│ Sheet views      │        │ ask_dataagent         │   │ 40+ tools    │
│ SkillHub panel   │        │ write_excel           │   │ workflows    │
│ Automation panel │        │ pd-smartdatalake      │   │ Claude       │
│ AI copilot       │        │ excelize-mcp          │   │              │
└──────────────────┘        └──────────────────────┘   └──────────────┘
         │                           │                        │
         └───────────────────────────┴────────────────────────┘
                         Same underlying data & sheets
```

---

## 3. Overall Layout

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  卖倍AI                                                    [🔔] [⚙] [👤]    │
├─────────────┬────────────────────────────────────────────┬───────────────────┤
│             │                                            │                   │
│  LEFT TREE  │           MAIN WORKSPACE                  │   AI COPILOT      │
│             │                                            │                   │
│  ▼ 我的店铺 │  ┌──────────────────────────────────────┐ │  ┌─────────────┐  │
│             │  │ 核算表  ● Live    [⚡ 2]  [⋮]        │ │  │ 🤖 卖倍AI   │  │
│  ▼ 运营数据 │  ├──────────────────────────────────────┤ │  │             │  │
│  ⊙ 驾驶舱  │  │ 全部 │ Shopee │ SHEIN │ TikTok       │ │  │ 快捷问题:   │  │
│  ▦ 核算表⚡2│  ├──────────────────────────────────────┤ │  │ [哪些SKU    │  │
│  ▦ 履约率⚡1│  │[利润偏低 6][高退款 4][成本超标 3]... │ │  │  利润最低?] │  │
│  ▦ 周汇总  │  ├──────────────────────────────────────┤ │  │             │  │
│             │  │                                      │ │  │ [本周vs     │  │
│  ▼ 广告管理 │  │   [spreadsheet content]              │ │  │  上周对比]  │  │
│  ⊙ 广告驾驶 │  │                                      │ │  │             │  │
│  ▦ 广告数据 │  │                                      │ │  │ 应用技能:   │  │
│  ▦ 链接汇总 │  │                                      │ │  │ [广告ROI   │  │
│             │  │                                      │ │  │  诊断 →]   │  │
│  ▼ 库存&ERP │  └──────────────────────────────────────┘ │  │             │  │
│  ⊙ ERP驾驶 │                                            │  │ [输入问题] │  │
│  ▦ 订单    │                                            │  └─────────────┘  │
│  ▦ ERP数据 │                                            │                   │
│  ──────────  │                                            │                   │
│  ⚡ 自动化  │                                            │                   │
│  🎯 SkillHub│                                            │                   │
│  ⚙  设置   │                                            │                   │
│  💬 Discord │                                            │                   │
└─────────────┴────────────────────────────────────────────┴───────────────────┘
```

---

## 4. Left Sidebar — Tree Nav Redesign

### Before (flat app menu)

```
⚙ 数据源配置 [NEW]
🧙 初始化向导 [NEW]
🎥 同步demo
🧩 数据整合
🤖 AI助手
📦 订单
📈 商业分析
📢 广告 [HOT]
🏭 ERP
📅 周汇总 [AUTO]
👥 运营汇总 [AUTO]
🔗 广告链接
🎯 SkillHub [NEW]
📚 帮助文档
ℹ  关于我们
```

### After (data tree, Feishu-style)

```
▼ 我的店铺
    └── ⊙ 店铺健康看板          ← automation dashboard node

▼ 运营数据
    ├── ▦ 核算表          ⚡ 2   ← sheet + automation badge
    ├── ▦ 履约率          ⚡ 1
    └── ▦ 周数据汇总

▼ 广告管理
    ├── ⊙ 广告驾驶舱             ← automation dashboard node
    ├── ▦ 广告数据       [HOT]
    └── ▦ 链接汇总

▼ 库存 & ERP
    ├── ▦ 订单管理
    └── ▦ ERP数据

──────────────────────────────
⚡ 自动化                [3]   ← active workflow count
🎯 SkillHub
⚙  设置 & 数据源
──────────────────────────────
💬 openclaw (Discord)  ● 在线
```

### Node types

```
▼  = collapsible group
⊙  = automation dashboard page (Feishu clock icon pattern)
▦  = sheet node
⚡N = N active automations linked to this sheet
●  = online/connected status
```

### Sheet node hover / right-click

```
▦ 核算表              ⚡ 2
│
└── context menu:
    ┌─────────────────────────┐
    │  ⚡ 核算自动刷新  ● 运行 │
    │  ⚡ 履约率监控   ● 运行 │
    │  + 新建自动化            │
    │  ─────────────────────  │
    │  ✏ 重命名                │
    │  🗑 删除                 │
    └─────────────────────────┘
```

---

## 5. Sheet View — Smart Filter Bar

### Full sheet header layout

```
┌──────────────────────────────────────────────────────────────────────────┐
│  📊 核算表  ● Live    [+ Create ▾]  [✦ AI]  [⚡ Automations 2]  [⋮]  [👤] │
├──────────────────────────────────────────────────────────────────────────┤
│  全部 │ Shopee │ SHEIN │ TikTok │ Lazada                                 │  ← platform tabs
├──────────────────────────────────────────────────────────────────────────┤
│  今天  昨天  [近7天]  近30天  自定义                                       │  ← date quick-pick
├──────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐  [+ Apply Skill ▾]  │
│  │ 利润偏低  6  │ │ 高退款率  4  │ │ 成本超预算 3 │                      │  ← segment chips
│  │ 利润率 < 5%  │ │ 退款率 > 10% │ │ 成本环比>20% │                      │
│  └──────────────┘ └──────────────┘ └──────────────┘                      │
├──────────────────────────────────────────────────────────────────────────┤
│  [spreadsheet rows — filtered instantly on chip click]                   │
└──────────────────────────────────────────────────────────────────────────┘
```

### Segment chips by sheet type

```
核算表:
  [利润偏低  N]  利润率 < 5%
  [高退款率  N]  退款率 > 10%
  [成本超预算 N] 成本环比 > 20%

履约率表:
  [履约率低  N]  履约率 < 85%
  [延迟发货  N]  超时 > 2天
  [缺货风险  N]  库存 < 7天

广告数据:
  [ROAS偏低  N]  ROAS < 2x
  [预算耗尽  N]  消耗 > 95%
  [点击率高  N]  CTR > 5%
```

### How "instant" filter works

```
Step 1 — Load all rows once on sheet open
         store in client state (zustand/useState)

Step 2 — Count computed client-side (useMemo)
         surgeCount = rows.filter(r => r.利润率 < 0.05).length
         → badge number updates when date range changes

Step 3 — On chip click, filter in memory (no API call)
         setActiveSegment("low_profit")
         filteredRows = rows.filter(segment.rule)
         sheet re-renders instantly

Step 4 — Delta indicators (环比 ↑↓) computed client-side
         compare current period vs previous period
         both periods loaded on initial fetch
         render via custom cell extension
```

### Delta indicator cell pattern

```
Current cell:
  ┌──────────┐
  │  63.37%  │  ← current value
  │  2.52% ↑ │  ← vs last period (green ↑ / red ↓)
  └──────────┘

Implemented via existing html-cell-extension pattern.
```

---

## 6. Sheet → Workflow Automation Panel

### Header button

```
[+ Create ▾]  [✦ AI]  [⚡ Automations 2]  [⋮]
                            │
                            └── click → slide-in panel (right side)
                                        badge N = active count
```

### Automation panel (slide-in, mirrors ai-sidebar)

```
┌──────────────────────────────┐
│ ⚡ Automations          [×]  │
│ Linked to this sheet         │
│──────────────────────────────│
│  ┌────────────────────────┐  │
│  │ ● Auto Refresh         │  │
│  │   Cost Sheet (核算)    │  │
│  │   ⏰ Daily 09:00       │  │
│  │   Last run: 2h ago     │  │
│  │   [Edit →]  [▶ Run]   │  │
│  └────────────────────────┘  │
│                              │
│  ┌────────────────────────┐  │
│  │ ● Monitor              │  │
│  │   Fulfillment Rate     │  │
│  │   📊 On data change    │  │
│  │   Last run: 1d ago     │  │
│  │   [Edit →]  [▶ Run]   │  │
│  └────────────────────────┘  │
│                              │
│  ────────────────────────    │
│  [+ Create New]              │
│  [→ View all in Workspace]   │
└──────────────────────────────┘

Status dots:
● green  = running / healthy
● amber  = idle / not triggered recently
● red    = last run failed
○ gray   = disabled
```

### New automation trigger picker

```
┌──────────────────────────────────────────────┐
│  New Automation for this sheet          [×]  │
│──────────────────────────────────────────────│
│  Choose a trigger:                           │
│                                              │
│  ┌──────────────┐  ┌──────────────┐          │
│  │  ⏰ Schedule │  │  📊 On Change│          │
│  │  Run at a    │  │  Sheet data  │          │
│  │  fixed time  │  │  is updated  │          │
│  └──────────────┘  └──────────────┘          │
│                                              │
│  ┌──────────────┐                            │
│  │  ▶ Manual   │                            │
│  │  Run on     │                            │
│  │  demand     │                            │
│  └──────────────┘                            │
│                                              │
│                [Cancel]  [Next →]            │
└──────────────────────────────────────────────┘
```

### Data relationship

```
Sheet: 69b91dd6bf42f58633fdc53b
│
├── Automation 1 ──→ Workflow: "Auto Refresh Cost Sheet"
│                            trigger: schedule daily 9am
│                            status: ● active
│                            last_run: 2h ago
│
├── Automation 2 ──→ Workflow: "Monitor Fulfillment Rate"
│                            trigger: on data change
│                            status: ● active
│                            last_run: 1d ago
│
└── [+ Create New] ──→ Workflow Builder (sheet_id pre-bound)
```

---

## 7. Workspace Page — Bi-directional Linking

### Workflow card — add sheet badge

```
Before:
┌──────────────────────────────────────────────────────────────────────┐
│  ✓  v5-s4SPU-group                              👁  ✏  ⚡  ↗  🗑  │
│     🕐 Last update 37 days ago                                        │
└──────────────────────────────────────────────────────────────────────┘

After:
┌──────────────────────────────────────────────────────────────────────┐
│  ✓  v5-s4SPU-group                              👁  ✏  ⚡  ↗  🗑  │
│     🕐 Last update 37 days ago   📊 核算表 ↗                         │
└──────────────────────────────────────────────────────────────────────┘
```

### Active workflow card — add sheet context

```
┌──────────────────────────────────────────────────────────────────────┐
│  Active   多店铺周数据统计                                   ⏸  🗑  │
│  🕐 Weekly Schedule   📅 Next Run: 2026-03-20 15:00:00               │
│  📊 Bound to: 核算表 ↗                                               │
└──────────────────────────────────────────────────────────────────────┘
```

### Full navigation flow

```
Workspace (/user/workspace)
│
├── My Workflows
│     └── [card] Cost Sheet Workflow   📊 核算表 ↗
│                       └── click ↗ ──→  Sheet view (69b91dd6...)
│                                              │
│                                              └── ⚡ Automations panel
│                                                    ├── [Edit →] ──→ /user/workflow/{id}
│                                                    └── [→ View all] ──→ /user/workspace
│
└── Active Workflows
      └── [card] 多店铺周数据统计   📊 核算表 ↗
```

---

## 8. ⊙ Automation Dashboard Node (Feishu pattern)

A dedicated page-node in the tree (not just a button) that gives a full overview:

```
⊙ 运营驾驶舱 · 自动化总览
┌────────────────────────────────────────────────────────┐
│  数据源状态                                            │
│  ┌──────────────┐  ┌──────────────┐                   │
│  │ Shopee API   │  │ SHEIN API    │                   │
│  │ ● 已同步     │  │ ○ 未配置     │                   │
│  │ 5min前       │  │ [去配置 →]   │                   │
│  └──────────────┘  └──────────────┘                   │
│                                                        │
│  关联自动化                                            │
│  ┌──────────────────────────────────────────────────┐ │
│  │ ⚡ 核算自动刷新   ● 运行中   上次 2h   [编辑]    │ │
│  │    触发: 每日9:00  →  核算表                     │ │
│  └──────────────────────────────────────────────────┘ │
│  ┌──────────────────────────────────────────────────┐ │
│  │ ⚡ 履约率监控     ● 运行中   上次 1d   [编辑]    │ │
│  │    触发: 数据变更  →  履约率表                   │ │
│  └──────────────────────────────────────────────────┘ │
│                                                        │
│  [+ 新建自动化]    [→ 查看全部工作流]                  │
└────────────────────────────────────────────────────────┘
```

---

## 9. AI Copilot Panel — Context-Aware

```
┌──────────────────────────────────────────────────────┐
│  🤖 卖倍AI助手                        [Discord ↗]   │
│  当前: 核算表 · Shopee · 近7天                       │
├──────────────────────────────────────────────────────┤
│  快捷问题 (基于当前表):                              │
│  ┌──────────────────┐  ┌──────────────────┐          │
│  │ 哪些SKU利润最低? │  │ 成本超预算的商品 │          │
│  └──────────────────┘  └──────────────────┘          │
│  ┌──────────────────┐  ┌──────────────────┐          │
│  │ 本周vs上周对比   │  │ 生成执行摘要     │          │
│  └──────────────────┘  └──────────────────┘          │
│                                                      │
│  ─────────────────────────────────────────────────  │
│  🔴 SKU-A  利润率仅2.1%，建议调整定价               │
│  🟡 退款率本周上升至12%，超预警线                   │
│                                                      │
│  ─────────────────────────────────────────────────  │
│  应用技能 (SkillHub):                                │
│  ┌─────────────────────────────────────────────┐    │
│  │ 📊 广告ROI诊断    [应用到当前表]             │    │
│  │ 🔍 选品竞品分析   [应用到当前表]             │    │
│  └─────────────────────────────────────────────┘    │
│                                                      │
│  [输入问题或指令...]                   [▶] [🎤]     │
└──────────────────────────────────────────────────────┘
```

Quick questions are generated from current sheet's column headers + active segment context.
SkillHub suggestions filtered to skills relevant to current sheet type.

---

## 10. SkillHub — Embedded Not Separate Page

```
Currently: /skillhub separate page — breaks context.

SkillHub lives in 3 places:

  1. Sidebar shortcut ──→ opens as slide-in panel (not full page nav)

  2. AI copilot panel ──→ "Apply Skill" section
                          suggestions based on current sheet type

  3. Sheet filter bar ──→ [+ Apply Skill ▾] button
                          picker shows skills for THIS sheet type only
                          ┌──────────────────────────────────────────┐
                          │ 📊 广告ROI诊断   E-commerce · Ads        │
                          │ 🔍 选品竞品分析  E-commerce · Research   │
                          │ 📦 库存预警模型  E-commerce · Inventory  │
                          │ [Browse all skills →]                    │
                          └──────────────────────────────────────────┘
```

---

## 11. openclaw (Discord) — Surfaced in Web UI

```
Sidebar bottom section:

  💬 openclaw (Discord)  ● 在线
  │
  └── expand:
      ┌──────────────────────────────────────────────┐
      │  Discord已连接  ● 在线                        │
      │                                              │
      │  最近活动:                                   │
      │  📊 "核算表利润分析" · 2h前  [查看对话]       │
      │  📈 "广告ROI诊断"   · 1d前  [查看对话]       │
      │                                              │
      │  [打开Discord]  [查看全部对话历史]            │
      └──────────────────────────────────────────────┘

Why: Discord conversations generate insights that should
     surface in the web workspace, not disappear in chat history.
     Same data, two access channels, one unified workspace.
```

---

## 12. Segment Config — Where It Comes From

### 3-layer priority

```
On sheet open:

  1. User-saved custom rules (DB)      ← highest priority
       ↓ none found?
  2. AI-generated from column headers  ← smart fallback
       ↓ AI unavailable?
  3. Hardcoded defaults by sheet type  ← always works
```

### Flow

```
                      Sheet opens
                           │
           ┌───────────────▼────────────────┐
           │  Has saved segments in DB?      │
           └──────┬──────────────┬───────────┘
                 YES             NO
                  │              │
           use saved        ┌────▼─────────────────┐
           segments         │  AI detect columns    │
                            │  POST column headers  │
                            │  → Claude suggests    │
                            │    segments + rules   │
                            └────┬─────────────────┘
                                 │
                    ┌────────────▼──────────────┐
                    │ Chips shown + toast:       │
                    │ "AI configured these for   │
                    │  your sheet — customize ⚙" │
                    └────────────┬──────────────┘
                                 │
                         User clicks ⚙
                                 │
                    ┌────────────▼──────────────┐
                    │  Settings page —           │
                    │  edit thresholds, save     │
                    └───────────────────────────┘
```

### Segment rule format (stored in DB)

```json
{
  "sheet_id": "69b91dd6bf42f58633fdc53b",
  "segments": [
    {
      "id": "low_profit",
      "label": "利润偏低",
      "column": "利润率",
      "operator": "<",
      "value": 5,
      "unit": "%",
      "color": "red",
      "enabled": true
    },
    {
      "id": "high_refund",
      "label": "高退款率",
      "column": "退款率",
      "operator": ">",
      "value": 10,
      "unit": "%",
      "color": "amber",
      "enabled": true
    }
  ]
}
```

Operators: `<`  `>`  `<=`  `>=`  `=`  `!=`
Seller adjusts threshold (5% → 8%) in settings UI — just a number input, no code.

### Settings page — Segment config

```
⚙ 设置 → Sheet Segments

┌────────────────────────────────────────────────────────────────┐
│  Sheet Segments                                                │
│  Smart filter chips for your sheets                           │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  核算表                                        [+ Add Segment] │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 利润偏低    利润率 < [5] %              🔴  [编辑] [删除]│  │
│  │ 高退款率    退款率 > [10] %            🟡  [编辑] [删除]│  │
│  │ 成本超标    成本环比 > [20] %          🔴  [编辑] [删除]│  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
│  履约率表                                      [+ Add Segment] │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 履约率低    履约率 < [85] %             🔴  [编辑] [删除]│  │
│  │ 延迟发货    超时 > [2] 天               🟡  [编辑] [删除]│  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
│  [+ Add Sheet Type]                                            │
└────────────────────────────────────────────────────────────────┘
```

---

## 13. Setup Wizard — First Run Only

```
Currently: 初始化向导 always visible in sidebar (feels unfinished).

Fix: Progressive onboarding — wizard only shows until setup complete.

  First visit (no data connected):
  ┌──────────────────────────────────────────────────────┐
  │  欢迎使用卖倍AI                                      │
  │  Step 1 ──── Step 2 ──── Step 3 ──── Step 4         │
  │  接入数据    创建表格    配置工作流    完成            │
  │                                                      │
  │  [Shopee API]  [SHEIN API]  [ZIP 导入]              │
  └──────────────────────────────────────────────────────┘

  After setup complete:
  - 初始化向导 removed from sidebar permanently
  - ⚙ 设置 contains re-config when needed
  - Data source status shown as small ● indicator in tree
```

---

## 14. Backend Requirements

### New

```
sheet_automations collection / field:
  { sheet_id, workflow_id, name, trigger_type, status, last_run }

New TRPC routes:
  getAutomationsBySheetId(sheetId)     → automation panel
  getSegmentsBySheetId(sheetId)        → filter chips
  saveSegments(sheetId, segments[])    → settings page
  suggestSegments(sheetId, columns[])  → AI column detection (calls fastestai-api)
```

### Reused (zero changes)

```
/user/workflow/{id}     → Edit Workflow page (already built)
/user/workspace         → Workspace page (already built)
WorkflowsList           → reuse with sheet badge added
ScheduleWorkflowDialog  → reuse as-is
```

---

## 15. Build Priority

```
P0 — Sidebar tree restructure              pure UI, maibei-demo.tsx
     Group flat items → data tree
     Add ⊙ ▦ node types + ⚡ badge counts

P1 — ⚡ Automations button + panel         needs sheet_id on workflow doc
     Add to SpreadsheetHeader
     New AutomationPanel component (mirror ai-sidebar)

P2 — Smart filter bar (segment chips)      client-side only
     Define hardcoded rules per sheet type
     Filter rows in memory, instant re-render

P3 — Workspace bi-directional links        small addition to WorkflowsList
     📊 sheet badge on workflow cards
     [→ go to sheet] navigation

P4 — AI copilot panel upgrade              moderate
     Context-aware quick questions
     SkillHub suggestions based on sheet type

P5 — Segment settings page                 new page + TRPC routes
     User-editable thresholds
     AI auto-suggest on first open

P6 — openclaw activity in web sidebar      needs Discord history API
     Surface recent Discord conversations
     Unified web + Discord workspace feel
```

---

## 16. Key Design Principles

```
1. DATA TREE not app menu
   User navigates their data, not app features.
   Mirrors Feishu ecommerce template pattern.

2. AUTOMATION is first-class, not buried
   ⚡ badge visible on every sheet node.
   ⊙ dashboard node as dedicated page.
   Panel accessible from sheet header.

3. AI is contextual, not generic
   Copilot knows which sheet is open.
   Quick questions generated from actual columns.
   SkillHub filtered to relevant skills.

4. SEGMENTS answer "what needs attention now"
   Pre-computed, not raw numbers.
   Instant client-side filter — no API call on click.
   User-configurable thresholds via settings page.

5. DISCORD + WEB = one workspace
   OpenClaw conversations surface in web UI.
   Same data, two access channels.
   Activity log bridges the two surfaces.

6. PROGRESSIVE onboarding
   Setup wizard disappears after first run.
   Demo labels removed from production UI.
   Status indicators replace badges like [NEW] [AUTO].
```
