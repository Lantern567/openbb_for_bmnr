import { alpha, createTheme } from '@mui/material/styles';

const darkPalette = {
  primary: {
    main: '#00acff',
  },
  secondary: {
    main: '#5864ff',
  },
  background: {
    default: '#0f1015',
    paper: '#161721',
  },
  text: {
    primary: '#f7f9fb',
    secondary: alpha('#f7f9fb', 0.72),
  },
};

const lightPalette = {
  primary: {
    main: '#0052cc',
  },
  secondary: {
    main: '#5864ff',
  },
  background: {
    default: '#f5f7fb',
    paper: '#ffffff',
  },
  text: {
    primary: '#0b0d18',
    secondary: alpha('#0b0d18', 0.72),
  },
};

export const createAppTheme = (mode: 'light' | 'dark') =>
  createTheme({
    palette: {
      mode,
      ...(mode === 'dark' ? darkPalette : lightPalette),
    },
    typography: {
      fontFamily:
        "'Inter', 'Segoe UI', Roboto, -apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif",
      h1: {
        fontWeight: 700,
      },
      h2: {
        fontWeight: 700,
      },
      h3: {
        fontWeight: 600,
      },
    },
    shape: {
      borderRadius: 12,
    },
    components: {
      MuiPaper: {
        styleOverrides: {
          root: {
            backgroundImage: 'none',
          },
        },
      },
      MuiButton: {
        defaultProps: {
          disableElevation: true,
        },
        styleOverrides: {
          root: {
            textTransform: 'none',
            fontWeight: 600,
            borderRadius: 999,
          },
        },
      },
      MuiTableHead: {
        styleOverrides: {
          root: {
            '& .MuiTableCell-head': {
              fontWeight: 600,
            },
          },
        },
      },
    },
  });
