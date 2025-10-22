import { Paper, Stack, Typography } from '@mui/material';
import Plot from 'react-plotly.js';

import { QueryState } from '@/components/QueryState.tsx';

import type { PlotlyFigure } from '@/api/schemas.ts';
import type { Config, Layout, ModeBarDefaultButtons, PlotData } from 'plotly.js';

type PlotCardProps = {
  title: string;
  subtitle?: string;
  figure?: PlotlyFigure;
  isLoading: boolean;
  error?: Error | null;
  onRetry?: () => void;
  height?: number;
};

const DEFAULT_MODEBAR_REMOVALS: ModeBarDefaultButtons[] = [
  'lasso2d',
  'select2d',
  'autoScale2d',
  'hoverClosestCartesian',
  'hoverCompareCartesian',
  'resetScale2d',
];

export const PlotCard = ({
  title,
  subtitle,
  figure,
  isLoading,
  error,
  onRetry,
  height = 480,
}: PlotCardProps) => (
  <Paper sx={{ p: 3, height: '100%' }}>
    <Stack spacing={2}>
      <Stack spacing={0.5}>
        <Typography variant="h6">{title}</Typography>
        {subtitle ? (
          <Typography variant="body2" color="text.secondary">
            {subtitle}
          </Typography>
        ) : null}
      </Stack>
      <QueryState isLoading={isLoading} error={error} onRetry={onRetry} empty={!figure}>
        {figure ? (
          <Plot
            data={figure.data as PlotData[]}
            layout={
              {
                ...figure.layout,
                autosize: true,
                height,
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)',
                margin: { t: 48, r: 24, b: 48, l: 56, ...(figure.layout?.margin ?? {}) },
              } satisfies Partial<Layout>
            }
            config={{
              responsive: true,
              displaylogo: false,
              modeBarButtonsToRemove: DEFAULT_MODEBAR_REMOVALS,
              ...(figure.config ?? {}),
            } as Partial<Config>}
            style={{ width: '100%', height }}
            useResizeHandler
          />
        ) : null}
      </QueryState>
    </Stack>
  </Paper>
);
