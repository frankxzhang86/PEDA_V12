"""
PEDA自动化处理工具 - 完整GUI界面
支持英语、德语和中文三语言切换
包含所有功能的完整实现
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import queue
import json
import os
import base64
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
import sys

# 导入语言配置模块
from gui.languages import LANGUAGES, get_text, get_available_languages, get_language_display_name, validate_language_code

# 导入文件管理模块
from gui.file_manager import FileManager, validate_file_paths

# 导入UI组件模块
from gui.ui_components import UIComponentManager

# 导入功能控制模块
from gui.function_controller import FunctionController

# 注：避免在GUI冷启动阶段导入重量级依赖（如 pandas/playwright）。
# 相关函数在 FunctionController.run_processing 内部按需延迟导入。

class PEDAAutomationGUI:
    """PEDA自动化处理工具GUI界面"""
    
    def __init__(self):
        try:
            self.root = tk.Tk()
            self.current_language = 'zh'  # 默认中文
            self.system_language = 'zh'   # 默认中文
            self.config_file = 'peda_config.json'
            self.log_queue = queue.Queue()
            
            # 处理状态
            self.is_processing = False
            self.processing_thread = None
            self.processed_count = 0
            self.total_count = 0
            self.success_count = 0
            self.failed_count = 0
            self.skipped_count = 0
              # 初始化上传记录
            self.upload_records = []
            
            # 初始化文件管理器
            self.file_manager = FileManager(log_callback=self.log_message)
            
            # 初始化UI组件管理器
            self.ui_manager = None
            
            # 初始化功能控制器
            self.function_controller = None
            
            # 界面变量
            self.setup_variables()
            self.setup_styles()
            self.init_ui()
            self.load_config()
            self.start_log_monitor()
        except Exception as e:
            print("[EXCEPTION] PEDAAutomationGUI.__init__:", e)
            import traceback
            traceback.print_exc()
            raise
        
    def start_log_monitor(self):
        """启动日志监控"""
        pass
        
    def setup_variables(self):
        """设置界面变量"""
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.remember_password_var = tk.BooleanVar()
        self.show_password_var = tk.BooleanVar()
        self.excel_file_var = tk.StringVar()
        self.document_path_var = tk.StringVar()
        self.ui_language_var = tk.StringVar(value='中文')
        self.system_language_var = tk.StringVar(value='中文')
        self.progress_var = tk.DoubleVar()
        self.current_status_var = tk.StringVar(value='Ready')
        self.login_url_var = tk.StringVar()  # 登录网址变量
        
    def setup_styles(self):
        """设置现代化样式"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # 定义改进的现代化颜色方案
        self.colors = {
            'primary': '#1e40af',           
            'primary_light': '#3b82f6',     
            'primary_dark': '#1e3a8a',      
            'primary_pale': '#dbeafe',      
            'secondary': '#8b5cf6',         
            'secondary_light': '#a78bfa',   
            'secondary_dark': '#7c3aed',    
            'success': '#059669',           
            'success_light': '#10b981',     
            'success_pale': '#d1fae5',      
            'danger': '#dc2626',            
            'danger_light': '#ef4444',      
            'danger_pale': '#fee2e2',       
            'warning': '#d97706',           
            'warning_light': '#f59e0b',     
            'warning_pale': '#fef3c7',      
            'info': '#0ea5e9',              
            'info_light': '#38bdf8',        
            'info_pale': '#e0f2fe',         
            'neutral_50': '#fafafa',        
            'neutral_100': '#f5f5f5',       
            'neutral_200': '#e5e5e5',       
            'neutral_300': '#d1d5db',       
            'neutral_400': '#9ca3af',       
            'neutral_500': '#6b7280',       
            'neutral_600': '#4b5563',       
            'neutral_700': '#374151',       
            'neutral_800': '#1f2937',       
            'neutral_900': '#111827',       
            'white': '#ffffff',
            'light': '#f8fafc',
            'light_border': '#e2e8f0',
            'dark': '#1e293b',
            'medium': '#64748b',
            'card_bg': '#f8fafc',
            'hover': '#f1f5f9',
        }
        self.configure_styles()
        
    def configure_styles(self):
        """配置TTK样式"""
        # 标签框架样式
        self.style.configure('Title.TLabelframe', 
                           background=self.colors['card_bg'],
                           borderwidth=1,
                           relief='solid',
                           bordercolor=self.colors['light_border'])
        self.style.configure('Title.TLabelframe.Label',
                           background=self.colors['card_bg'],
                           foreground=self.colors['dark'],
                           font=('微软雅黑', 10, 'bold'))
        
        # 进度条样式
        self.style.configure('Custom.Horizontal.TProgressbar',
                           background=self.colors['primary'],
                           troughcolor=self.colors['light_border'],
                           borderwidth=0,
                           lightcolor=self.colors['primary'],
                           darkcolor=self.colors['primary'])
        
    def init_ui(self):
        """初始化用户界面"""
        # 先隐藏窗口，防止跳动
        self.root.withdraw()
        self.root.title("PEDA Automation Tool v1.0")
        self.root.configure(bg=self.colors['white'])
        # 不设置geometry，等UI全部加载后再设置

        # 创建UI组件管理器
        self.ui_manager = UIComponentManager(self)
        # 创建功能控制器
        self.function_controller = FunctionController(self)
        # 使用UI组件管理器创建界面
        self.ui_manager.create_main_container()
        self.ui_manager.create_header()
        self.ui_manager.create_content_area()
        self.ui_manager.create_status_bar()
        # 启动时间更新
        self.update_time()
        # 所有UI加载完毕后再设置大小和居中，并显示窗口
        self.root.geometry("900x900")
        self.center_window()
        self.root.deiconify()
        
    def center_window(self):
        """窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def update_time(self):
        """更新时间显示"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
          
    # 委托方法到功能控制器
    def choose_excel_file(self):
        return self.function_controller.choose_excel_file()
            
    def choose_document_folder(self):
        return self.function_controller.choose_document_folder()
              
    def validate_inputs(self):
        return self.function_controller.validate_inputs()
        
    def start_processing(self):
        return self.function_controller.start_processing()
        
    def stop_processing(self):
        return self.function_controller.stop_processing()
        
    def reset_processing(self):
        return self.function_controller.reset_processing()
        
    def reset_stats(self):
        return self.function_controller.reset_stats()
        
    def run_processing(self):
        return self.function_controller.run_processing()
    
    def update_progress_from_callback(self, progress, status):
        return self.function_controller.update_progress_from_callback(progress, status)
    
    def log_message_from_callback(self, message, level="INFO"):
        return self.function_controller.log_message_from_callback(message, level)
    
    def add_upload_record(self, filename, status, error_msg="", file_type="PDF", file_size=""):
        return self.function_controller.add_upload_record(filename, status, error_msg, file_type, file_size)
            
    def update_progress_display(self):
        return self.function_controller.update_progress_display()
        
    def update_stats_display(self):
        return self.function_controller.update_stats_display()
        
    def update_status(self, status):
        return self.function_controller.update_status(status)
        
    def log_message(self, message, level="INFO"):
        return self.function_controller.log_message(message, level)
        
    def clear_log(self):
        return self.function_controller.clear_log()
        
    def download_report(self):
        return self.function_controller.download_report()

    def download_error_log(self):
        return self.function_controller.download_error_log()

    def download_upload_record(self):
        return self.function_controller.download_upload_record()
    
    # 语言切换方法
    def switch_language(self, lang):
        """切换界面语言"""
        if lang not in LANGUAGES:
            lang = 'zh'
        
        self.current_language = lang
        self.update_ui_texts()
        self.update_language_buttons()
        self.save_config()

    def update_language_buttons(self):
        """更新语言按钮的选中状态"""
        # 重置所有按钮状态
        self.en_btn.config(bg=self.colors['primary_pale'], fg=self.colors['primary'], font=('微软雅黑', 9))
        self.de_btn.config(bg=self.colors['primary_pale'], fg=self.colors['primary'], font=('微软雅黑', 9))
        self.zh_btn.config(bg=self.colors['primary_pale'], fg=self.colors['primary'], font=('微软雅黑', 9))
        
        # 高亮当前选中的语言按钮
        if self.current_language == 'en':
            self.en_btn.config(bg=self.colors['white'], fg=self.colors['primary'], font=('微软雅黑', 9, 'bold'))
        elif self.current_language == 'de':
            self.de_btn.config(bg=self.colors['white'], fg=self.colors['primary'], font=('微软雅黑', 9, 'bold'))
        elif self.current_language == 'zh':
            self.zh_btn.config(bg=self.colors['white'], fg=self.colors['primary'], font=('微软雅黑', 9, 'bold'))
        
    def update_ui_texts(self):
        """更新界面文本"""
        try:
            if self.current_language not in LANGUAGES:
                self.current_language = 'zh'
            texts = LANGUAGES[self.current_language]
            # 更新窗口标题
            self.root.title(texts['title'])
            # 区域标题
            if hasattr(self, 'login_frame'):
                self.login_frame.config(text=texts['login_info'])
            if hasattr(self, 'file_frame'):
                self.file_frame.config(text=texts['file_selection'])
            if hasattr(self, 'control_frame'):
                self.control_frame.config(text=texts['operation_control'])
            if hasattr(self, 'progress_frame'):
                self.progress_frame.config(text=texts['processing_status'])
            if hasattr(self, 'record_frame'):
                self.record_frame.config(text=texts['record_management'])
            # 标签页
            if hasattr(self, 'notebook'):
                self.notebook.tab(0, text=texts['main_tab'])
                self.notebook.tab(1, text=texts['logs_tab'])
            # 登录区
            if hasattr(self, 'login_url_label'):
                self.login_url_label.config(text=texts.get('login_url', '登录网址'))
            if hasattr(self, 'username_label'):
                self.username_label.config(text=texts['username'])
            if hasattr(self, 'password_label'):
                self.password_label.config(text=texts['password'])
            if hasattr(self, 'remember_cb'):
                self.remember_cb.config(text=texts['remember_password'])
            if hasattr(self, 'show_password_cb'):
                self.show_password_cb.config(text=texts['show_password'])
            if hasattr(self, 'save_settings_btn'):
                self.save_settings_btn.config(text=texts.get('save_settings', texts.get('login', '保存')))
            # 文件选择区
            if hasattr(self, 'excel_file_label'):
                self.excel_file_label.config(text=texts['excel_file'])
            if hasattr(self, 'excel_btn'):
                self.excel_btn.config(text=texts['choose_file'])
            if hasattr(self, 'document_path_label'):
                self.document_path_label.config(text=texts['document_path'])
            if hasattr(self, 'document_btn'):
                self.document_btn.config(text=texts['choose_folder'])
            # 操作按钮
            if hasattr(self, 'start_btn'):
                self.start_btn.config(text=texts['start_processing'])
            if hasattr(self, 'stop_btn'):
                self.stop_btn.config(text=texts['stop_processing'])
            if hasattr(self, 'reset_btn'):
                self.reset_btn.config(text=texts['reset'])
            # 进度区
            if hasattr(self, 'total_progress_label'):
                self.total_progress_label.config(text=texts['total_progress'])
            if hasattr(self, 'current_label'):
                self.current_label.config(text=texts['current_status'])
            # 统计标签
            if hasattr(self, 'stats_text_labels'):
                stats_mapping = {'success': 'success', 'failed': 'failed', 'total': 'total'}
                for key, text_key in stats_mapping.items():
                    if key in self.stats_text_labels:
                        self.stats_text_labels[key].config(text=texts[text_key])
            # 记录管理
            if hasattr(self, 'download_report_btn'):
                self.download_report_btn.config(text=texts['download_report'])
            if hasattr(self, 'download_error_btn'):
                self.download_error_btn.config(text=texts['download_error_log'])
            if hasattr(self, 'download_upload_btn'):
                self.download_upload_btn.config(text=texts['download_upload_record'])
            # 日志区
            if hasattr(self, 'log_title_label'):
                self.log_title_label.config(text=texts['log_output'])
            if hasattr(self, 'clear_log_btn'):
                self.clear_log_btn.config(text=texts['clear_log'])
            # 状态栏
            if hasattr(self, 'status_text'):
                self.status_text.config(text=texts['ready'])
            # 当前状态
            self.current_status_var.set(texts['ready'])
        except Exception as e:
            print(f"更新界面文本错误: {e}")
            
    # 配置管理方法
    def save_config(self):
        """保存配置到文件"""
        try:
            self.file_manager.set_paths(
                excel_path=self.excel_file_var.get(),
                document_path=self.document_path_var.get()
            )
            
            config = {
                'username': self.username_var.get() if not self.remember_password_var.get() else self.username_var.get(),
                'password': self.encrypt_password(self.password_var.get()) if self.remember_password_var.get() else "",
                'remember_password': self.remember_password_var.get(),
                'excel_file': self.excel_file_var.get(),
                'document_path': self.document_path_var.get(),
                'current_language': self.current_language,
                'system_language': self.system_language,
                'login_url': self.login_url_var.get(),
                'browser': {
                    'preferred_type': getattr(self, 'browser_preferred_type', 'auto'),
                    'custom_path': getattr(self, 'browser_custom_path', None)
                }
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            self.log_message(get_text(self.current_language, 'config_saved'))
            # 配置保存后可触发后台预热（延迟导入 pandas/playwright），加快后续处理启动
            try:
                if hasattr(self, 'function_controller') and self.function_controller:
                    self.function_controller.start_preload()
            except Exception:
                pass
            
        except Exception as e:
            self.log_message(f"保存配置失败: {str(e)}", "ERROR")

    def load_config(self):
        """从文件加载配置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                self.username_var.set(config.get('username', ''))
                if config.get('remember_password', False):
                    self.password_var.set(self.decrypt_password(config.get('password', '')))
                self.remember_password_var.set(config.get('remember_password', False))
                
                excel_file = config.get('excel_file', '')
                document_path = config.get('document_path', '')
                self.excel_file_var.set(excel_file)
                self.document_path_var.set(document_path)
                
                self.file_manager.set_paths(excel_path=excel_file, document_path=document_path)
                
                self.current_language = config.get('current_language', 'zh')
                self.system_language = config.get('system_language', 'zh')
                
                self.login_url_var.set(config.get('login_url', ''))
                
                # 加载浏览器配置
                browser_config = config.get('browser', {})
                self.browser_preferred_type = browser_config.get('preferred_type', 'auto')
                self.browser_custom_path = browser_config.get('custom_path', None)
                
                self.update_ui_texts()
                self.update_language_buttons()
                
        except Exception as e:
            self.log_message(f"加载配置失败: {str(e)}", "ERROR")

    def encrypt_password(self, password):
        """简单的密码加密"""
        if not password:
            return ""
        return base64.b64encode(password.encode()).decode()

    def decrypt_password(self, encrypted):
        """简单的密码解密"""
        if not encrypted:
            return ""
        try:
            return base64.b64decode(encrypted.encode()).decode()
        except:
            return ""
            
    def run(self):
        """运行GUI应用"""
        self.root.mainloop()

    def toggle_password_visibility(self):
        """切换密码可见性"""
        if hasattr(self, 'password_entry'):
            if self.show_password_var.get():
                self.password_entry.config(show="")
            else:
                self.password_entry.config(show="*")

def main():
    print(">>> PEDAAutomationGUI main() called")
    try:
        app = PEDAAutomationGUI()
        app.run()
    except Exception as e:
        print(f"启动GUI失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()