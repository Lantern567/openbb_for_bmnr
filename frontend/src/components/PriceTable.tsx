import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from '@mui/material';
import dayjs from 'dayjs';

import { QueryState } from '@/components/QueryState.tsx';

import type { PriceTableEntry } from '@/api/schemas.ts';

const HEADERS: Array<{ key: keyof PriceTableEntry; label: string; align?: 'right' | 'left' }> = [
  { key: 'date', label: 'Date' },
  { key: 'open', label: 'Open', align: 'right' },
  { key: 'high', label: 'High', align: 'right' },
  { key: 'low', label: 'Low', align: 'right' },
  { key: 'close', label: 'Close', align: 'right' },
  { key: 'volume', label: 'Volume', align: 'right' },
];

type PriceTableProps = {
  title?: string;
  rows?: PriceTableEntry[];
  isLoading: boolean;
  error?: Error | null;
  onRetry?: () => void;
};

export const PriceTable = ({ title, rows, isLoading, error, onRetry }: PriceTableProps) => (
  <Paper sx={{ p: 3 }}>
    <Typography variant="h6" gutterBottom>
      {title ?? 'Historical Prices'}
    </Typography>
    <QueryState
      isLoading={isLoading}
      error={error}
      onRetry={onRetry}
      empty={!rows || rows.length === 0}
      emptyLabel="Price history is unavailable for the selected range."
    >
      <TableContainer sx={{ maxHeight: 480, mt: 2 }}>
        <Table size="small" stickyHeader>
          <TableHead>
            <TableRow>
              {HEADERS.map((header) => (
                <TableCell key={header.key} align={header.align ?? 'left'}>
                  {header.label}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {rows?.map((row) => (
              <TableRow key={row.date} hover>
                <TableCell>{dayjs(row.date).format('YYYY-MM-DD')}</TableCell>
                <TableCell align="right">{row.open.toFixed(2)}</TableCell>
                <TableCell align="right">{row.high.toFixed(2)}</TableCell>
                <TableCell align="right">{row.low.toFixed(2)}</TableCell>
                <TableCell align="right">{row.close.toFixed(2)}</TableCell>
                <TableCell align="right">{row.volume.toLocaleString()}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </QueryState>
  </Paper>
);
