import { z } from 'zod';

const NumberOrNull = z.number().nullable();
const JsonRecord = z.record(z.string(), z.any());

export const plotlyFigureSchema = z.object({
  data: z.array(JsonRecord),
  layout: JsonRecord,
  frames: z.array(JsonRecord).optional(),
  config: JsonRecord.optional(),
});

export type PlotlyFigure = z.infer<typeof plotlyFigureSchema>;

export const stockMetricsSchema = z.object({
  symbol: z.string(),
  current_price: z.number(),
  price_change: z.number(),
  price_change_pct: z.number(),
  rsi: NumberOrNull,
  mnav_per_share: NumberOrNull,
  p_mnav_ratio: NumberOrNull,
  premium_discount_pct: NumberOrNull,
  last_updated: z.string(),
});

export type StockMetrics = z.infer<typeof stockMetricsSchema>;

export const priceTableEntrySchema = z.object({
  date: z.string(),
  open: z.number(),
  high: z.number(),
  low: z.number(),
  close: z.number(),
  volume: z.number(),
});

export type PriceTableEntry = z.infer<typeof priceTableEntrySchema>;

export const priceTableSchema = z.array(priceTableEntrySchema);
