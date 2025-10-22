import { useContext } from 'react';

import { ColorModeContext } from '@/app/providers.tsx';

export const useColorMode = () => {
  const context = useContext(ColorModeContext);
  if (!context) {
    throw new Error('useColorMode must be used within AppProviders');
  }

  return context;
};
