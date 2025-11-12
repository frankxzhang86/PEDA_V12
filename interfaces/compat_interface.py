"""
兼容性接口文件
为了保持与原 auto_form_fill_2.py 的向后兼容性
"""

# 导入各模块的功能
from .cli_interface import main
from .gui_interface import run_with_gui_params

# 重新导出，保持原有接口
__all__ = ['main', 'run_with_gui_params'] 