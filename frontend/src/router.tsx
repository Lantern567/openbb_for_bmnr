import { createBrowserRouter, Navigate } from 'react-router-dom';

import { RootLayout } from '@/layouts/RootLayout.tsx';
import { DashboardPage } from '@/pages/dashboard/DashboardPage.tsx';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    children: [
      {
        index: true,
        element: <DashboardPage />,
      },
    ],
  },
  {
    path: '*',
    element: <Navigate to="/" replace />,
  },
]);
