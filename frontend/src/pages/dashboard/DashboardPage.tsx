import FilterAltIcon from '@mui/icons-material/FilterAlt';
import RefreshIcon from '@mui/icons-material/Refresh';
import { Button, Paper, Stack, TextField, Tooltip, Typography } from '@mui/material';
import Grid from '@mui/material/GridLegacy';
import { useMemo, useState } from 'react';

import { useMnavChart, usePriceTable, useScenarioAnalysis, useStockMetrics, useTechnicalChart } from '@/api/queries.ts';
import { PlotCard } from '@/components/PlotCard.tsx';
import { PriceTable } from '@/components/PriceTable.tsx';
import { StatCard } from '@/components/StatCard.tsx';
import { appConfig } from '@/config/env.ts';
import { useColorMode } from '@/hooks/useColorMode.ts';

import type { ChartTheme } from '@/api/stock.ts';



type DashboardFormState = {
  symbol: string;
  technicalDays: string;
  tableDays: string;
  sharesOutstanding: string;
  propertyFairValue: string;
  propertyBookValue: string;
  deferredTaxRate: string;
  scenarioConservative: string;
  scenarioBase: string;
  scenarioOptimistic: string;
};

type DashboardFilters = {
  symbol: string;
  technicalDays: number;
  tableDays: number;
  sharesOutstanding: number;
  propertyFairValue?: number;
  propertyBookValue?: number;
  deferredTaxRate?: number;
  conservativeMnav?: number;
  baseMnav?: number;
  optimisticMnav?: number;
};

const parseNumber = (value: string): number | undefined => {
  if (!value) {
    return undefined;
  }
  const normalized = value.replaceAll(',', '');
  const parsed = Number(normalized);
  if (Number.isNaN(parsed)) {
    return undefined;
  }
  return parsed;
};

const parsePercentage = (value: string): number | undefined => {
  const parsed = parseNumber(value);
  if (parsed === undefined) {
    return undefined;
  }
  return parsed / 100;
};

const clamp = (value: number, min: number, max: number) => Math.min(Math.max(value, min), max);

const INITIAL_FORM_STATE: DashboardFormState = {
  symbol: appConfig.defaultSymbol,
  technicalDays: '365',
  tableDays: '90',
  sharesOutstanding: '10000000',
  propertyFairValue: '',
  propertyBookValue: '',
  deferredTaxRate: '0',
  scenarioConservative: '',
  scenarioBase: '',
  scenarioOptimistic: '',
};

const buildFiltersFromForm = (form: DashboardFormState): DashboardFilters => {
  const symbol = form.symbol.trim().toUpperCase() || appConfig.defaultSymbol;
  const technicalDays = clamp(parseNumber(form.technicalDays) ?? 365, 30, 1095);
  const tableDays = clamp(parseNumber(form.tableDays) ?? 90, 30, 365);
  const sharesOutstanding = Math.max(parseNumber(form.sharesOutstanding) ?? 10000000, 1);
  const deferredTaxRate = parsePercentage(form.deferredTaxRate) ?? 0;

  return {
    symbol,
    technicalDays,
    tableDays,
    sharesOutstanding,
    propertyFairValue: parseNumber(form.propertyFairValue),
    propertyBookValue: parseNumber(form.propertyBookValue),
    deferredTaxRate,
    conservativeMnav: parseNumber(form.scenarioConservative),
    baseMnav: parseNumber(form.scenarioBase),
    optimisticMnav: parseNumber(form.scenarioOptimistic),
  };
};

