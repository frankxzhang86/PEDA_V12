# GUI模块包初始化文件
# PEDA自动化处理工具 - 图形用户界面模块
# 注意：不要在此处急切导入子模块，避免导入锁冲突导致 KeyboardInterrupt。
# 使用方应直接 from gui.peda_gui_complete import ... 按需导入。

__all__ = ['PEDAAutomationGUI', 'main', 'start_gui_main']


def __getattr__(name):
    """延迟导入，避免包初始化时触发重量级依赖加载"""
    if name in ('PEDAAutomationGUI', 'main'):
        from .peda_gui_complete import PEDAAutomationGUI, main
        return PEDAAutomationGUI if name == 'PEDAAutomationGUI' else main
    if name == 'start_gui_main':
        from .start_gui import main as start_gui_main
        return start_gui_main
    raise AttributeError(f"module 'gui' has no attribute {name!r}")