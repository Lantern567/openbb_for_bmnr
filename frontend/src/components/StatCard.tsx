import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';
import { Chip, Paper, Stack, Typography } from '@mui/material';
import numeral from 'numeral';

type StatCardProps = {
  label: string;
  value: number | null | undefined;
  formatter?: (value: number) => string;
  change?: number | null;
  changeFormatter?: (value: number) => string;
  suffix?: string;
  prefix?: string;
};

const defaultFormatter = (value: number) => numeral(value).format('0,0.00');

export const StatCard = ({
  label,
  value,
  formatter = defaultFormatter,
  change,
  changeFormatter = (v) => numeral(v).format('+0,0.00'),
  suffix = '',
  prefix = '',
}: StatCardProps) => {
  const formattedValue =
    value === null || value === undefined ? 'N/A' : `${prefix}${formatter(value)}${suffix}`;

  const hasChange = typeof change === 'number' && !Number.isNaN(change);
  const positive = hasChange && change > 0;
  const negative = hasChange && change < 0;

  return (
    <Paper
      variant="outlined"
      sx={{
        p: 2.5,
        height: '100%',
      }}
    >
      <Stack spacing={1.5}>
        <Typography variant="overline" color="text.secondary">
          {label}
        </Typography>
        <Typography variant="h5" fontWeight={700}>
          {formattedValue}
        </Typography>
        {hasChange ? (
          <Chip
            color={positive ? 'success' : negative ? 'error' : 'default'}
            icon={positive ? <ArrowUpwardIcon /> : <ArrowDownwardIcon />}
            label={changeFormatter?.(change!)}
            size="small"
            sx={{
              alignSelf: 'flex-start',
              '& .MuiChip-icon': {
                color: 'inherit',
              },
            }}
          />
        ) : null}
      </Stack>
    </Paper>
  );
};
