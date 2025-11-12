# PEDA自动化处理工具 V12

## 简介
PEDA自动化处理工具V12是一款基于Python和Playwright的批量表单自动化、文档上传与PDF导出工具，支持现代化GUI和多语言界面。

## 快速安装（Windows用户推荐）
1. 确保已安装 Python 3.8 或更高版本
2. 双击运行 `install.bat` 脚本，将自动完成：
   - **自动创建虚拟环境** (venv)
   - 升级 pip 到最新版本
   - 安装所有Python依赖包
   - 安装 Playwright 浏览器（Chromium, Firefox, WebKit）
   - 创建桌面快捷方式

## 手动安装
1. 安装Python 3.8及以上版本
2. 创建并激活虚拟环境：
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```
3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

## 启动程序

### Windows 用户（推荐）
- **双击桌面快捷方式** "PEDA V12"
- 或双击运行 `run_gui.bat`（GUI界面）
- 或双击运行 `run_cli.bat`（命令行界面）

### 手动启动
- **GUI界面启动**（推荐）：
  ```bash
  # 先激活虚拟环境
  # Windows: venv\Scripts\activate
  # macOS/Linux: source venv/bin/activate
  
  python start.py
  ```
  或
  ```bash
  python gui/start_gui.py
  ```

- **命令行界面启动**：
  ```bash
  python -m interfaces.cli_interface
  ```

## 使用说明
1. 启动程序后，按界面提示输入用户名、密码
2. 选择包含产品数据的Excel文件
3. 选择文档所在目录
4. 点击"开始处理"按钮
5. 程序将自动完成表单填写、文档上传和PDF导出

## 目录结构
```
PEDA_V12/
├── start.py              # 主入口文件
├── install.bat           # Windows自动安装脚本
├── requirements.txt      # Python依赖清单
├── peda_config.json      # 配置文件
├── config/               # 配置模块
├── core/                 # 核心工作流引擎
├── modules/              # 功能模块
│   ├── browser_manager.py
│   ├── data_processor.py
│   ├── document_manager.py
│   ├── form_handler.py
│   └── pdf_processor.py
├── gui/                  # 图形界面
│   ├── peda_gui_complete.py
│   └── start_gui.py
└── interfaces/           # 接口层（CLI/GUI）
```

## 主要功能
- ✅ 批量处理Excel数据
- ✅ 自动填写表单
- ✅ 智能文档分类上传
- ✅ PDF自动生成和下载
- ✅ 多语言界面支持
- ✅ 容错机制和断点续传
- ✅ 实时进度显示

## 系统要求
- Python 3.8 或更高版本
- Windows 10/11 或 macOS 10.13+ 或 Linux
- 至少 2GB 可用磁盘空间（用于浏览器安装）
- 稳定的网络连接（首次安装时）

## 注意事项
- 首次运行前请确保完成依赖安装
- Excel文件必须包含必需的列（如：Part Number）
- 文档文件需按产品编号组织在对应文件夹中
- 建议使用虚拟环境运行程序

## 常见问题

### Q: 如何创建虚拟环境？
**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Q: 浏览器启动失败？
- 确认已运行 `playwright install` 安装浏览器
- 检查是否有防火墙或杀毒软件阻止

### Q: Excel文件格式要求？
- 必须包含 `Part Number` 列
- 支持 .xlsx 和 .xls 格式
- 确保数据格式正确，无空行

### Q: 文档上传失败？
- 检查文档文件夹结构是否正确
- 确认文件名不包含特殊字符
- 验证文件格式是否支持

### Q: 遇到权限问题（Windows）？
在 PowerShell 中运行：
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```


## PowerShell 安装与启动详细步骤（Windows）

### 方式一：使用自动安装脚本（推荐）
1. 打开 PowerShell（建议以管理员身份运行）
2. 进入项目目录：
   ```powershell
   cd C:\Path\To\PEDA_V12
   ```
3. 双击运行 `install.bat` 或在命令行中执行：
   ```powershell
   .\install.bat
   ```
4. 等待安装完成后，启动程序：
   ```powershell
   python start.py
   ```

### 方式二：手动安装
1. 打开 PowerShell（建议以管理员身份运行）
2. 进入项目目录：
   ```powershell
   cd C:\Path\To\PEDA_V12
   ```
3. （推荐）创建并激活虚拟环境：
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
4. 安装依赖：
   ```powershell
   pip install --upgrade pip
   pip install -r requirements.txt
   playwright install
   ```
5. 启动程序：
   ```powershell
   python start.py
   ```

### 使用程序
按照界面提示操作：
1. 输入用户名和密码
2. 选择Excel数据文件
3. 选择文档所在目录
4. 点击"开始处理"按钮

## 技术栈
- **Python 3.8+** - 主要编程语言
- **Playwright** - 浏览器自动化框架
- **Pandas** - 数据处理
- **Tkinter** - GUI界面
- **OpenPyXL** - Excel文件处理

## 开发者信息
- 版本：V12
- 更新日期：2024
- 开发者：Frank Zhang

## 许可证
本项目仅供内部使用。

---
如需详细说明、开发文档或遇到问题，请联系开发者。
