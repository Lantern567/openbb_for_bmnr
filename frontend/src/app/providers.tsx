import { CssBaseline, ThemeProvider } from '@mui/material';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import {
  createContext,
  type PropsWithChildren,
  useCallback,
  useEffect,
  useMemo,
  useState,
} from 'react';

import { createAppTheme } from '@/app/theme.ts';

type ColorMode = 'light' | 'dark';

type ColorModeContextValue = {
  mode: ColorMode;
  toggleMode: () => void;
  setMode: (mode: ColorMode) => void;
};

export const ColorModeContext = createContext<ColorModeContextValue | undefined>(undefined);

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

const LOCAL_STORAGE_KEY = 'openbb-color-mode';

const getInitialMode = (): ColorMode => {
  if (typeof window === 'undefined') {
    return 'dark';
  }

  const stored = window.localStorage.getItem(LOCAL_STORAGE_KEY) as ColorMode | null;
  if (stored === 'light' || stored === 'dark') {
    return stored;
  }

  if (window.matchMedia?.('(prefers-color-scheme: light)').matches) {
    return 'light';
  }

  return 'dark';
};

export const AppProviders = ({ children }: PropsWithChildren) => {
  const [mode, setMode] = useState<ColorMode>(getInitialMode);

  useEffect(() => {
    window.localStorage.setItem(LOCAL_STORAGE_KEY, mode);
  }, [mode]);

  const toggleMode = useCallback(() => {
    setMode((prev) => (prev === 'dark' ? 'light' : 'dark'));
  }, []);

  const contextValue = useMemo(
    () => ({
      mode,
      toggleMode,
      setMode,
    }),
    [mode, toggleMode],
  );

  const theme = useMemo(() => createAppTheme(mode), [mode]);

  return (
    <ColorModeContext.Provider value={contextValue}>
      <QueryClientProvider client={queryClient}>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          {children}
          <ReactQueryDevtools initialIsOpen={false} />
        </ThemeProvider>
      </QueryClientProvider>
    </ColorModeContext.Provider>
  );
};
