import { useQuery, type UseQueryOptions } from '@tanstack/react-query';

import {
  fetchMnavChart,
  fetchMetrics,
  fetchPriceTable,
  fetchScenarioAnalysis,
  fetchTechnicalChart,
} from '@/api/stock.ts';

import type { PlotlyFigure, PriceTableEntry, StockMetrics } from '@/api/schemas.ts';
import type {
  MetricsParams,
  MnavChartParams,
  PriceTableParams,
  ScenarioAnalysisParams,
  TechnicalChartParams,
} from '@/api/stock.ts';

export const queryKeys = {
  technicalChart: (params: TechnicalChartParams) => [
    'technical-chart',
    params.symbol,
    params.days,
    params.theme,
  ],
  mnavChart: (params: MnavChartParams) => [
    'mnav-chart',
    params.symbol,
    params.days,
    params.theme,
    params.sharesOutstanding,
    params.propertyFairValue,
    params.propertyBookValue,
    params.deferredTaxRate,
  ],
  scenarioAnalysis: (params: ScenarioAnalysisParams) => [
    'scenario-analysis',
    params.symbol,
    params.theme,
    params.sharesOutstanding,
    params.conservativeMnav,
    params.baseMnav,
    params.optimisticMnav,
  ],
  priceTable: (params: PriceTableParams) => ['price-table', params.symbol, params.days],
  metrics: (params: MetricsParams) => ['metrics', params.symbol, params.sharesOutstanding],
} as const;

export const useTechnicalChart = (
  params: TechnicalChartParams,
  options?: UseQueryOptions<PlotlyFigure, Error>,
) =>
  useQuery<PlotlyFigure, Error>({
    queryKey: queryKeys.technicalChart(params),
    queryFn: () => fetchTechnicalChart(params),
    staleTime: 1000 * 60 * 5,
    ...options,
  });

export const useMnavChart = (
  params: MnavChartParams,
  options?: UseQueryOptions<PlotlyFigure, Error>,
) =>
  useQuery<PlotlyFigure, Error>({
    queryKey: queryKeys.mnavChart(params),
    queryFn: () => fetchMnavChart(params),
    staleTime: 1000 * 60 * 5,
    ...options,
  });

export const useScenarioAnalysis = (
  params: ScenarioAnalysisParams,
  options?: UseQueryOptions<PlotlyFigure, Error>,
) =>
  useQuery<PlotlyFigure, Error>({
    queryKey: queryKeys.scenarioAnalysis(params),
    queryFn: () => fetchScenarioAnalysis(params),
    staleTime: 1000 * 60 * 5,
    ...options,
  });

export const usePriceTable = (
  params: PriceTableParams,
  options?: UseQueryOptions<PriceTableEntry[], Error>,
) =>
  useQuery<PriceTableEntry[], Error>({
    queryKey: queryKeys.priceTable(params),
    queryFn: () => fetchPriceTable(params),
    staleTime: 1000 * 60 * 5,
    ...options,
  });

export const useStockMetrics = (
  params: MetricsParams,
  options?: UseQueryOptions<StockMetrics, Error>,
) =>
  useQuery<StockMetrics, Error>({
    queryKey: queryKeys.metrics(params),
    queryFn: () => fetchMetrics(params),
    staleTime: 1000 * 60,
    ...options,
  });
