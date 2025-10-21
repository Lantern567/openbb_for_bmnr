# OpenBB Workspace 网页端配置指南

本指南将详细介绍如何将BMNR股票分析系统连接到OpenBB Workspace网页端，实现专业级可视化和AI分析。

## 📋 目录

- [前提条件](#前提条件)
- [第一步：启动后端服务](#第一步启动后端服务)
- [第二步：登录OpenBB Workspace](#第二步登录openbb-workspace)
- [第三步：添加自定义后端](#第三步添加自定义后端)
- [第四步：使用小部件](#第四步使用小部件)
- [第五步：配置小部件参数](#第五步配置小部件参数)
- [第六步：使用OpenBB AI](#第六步使用openbb-ai)
- [常见问题](#常见问题)
- [故障排除](#故障排除)

---

## 前提条件

在开始之前，确保您已经完成以下步骤：

✅ 安装了conda环境 `bmnr_analysis`
✅ 安装了所有Python依赖
✅ 有OpenBB账号（如果没有，请访问 https://pro.openbb.co 注册）
✅ 稳定的网络连接

---

## 第一步：启动后端服务

### 1.1 打开终端（命令提示符或PowerShell）

**Windows快捷键:**
- 按 `Win + R`，输入 `cmd` 或 `powershell`，回车

### 1.2 激活conda环境

```bash
conda activate bmnr_analysis
```

您应该看到命令提示符前面出现 `(bmnr_analysis)` 标识。

### 1.3 进入backend目录

```bash
cd E:\code\openbb_for_finance\backend
```

> **注意**: 如果您的项目在不同路径，请修改为您的实际路径。

### 1.4 启动FastAPI服务

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 1.5 验证服务启动成功

您应该看到类似以下输出：

```
INFO:     Will watch for changes in these directories: ['E:\\code\\openbb_for_finance\\backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

✅ **看到这些信息表示后端服务已成功启动！**

> **重要**: 保持这个终端窗口开启！关闭它会停止服务。

### 1.6 测试服务（可选）

打开浏览器，访问：
```
http://localhost:8000
```

您应该看到API信息的JSON响应：
```json
{
  "name": "BMNR Stock Analysis Backend",
  "version": "1.0.0",
  "description": "Custom backend for OpenBB Workspace",
  "endpoints": {
    "widgets": "/widgets.json",
    "apps": "/apps.json",
    ...
  }
}
```

访问API文档：
```
http://localhost:8000/docs
```

您将看到Swagger UI界面，显示所有可用的API端点。

---

## 第二步：登录OpenBB Workspace

### 2.1 访问OpenBB Workspace

打开浏览器（推荐使用Chrome、Edge或Firefox），访问：

```
https://pro.openbb.co
```

### 2.2 登录账号

- 如果您已有账号，点击 **"Sign In"** 登录
- 如果您没有账号，点击 **"Sign Up"** 注册

**注册步骤:**
1. 输入邮箱地址
2. 设置密码
3. 验证邮箱（查收验证邮件）
4. 完成注册

### 2.3 进入主界面

登录后，您将看到OpenBB Workspace的主界面：

- **左侧导航栏**: Dashboard、Apps、Settings等
- **中间区域**: 仪表板或内容展示区
- **右上角**: 用户菜单和设置

---

## 第三步：添加自定义后端

### 3.1 找到Apps页面

在左侧导航栏中，点击 **"Apps"** 图标（通常是第二或第三个图标）。

### 3.2 点击"Connect backend"按钮

在Apps页面顶部，您会看到 **"Connect backend"** 按钮，点击它。

### 3.3 填写后端信息

一个对话框将弹出，要求您填写后端信息：

#### 填写表单:

| 字段 | 说明 | 填写内容 |
|------|------|----------|
| **Name** | 后端的显示名称 | `BMNR Analysis` 或任何您喜欢的名称 |
| **URL** | 后端服务地址 | `http://localhost:8000` |

> **重要提示:**
> - URL必须是 `http://localhost:8000`（**不是** `127.0.0.1:8000`）
> - 不要在URL末尾添加斜杠 `/`
> - 确保使用 `http://` 而不是 `https://`

#### 示例填写:
```
Name: BMNR Analysis
URL:  http://localhost:8000
```

### 3.4 测试连接

填写完成后，点击 **"Test"** 按钮。

**成功的响应:**
```
✅ Test successful - Found 5 widgets
```

这表示：
- ✅ 后端服务正在运行
- ✅ 连接成功
- ✅ 发现了5个小部件配置

**如果测试失败，请参考 [故障排除](#故障排除) 部分。**

### 3.5 添加后端

测试成功后，点击 **"Add"** 按钮。

您的BMNR Analysis后端现在已添加到OpenBB Workspace！

---

## 第四步：使用小部件

### 4.1 进入Dashboard

点击左侧导航栏的 **"Dashboard"** 图标（第一个图标）。

### 4.2 添加Widget

点击右上角的 **"Add Widget"** 按钮（或中间区域的加号图标）。

### 4.3 查找BMNR小部件

在弹出的小部件库中：

**方法1: 使用搜索**
- 在搜索框中输入 `BMNR`
- 所有BMNR相关的小部件将显示

**方法2: 浏览分类**
- 在左侧分类中找到 **"BMNR Analysis Backend"**
- 或查找 **"Stock Analysis"**、**"Valuation"** 等分类

### 4.4 可用的5个小部件

#### 📈 1. BMNR Technical Analysis（技术分析）

**功能:** 显示BMNR股票的技术分析图表

**包含内容:**
- 蜡烛图（Candlestick Chart）
- 移动平均线（MA 20、MA 50）
- 成交量

**默认参数:**
- `symbol`: BMNR
- `days`: 365（一年数据）
- `raw`: false

**适用场景:** 查看价格趋势、识别支撑阻力位

---

#### 💰 2. BMNR mNAV Analysis（mNAV估值分析）

**功能:** 显示修正净资产值分析

**包含内容:**
- 股价 vs mNAV对比线
- P/mNAV比率趋势
- 溢价/折价百分比

**关键参数:**
- `symbol`: BMNR
- `days`: 365
- **`shares_outstanding`**: **流通股数**（⚠️ 必须准确填写！）
- `property_fair_value`: 物业公允价值（可选）
- `property_book_value`: 物业账面价值（可选）
- `deferred_tax_rate`: 递延税率（默认0.0）

**适用场景:** 估值分析、判断股价是否被高估或低估

---

#### 📋 3. BMNR Price Data（价格数据表）

**功能:** 显示历史价格数据表格

**包含内容:**
- 日期（Date）
- 开盘价（Open）
- 最高价（High）
- 最低价（Low）
- 收盘价（Close）
- 成交量（Volume）

**默认参数:**
- `symbol`: BMNR
- `days`: 90（最近90天）

**适用场景:** 查看详细的历史价格数据、导出数据

---

#### 🎯 4. BMNR Key Metrics（关键指标）

**功能:** 实时关键指标看板

**包含内容:**
- 当前价格
- 价格变化
- 价格变化百分比
- RSI（相对强弱指数）
- 每股mNAV
- P/mNAV比率
- 溢价/折价百分比
- 最后更新时间

**关键参数:**
- `symbol`: BMNR
- `shares_outstanding`: 流通股数

**适用场景:** 快速查看核心指标、监控实时变化

---

#### 📊 5. BMNR mNAV Scenarios（场景分析）

**功能:** 对比不同mNAV估值场景

**包含内容:**
- 保守估值（Conservative）
- 基准估值（Base Case）
- 乐观估值（Optimistic）
- 当前股价参考线

**参数:**
- `symbol`: BMNR
- `shares_outstanding`: 流通股数
- `conservative_mnav`: 保守场景的mNAV（可选）
- `base_mnav`: 基准场景的mNAV（可选，自动计算）
- `optimistic_mnav`: 乐观场景的mNAV（可选）

**适用场景:** 压力测试、估值区间分析

---

### 4.5 添加小部件到Dashboard

1. 点击您想要的小部件
2. 小部件将立即添加到您的Dashboard
3. 您可以拖动调整位置和大小

---

## 第五步：配置小部件参数

### 5.1 打开小部件设置

在Dashboard中，找到您添加的小部件，点击右上角的 **⚙️ 设置图标** 或 **三点菜单**。

### 5.2 调整参数

#### 示例：配置mNAV Analysis小部件

**场景:** 您要分析BMNR的mNAV，已知流通股数为50,000,000股

**配置步骤:**

1. 点击 "BMNR mNAV Analysis" 小部件的设置
2. 找到参数配置区域
3. 填写参数：

```
Symbol: BMNR
Days: 365
Shares Outstanding: 50000000    ⚠️ 重要！必须准确
Property Fair Value: 留空（除非有准确数据）
Property Book Value: 留空（除非有准确数据）
Deferred Tax Rate: 0.0
Raw: false
```

4. 点击 **"Save"** 或 **"Apply"** 保存

### 5.3 查看数据

参数保存后，小部件会自动刷新并显示新数据。

### 5.4 常用参数说明

| 参数 | 说明 | 推荐值 | 注意事项 |
|------|------|--------|----------|
| **symbol** | 股票代码 | BMNR | 大写字母 |
| **days** | 历史数据天数 | 365（1年）<br>180（半年）<br>90（季度） | 数值越大加载越慢 |
| **shares_outstanding** | 流通股数 | 实际股数 | ⚠️ 必须准确！影响mNAV计算 |
| **property_fair_value** | 物业公允价值 | 根据评估报告 | 可选，用于公允价值调整 |
| **property_book_value** | 物业账面价值 | 从资产负债表获取 | 与fair_value配对使用 |
| **deferred_tax_rate** | 递延税率 | 0.0 - 0.30 | 通常为10%（0.10） |
| **raw** | 返回原始数据 | false | true时返回JSON供AI分析 |

---

## 第六步：使用OpenBB AI

OpenBB Workspace集成了AI助手，可以帮您分析数据。

### 6.1 打开AI面板

在OpenBB Workspace界面中，点击右上角或右侧的 **AI图标** 或 **"Copilot"** 按钮。

### 6.2 与AI对话

AI可以访问您Dashboard中的小部件数据。您可以问：

#### 技术分析相关:
```
- "分析BMNR的技术指标趋势"
- "BMNR当前的RSI值说明了什么？"
- "BMNR的移动平均线显示什么趋势？"
- "根据技术指标，BMNR是超买还是超卖？"
```

#### mNAV估值相关:
```
- "BMNR的P/mNAV比率说明了什么？"
- "BMNR当前是溢价还是折价交易？"
- "解释一下三种mNAV场景的区别"
- "基于mNAV分析，BMNR的估值合理吗？"
```

#### 综合分析:
```
- "综合技术指标和mNAV，给出BMNR的投资建议"
- "BMNR最近一个月的表现如何？"
- "对比BMNR的价格走势和mNAV趋势"
```

### 6.3 AI分析的优势

- 🤖 自动读取您的小部件数据
- 📊 生成详细的分析报告
- 💡 提供洞察和建议
- 🔄 实时更新分析

---

## 常见问题

### Q1: 我需要什么样的OpenBB账号？

**A:** 免费账号即可使用自定义后端功能。高级功能（如更多数据源）需要付费订阅。

### Q2: 后端服务必须一直运行吗？

**A:** 是的。只要您想在OpenBB Workspace中查看BMNR数据，后端服务就必须运行。您可以：
- 最小化终端窗口（不要关闭）
- 在服务器上持续运行
- 需要时启动，不用时关闭

### Q3: 可以同时使用Streamlit和OpenBB Workspace吗？

**A:** 可以！它们使用不同的端口：
- Backend: 8000
- Streamlit: 8501

您可以在一个终端运行Backend，在另一个终端运行Streamlit。

### Q4: 如何找到BMNR的准确流通股数？

**A:** 您可以从以下途径获取：
1. 公司财报（年报、季报）
2. 金融数据网站（Yahoo Finance、Bloomberg等）
3. 交易所公告
4. OpenBB Platform数据

### Q5: 小部件数据多久更新一次？

**A:** 取决于数据源：
- **实时数据**: 刷新小部件即可获取最新数据
- **历史数据**: 每天更新一次
- 您可以手动点击刷新按钮强制更新

### Q6: 可以分析其他股票吗？

**A:** 可以！只需修改小部件参数中的 `symbol` 为其他股票代码即可。

### Q7: 如何导出数据？

**方法1:** 使用 "Price Data" 小部件，点击导出按钮

**方法2:** 访问API直接获取JSON数据:
```
http://localhost:8000/bmnr/price_table?symbol=BMNR&days=90
```

### Q8: 可以在移动设备上使用吗？

**A:** OpenBB Workspace网页端支持移动浏览器访问，但：
- 后端服务必须在您的电脑上运行
- 移动设备和电脑需要在同一网络
- 体验可能不如桌面端

---

## 故障排除

### 问题1: 测试连接失败 - "Connection refused"

**症状:**
```
❌ Connection refused
❌ Failed to connect to backend
```

**原因及解决方案:**

**1. 后端服务未启动**
```bash
# 检查后端是否运行
# 打开浏览器访问 http://localhost:8000
# 如果无法访问，说明服务未运行

# 解决方案：启动后端
cd E:\code\openbb_for_finance\backend
conda activate bmnr_analysis
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**2. URL填写错误**
```
❌ 错误: http://127.0.0.1:8000
❌ 错误: http://localhost:8000/
❌ 错误: https://localhost:8000

✅ 正确: http://localhost:8000
```

**3. 防火墙阻止**
- Windows Defender可能阻止端口8000
- 解决方案: 允许Python通过防火墙

**4. 端口被占用**
```bash
# 检查8000端口是否被占用
netstat -ano | findstr :8000

# 如果被占用，更改端口
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
# 然后在OpenBB中使用 http://localhost:8001
```

---

### 问题2: 找到0个小部件

**症状:**
```
✅ Connection successful
⚠️ Found 0 widgets
```

**原因:**
- `widgets.json` 文件配置问题
- API端点错误

**解决方案:**

1. 访问 http://localhost:8000/widgets.json
2. 检查是否返回JSON数据
3. 如果返回错误，检查 `backend/widgets.json` 文件是否存在且格式正确

---

### 问题3: 小部件显示错误或无数据

**症状:**
- 小部件显示 "Error loading data"
- 小部件空白
- 显示 "No data available"

**原因及解决方案:**

**1. 股票代码不存在**
```
# 确保BMNR是有效的股票代码
# 如果不是，更改为实际存在的代码
```

**2. 日期范围太大**
```
# 减少days参数
# 例如从365改为90
```

**3. mNAV参数缺失**
```
# mNAV分析需要shares_outstanding
# 确保填写了准确的流通股数
```

**4. 网络连接问题**
```
# OpenBB Platform需要网络获取数据
# 检查您的网络连接
```

**5. 检查后端日志**
```
# 查看运行uvicorn的终端窗口
# 查找错误信息
```

---

### 问题4: "ModuleNotFoundError" 错误

**症状:**
后端启动时显示：
```
ModuleNotFoundError: No module named 'src'
ModuleNotFoundError: No module named 'openbb'
```

**解决方案:**

```bash
# 确保在正确的环境
conda activate bmnr_analysis

# 重新安装依赖
cd E:\code\openbb_for_finance
pip install -r requirements.txt

cd backend
pip install -r requirements.txt

# 验证安装
python -c "import openbb; import fastapi; print('OK')"
```

---

### 问题5: 图表主题不匹配

**症状:**
- 图表是深色但背景是浅色
- 颜色显示不协调

**解决方案:**

这是自动处理的，OpenBB会传递 `theme` 参数。如果有问题：

1. 检查 `backend/plotly_theme.py` 文件
2. 确认 `get_theme()` 函数正常工作
3. 刷新小部件

---

### 问题6: 性能问题（加载慢）

**症状:**
- 小部件加载时间超过10秒
- 图表响应缓慢

**解决方案:**

**1. 减少历史数据量**
```
# 将days从365改为90或30
days: 30  # 最近一个月
```

**2. 使用数据缓存**
```python
# backend/main.py已包含基本缓存
# 如需更强缓存，可以添加Redis
```

**3. 优化网络**
```
# 确保网络稳定
# OpenBB数据获取依赖网络速度
```

---

### 问题7: AI无法访问我的数据

**症状:**
- AI回答 "I don't have access to that data"
- AI无法看到小部件内容

**解决方案:**

1. 确保小部件参数中 `raw` 设置为 `true` （针对AI分析）
2. 刷新Dashboard
3. 重新提问AI

---

## 🎯 最佳实践

### 1. Dashboard布局建议

**推荐布局:**
```
+------------------+------------------+
|  Technical       |   Key Metrics    |
|  Analysis        |                  |
|  (大图)          |   (指标卡)       |
+------------------+------------------+
|  mNAV Analysis                      |
|  (中等大小)                         |
+------------------+------------------+
|  Scenario        |   Price Data     |
|  Analysis        |   (表格)         |
+------------------+------------------+
```

### 2. 参数设置建议

**日常监控:**
- days: 30-90
- 更新频率: 每日一次

**深度分析:**
- days: 180-365
- 配合Jupyter Notebook使用

**演示展示:**
- days: 90
- 使用场景分析对比

### 3. 数据更新频率

- **实时监控**: 每小时刷新
- **日常分析**: 每天早上更新
- **周度报告**: 每周一更新

---

## 🚀 下一步

成功配置OpenBB Workspace后，您可以：

1. **探索更多功能**
   - 尝试不同的参数组合
   - 创建多个Dashboard视图
   - 使用OpenBB AI进行深度分析

2. **学习高级用法**
   - 查看 [Backend API文档](../backend/README.md)
   - 阅读 [快速开始指南](QUICKSTART.md)
   - 自定义Widget配置

3. **分享您的Dashboard**
   - OpenBB支持Dashboard导出和分享
   - 创建模板供团队使用

4. **集成其他工具**
   - 结合Streamlit本地分析
   - 使用Jupyter Notebook深度研究
   - 导出数据到Excel

---

## 📞 需要帮助？

如果遇到本指南未涵盖的问题：

1. 查看 [主README](../README.md) 的故障排除部分
2. 查看 [Backend README](../backend/README.md)
3. 检查OpenBB文档: https://docs.openbb.co/workspace
4. 查看FastAPI文档: https://fastapi.tiangolo.com

---

**祝您使用愉快！📊**

最后更新: 2025年
