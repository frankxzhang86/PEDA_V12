"""
PEDA自动化处理工具 - 功能控制模块
包含所有功能和业务逻辑处理
"""

import threading
from datetime import datetime
from tkinter import messagebox, filedialog
from .languages import get_text, LANGUAGES


class FunctionController:
    """功能控制器 - 负责处理所有业务逻辑和功能控制"""
    
    def __init__(self, parent_app):
        """
        初始化功能控制器
        
        Args:
            parent_app: 父应用程序实例（PEDAAutomationGUI）
        """
        self.app = parent_app
        self.use_browser_reuse = True  # 默认使用浏览器复用模式
        # 预热标志，防止重复预热
        self._preload_started = False
        self._preload_lock = threading.Lock()
        # 缓存浏览器查找器实例（用于预热和后续使用）
        self._browser_finder = None
        
    # =================
    # 文件选择方法
    # =================
    
    def choose_excel_file(self):
        """选择Excel文件"""
        file_path = self.app.file_manager.choose_excel_file()
        if file_path:
            self.app.excel_file_var.set(file_path)
            # 在用户选择了Excel文件后，后台预热重量级模块（pandas, playwright）
            try:
                self.start_preload()
            except Exception:
                # 预热失败不影响功能
                pass
            
    def choose_document_folder(self):
        """选择文档文件夹"""
        folder_path = self.app.file_manager.choose_document_folder()
        if folder_path:
            self.app.document_path_var.set(folder_path)
    
    # =================
    # 处理控制方法
    # =================
    
    def validate_inputs(self):
        """验证输入"""
        if not self.app.username_var.get().strip():
            messagebox.showerror("Error", get_text(self.app.current_language, 'enter_credentials'))
            return False
            
        if not self.app.password_var.get().strip():
            messagebox.showerror("Error", get_text(self.app.current_language, 'enter_credentials'))
            return False
            
        # 使用文件管理器验证文件路径
        excel_path = self.app.excel_file_var.get().strip()
        document_path = self.app.document_path_var.get().strip()
        
        if not excel_path:
            messagebox.showerror("Error", get_text(self.app.current_language, 'select_excel_first'))
            return False
            
        if not document_path:
            messagebox.showerror("Error", get_text(self.app.current_language, 'select_document_path'))
            return False
        
        # 使用文件管理器验证路径有效性
        if not self.app.file_manager.validate_all_paths(excel_path, document_path):
            messagebox.showerror("Error", "Selected files or folders are not valid")
            return False
            
        return True
        
    def start_processing(self):
        """开始处理"""
        print("[DEBUG] start_processing called")
        self.log_message("点击了开始处理按钮", "INFO")
        
        if not self.validate_inputs():
            self.log_message("输入验证失败", "ERROR")
            return
            
        if self.app.is_processing:
            self.log_message("处理已在进行中", "WARNING")
            return
            
        self.log_message("开始启动处理线程", "INFO")
        self.app.is_processing = True
        self.app.start_btn.config(state='disabled')
        self.app.stop_btn.config(state='normal', fg=self.app.colors['white'])
        
        # 重置统计
        self.reset_stats()
        
        # 在后台线程中运行处理
        self.app.processing_thread = threading.Thread(target=self.run_processing, daemon=True)
        self.app.processing_thread.start()
        self.log_message("处理线程已启动", "INFO")
        
        self.log_message(get_text(self.app.current_language, 'processing_started'))
        self.update_status(get_text(self.app.current_language, 'processing'))
        
    def stop_processing(self):
        """停止处理"""
        self.app.is_processing = False
        self.app.start_btn.config(state='normal')
        self.app.stop_btn.config(state='disabled', fg=self.app.colors['white'])
        
        self.log_message("Processing stopped by user")
        self.update_status(get_text(self.app.current_language, 'idle'))
        
    def reset_processing(self):
        """重置处理状态"""
        self.stop_processing()
        self.reset_stats()
        self.app.progress_var.set(0)
        self.update_progress_display()
        
        self.update_status(get_text(self.app.current_language, 'ready'))
        self.log_message("Processing reset")
        
    def reset_stats(self):
        """重置统计数据"""
        self.app.processed_count = 0
        self.app.total_count = 0
        self.app.success_count = 0
        self.app.failed_count = 0
        self.app.skipped_count = 0
        self.update_stats_display()
        
    def run_processing(self):
        """运行处理逻辑"""
        print("[DEBUG] run_processing called")
        result = None  # 新增：用于保存处理结果
        try:
            # 延迟导入，避免应用启动时加载重量级依赖（playwright/pandas 等）
            from interfaces.gui_interface import (
                run_with_gui_params, run_with_gui_params_v2
            )
            # 获取用户输入的参数
            excel_path = self.app.excel_file_var.get()
            print(f"[DEBUG] excel_path: {excel_path}")
            document_path = self.app.document_path_var.get()
            print(f"[DEBUG] document_path: {document_path}")
            username = self.app.username_var.get()
            print(f"[DEBUG] username: {username}")
            password = self.app.password_var.get()
            print(f"[DEBUG] password: {password}")
            
            # 系统语言映射
            sys_lang_map = {
                'English': 'en',
                'Deutsch': 'de', 
                '中文': 'zh'
            }
            system_language = sys_lang_map.get(self.app.system_language_var.get(), 'zh')
            
            self.log_message(f"开始PEDA自动化处理:")
            self.log_message(f"- Excel文件: {excel_path}")
            self.log_message(f"- 文档路径: {document_path}")
            self.log_message(f"- 用户: {username}")
            self.log_message(f"- 系统语言: {system_language}")
            
            print(f"[DEBUG] use_browser_reuse: {self.use_browser_reuse}")
            # 根据模式选择处理函数
            if self.use_browser_reuse:
                print("[DEBUG] about to call run_with_gui_params_v2")
                # 获取浏览器配置
                browser_path = getattr(self.app, 'browser_custom_path', None)
                preferred_browser = getattr(self.app, 'browser_preferred_type', 'auto')
                # 获取登录URL
                login_url = self.app.login_url_var.get() if self.app.login_url_var.get().strip() else None
                
                result = run_with_gui_params_v2(
                    excel_path=excel_path,
                    document_path=document_path,
                    username=username,
                    password=password,
                    system_language=system_language,
                    progress_callback=self.update_progress_from_callback,
                    log_callback=self.log_message_from_callback,
                    upload_record_callback=self.add_upload_record,
                    login_url=login_url,
                    browser_path=browser_path,
                    preferred_browser=preferred_browser,
                    browser_finder=self._browser_finder  # 传递预热的 browser_finder
                )
                print(f"[DEBUG] run_with_gui_params_v2 returned: {result}")
            else:
                print("[DEBUG] about to call run_with_gui_params")
                result = run_with_gui_params(
                    excel_path=excel_path,
                    document_path=document_path,
                    username=username,
                    password=password,
                    system_language=system_language,
                    progress_callback=self.update_progress_from_callback,
                    log_callback=self.log_message_from_callback
                )
                print(f"[DEBUG] run_with_gui_params returned: {result}")
            # 新增：同步统计到界面
            if isinstance(result, dict):
                self.app.success_count = result.get('success', 0)
                self.app.failed_count = result.get('failed', 0)
                self.app.total_count = result.get('total', 0)
                # === 关键：同步上传记录 ===
                if 'upload_records' in result:
                    self.app.upload_records = result['upload_records']
                    # 新增：刷新表格
                    self.app.root.after(0, self.app.ui.refresh_upload_records_table)
                self.app.root.after(0, self.update_stats_display)
            if result and (not isinstance(result, dict) or result.get('success', 0) > 0):
                self.log_message("🎉 所有处理完成！", "SUCCESS")
            else:
                self.log_message("⚠️ 处理过程中出现错误", "ERROR")
        except Exception as e:
            self.log_message(f"处理过程中发生异常: {str(e)}", "ERROR")
        finally:
            self.app.is_processing = False
            self.app.root.after(0, lambda: self.app.start_btn.config(state='normal'))
            self.app.root.after(0, lambda: self.app.stop_btn.config(state='disabled', fg=self.app.colors['white']))
            
            texts = LANGUAGES[self.app.current_language]
            self.app.root.after(0, lambda: self.update_status(texts['ready']))
            self.app.root.after(0, lambda: self.log_message(texts['processing_complete']))

    def start_preload(self):
        """在后台异步预加载重量级依赖，减少用户点击开始时的等待。"""
        with self._preload_lock:
            if self._preload_started:
                return
            self._preload_started = True

        def _worker():
            try:
                self.log_message("预热：开始在后台加载 pandas 和 playwright 模块...", "INFO")
                try:
                    import importlib
                    importlib.import_module('pandas')
                    self.log_message("预热：pandas 导入完成", "INFO")
                except Exception as e:
                    self.log_message(f"预热警告：pandas 导入失败或未安装: {e}", "WARNING")

                try:
                    # 导入 playwright 的 sync_api，注意如果未安装会抛异常
                    import importlib
                    importlib.import_module('playwright.sync_api')
                    self.log_message("预热：playwright 导入完成", "INFO")
                except Exception as e:
                    self.log_message(f"预热警告：playwright 导入失败或未安装: {e}", "WARNING")

                # 预热浏览器查找（查找并缓存浏览器路径，不启动浏览器）
                try:
                    self.log_message("预热：开始查找浏览器路径...", "INFO")
                    from modules.browser_finder import BrowserFinder
                    
                    # 创建浏览器查找器实例并缓存
                    self._browser_finder = BrowserFinder(log_callback=self.log_message)
                    
                    # 执行查找（会自动缓存结果到 finder 内部）
                    browser_path, browser_type = self._browser_finder.find_browser()
                    
                    if browser_path:
                        self.log_message(f"预热：浏览器查找完成 - {browser_type}: {browser_path}", "INFO")
                    else:
                        self.log_message("预热警告：未找到可用浏览器，后续处理时将重新查找", "WARNING")
                except Exception as e:
                    self.log_message(f"预热警告：浏览器查找失败: {e}", "WARNING")

                self.log_message("预热完成。", "INFO")
            except Exception as e:
                self.log_message(f"预热时发生异常: {e}", "WARNING")

        t = threading.Thread(target=_worker, daemon=True)
        t.start()
    
    def update_progress_from_callback(self, progress, status):
        """从处理回调更新进度"""
        def update():
            self.app.progress_var.set(progress)
            self.app.current_status_var.set(status)
            self.update_progress_display()
        self.app.root.after(0, update)
    
    def log_message_from_callback(self, message, level="INFO"):
        print(f"[DEBUG] log_message_from_callback called: {message} [{level}]")
        """从处理回调添加日志"""
        def add_log():
            self.log_message(message, level)
        self.app.root.after(0, add_log)
    
    def add_upload_record(self, part_number, filename, success, reason=""):
        """添加上传记录（标准化字段）"""
        if not hasattr(self.app, 'upload_records'):
            self.app.upload_records = []
        record = {
            'Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Part_number': part_number,
            'FileName': filename,
            'Success': success,
            'Reason': reason
        }
        self.app.upload_records.append(record)

    def download_report(self):
        """下载处理报告（明细：件号+文件名，每个文件一行，成功/失败都记录）"""
        try:
            # 延迟导入 pandas，避免GUI冷启动变慢
            import pandas as pd
            # 自动生成文件名：YYYYDDMM_file_name.xlsx
            today = datetime.now().strftime("%Y%d%m")
            default_name = f"{today}_file_upload_report.xlsx"
            filename = filedialog.asksaveasfilename(
                title="保存处理报告",
                defaultextension=".xlsx",
                initialfile=default_name,
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
            )
            if filename:
                # 导出明细：件号+文件名
                if hasattr(self.app, 'upload_records') and self.app.upload_records:
                    df = pd.DataFrame(self.app.upload_records)
                    # 只保留件号和文件名两列
                    df = df[['Part_number', 'FileName']]
                else:
                    df = pd.DataFrame(columns=['Part_number', 'FileName'])
                df.to_excel(filename, index=False)
                messagebox.showinfo("成功", f"报告已保存到: {filename}")
                self.log_message(f"处理报告已保存: {filename}")
        except Exception as e:
            messagebox.showerror("错误", f"保存报告失败: {str(e)}")
            self.log_message(f"保存报告失败: {str(e)}", "ERROR")

    def download_error_log(self):
        """下载错误日志"""
        try:
            filename = filedialog.asksaveasfilename(
                title="保存错误日志",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if filename:
                log_content = self.app.log_text.get(1.0, 'end')
                
                header = f"""
=== PEDA 自动化处理工具 - 错误日志 ===
生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
用户: {self.app.username_var.get()}
Excel文件: {self.app.excel_file_var.get()}
文档路径: {self.app.document_path_var.get()}
系统语言: {self.app.current_language}
=== 日志内容 ===

"""
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(header + log_content)
                
                messagebox.showinfo("成功", f"错误日志已保存到: {filename}")
                self.log_message(f"错误日志已保存: {filename}")
                
        except Exception as e:
            messagebox.showerror("错误", f"保存错误日志失败: {str(e)}")
            self.log_message(f"保存错误日志失败: {str(e)}", "ERROR")

    def download_upload_record(self):
        """下载上传记录（标准表头）"""
        try:
            # 延迟导入 pandas，避免GUI冷启动变慢
            import pandas as pd
            default_name = datetime.now().strftime("%Y%m%d") + "_Upload_records.xlsx"
            filename = filedialog.asksaveasfilename(
                title="保存上传记录",
                defaultextension=".xlsx",
                initialfile=default_name,
                filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv"), ("All files", "*.*")]
            )
            if filename:
                columns = ['Date', 'Part_number', 'FileName', 'Success', 'Reason']
                if hasattr(self.app, 'upload_records') and self.app.upload_records:
                    df = pd.DataFrame(self.app.upload_records)
                    df = df.reindex(columns=columns)
                else:
                    df = pd.DataFrame(columns=columns)
                sheet_name = datetime.now().strftime("%Y%m%d") + "_Upload_records"
                if filename.endswith('.xlsx'):
                    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                else:
                    df.to_csv(filename, index=False, encoding='utf-8-sig')
                messagebox.showinfo("成功", f"上传记录已保存到: {filename}")
                self.log_message(f"上传记录已保存: {filename}")
        except Exception as e:
            messagebox.showerror("错误", f"保存上传记录失败: {str(e)}")
            self.log_message(f"保存上传记录失败: {str(e)}", "ERROR")

    def log_message(self, message, level="INFO"):
        """添加日志消息（防止未定义报错）"""
        # 若无日志控件，直接打印
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            formatted_message = f"[{timestamp}] {level}: {message}\n"
            if hasattr(self.app, 'log_text'):
                self.app.log_text.config(state='normal')
                self.app.log_text.insert('end', formatted_message)
                self.app.log_text.config(state='disabled')
                self.app.log_text.see('end')
            else:
                print(formatted_message)
        except Exception as e:
            print(f"[log_message ERROR] {e} | 原始消息: {message}")
    
    def update_stats_display(self):
        """更新统计显示，防止未定义报错"""
        try:
            if hasattr(self.app, 'stats_labels'):
                self.app.stats_labels['success'].config(text=str(getattr(self.app, 'success_count', 0)))
                self.app.stats_labels['failed'].config(text=str(getattr(self.app, 'failed_count', 0)))
                self.app.stats_labels['total'].config(text=str(getattr(self.app, 'total_count', 0)))
            else:
                print(f"[update_stats_display] 成功:{getattr(self.app, 'success_count', 0)} 失败:{getattr(self.app, 'failed_count', 0)} 总数:{getattr(self.app, 'total_count', 0)}")
        except Exception as e:
            print(f"[update_stats_display ERROR] {e}")
    
    def update_progress_display(self):
        """更新进度显示，防止未定义报错"""
        try:
            if hasattr(self.app, 'progress_label') and hasattr(self.app, 'progress_var'):
                progress = self.app.progress_var.get()
                self.app.progress_label.config(text=f"{progress:.0f}%")
            else:
                print(f"[update_progress_display] 当前进度: {getattr(self.app, 'progress_var', 0)}")
        except Exception as e:
            print(f"[update_progress_display ERROR] {e}")

    def update_status(self, status):
        """更新状态显示，防止未定义报错"""
        try:
            if hasattr(self.app, 'status_text'):
                self.app.status_text.config(text=status)
            else:
                print(f"[update_status] 状态: {status}")
        except Exception as e:
            print(f"[update_status ERROR] {e}")
    
    def clear_log(self):
        """清空日志显示区"""
        try:
            if hasattr(self.app, 'log_text'):
                self.app.log_text.config(state='normal')
                self.app.log_text.delete(1.0, 'end')
                self.app.log_text.config(state='disabled')
        except Exception as e:
            print(f"[clear_log ERROR] {e}")