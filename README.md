# BMNR 股票分析系统

一个功能完整的股票分析工具，专注于BMNR股票的技术分析和修正净资产值（mNAV）估值计算。

[![Python 3.9-3.12](https://img.shields.io/badge/python-3.9--3.12-blue.svg)](https://www.python.org/downloads/)
[![OpenBB](https://img.shields.io/badge/OpenBB-4.0%2B-green.svg)](https://openbb.co/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 📊 核心功能

### 技术分析
- **K线图表**: 交互式蜡烛图配合成交量展示
- **趋势指标**: 移动平均线（MA 5, 10, 20, 50, 100, 200）、EMA、MACD
- **动量指标**: RSI、随机振荡器（Stochastic Oscillator）
- **波动率指标**: 布林带（Bollinger Bands）、ATR
- **成交量指标**: OBV、VWAP

### mNAV 估值分析
- **修正净资产值计算**: 适用于REITs和资产密集型公司的行业标准估值方法
- **P/mNAV 比率分析**: 追踪股价相对净资产值的溢价/折价
- **公允价值调整**: 支持物业重估
- **历史趋势**: 可视化 P/mNAV 比率的历史变化
- **场景对比**: 对比多个估值场景（保守、基准、乐观）

### OpenBB Workspace 集成 ⭐
- **专业可视化**: 在OpenBB Workspace中展示您的分析
- **5个自定义小部件**: 技术分析、mNAV分析、价格表、关键指标、场景分析
- **AI支持**: 使用OpenBB AI分析您的数据
- **主题自适应**: 自动匹配深色/浅色主题
- **实时数据**: 通过OpenBB Platform获取实时市场数据

### 交互式仪表板
- Streamlit Web应用
- 可自定义参数和日期范围
- 交互式Plotly可视化
- 数据导出功能（CSV格式）

## 📁 项目结构

```
openbb_for_finance/
├── backend/                # OpenBB Workspace 后端
│   ├── main.py            # FastAPI 应用程序
│   ├── widgets.json       # 小部件配置
│   ├── apps.json          # 应用配置
│   ├── plotly_theme.py    # OpenBB 主题
│   ├── requirements.txt   # 后端依赖
│   └── README.md          # 后端文档
├── src/                   # 核心分析模块
│   ├── config.py          # 配置设置
│   ├── data_fetcher.py    # 数据获取模块
│   ├── mnav_calculator.py # mNAV计算引擎
│   ├── indicators.py      # 技术与基本面指标
│   └── visualizer.py      # 绘图和可视化
├── data/                  # 数据目录
│   ├── raw/               # 原始数据缓存
│   └── processed/         # 处理后数据
├── notebooks/             # Jupyter notebooks
├── output/                # 导出的图表和报告
├── docs/                  # 文档
├── app.py                 # Streamlit Web应用
├── quick_start.py         # 快速演示脚本
├── requirements.txt       # Python依赖
└── README.md             # 本文件
```

## 🚀 快速开始

### 前置要求
- Python 3.9 - 3.12
- Anaconda 或 Miniconda（推荐）
- 稳定的网络连接（用于获取市场数据）

### 方法一：使用 Conda（推荐）

#### 1. 创建 Conda 环境

```bash
# 创建名为 bmnr_analysis 的环境，使用 Python 3.11
conda create -n bmnr_analysis python=3.11 -y

# 激活环境
conda activate bmnr_analysis
```

#### 2. 安装依赖

```bash
# 切换到项目目录
cd E:\code\openbb_for_finance

# 安装主项目依赖
pip install -r requirements.txt

# 安装后端依赖
cd backend
pip install -r requirements.txt
```

#### 3. 验证安装

```bash
# 返回项目根目录
cd ..

# 测试依赖
python -c "import openbb; import fastapi; import streamlit; print('All dependencies installed successfully!')"
```

### 方法二：使用 pip（不推荐新手）

```bash
# 安装主依赖
pip install -r requirements.txt

# 安装后端依赖
cd backend
pip install -r requirements.txt
```

## 📱 使用方法

### Option 1: OpenBB Workspace 集成（推荐）✨

这是最专业的使用方式，可以将您的分析展示在OpenBB的专业界面中。

#### 步骤 1: 启动后端服务

```bash
# 激活 conda 环境
conda activate bmnr_analysis

# 进入 backend 目录
cd E:\code\openbb_for_finance\backend

# 启动 FastAPI 服务
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

您应该看到类似输出：
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

#### 步骤 2: 连接到 OpenBB Workspace

1. **访问 OpenBB Workspace**
   - 打开浏览器访问: https://pro.openbb.co
   - 登录您的OpenBB账号（如果没有账号，需要先注册）

2. **添加自定义后端**
   - 在左侧导航栏，点击 **"Apps"** 图标
   - 点击页面顶部的 **"Connect backend"** 按钮

3. **填写后端信息**
   - **Name（名称）**: `BMNR Analysis` 或任何您喜欢的名称
   - **URL**: `http://localhost:8000`
   - 点击 **"Test"** 按钮

4. **验证连接**
   - 如果配置正确，您将看到：
     ```
     ✅ Test successful - Found 5 widgets
     ```
   - 如果出现错误，请检查后端服务是否正在运行

5. **添加后端**
   - 点击 **"Add"** 按钮完成添加

#### 步骤 3: 使用小部件

1. **进入仪表板**
   - 点击左侧的 **"Dashboard"** 图标
   - 点击右上角的 **"Add Widget"** 按钮

2. **查找 BMNR 小部件**
   - 在搜索框中输入 `BMNR`
   - 或者在分类中找到 **"BMNR Analysis Backend"**

3. **可用的小部件**

   | 小部件 | 功能 | 说明 |
   |--------|------|------|
   | 📈 **BMNR Technical Analysis** | 技术分析图表 | 蜡烛图 + 移动平均线 + 技术指标 |
   | 💰 **BMNR mNAV Analysis** | mNAV估值分析 | 股价 vs mNAV，P/mNAV比率趋势 |
   | 📋 **BMNR Price Data** | 历史价格数据 | OHLCV数据表格 |
   | 🎯 **BMNR Key Metrics** | 关键指标看板 | 实时价格、RSI、mNAV比率等 |
   | 📊 **BMNR mNAV Scenarios** | 场景对比分析 | 保守/基准/乐观三种估值场景 |

4. **配置小部件参数**

   每个小部件都有可调整的参数：

   **技术分析图表参数:**
   - `symbol`: 股票代码（默认: BMNR）
   - `days`: 历史数据天数（默认: 365）
   - `raw`: 返回原始数据供AI分析（默认: false）

   **mNAV分析参数:**
   - `symbol`: 股票代码
   - `days`: 历史数据天数
   - `shares_outstanding`: 流通股数（**重要！需要准确填写**）
   - `property_fair_value`: 物业公允价值（可选）
   - `property_book_value`: 物业账面价值（可选）
   - `deferred_tax_rate`: 递延税率（默认: 0.0）

#### 步骤 4: 与 OpenBB AI 对话

1. 在OpenBB Workspace中，点击 AI 图标
2. 您可以询问关于BMNR数据的问题，例如：
   - "分析 BMNR 的技术指标趋势"
   - "BMNR 的 P/mNAV 比率说明了什么？"
   - "对比 BMNR 的三种估值场景"

> **详细配置指南**: 查看 [docs/OPENBB_WORKSPACE_SETUP.md](docs/OPENBB_WORKSPACE_SETUP.md) 获取带截图的详细步骤

### Option 2: Streamlit 仪表板

在另一个终端窗口运行：

```bash
# 激活环境
conda activate bmnr_analysis

# 运行 Streamlit 应用
streamlit run app.py
```

浏览器会自动打开 `http://localhost:8501`

**功能特性:**
- 调整日期范围
- 启用/禁用 mNAV 分析
- 配置公允价值调整
- 查看技术指标
- 导出数据到 CSV

### Option 3: Python 脚本

#### 测试数据获取
```bash
conda activate bmnr_analysis
cd src
python data_fetcher.py
```

#### 测试 mNAV 计算
```bash
python mnav_calculator.py
```

#### 测试技术指标
```bash
python indicators.py
```

### Option 4: Jupyter Notebooks

```bash
conda activate bmnr_analysis
jupyter notebook
```

在 `notebooks/` 文件夹中创建您自己的分析。

## 🔧 配置

### 自定义设置

编辑 `src/config.py` 来自定义：

```python
# 股票代码
DEFAULT_SYMBOL = "BMNR"

# 技术指标参数
MA_PERIODS = [5, 10, 20, 50, 100, 200]
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26

# 图表设置
CHART_HEIGHT = 800
CHART_THEME = "plotly_white"
```

### OpenBB 配置

如果您有 OpenBB Personal Access Token (PAT):

#### Windows:
```bash
set OPENBB_PAT=your_token_here
```

#### Mac/Linux:
```bash
export OPENBB_PAT=your_token_here
```

或添加到 `src/config.py`:
```python
OPENBB_PAT = "your_token_here"
```

## 💡 使用示例

### 示例 1: 快速技术分析

```python
from src.data_fetcher import StockDataFetcher
from src.indicators import TechnicalIndicators
from src.visualizer import StockVisualizer

# 获取数据
fetcher = StockDataFetcher("BMNR")
data = fetcher.get_historical_data("2024-01-01", "2024-12-31")

# 计算指标
tech = TechnicalIndicators(data)
df = tech.calculate_all_indicators()

# 可视化
viz = StockVisualizer("BMNR")
fig = viz.plot_technical_indicators(df)
fig.show()
```

### 示例 2: mNAV 分析

```python
from src.data_fetcher import StockDataFetcher
from src.mnav_calculator import mNAVCalculator

# 获取基本面数据
fetcher = StockDataFetcher("BMNR")
fundamental = fetcher.get_all_fundamental_data()

# 计算 mNAV
calc = mNAVCalculator(
    balance_sheet=fundamental['balance_sheet'],
    shares_outstanding=10000000  # 替换为实际流通股数
)

mnav_data = calc.calculate_mnav_with_fair_value(
    property_fair_value=500000000,
    property_book_value=400000000,
    deferred_tax_rate=0.10
)

print(f"每股 mNAV: ${mnav_data['mnav_per_share']:.2f}")
```

## 📊 mNAV 计算说明

### 什么是 mNAV?

Modified Net Asset Value (mNAV) 是一种估值方法，常用于：
- 房地产投资信托（REITs）
- 资产管理公司
- 拥有大量有形资产的公司

### 计算公式

```
mNAV = (资产公允价值 - 负债 - 少数股东权益 - 递延税项) / 流通股数
```

### 如何使用 mNAV 分析

1. **启用 mNAV** 在侧边栏中
2. **输入流通股数**: 总股份数量
3. **可选 - 公允价值调整**:
   - 物业公允价值: 市场/评估价值
   - 物业账面价值: 资产负债表价值
   - 递延税率: 重估收益的税率

4. **解读结果**:
   - **P/mNAV > 1.0**: 溢价交易（可能高估）
   - **P/mNAV < 1.0**: 折价交易（可能低估）
   - **P/mNAV ≈ 1.0**: 接近公允价值交易

## 🔍 数据来源

- **价格数据**: OpenBB Platform (Yahoo Finance provider)
- **基本面数据**: OpenBB Platform
- **技术指标**: TA-Lib library

## ⚠️ 故障排除

### 问题 1: 找不到 BMNR 数据

**解决方案:**
1. 验证 BMNR 是正确的股票代码
2. 检查网络连接
3. 尝试不同的日期范围
4. 验证 OpenBB 是否正确安装

### 问题 2: 无法获取基本面数据

**解决方案:**
1. 某些股票可能基本面数据有限
2. 尝试使用 `provider="fmp"` 或其他 OpenBB 提供商
3. 检查股票是否公开交易

### 问题 3: 模块未找到错误

**解决方案:**
```bash
# 确保在正确的环境中
conda activate bmnr_analysis

# 重新安装依赖
pip install -r requirements.txt --upgrade
```

### 问题 4: Backend 无法连接到 OpenBB Workspace

**解决方案:**
1. 确认后端正在运行: 检查终端是否显示 "Uvicorn running on..."
2. 检查 URL: 必须是 `http://localhost:8000` （不是 `127.0.0.1`）
3. 检查防火墙: 允许端口 8000 的连接
4. 尝试重启后端服务

### 问题 5: 导入错误 (ModuleNotFoundError)

**已知问题和修复:**

如果遇到以下错误：
```
ModuleNotFoundError: No module named 'config'
ModuleNotFoundError: No module named 'mnav_calculator'
```

这是因为相对导入问题。确保：
1. 项目根目录在 Python 路径中
2. 使用相对导入（`from .module import ...`）
3. 从项目根目录运行脚本

## 🎯 性能优化建议

1. **数据缓存**: Streamlit 中历史数据缓存 1 小时
2. **日期范围**: 使用较短的日期范围以加快加载速度
3. **指标选择**: 取消选择未使用的指标以提高性能

## 📚 高级用法

### 自定义指标

在 `src/indicators.py` 中添加您自己的指标:

```python
def calculate_custom_indicator(self) -> pd.DataFrame:
    df = self.df.copy()
    # 您的计算逻辑
    df['custom_indicator'] = ...
    return df
```

### 自定义可视化

在 `src/visualizer.py` 中添加图表:

```python
def plot_custom_chart(self, df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    # 您的可视化逻辑
    return fig
```

## 🤝 贡献

欢迎贡献！改进方向：

- [ ] 添加更多技术指标
- [ ] 支持多股票对比
- [ ] 添加警报和通知功能
- [ ] 投资组合跟踪
- [ ] 回测功能

## 📦 依赖项

主要依赖:
- `openbb>=4.0.0` - 金融数据平台
- `pandas>=2.0.0` - 数据处理
- `plotly>=5.14.0` - 交互式图表
- `streamlit>=1.28.0` - Web仪表板
- `fastapi>=0.104.0` - Backend API
- `uvicorn>=0.24.0` - ASGI 服务器
- `ta>=0.11.0` - 技术分析
- `numpy>=1.24.0` - 数值计算

查看 `requirements.txt` 了解完整列表。

## 📄 许可证

本项目开源，可用于教育和个人用途。

## ⚠️ 免责声明

**重要**: 本工具仅用于教育和信息目的。

- 不构成财务建议
- 过往表现不保证未来结果
- 始终进行自己的研究
- 在做出投资决策前咨询合格的财务顾问
- 开发者对任何财务损失不承担责任

## 💬 支持

遇到问题或有疑问：
1. 查看故障排除部分
2. 查看 OpenBB 文档: https://docs.openbb.co
3. 查看 Streamlit 文档: https://docs.streamlit.io
4. 查看 [docs/](docs/) 文件夹中的详细指南

## 🎓 文档

- [OpenBB Workspace 配置指南](docs/OPENBB_WORKSPACE_SETUP.md) - 详细的网页端配置步骤（带截图）
- [Backend API 文档](backend/README.md) - Backend API 详细说明
- [快速开始指南](docs/QUICKSTART.md) - 5分钟快速上手

## 📅 版本历史

### v1.0.0 (当前版本)
- ✅ 初始发布
- ✅ 15+ 技术指标
- ✅ mNAV 计算与公允价值调整
- ✅ 交互式 Streamlit 仪表板
- ✅ OpenBB Workspace 集成
- ✅ 5 个自定义小部件
- ✅ 数据导出功能

## 🙏 致谢

- **OpenBB Platform**: 金融数据基础设施
- **Plotly**: 交互式可视化库
- **Streamlit**: Web应用框架
- **TA-Lib**: 技术分析指标

---

**使用 ❤️ 构建，专注于 BMNR 股票分析**

最后更新: 2025年

---

## 🚀 快速命令参考

```bash
# 创建并激活环境
conda create -n bmnr_analysis python=3.11 -y
conda activate bmnr_analysis

# 安装依赖
pip install -r requirements.txt
cd backend && pip install -r requirements.txt && cd ..

# 启动 Backend (终端 1)
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 启动 Streamlit (终端 2 - 可选)
streamlit run app.py
```

**Backend API**: http://localhost:8000
**API 文档**: http://localhost:8000/docs
**Streamlit 仪表板**: http://localhost:8501
**OpenBB Workspace**: https://pro.openbb.co
