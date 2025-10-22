import { Alert, Box, Button, CircularProgress, Stack, Typography } from '@mui/material';

import type { ReactNode } from 'react';

type QueryStateProps = {
  isLoading: boolean;
  error?: Error | null;
  onRetry?: () => void;
  empty?: boolean;
  emptyLabel?: string;
  children: ReactNode;
};

export const QueryState = ({
  isLoading,
  error,
  onRetry,
  empty,
  emptyLabel,
  children,
}: QueryStateProps) => {
  if (isLoading) {
    return (
      <Box
        display="flex"
        alignItems="center"
        justifyContent="center"
        minHeight={240}
        py={4}
      >
        <Stack spacing={2} alignItems="center">
          <CircularProgress />
          <Typography variant="body2" color="text.secondary">
            Loading data...
          </Typography>
        </Stack>
      </Box>
    );
  }

  if (error) {
    return (
      <Alert
        severity="error"
        action={
          onRetry ? (
            <Button color="inherit" size="small" onClick={onRetry}>
              Retry
            </Button>
          ) : undefined
        }
      >
        {error.message || 'Something went wrong while loading data.'}
      </Alert>
    );
  }

  if (empty) {
    return (
      <Box display="flex" alignItems="center" justifyContent="center" py={4}>
        <Typography variant="body2" color="text.secondary">
          {emptyLabel ?? 'No data available for the current filters.'}
        </Typography>
      </Box>
    );
  }

  return <>{children}</>;
};
