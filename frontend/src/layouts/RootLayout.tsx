import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';
import {
  AppBar,
  Box,
  Container,
  IconButton,
  Stack,
  Toolbar,
  Tooltip,
  Typography,
} from '@mui/material';
import { Outlet } from 'react-router-dom';

import { appConfig } from '@/config/env.ts';
import { useColorMode } from '@/hooks/useColorMode.ts';

export const RootLayout = () => {
  const { mode, toggleMode } = useColorMode();

  return (
    <Box display="flex" flexDirection="column" minHeight="100vh">
      <AppBar
        position="sticky"
        enableColorOnDark
        color="transparent"
        elevation={0}
        sx={{ backdropFilter: 'blur(16px)', borderBottom: '1px solid', borderColor: 'divider' }}
      >
        <Toolbar sx={{ minHeight: { xs: 64, sm: 72 } }}>
          <Stack
            direction="row"
            alignItems="center"
            justifyContent="space-between"
            width="100%"
            spacing={3}
          >
            <Box>
              <Typography variant="h6" component="div" fontWeight={700}>
                OpenBB Workspace Dashboard
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Connected to backend at {appConfig.apiBaseUrl}
              </Typography>
            </Box>
            <Tooltip title={`Switch to ${mode === 'dark' ? 'light' : 'dark'} mode`}>
              <IconButton color="inherit" onClick={toggleMode} aria-label="toggle color mode">
                {mode === 'dark' ? <Brightness7Icon /> : <Brightness4Icon />}
              </IconButton>
            </Tooltip>
          </Stack>
        </Toolbar>
      </AppBar>
      <Box component="main" flexGrow={1} py={{ xs: 3, sm: 4 }} bgcolor="background.default">
        <Container maxWidth="xl">
          <Outlet />
        </Container>
      </Box>
      <Box component="footer" py={3} borderTop="1px solid" borderColor="divider">
        <Container maxWidth="xl">
          <Typography variant="caption" color="text.secondary">
            Built with React, Vite, and FastAPI. Data provided by OpenBB backend endpoints.
          </Typography>
        </Container>
      </Box>
    </Box>
  );
};
