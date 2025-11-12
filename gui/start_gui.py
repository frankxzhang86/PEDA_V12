#!/usr/bin/env python3
"""
PEDA自动化处理工具启动脚本
启动带有现代化GUI界面的PEDA自动化处理工具
"""

import sys
import os

# 确保V12根目录在Python路径中
v12_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if v12_root not in sys.path:
    sys.path.insert(0, v12_root)

try:
    from gui.peda_gui_complete import main
    
    if __name__ == "__main__":
        print("=" * 60)
        print("🚀 启动PEDA自动化处理工具")
        print("=" * 60)
        print("功能特点:")
        print("✅ 现代化GUI界面")
        print("✅ 三语言支持 (English/Deutsch/中文)")
        print("✅ 用户名密码输入")
        print("✅ 实时进度跟踪")
        print("✅ 详细日志输出")
        print("✅ 配置保存加载")
        print("✅ 完整下载功能")
        print("=" * 60)
        
        # 启动GUI应用
        main()
        
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("请确保所有依赖已正确安装:")
    print("- pandas")
    print("- playwright")
    print("- tkinter (通常预装)")
    sys.exit(1)
except Exception as e:
    print(f"❌ 启动错误: {e}")
    sys.exit(1) 