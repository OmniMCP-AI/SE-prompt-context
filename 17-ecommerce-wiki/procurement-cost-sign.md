# 采购成本 Sign and Formula Usage

`采购成本 < 0` in this workbook is an ERP-layer bookkeeping convention, not a report-layer display sign.

## What `采购成本` means in ERP

In the daily and weekly backfill logic, the backend writes `入库单明细.采购费用` back into `ERP.采购成本` as a negative number:

- Code: [api.py](/Users/dengwei/work/ai/maybeai-uni/fastestai-playground/src/fastestai_playground/excel/router/api.py:4293)
- Explanation: [七木.md](/Users/dengwei/work/ai/maybeai-uni/fastestai-playground/七木.md:337)

The write-back rule is:

```text
ERP.采购成本 = - round(采购费用CNY * 汇率 * 出库SKU销量, 2)
```

So in the raw `ERP` sheet, `采购成本` represents a cost outflow and is intentionally stored as a negative value.

## How report sheets use it

Report sheets do not directly use the negative ERP value as-is. They first convert it into a positive `采购总成本`.

In `日数据-all`, the SQL formula defines:

```sql
ABS(SUM(COALESCE(CAST(trim("采购成本") AS REAL), 0))) AS buy_cost_sum
```

Then it maps:

```text
buy_cost_sum AS "采购总成本"
```

This positive `采购总成本` is then used in profit formulas:

- `产品毛利润 = 订单收入 - 采购总成本`
- `产品毛利润率 = 产品毛利润 / 销售额`
- `市场毛利润 = 产品毛利润 - 营销成本`

## Workbook-level formula usage

In downstream report sheets such as `日数据-小组` and `日数据-家具家居`:

- `Q = 采购总成本`
- `S = 产品毛利润 = N - Q - R`

That means:

```text
产品毛利润 = 订单收入 - 采购总成本 - 自配送费用
```

So the report logic uses the positive cost amount after normalization, not the negative sign from the raw ERP field.

## Practical interpretation

- `ERP.采购成本 < 0`: normal in raw data
- `采购总成本 > 0`: normal in report sheets
- If some ERP rows use positive cost while others use negative cost, report aggregation can become inconsistent

## Conclusion

This pipeline assumes:

1. Raw `ERP.采购成本` is stored as a negative cost/outflow field.
2. Report layers convert it with `ABS(...)` into positive `采购总成本`.
3. Profit formulas subtract `采购总成本` from `订单收入`.
