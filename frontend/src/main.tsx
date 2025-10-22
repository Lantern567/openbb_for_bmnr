import { StrictMode } from 'react';
import ReactDOM from 'react-dom/client';

import { AppProviders } from './app/providers.tsx';
import App from './App.tsx';
import './styles/global.css';

const rootElement = document.getElementById('app');

if (!rootElement) {
  throw new Error('Root element "#app" was not found in the document.');
}

ReactDOM.createRoot(rootElement).render(
  <StrictMode>
    <AppProviders>
      <App />
    </AppProviders>
  </StrictMode>,
);
