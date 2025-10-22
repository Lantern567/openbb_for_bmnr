import axios from 'axios';

import { appConfig } from '@/config/env.ts';

export const apiClient = axios.create({
  baseURL: appConfig.apiBaseUrl,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000, // 增加到 60 秒，给后端更多时间获取数据
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.data?.error) {
      return Promise.reject(new Error(error.response.data.error));
    }

    if (error.message) {
      return Promise.reject(new Error(error.message));
    }

    return Promise.reject(error);
  },
);

export const buildQueryString = (params: Record<string, unknown>) => {
  const query = new URLSearchParams();

  Object.entries(params).forEach(([key, value]) => {
    if (value === undefined || value === null) {
      return;
    }

    query.append(key, String(value));
  });

  return query.toString();
};
