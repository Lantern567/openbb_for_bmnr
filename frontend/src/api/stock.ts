import { apiClient, buildQueryString } from '@/api/client.ts';
import {
  plotlyFigureSchema,
  priceTableSchema,
  stockMetricsSchema,
  type PlotlyFigure,
  type PriceTableEntry,
  type StockMetrics,
} from '@/api/schemas.ts';

const endpoints = {
  technicalChart: '/bmnr/technical_chart',
  mnavChart: '/bmnr/mnav_chart',
  priceTable: '/bmnr/price_table',
  metrics: '/bmnr/metrics',
  scenarioAnalysis: '/bmnr/scenario_analysis',
} as const;

export type ChartTheme = 'dark' | 'light';

export type TechnicalChartParams = {
  symbol: string;
  days: number;
  theme: ChartTheme;
};

export type MnavChartParams = {
  symbol: string;
  days: number;
  sharesOutstanding: number;
  propertyFairValue?: number;
  propertyBookValue?: number;
  deferredTaxRate?: number;
  theme: ChartTheme;
};

export type ScenarioAnalysisParams = {
  symbol: string;
  sharesOutstanding: number;
  conservativeMnav?: number;
  baseMnav?: number;
  optimisticMnav?: number;
  theme: ChartTheme;
};

export type PriceTableParams = {
  symbol: string;
  days: number;
};

export type MetricsParams = {
  symbol: string;
  sharesOutstanding: number;
};

export const fetchTechnicalChart = async (
  params: TechnicalChartParams,
): Promise<PlotlyFigure> => {
  const query = buildQueryString({
    symbol: params.symbol,
    days: params.days,
    theme: params.theme,
  });
  const { data } = await apiClient.get(`${endpoints.technicalChart}?${query}`);
  return plotlyFigureSchema.parse(data);
};

export const fetchMnavChart = async (params: MnavChartParams): Promise<PlotlyFigure> => {
  const query = buildQueryString({
    symbol: params.symbol,
    days: params.days,
    shares_outstanding: params.sharesOutstanding,
    property_fair_value: params.propertyFairValue,
    property_book_value: params.propertyBookValue,
    deferred_tax_rate: params.deferredTaxRate,
    theme: params.theme,
  });

  const { data } = await apiClient.get(`${endpoints.mnavChart}?${query}`);
  return plotlyFigureSchema.parse(data);
};

export const fetchScenarioAnalysis = async (
  params: ScenarioAnalysisParams,
): Promise<PlotlyFigure> => {
  const query = buildQueryString({
    symbol: params.symbol,
    shares_outstanding: params.sharesOutstanding,
    conservative_mnav: params.conservativeMnav,
    base_mnav: params.baseMnav,
    optimistic_mnav: params.optimisticMnav,
    theme: params.theme,
  });

  const { data } = await apiClient.get(`${endpoints.scenarioAnalysis}?${query}`);
  return plotlyFigureSchema.parse(data);
};

export const fetchPriceTable = async (params: PriceTableParams): Promise<PriceTableEntry[]> => {
  const query = buildQueryString({
    symbol: params.symbol,
    days: params.days,
  });

  const { data } = await apiClient.get(`${endpoints.priceTable}?${query}`);
  return priceTableSchema.parse(data);
};

export const fetchMetrics = async (params: MetricsParams): Promise<StockMetrics> => {
  const query = buildQueryString({
    symbol: params.symbol,
    shares_outstanding: params.sharesOutstanding,
  });

  const { data } = await apiClient.get(`${endpoints.metrics}?${query}`);
  return stockMetricsSchema.parse(data);
};
