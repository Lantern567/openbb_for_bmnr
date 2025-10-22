const normalizeUrl = (value: string) => value.replace(/\/+$/, '');

export const appConfig = {
  apiBaseUrl: normalizeUrl(
    import.meta.env.VITE_API_BASE_URL?.toString() ?? 'http://localhost:8000',
  ),
  defaultSymbol: import.meta.env.VITE_DEFAULT_SYMBOL?.toString() ?? 'BMNR',
};

export type AppConfig = typeof appConfig;
