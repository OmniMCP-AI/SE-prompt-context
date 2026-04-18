# MaybeAI Ecommerce AI UX Solution

> Last updated: 2026-03-20
> Scope: `app-factory/apps/clawAI`, `app-factory/apps/chat`, `openclaw-deploy`

---

## Positioning

MaybeAI should not feel like:
- a BI dashboard
- a spreadsheet tool
- a workflow builder
- a chat assistant

It should feel like one product:

```text
Ecommerce AI Operating System
|
|-- Connect data
|-- Monitor business
|-- Investigate issues
|-- Take action
|-- Automate repeat work
```

Core loop:

```text
Monitor -> Investigate -> Act -> Automate
```

This is the main UX principle for all pages.

---

## Current Strengths To Build Around

Existing surfaces already support the right direction:

- `app-factory/apps/clawAI/app/components/maibei-demo.tsx`
  - seller-facing shell with business modules
- `app-factory/apps/clawAI/app/components/setup-wizard.tsx`
  - onboarding, sheet creation, workflow forking, ingestion
- `app-factory/apps/chat/app/components/spreadsheet/ai-sidebar/*`
  - in-sheet AI copilot, sheet/range context, OpenClaw support
- `app-factory/apps/clawAI/app/components/skillhub.tsx`
  - reusable business skills and templates
- `openclaw-deploy/mac-mini/ARCHITECTURE.md`
  - assistant can answer data questions and edit sheets across channels

Conclusion: the opportunity is not new capability; it is product unification.

---

## Product Model

The primary object should be:

```text
Store / Seller Workspace
   |
   |-- Data Sources
   |-- Business Views
   |-- Sheets
   |-- Automations
   |-- AI Assistant
   |-- Skills / Templates
```

Do not center the product on internal concepts like `workflow_id`, `sheet_id`, or tool pages.

For ecommerce users, visible language should be:
- low margin SKUs
- ad ROI anomaly
- fulfillment risk
- weekly summary
- influencer collaboration progress

Use `workflow`, `skill`, and `sheet` as secondary concepts.

---

## Recommended Information Architecture

```text
卖倍AI
|
|-- Overview
|-- Data Sources
|   |-- Store Connections
|   |-- Import History
|   |-- Sync Health
|
|-- Operations
|   |-- Orders
|   |-- Ads
|   |-- ERP
|   |-- Weekly Summary
|   |-- Influencer / Live
|
|-- Sheets
|   |-- 商品表
|   |-- 核算表
|   |-- 履约表
|
|-- Automations
|   |-- Automation Center
|   |-- Workflow Templates
|   |-- Run History
|
|-- AI
|   |-- Assistant
|   |-- SkillHub
|
|-- Help
```

Design goal:
- navigation by business job
- not by implementation module

---

## Page Roles

### 1. Overview

Purpose:
- business health
- anomalies
- recommended actions
- assistant entry

Suggested structure:

```text
+--------------------------------------------------------------------------------+
| Overview                                                                       |
| [销量暴涨 71] [低利润 6] [高退款率 4] [履约异常 12]                              |
|--------------------------------------------------------------------------------|
| filtered table / ranked list / alerts                                          |
|--------------------------------------------------------------------------------|
| Quick actions: [Ask AI] [Create Alert] [Create Automation] [Export]            |
+--------------------------------------------------------------------------------+
```

### 2. Data Sources

Current setup/config experience should become a live control center, not only onboarding.

Responsibilities:
- connect Shopee / SHEIN / TikTok / Lazada
- upload ZIP
- monitor sync health
- show related sheets
- suggest recommended automations

Suggested structure:

```text
+--------------------------------------------------------------------------------+
| Data Sources                                                   [Automation Hub]|
|--------------------------------------------------------------------------------|
| Store connections | Last sync | Failed syncs | Import history                  |
|--------------------------------------------------------------------------------|
| Recommended automations                                                        |
| Auto refresh cost sheet         [Enable]                                       |
| Monitor fulfillment rate        [Enable]                                       |
| Weekly store summary            [Enable]                                       |
+--------------------------------------------------------------------------------+
```

