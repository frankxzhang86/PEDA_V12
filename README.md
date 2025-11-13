# PEDA自动化处理工具 V12

一款基于Python和Playwright的批量表单自动化、文档上传与PDF导出工具，支持现代化GUI和多语言界面。

## 主要功能
- ✅ **批量处理**: 从Excel文件读取数据，全自动处理多个零件号。
- ✅ **自动填表**: 自动登录系统并填写Web表单。
- ✅ **智能上传**: 根据零件号和预设类别，精确上传相关文档。
- ✅ **PDF导出**: 自动生成并下载处理完成的PDF文件。
- ✅ **图形界面**: 提供简单易用的GUI，支持实时进度显示和日志。
- ✅ **容错机制**: 包含错误处理和重试逻辑，并能在出错时保存截图。
- ✅ **多语言**: 支持英语、德语和中文界面。

## 系统要求
- **操作系统**: Windows 10/11, macOS, or Linux
- **Python版本**: Python 3.8 或更高版本
- **磁盘空间**: 至少 2GB 可用空间（用于安装浏览器核心）
- **网络**: 首次安装和运行时需要稳定的网络连接

---

## 1. 安装指南

### 方式一：使用自动安装脚本 (Windows推荐)
1.  确保已安装 Python 3.8 或更高版本。
2.  双击运行 `install.bat` 脚本。它将自动完成所有设置，包括：
    - 创建Python虚拟环境 (`venv` 文件夹)。
    - 安装所有必要的Python库。
    - 安装Playwright所需的浏览器。
    - 在项目目录和桌面上创建启动快捷方式。

### 方式二：手动安装
1.  **创建并激活虚拟环境**:
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate
    
    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
2.  **安装依赖**:
    ```bash
    # 确保pip是最新版本
    pip install --upgrade pip
    # 从requirements.txt安装库
    pip install -r requirements.txt
    # 安装Playwright浏览器
    playwright install
    ```

---

## 2. 输入数据要求 (重要)

为了确保程序能正确运行，请务必遵循以下数据格式要求。

### Excel 文件要求
- 文件必须是 `.xlsx` 格式。
- 表格的第一行必须是字段名，且字段名**严格区分大小写**。
- 必须包含以下10个字段：

| 字段名                      | 说明         | 是否必填 | 示例值                             |
| --------------------------- | ------------ | -------- | ---------------------------------- |
| `part_number`               | 零件号       | **必填** | `123456`                           |
| `external_info`             | 外部信息     | **必填** | `Some external info`               |
| `internal_comment`          | 内部备注     | **必填** | `Internal testing comment`         |
| `project_type`              | 项目类型     | **必填** | `2`                                |
| `reason`                    | 原因         | **必填** | `250`                              |
| `sample_quantity`           | 样品数量     | **必填** | `10`                               |
| `decision_region`           | 决策区域     | **必填** | `Asia`                             |
| `decision_value`            | 决策值       | **必填** | `10`                               |
| `document_maintenance_path` | 文档主目录   | **必填** | `D:\PEDA\Documents`                |
| `document_path`             | 附件文件路径 | 选填     | `D:\PEDA\Documents\123456\info.pdf` |

### 文档目录结构要求
- 在 `document_maintenance_path` 指定的路径下，为每个零件号创建一个文件夹。
- 在每个零件号文件夹内，根据文档类型创建子文件夹。**文件夹名称必须与下方列表完全一致**。

**示例目录结构**:
```
D:\PEDA\Documents\  <-- 这是 "document_maintenance_path"
├── 123456\
│   ├── Image Documentation\
│   ├── Technical Datasheet\
│   ├── Confidential\
│   ├── Measurement Report\
│   ├── Technical Drawing\
│   └── Other\
└── 654321\
    ├── Image Documentation\
    ├── Technical Datasheet\
    └── ... (其他类别文件夹)
```
- 程序会自动扫描这些文件夹，并将找到的文件上传到系统中对应的类别下。

---

## 3. 运行程序

### GUI 模式 (推荐)
- **快捷方式**: 双击 `install.bat` 创建的 "启动 PEDA V12" 快捷方式。
- **批处理文件**: 双击 `run_gui.bat`。
- **手动启动**:
  ```bash
  # 首先激活虚拟环境
  # venv\Scripts\activate
  python start.py
  ```

### 命令行 (CLI) 模式
- **批处理文件**: 双击 `run_cli.bat`。
- **手动启动**:
  ```bash
  # 首先激活虚拟环境
  # venv\Scripts\activate
  python -m interfaces.cli_interface
  ```

---

## 4. 工作流程

当您点击“开始处理”后，工具将自动执行以下步骤：
1.  **读取输入**: 获取您在GUI中输入的用户名、密码、Excel文件路径和文档主目录。
2.  **解析数据**: 使用Pandas读取并解析Excel文件中的所有行。
3.  **启动浏览器**: 启动一个Playwright控制的浏览器实例。
4.  **用户登录**: 自动导航到PEDA登录页面并完成登录。
5.  **循环处理**:
    - 对于Excel中的每一行数据：
        a. 在系统中搜索对应的 `part_number`。
        b. 自动填写表单中的 `project_type`, `reason` 等字段。
        c. 扫描对应的文档目录，将文件上传到正确的类别中。
        d. 保存并验证条目。
        e. 记录成功或失败状态。
6.  **生成报告**: 处理完成后，在界面上显示成功、失败和跳过的总数。

---

## 5. 项目结构
```
PEDA_V12/
├── start.py              # 主入口文件
├── install.bat           # Windows自动安装脚本
├── run_gui.bat           # GUI启动脚本
├── requirements.txt      # Python依赖清单
├── config/               # 配置模块
├── core/                 # 核心工作流引擎
├── modules/              # 功能模块 (浏览器、数据、表单处理等)
├── gui/                  # 图形界面代码
└── interfaces/           # 接口层 (CLI/GUI)
```

## 技术栈
- **核心语言**: Python 3.8+
- **浏览器自动化**: Playwright
- **数据处理**: Pandas, OpenPyXL
- **图形界面**: Tkinter

## 开发者
- **版本**: 12.0
- **开发者**: Frank Zhang

## 许可证
本项目仅供内部使用。