export const DashboardPage = () => {
  const { mode } = useColorMode();
  const [formState, setFormState] = useState<DashboardFormState>(INITIAL_FORM_STATE);
  const [filters, setFilters] = useState<DashboardFilters>(() => buildFiltersFromForm(INITIAL_FORM_STATE));

  const chartTheme: ChartTheme = mode === 'dark' ? 'dark' : 'light';

  const technicalChartQuery = useTechnicalChart({
    symbol: filters.symbol,
    days: filters.technicalDays,
    theme: chartTheme,
  });

  const mnavChartQuery = useMnavChart({
    symbol: filters.symbol,
    days: filters.technicalDays,
    sharesOutstanding: filters.sharesOutstanding,
    propertyFairValue: filters.propertyFairValue,
    propertyBookValue: filters.propertyBookValue,
    deferredTaxRate: filters.deferredTaxRate,
    theme: chartTheme,
  });

  const scenarioQuery = useScenarioAnalysis({
    symbol: filters.symbol,
    sharesOutstanding: filters.sharesOutstanding,
    conservativeMnav: filters.conservativeMnav,
    baseMnav: filters.baseMnav,
    optimisticMnav: filters.optimisticMnav,
    theme: chartTheme,
  });

  const priceTableQuery = usePriceTable({
    symbol: filters.symbol,
    days: filters.tableDays,
  });

  const metricsQuery = useStockMetrics({
    symbol: filters.symbol,
    sharesOutstanding: filters.sharesOutstanding,
  });

  const metrics = metricsQuery.data;

  const handleInputChange =
    (field: keyof DashboardFormState) => (event: React.ChangeEvent<HTMLInputElement>) => {
      setFormState((prev) => ({
        ...prev,
        [field]: event.target.value,
      }));
    };

  const handleApply = () => {
    setFilters(buildFiltersFromForm(formState));
  };

  const handleReset = () => {
    setFormState(INITIAL_FORM_STATE);
    setFilters(buildFiltersFromForm(INITIAL_FORM_STATE));
  };

  const statCards = useMemo(
    () => [
      {
        label: 'Current Price',
        value: metrics?.current_price,
        prefix: '$',
        change: metrics?.price_change,
      },
      {
        label: 'Daily Change %',
        value: metrics?.price_change_pct,
        suffix: '%',
        formatter: (value: number) => value.toFixed(2),
        change: null,
      },
      {
        label: 'RSI (14)',
        value: metrics?.rsi,
        formatter: (value: number) => value.toFixed(2),
      },
      {
        label: 'mNAV per Share',
        value: metrics?.mnav_per_share,
        prefix: '$',
        change: null,
      },
      {
        label: 'P/mNAV Ratio',
        value: metrics?.p_mnav_ratio,
        formatter: (value: number) => value.toFixed(2),
      },
      {
        label: 'Premium / Discount',
        value: metrics?.premium_discount_pct,
        suffix: '%',
        formatter: (value: number) => value.toFixed(2),
      },
    ],
    [metrics],
  );

  return (
    <Stack spacing={4} pb={6}>
      <Paper sx={{ p: 3 }}>
        <Stack spacing={3}>
          <Stack direction="row" alignItems="center" spacing={1}>
            <FilterAltIcon fontSize="small" color="primary" />
            <Typography variant="h6">Analysis Filters</Typography>
          </Stack>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                label="Symbol"
                value={formState.symbol}
                onChange={handleInputChange('symbol')}
                fullWidth
                inputProps={{ style: { textTransform: 'uppercase' } }}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                label="Historical Days (Charts)"
                type="number"
                value={formState.technicalDays}
                onChange={handleInputChange('technicalDays')}
                fullWidth
                inputProps={{ min: 30, max: 1095 }}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                label="Historical Days (Table)"
                type="number"
                value={formState.tableDays}
                onChange={handleInputChange('tableDays')}
                fullWidth
                inputProps={{ min: 30, max: 365 }}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                label="Shares Outstanding"
                type="number"
                value={formState.sharesOutstanding}
                onChange={handleInputChange('sharesOutstanding')}
                fullWidth
                inputProps={{ min: 1 }}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                label="Property Fair Value"
                type="number"
                value={formState.propertyFairValue}
                onChange={handleInputChange('propertyFairValue')}
                fullWidth
                helperText="Optional override"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                label="Property Book Value"
                type="number"
                value={formState.propertyBookValue}
                onChange={handleInputChange('propertyBookValue')}
                fullWidth
                helperText="Optional override"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                label="Deferred Tax Rate %"
                type="number"
                value={formState.deferredTaxRate}
                onChange={handleInputChange('deferredTaxRate')}
                fullWidth
                helperText="Enter as percentage (e.g., 10 for 10%)"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                label="Scenario Conservative mNAV"
                type="number"
                value={formState.scenarioConservative}
                onChange={handleInputChange('scenarioConservative')}
                fullWidth
                helperText="Optional override"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                label="Scenario Base mNAV"
                type="number"
                value={formState.scenarioBase}
                onChange={handleInputChange('scenarioBase')}
                fullWidth
                helperText="Optional override"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                label="Scenario Optimistic mNAV"
                type="number"
                value={formState.scenarioOptimistic}
                onChange={handleInputChange('scenarioOptimistic')}
                fullWidth
                helperText="Optional override"
              />
            </Grid>
          </Grid>
          <Stack direction="row" spacing={2} justifyContent="flex-end">
            <Tooltip title="Restore defaults">
              <Button variant="text" color="inherit" onClick={handleReset} startIcon={<RefreshIcon />}>
                Reset
              </Button>
            </Tooltip>
            <Button variant="contained" onClick={handleApply}>
              Apply filters
            </Button>
          </Stack>
        </Stack>
      </Paper>

      <Grid container spacing={2}>
        {statCards.map((card) => (
          <Grid item xs={12} sm={6} md={4} lg={2} key={card.label}>
            <StatCard {...card} />
          </Grid>
        ))}
      </Grid>

      <Grid container spacing={2}>
        <Grid item xs={12} lg={6}>
          <PlotCard
            title="Technical Analysis"
            subtitle={`${filters.symbol} - ${filters.technicalDays} days`}
            figure={technicalChartQuery.data}
            isLoading={technicalChartQuery.isLoading}
            error={technicalChartQuery.error}
            onRetry={() => technicalChartQuery.refetch()}
            height={480}
          />
        </Grid>
        <Grid item xs={12} lg={6}>
          <PlotCard
            title="mNAV vs Price"
            subtitle={`Shares outstanding: ${filters.sharesOutstanding.toLocaleString()}`}
            figure={mnavChartQuery.data}
            isLoading={mnavChartQuery.isLoading}
            error={mnavChartQuery.error}
            onRetry={() => mnavChartQuery.refetch()}
            height={480}
          />
        </Grid>
      </Grid>

      <Grid container spacing={2}>
        <Grid item xs={12} lg={6}>
          <PlotCard
            title="mNAV Scenario Analysis"
            subtitle="Compare conservative, base, and optimistic cases against current price"
            figure={scenarioQuery.data}
            isLoading={scenarioQuery.isLoading}
            error={scenarioQuery.error}
            onRetry={() => scenarioQuery.refetch()}
            height={420}
          />
        </Grid>
        <Grid item xs={12} lg={6}>
          <PriceTable
            title={`${filters.symbol} Price History`}
            rows={priceTableQuery.data}
            isLoading={priceTableQuery.isLoading}
            error={priceTableQuery.error}
            onRetry={() => priceTableQuery.refetch()}
          />
        </Grid>
      </Grid>
    </Stack>
  );
};

export default DashboardPage;
