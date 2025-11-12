# PEDA自动化处理工具 V9

## 简介
PEDA自动化处理工具V9是一款基于Python和Playwright的批量表单自动化、文档上传与PDF导出工具，支持现代化GUI和多语言界面。

## 快速使用
1. 安装Python 3.8及以上。
2. 安装依赖：
   ```
   pip install -r requirements.txt
   playwright install chromium
   ```
3. 启动程序：
   ```
   python start.py
   ```
4. 按界面提示输入用户名、密码，选择Excel和文档目录，点击“开始处理”。

## 目录结构
- start.py           # 主入口
- chrome-win/        # 浏览器内核（与exe同级）
- requirements.txt   # 依赖
- gui/ modules/ ...  # 主要代码

## 注意事项
- 分发时请确保chrome-win文件夹与exe或主程序同级。
- 如打包为exe，chrome-win同样需手动放置。
- 仅支持Windows 10及以上。

## 常见问题
- 启动报错请检查依赖和chrome-win目录。
- 浏览器无法启动请确认chromium路径设置正确。

## PowerShell 安装与启动详细步骤

1. 打开 PowerShell（建议以管理员身份）。
2. 进入项目目录，例如：
   ```powershell
   cd C:\OES\AI\PIMS_Automation\PEDA_V5
   ```
3. （可选）创建并激活虚拟环境：
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
4. 安装依赖：
   ```powershell
   pip install -r requirements.txt
   playwright install chromium
   ```
5. 启动程序：
   ```powershell
   python start.py
   ```
6. 按照界面提示操作：输入用户名、密码，选择Excel和文档目录，点击“开始处理”。

> 注意事项：
> - 如遇权限问题，可尝试以管理员身份运行PowerShell。
> - 若提示“无法加载脚本”，可先运行：
>   ```powershell
>   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
>   ```
> - 若打包为exe，直接双击exe文件即可，无需命令行。

---
如需详细说明、开发文档或遇到问题，请联系开发者。
