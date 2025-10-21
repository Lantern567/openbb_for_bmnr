# API密钥配置指南

本项目需要配置API密钥才能获取实时股票数据。

## 📋 获取免费API密钥

### 1. Financial Modeling Prep (FMP) - 推荐

**免费额度**: 250次/天

**获取步骤**:
1. 访问: https://site.financialmodelingprep.com/developer/docs
2. 点击 "Get your Free API Key" 注册
3. 登录后在Dashboard找到API Key

### 2. Polygon.io - 推荐（支持BMNR）

**免费额度**: 5次/分钟

**获取步骤**:
1. 访问: https://polygon.io/
2. 点击 "Get Free API Key"
3. 注册后在Dashboard的"API Keys"找到密钥

### 3. Alpha Vantage - 可选

**免费额度**: 25次/天

**获取步骤**:
1. 访问: https://www.alphavantage.co/support/#api-key
2. 填写表单（姓名+邮箱）
3. 立即收到API Key

---

## ⚙️ 配置方法

### 方法1: 使用启动脚本（推荐）

1. 复制示例文件:
   ```cmd
   copy start_backend_with_keys.bat.example start_backend_with_keys.bat
   ```

2. 编辑 `start_backend_with_keys.bat`，替换API密钥:
   ```batch
   SET OPENBB_FMP_API_KEY=your_actual_fmp_key_here
   SET OPENBB_POLYGON_API_KEY=your_actual_polygon_key_here
   ```

3. 启动backend:
   ```cmd
   start_backend_with_keys.bat
   ```

### 方法2: 设置环境变量

**Windows (临时设置)**:
```cmd
SET OPENBB_FMP_API_KEY=your_fmp_key_here
SET OPENBB_POLYGON_API_KEY=your_polygon_key_here
```

**Windows (永久设置)**:
1. 右键"此电脑" → 属性 → 高级系统设置
2. 环境变量 → 系统变量 → 新建
3. 添加:
   - 变量名: `OPENBB_FMP_API_KEY`
   - 变量值: 您的FMP密钥

### 方法3: 使用配置脚本

运行交互式配置脚本:
```cmd
python setup_api_keys.py
```

---

## ⚠️ 安全注意事项

**重要**:
- ❌ **不要**将包含真实API密钥的文件提交到Git
- ❌ **不要**在公开场合分享您的API密钥
- ✅ 使用 `.gitignore` 忽略包含密钥的文件
- ✅ 使用环境变量管理密钥

**已自动忽略的文件**:
- `start_backend_with_keys.bat` (包含真实密钥)
- `.env` 和 `.env.local`

**安全的示例文件**:
- `start_backend_with_keys.bat.example` (仅供参考，无真实密钥)

---

## ✅ 验证配置

启动backend后，检查输出:

**成功** ✅:
```
[OK] API keys configured: FMP, Polygon
```

**失败** ❌:
```
[WARNING] No API keys configured - using fallback sample data
```

---

## 🔍 故障排除

### 问题: Widgets显示 "Empty"

**原因**: API密钥未正确配置

**解决方案**:
1. 确认环境变量已设置
2. 重启backend
3. 检查backend启动日志

### 问题: Rate Limit 错误

**原因**: API调用次数超限

**解决方案**:
1. 等待几分钟后重试
2. 使用多个数据源（系统会自动切换）
3. 升级到付费tier

---

## 📚 相关文档

- [主README](README.md)
- [快速开始](docs/QUICKSTART.md)
- [OpenBB Workspace配置](docs/OPENBB_WORKSPACE_SETUP.md)