### 3. Operations Pages

These should use instant in-place filtering like strong BI products.

Pattern:

```text
[全部] [销量暴涨 71] [低销量 103] [高退款率 4] [低利润 6] [履约异常 12]
--------------------------------------------------------------------------------
table refreshes instantly below
```

Why:
- no page jump
- no context loss
- users inspect and act faster

### 4. Sheets

Sheets remain the flexible investigation workspace, but need a business control layer above them.

Pattern:

```text
+--------------------------------------------------------------------------------+
| 商品表   Live   | Used by 2 workflows                   [AI] [Automation 2]    |
| 来源: Shopee API | Last sync: 5 min ago                                      |
|--------------------------------------------------------------------------------|
| [全部] [销量暴涨] [低利润] [高退款率] [履约异常]                                |
|--------------------------------------------------------------------------------|
| spreadsheet canvas                                                              |
+--------------------------------------------------------------------------------+
```

### 5. Automations

Automation should be a first-class object, but not the first place users land.

Recommended role:
- quick management from sheet or business page
- deep management in Automation Center / workflow page

### 6. AI

The assistant should be a control layer, not a utility panel.

Recommended modes:

```text
[Ask] [Analyze] [Edit] [Automate]
```

Examples:
- Ask: why did fulfillment rate drop this week?
- Analyze: compare Thailand vs Malaysia low-margin SKUs
- Edit: add a column for margin band
- Automate: monitor this segment every morning and notify ops

---

## Sheet <-> Workflow Relationship Model

Relationship:

```text
Sheet 1 -> N Workflows
```

Recommended UX:
- top-right `Automation` button in sheet header
- visible badge count
- lightweight right drawer
- deep links into existing workflow pages

Header pattern:

```text
[AI Assistant] [Automation 2] [More]
```

Drawer pattern:

```text
+--------------------------------------------------------------+
| Automation for this sheet                                [X] |
|--------------------------------------------------------------|
| Source sheet: 商品表                                          |
| [ + Create automation ]                                      |
|--------------------------------------------------------------|
| Auto refresh cost sheet                            Active    |
| Trigger: On sheet update                                      |
| Last run: 2 min ago                                           |
| [Open workflow] [Pause]                                       |
|--------------------------------------------------------------|
| Monitor fulfillment rate                          Active     |
| Trigger: Weekly                                               |
| Next run: 2026-03-20 15:00                                    |
| [Open workflow] [Pause]                                       |
|--------------------------------------------------------------|
| [View all in Workspace]                                       |
+--------------------------------------------------------------+
```

Use current workflow/workspace page as the deep-management destination, not as the only entry.

Recommended link style:

```text
/workspace?sheetId=<sheetId>&source=sheet
```

The workflow editor should also link back to the source sheet:

```text
Source sheet: 商品表 [Open sheet]
```

This creates two-way navigation:

```text
Sheet -> Automation Drawer -> Workflow Editor
Workflow Editor -> Source Sheet
```

---

## Segment Cards / Business Filters

The segment cards proposed in the UX are a configurable business layer above table/sheet views.

Definition:

```text
Segment card = saved business rule + count + action entry
```

Example:

```text
[销量暴涨 71]
=> sales_growth_7d > 30%
```

Recommended source of truth:
- config table or config sheet

Example schema:

```text
| id               | name     | scope   | rule                    | color  | enabled |
| sales_spike      | 销量暴涨 | product | sales_growth_7d > 30    | blue   | true    |
| low_margin       | 低利润   | product | profit_rate < 0.05      | red    | true    |
| high_refund      | 高退款率 | product | refund_rate > 0.10      | orange | true    |
| fulfillment_risk | 履约异常 | order   | fulfillment_rate < 0.95 | gold   | true    |
```

Recommended rollout:

### Phase 1
- source of truth in config table
- cards render from config
- clicking card filters table/sheet instantly

### Phase 2
- add `Manage Segments` page or drawer
- admin edits label, threshold, color, order, enabled status

### Phase 3
- AI-assisted config
- create segment from prompt
- turn current filter into segment
- create automation from segment

