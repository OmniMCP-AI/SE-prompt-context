# Sheet Harness Plan

## Goal

Make LLM-generated spreadsheet output reliable for ecommerce product research workflows by separating:

1. research generation
2. sheet contract enforcement
3. write + style application
4. post-write verification
5. optional evaluator/reviewer logic

The target outcome is:

- date columns display as `yyyy-mm-dd`
- numeric business columns store raw numbers only
- currency/unit symbols are handled by style or header semantics, not embedded in cell values
- sheet writes become deterministic enough for non-technical users

## Problem Summary

Observed failure modes:

1. LLM output is not strictly formatted.
2. The ecommerce research skill focuses on research quality, not cell-level formatting.
3. There is no mandatory revise/verify loop after write-back.
4. Some failures may come from backend or sheet-write behavior, but the current harness does not isolate them.

Example issues seen in sheets:

- date column contains Excel serials like `46126`
- number-only columns contain `RMB 67.04`, `$25.62`, `$384,300.00`
- mixed-content cells are written into typed columns
- values may be semantically correct but displayed incorrectly because style is missing

## Harness Strategy

Follow the staged harness approach:

### Phase 1: Strong Harness

Use a single execution path with strong constraints.

- Research agent outputs structured row JSON, not final sheet-ready prose
- Harness reads headers first
- Harness builds a sheet output contract
- Harness normalizes values before write
- Harness writes with header-aware APIs
- Harness applies styles explicitly

### Phase 2: Deterministic Feedback Loop

Add computational verification after write.

- Read back with `UNFORMATTED_VALUE` to verify raw storage type
- Read back with `FORMATTED_VALUE` to verify display result
- Compare actual values against the contract
- Repair only the cells/columns that violate the contract

Important note:

- MCP `read_sheet` already supports `value_render_option`
- REST `/api/read_sheet` should also support `value_render_option` for parity

### Phase 3: Evaluator-in-Loop

Add an independent LLM reviewer only after deterministic checks exist.

- reviewer sees headers, expected contract, raw values, formatted values, style summary
- reviewer catches semantic mistakes not covered by deterministic rules
- reviewer proposes minimal fixes

## Recommended Architecture

### Pattern

Start with `single agent + strong harness`, then grow into `evaluator-in-loop`.

Do not start with free-form research agent -> direct sheet write.

### Logical Components

1. Research Agent
2. Sheet Contract Builder
3. Row Normalizer
4. Sheet Writer
5. Style Applier
6. Deterministic Verifier
7. Optional LLM Evaluator

## Phase 1 Proper Implementation

Phase 1 should not be implemented as prompt text only. It should be an explicit contract-driven layer in code.

### 1. Sheet Output Contract

Build a per-worksheet contract:

`header -> expected_type + format_code + sanitizer + validator + write_policy`

Suggested contract shape:

```json
{
  "worksheet": "Products",
  "headers": {
    "日期": {
      "expected_type": "date",
      "format_code": "yyyy-mm-dd",
      "write_policy": "raw_date_or_excel_date",
      "sanitizer": "date",
      "validator": "date"
    },
    "客单价 (¥)": {
      "expected_type": "decimal",
      "format_code": "0.00",
      "write_policy": "number_only",
      "sanitizer": "currency_to_number",
      "validator": "decimal"
    },
    "预估月 GMV (¥)": {
      "expected_type": "decimal",
      "format_code": "#,##0.00",
      "write_policy": "number_only",
      "sanitizer": "currency_to_number",
      "validator": "decimal"
    }
  }
}
```

### 2. Contract Source Priority

The contract should be resolved in this order:

1. explicit template schema registry
2. header-name rules
3. heuristic inference from header text
4. fallback to text/general

This is important:

- for stable ecommerce templates, use a schema registry
- do not rely on header guessing alone
- heuristics are fallback only

### 3. Schema Registry

Add a reusable registry for known templates and known headers.

Two levels are recommended:

1. worksheet/template-level schema
2. global header-level defaults

Example:

- template `shopee_competitor_products_v1`
- global header rule for `日期`
- global header rule for `/GMV/`
- global header rule for `/客单价/`

This avoids repeated inference drift across runs.

### 4. Expected Types

Recommended initial types:

- `text`
- `integer`
- `decimal`
- `percent`
- `date`
- `datetime`
- `url`
- `image_url`
- `enum`

If uncertain, use `text`.

### 5. Write Policies

Write policy must be separate from expected type.

Examples:

- `number_only`
- `preserve_text_exactly`
- `raw_date_or_excel_date`
- `formula_allowed`
- `url_text`

This matters because some columns are text even if they contain digits.

### 6. Sanitizers

Sanitizers should be deterministic functions, not LLM reasoning.

Recommended initial sanitizer set:

