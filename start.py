#!/usr/bin/env python3
"""
PEDA自动化处理工具 V12 - 主启动脚本
V12独立版本的主入口点
"""

import sys
import os

# 自动加载外部依赖目录（如libs）
if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)
    libs_path = os.path.join(base_dir, 'libs')
    if os.path.exists(libs_path):
        sys.path.insert(0, libs_path)

# 确保当前目录（V12根目录）在Python路径中
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def get_chrome_executable():
    """
    获取 chrome-win 目录下 chrome.exe 的绝对路径，兼容 PyInstaller 打包环境。
    """
    if getattr(sys, 'frozen', False):
        # exe模式，返回exe所在目录
        base_dir = os.path.dirname(sys.executable)
    else:
        # 源码模式，返回py文件所在目录
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "chrome-win", "chrome.exe")

def main():
    """主函数"""
    try:
        print(">>> main() started")
        print("=" * 70)
        print("🚀 PEDA自动化处理工具 V12")
        print("=" * 70)
        print("版本特点:")
        print("✅ 独立V12版本")
        print("✅ 现代化GUI界面")
        print("✅ 三语言支持 (English/Deutsch/中文)")
        print("✅ 完整的模块化架构")
        print("✅ 用户名密码输入")
        print("✅ 实时进度跟踪")
        print("✅ 详细日志输出")
        print("✅ 配置保存加载")
        print("✅ 完整下载功能")
        print("=" * 70)
        
        # 导入并启动GUI
        from gui.peda_gui_complete import main as gui_main
        gui_main()
        
    except ImportError as e:
        print(f"❌ 模块导入错误: {e}")
        print("\n请检查以下依赖是否正确安装:")
        print("- pandas")
        print("- playwright")
        print("- tkinter (通常预装)")
        print("\n安装命令:")
        print("pip install pandas playwright")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"❌ 启动错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()