Important:
- end users should interact with cards
- admins can manage via form UI
- config table remains the backend source of truth

---

## Assistant UX Strategy

OpenClaw capability means the assistant can be more than chat:
- answer business questions
- query table/sheet data
- edit sheet content
- automate actions
- work across web and external channels

This should be visible in UX.

Recommended unified assistant model:

```text
Same brain, different surfaces
|
|-- Overview assistant
|-- Operations assistant
|-- Sheet assistant
|-- Discord / external assistant
```

Recommended assistant context chips:

On a business page:

```text
Context: Shopee Thailand | 商品利润分析 | 最近30天 | 筛选: 高退款率
```

On a sheet:

```text
Context: 商品表 | Sheet range A1:H120 | Linked to 2 workflows
```

Recommended persistent right rail:

```text
| AI Assistant |
| Automation   |
| Activity     |
```

Tab roles:
- `AI Assistant`: ask, analyze, edit, automate
- `Automation`: linked workflows, create new, open workflow
- `Activity`: recent runs, sync events, failures, assistant actions

---

## SkillHub Positioning

SkillHub should not remain a standalone discovery page only.

It should become:
- capability marketplace
- workflow starter kit
- assistant prompt pack
- merchant playbook library

Recommended contextual entry points:
- from assistant suggestions
- from `Create automation`
- from a filtered segment
- from setup recommendations

Good actions:
- `Use skill`
- `Run on current sheet`
- `Create automation from skill`
- `Ask AI with this skill`

---

## Recommended UX Patterns By Journey

### Journey A: onboarding

```text
Connect store / upload ZIP
-> create sheets
-> fork starter workflows
-> verify sync
-> land in Overview
```

### Journey B: investigate anomaly

```text
See KPI / segment card
-> click segment
-> table or sheet refreshes instantly
-> inspect rows
-> ask assistant why
-> assistant suggests action
```

### Journey C: operationalize insight

```text
filtered segment
-> create automation
-> link to sheet/workflow
-> monitor in Automation Center
```

### Journey D: collaborate with assistant

```text
user asks in web or Discord
-> assistant uses same business context
-> reads data / edits sheet / triggers automation
```

---

## Design Principles

### 1. Business-first language

Prefer:
- low margin SKUs
- fulfillment risk
- ad ROI anomaly
- weekly summary

Over:
- workflow
- trigger
- automation type
- spreadsheet artifact

### 2. In-place update over page jump

When clicking segment cards or insights:
- update only table/sheet region
- avoid whole-page reload
- keep header, filters, context stable

### 3. Visible relationships

Every important page should expose linked objects:
- on config page: related sheets + recommended automations
- on sheet page: used by workflows
- on workflow page: source sheet and destination sheet

### 4. Same assistant identity everywhere

Users should feel:
- there is one assistant
- it understands the current page
- it can help investigate, edit, and automate

### 5. Use sheets as canvas, not as the whole product

Sheets are strong because users trust them.
But the product layer above sheets should provide:
- business segments
- automation relationships
- assistant context
- recommended actions

---

## Suggested MVP Sequence

### MVP 1
- clean left-nav IA
- add `Automation` to main navigation
- convert config/setup page into Data Sources control center

### MVP 2
- add segment cards above business tables
- instant in-place table refresh
- quick actions below filtered results

### MVP 3
- add sheet header `Automation` button with count badge
- add sheet-scoped automation drawer
- deep-link to existing workflow/workspace page

### MVP 4
- unify assistant modes: Ask / Analyze / Edit / Automate
- expose assistant consistently on Overview, Operations, and Sheets

### MVP 5
- connect SkillHub contextually to automations and assistant suggestions

---

## Summary

The best direction is:

```text
Seller Workspace
|
|-- Monitor business
|-- Investigate with table/sheet
|-- Ask AI in context
|-- Take action
|-- Automate what repeats
```

This gives MaybeAI a stronger position than a normal BI tool or sheet app because it combines:
- ecommerce business views
- spreadsheet flexibility
- workflow automation
- OpenClaw assistant capability
- reusable skills/templates

The product should feel like one connected ecommerce AI system, not several separate tools.
