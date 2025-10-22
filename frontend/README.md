# OpenBB Workspace 前端

自定义的 React + Vite 仪表盘项目，对接位于 `../backend` 的 FastAPI 后端。

## 快速开始

```bash
npm install
npm run dev
```

开发服务器默认运行在 http://localhost:3000，并期待后端服务可在 `http://localhost:8000` 访问（可通过环境变量修改）。

## 环境变量

如需覆盖默认配置，可在本目录创建 `.env.local`，示例：

```
VITE_API_BASE_URL=http://localhost:8000
VITE_DEFAULT_SYMBOL=BMNR
```

## 常用脚本

- `npm run dev`：启动 Vite 开发服务器
- `npm run build`：类型检查并生成生产构建
- `npm run preview`：预览 build 输出
- `npm run lint`：运行 ESLint
- `npm run format`：使用 Prettier 校验 ts/tsx/css

## 技术栈

- React 19
- Vite 7
- TypeScript
- Material UI 7
- React Query 5
- Plotly.js（图表渲染）
- Zod（运行时数据校验）
