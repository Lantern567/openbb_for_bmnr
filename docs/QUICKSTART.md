# BMNR 股票分析系统 - 5分钟快速开始

这是一个超级简洁的快速入门指南，帮助您在5分钟内启动并运行BMNR股票分析系统。

## 🎯 快速导航

- **完全新手?** → 从头开始跟随本指南
- **已安装环境?** → 直接跳到 [运行系统](#运行系统)
- **想要详细文档?** → 查看 [完整README](../README.md)

---

## ⚡ 60秒总览

**这个系统是什么？**
- BMNR股票的专业分析工具
- 技术指标 + mNAV估值分析
- 可以在OpenBB Workspace中展示

**有什么用？**
- 📈 查看K线图和技术指标
- 💰 计算修正净资产值（mNAV）
- 🎯 判断股票估值是否合理
- 🤖 使用OpenBB AI分析数据

---

## 📦 第一步：安装（5分钟）

### 1.1 检查前提条件

您需要：
- ✅ Python 3.9-3.12
- ✅ Anaconda（或Miniconda）
- ✅ 网络连接

**检查Python版本:**
```bash
python --version
# 应显示 Python 3.9.x 到 3.12.x
```

**检查Conda:**
```bash
conda --version
# 应显示 conda 4.x.x 或更高
```

### 1.2 一键安装

打开终端（命令提示符），复制粘贴以下命令：

```bash
# 创建环境
conda create -n bmnr_analysis python=3.11 -y

# 激活环境
conda activate bmnr_analysis

# 进入项目目录（修改为您的实际路径）
cd E:\code\openbb_for_finance

# 安装所有依赖
pip install -r requirements.txt && cd backend && pip install -r requirements.txt && cd ..

# 验证安装
python -c "import openbb; import fastapi; import streamlit; print('✅ 安装成功！')"
```

看到 "✅ 安装成功！" 就可以了！

---

## 🚀 第二步：运行系统（2分钟）

您有3个选项，选择最适合您的：

### 选项A: OpenBB Workspace集成（推荐！最专业）

**1. 启动Backend**
```bash
# 终端1
conda activate bmnr_analysis
cd E:\code\openbb_for_finance\backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**2. 连接OpenBB**
- 访问: https://pro.openbb.co
- 点击 Apps → Connect backend
- Name: `BMNR Analysis`
- URL: `http://localhost:8000`
- 点击 Test → Add

**3. 添加小部件**
- 进入 Dashboard
- 点击 Add Widget
- 搜索 "BMNR"
- 添加您想要的小部件

✅ **完成！** 现在您可以在OpenBB的专业界面中查看分析了。

---

### 选项B: Streamlit Web应用（最简单）

```bash
conda activate bmnr_analysis
cd E:\code\openbb_for_finance
streamlit run app.py
```

浏览器会自动打开 `http://localhost:8501`

✅ **完成！** 在Web界面中调整参数、查看图表。

---

### 选项C: Python脚本（最灵活）

```bash
conda activate bmnr_analysis
cd E:\code\openbb_for_finance\src
python data_fetcher.py
```

✅ **完成！** 在代码中自定义您的分析。

---

## 📊 第三步：开始分析（2分钟）

### 如果使用OpenBB Workspace:

**添加这5个小部件:**

1. **BMNR Technical Analysis** - 看价格趋势
2. **BMNR Key Metrics** - 看关键数据
3. **BMNR mNAV Analysis** - 看估值
4. **BMNR Price Data** - 看详细数据
5. **BMNR mNAV Scenarios** - 看估值区间

**配置mNAV参数:**
```
Shares Outstanding: 50000000  （替换为实际流通股数）
```

**与AI对话:**
```
"分析BMNR的技术指标"
"BMNR的mNAV说明了什么？"
```

### 如果使用Streamlit:

1. 在侧边栏选择日期范围
2. 勾选"启用mNAV分析"
3. 输入流通股数
4. 查看生成的图表
5. 点击"导出数据"下载CSV

---

## 🎓 常见操作

### 每次使用前

```bash
# 激活环境
conda activate bmnr_analysis

# 启动Backend（如果使用OpenBB）
cd E:\code\openbb_for_finance\backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 或启动Streamlit
streamlit run app.py
```

### 更新数据

**OpenBB Workspace:** 点击小部件的刷新按钮

**Streamlit:** 点击右上角的 "Rerun" 或按 `R`

### 更改股票代码

只需将 `symbol` 参数从 `BMNR` 改为其他代码，例如 `AAPL`、`TSLA`

---

## ❓ 快速解决问题

### 后端无法启动？

```bash
# 检查端口是否被占用
netstat -ano | findstr :8000

# 更改端口
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### OpenBB连接失败？

1. ✅ 确认后端正在运行（终端显示"Uvicorn running"）
2. ✅ URL是 `http://localhost:8000`（不是127.0.0.1）
3. ✅ 防火墙允许端口8000

### 找不到数据？

1. ✅ 检查股票代码是否正确
2. ✅ 检查网络连接
3. ✅ 尝试减少日期范围（例如30天）

### 模块导入错误？

```bash
# 重新安装
conda activate bmnr_analysis
pip install -r requirements.txt --upgrade
```

---

## 📁 文件位置

**项目目录结构:**
```
E:\code\openbb_for_finance\
├── backend/          ← Backend服务在这里
│   ├── main.py
│   └── uvicorn在这里运行
├── src/              ← 核心代码
├── app.py            ← Streamlit应用
└── requirements.txt  ← 依赖列表
```

**常用命令目录:**
```bash
cd E:\code\openbb_for_finance          # 项目根目录
cd E:\code\openbb_for_finance\backend  # Backend目录
cd E:\code\openbb_for_finance\src      # 源代码目录
```

---

## 🔗 重要链接

| 链接 | 用途 |
|------|------|
| http://localhost:8000 | Backend API |
| http://localhost:8000/docs | API文档（Swagger UI） |
| http://localhost:8501 | Streamlit应用 |
| https://pro.openbb.co | OpenBB Workspace |

---

## 📚 学习更多

完成快速开始后，您可以：

1. **阅读完整文档**
   - [主README](../README.md) - 完整功能介绍
   - [OpenBB配置指南](OPENBB_WORKSPACE_SETUP.md) - 详细配置步骤
   - [Backend文档](../backend/README.md) - API详解

2. **探索高级功能**
   - 自定义技术指标
   - 创建Jupyter Notebook分析
   - 添加自己的股票代码

3. **优化使用体验**
   - 创建快捷启动脚本
   - 设置自动化任务
   - 集成其他数据源

---

## 🎯 下一步建议

### 第1天：熟悉基础
- ✅ 成功启动系统
- ✅ 添加所有5个小部件
- ✅ 查看BMNR的技术图表

### 第2天：学习mNAV
- ✅ 理解mNAV概念
- ✅ 找到BMNR的准确流通股数
- ✅ 配置mNAV参数

### 第3天：高级分析
- ✅ 使用OpenBB AI分析
- ✅ 对比不同场景
- ✅ 导出数据进行深度分析

### 第1周：掌握系统
- ✅ 分析其他股票
- ✅ 自定义Dashboard布局
- ✅ 创建定期分析报告

---

## 💡 专业技巧

**技巧1: 创建启动脚本**

创建 `start_backend.bat` (Windows):
```batch
@echo off
call conda activate bmnr_analysis
cd E:\code\openbb_for_finance\backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

双击运行！

**技巧2: 快速切换股票**

在OpenBB中创建多个Dashboard，每个分析不同股票。

**技巧3: 定时任务**

使用Windows任务计划程序，每天早上自动启动Backend。

---

## ✅ 完成检查清单

在开始使用前，确保：

- [ ] Python 3.9-3.12 已安装
- [ ] Conda 已安装
- [ ] 项目依赖已安装
- [ ] Backend 可以成功启动
- [ ] 已注册 OpenBB 账号（如使用Workspace）
- [ ] 已知道 BMNR 的流通股数

**全部完成？** 🎉 恭喜！您已经准备好开始专业的股票分析了！

---

## 📞 需要帮助？

- **详细文档**: [主README](../README.md)
- **配置问题**: [OpenBB配置指南](OPENBB_WORKSPACE_SETUP.md)
- **API参考**: [Backend README](../backend/README.md)

---

**祝您分析愉快！** 📈

记住：这只是个工具，投资需谨慎！始终进行自己的研究并咨询专业财务顾问。

---

最后更新: 2025年