- `trim`
- `normalize_whitespace`
- `date`
- `currency_to_number`
- `percent_to_number`
- `integer`
- `decimal`
- `url`
- `pass_through_text`

Examples:

- `RMB 67.04` -> `67.04`
- `$384,300.00` -> `384300.00`
- `2026/04/14` -> `2026-04-14`
- `约24件/月（30天6条评论×4）` stays text

### 7. Validators

Validators should check:

- type validity
- empty/null policy
- allowed range where needed
- output form after sanitization

Examples:

- date must parse and normalize to `yyyy-mm-dd`
- decimal must become a raw number
- integer must not contain decimal places
- text columns must not be auto-coerced to numeric unless explicitly configured

## Suggested Execution Flow

### Step A: Read Headers

Use `read_headers` first.

Optional:

- read a narrow sample with `read_sheet` if headers alone are not enough

### Step B: Build Contract

Resolve:

- worksheet schema if known
- header-level defaults
- heuristic fallback

Produce a concrete contract object for the current worksheet.

### Step C: Generate Structured Rows

The research agent must output row objects keyed by header name.

It should not output:

- display-formatted currency strings for numeric columns
- free-form markdown
- combined commentary inside typed cells

### Step D: Normalize Rows

For each cell:

1. look up header contract
2. apply sanitizer
3. validate
4. either:
   - accept normalized value
   - downgrade to text if allowed
   - reject and log contract violation

### Step E: Write Values

Prefer header-aware APIs:

- `update_data_keep_headers`
- `update_range_by_lookup`

Avoid blind positional append for this workflow unless the target is append-only and contract-safe.

### Step F: Apply Styles

Apply styles by column/range after writing values.

Use explicit `format_code` values.

Examples:

- `日期` -> `yyyy-mm-dd`
- `客单价 (¥)` -> `0.00`
- `预估月 GMV (¥)` -> `#,##0.00` or `#,##0`

Do not use generic `currency` format for RMB-labeled columns if it injects `$`.

## Verification Design

### Deterministic Verification Inputs

After write:

1. read back with `UNFORMATTED_VALUE`
2. read back with `FORMATTED_VALUE`
3. optionally inspect styles

### What to Verify

For each column:

- raw type matches expected type
- formatted display matches expected format
- forbidden symbols are absent from number-only columns
- date columns do not show serials

### Example Checks

- `日期`
  - raw value must be parseable as date/date-serial
  - formatted value must match `^\d{4}-\d{2}-\d{2}$`
- `客单价 (¥)`
  - raw value must be numeric
  - formatted value must not contain `RMB` or `$`
- `预估月 GMV (¥)`
  - raw value must be numeric
  - formatted value must not contain currency prefixes

## Repair Loop

If verification fails:

1. classify failure
2. choose repair action
3. re-read only affected range if needed
4. patch value or style

Failure classes:

- wrong raw value
- correct raw value, wrong style
- wrong column mapping
- unsupported mixed-content output

## Recommended Code Shape

Implement Phase 1 as code modules, not prompt fragments.

Suggested modules:

1. `sheet_contract_registry`
   - template schemas
   - header-level defaults

2. `sheet_contract_inference`
   - fallback header heuristics

3. `sheet_normalizers`
   - deterministic sanitizer functions

4. `sheet_validators`
   - type and format validators

5. `sheet_write_orchestrator`
   - read headers
   - build contract
   - normalize
   - write
   - style

6. `sheet_verifier`
   - raw/formatted comparison

## Skill Changes

The ecommerce research skill should change responsibility:

### Current Problem

- skill is optimized for research output
- skill is not optimized for typed spreadsheet output

### Recommended Change

Research skill returns:

- structured row objects
- optional notes field
- optional evidence field

Sheet skill / harness handles:

- type coercion
- formatting
- write order
- style application
- verification

## Initial Rollout Recommendation

### MVP

1. create schema registry for the target ecommerce template
2. implement contract builder
3. implement sanitizer + validator set for:
   - date
   - integer
   - decimal
   - text
4. write using `update_data_keep_headers`
5. apply `batch_set_cell_style`
6. verify with MCP `read_sheet`

### Hardening

Add regression tests for:

- `46126` in date column
- `RMB 67.04` in numeric column
- `$384,300.00` in number-only GMV column
- mixed text in numeric field
- unknown headers defaulting to text

## Non-Goals for Phase 1

Do not attempt all of these immediately:

- full semantic LLM judging
- automatic schema learning from arbitrary unknown sheets
- universal support for every business template
- full backend bug attribution

Phase 1 should prioritize deterministic correctness for known ecommerce templates.

## Implementation Guidance Summary

The correct implementation is:

- explicit contract object
- deterministic sanitization
- deterministic validation
- header-aware write path
- explicit style application

It is not:

- a better prompt alone
- free-form research agent direct-to-sheet
- LLM-only revise loop without typed checks

