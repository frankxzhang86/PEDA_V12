"""
PEDA自动化处理工具 - 文件处理模块
负责文件选择、验证和路径管理功能
"""

import os
import pandas as pd
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import Optional, List, Dict, Any, Callable


class FileManager:
    """文件管理器类 - 处理所有文件相关操作"""
    
    def __init__(self, log_callback: Optional[Callable[[str, str], None]] = None):
        """
        初始化文件管理器
        
        Args:
            log_callback: 日志回调函数，用于记录操作日志
        """
        self.log_callback = log_callback
        self.excel_file_path = ""
        self.document_folder_path = ""
        
        # 支持的文件类型
        self.supported_excel_types = [
            ("Excel files", "*.xlsx *.xls"),
            ("CSV files", "*.csv"),
            ("All files", "*.*")
        ]
        
    def log(self, message: str, level: str = "INFO"):
        """记录日志消息"""
        if self.log_callback:
            self.log_callback(message, level)
    
    # =================
    # 文件选择方法
    # =================
    
    def choose_excel_file(self) -> Optional[str]:
        """
        选择Excel文件
        
        Returns:
            Optional[str]: 选中的文件路径，如果取消选择则返回None
        """
        try:
            file_path = filedialog.askopenfilename(
                title="Choose Excel File",
                filetypes=self.supported_excel_types
            )
            
            if file_path:
                self.excel_file_path = file_path
                self.log(f"Selected Excel file: {file_path}")
                return file_path
            return None
            
        except Exception as e:
            self.log(f"选择Excel文件时出错: {str(e)}", "ERROR")
            return None
            
    def choose_document_folder(self) -> Optional[str]:
        """
        选择文档文件夹
        
        Returns:
            Optional[str]: 选中的文件夹路径，如果取消选择则返回None
        """
        try:
            folder_path = filedialog.askdirectory(title="Choose Document Folder")
            
            if folder_path:
                self.document_folder_path = folder_path
                self.log(f"Selected document path: {folder_path}")
                return folder_path
            return None
            
        except Exception as e:
            self.log(f"选择文档文件夹时出错: {str(e)}", "ERROR")
            return None
    
    # =================
    # 文件验证方法
    # =================
    
    def validate_excel_file(self, file_path: str) -> bool:
        """
        验证Excel文件是否有效
        
        Args:
            file_path (str): Excel文件路径
            
        Returns:
            bool: 文件是否有效
        """
        try:
            if not file_path or not file_path.strip():
                self.log("Excel文件路径为空", "ERROR")
                return False
                
            if not os.path.exists(file_path):
                self.log(f"Excel文件不存在: {file_path}", "ERROR")
                return False
                
            # 检查文件扩展名
            file_ext = Path(file_path).suffix.lower()
            if file_ext not in ['.xlsx', '.xls', '.csv']:
                self.log(f"不支持的文件格式: {file_ext}", "ERROR")
                return False
                
            # 尝试读取文件头部以验证格式
            try:
                if file_ext == '.csv':
                    pd.read_csv(file_path, nrows=1)
                else:
                    pd.read_excel(file_path, nrows=1)
                    
                self.log(f"Excel文件验证成功: {file_path}")
                return True
                
            except Exception as read_error:
                self.log(f"Excel文件格式错误: {str(read_error)}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"验证Excel文件时出错: {str(e)}", "ERROR")
            return False
    
    def validate_document_folder(self, folder_path: str) -> bool:
        """
        验证文档文件夹是否有效
        
        Args:
            folder_path (str): 文档文件夹路径
            
        Returns:
            bool: 文件夹是否有效
        """
        try:
            if not folder_path or not folder_path.strip():
                self.log("文档文件夹路径为空", "ERROR")
                return False
                
            if not os.path.exists(folder_path):
                self.log(f"文档文件夹不存在: {folder_path}", "ERROR")
                return False
                
            if not os.path.isdir(folder_path):
                self.log(f"指定路径不是文件夹: {folder_path}", "ERROR")
                return False
                
            # 检查文件夹是否可读
            if not os.access(folder_path, os.R_OK):
                self.log(f"文档文件夹无读取权限: {folder_path}", "ERROR")
                return False
                
            self.log(f"文档文件夹验证成功: {folder_path}")
            return True
            
        except Exception as e:
            self.log(f"验证文档文件夹时出错: {str(e)}", "ERROR")
            return False
    
    def validate_all_paths(self, excel_path: str, document_path: str) -> bool:
        """
        验证所有文件路径
        
        Args:
            excel_path (str): Excel文件路径
            document_path (str): 文档文件夹路径
            
        Returns:
            bool: 所有路径是否都有效
        """
        excel_valid = self.validate_excel_file(excel_path)
        folder_valid = self.validate_document_folder(document_path)
        
        return excel_valid and folder_valid
    
    # =================
    # 文件读取方法
    # =================
    
    def read_excel_data(self, file_path: str) -> Optional[List[Dict[str, Any]]]:
        """
        读取Excel文件数据
        
        Args:
            file_path (str): Excel文件路径
            
        Returns:
            Optional[List[Dict[str, Any]]]: 读取的数据列表，失败时返回None
        """
        try:
            if not self.validate_excel_file(file_path):
                return None
                
            file_ext = Path(file_path).suffix.lower()
            
            if file_ext == '.csv':
                df = pd.read_csv(file_path, encoding='utf-8-sig')
            else:
                df = pd.read_excel(file_path)
            
            # 转换为字典列表
            data_list = df.to_dict('records')
            
            self.log(f"成功读取Excel数据，共 {len(data_list)} 行")
            return data_list
            
        except Exception as e:
            self.log(f"读取Excel文件失败: {str(e)}", "ERROR")
            return None
    
    def get_excel_info(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        获取Excel文件信息
        
        Args:
            file_path (str): Excel文件路径
            
        Returns:
            Optional[Dict[str, Any]]: 文件信息字典
        """
        try:
            if not os.path.exists(file_path):
                return None
                
            file_stat = os.stat(file_path)
            file_info = {
                'path': file_path,
                'name': os.path.basename(file_path),
                'size': file_stat.st_size,
                'size_mb': round(file_stat.st_size / (1024 * 1024), 2),
                'modified_time': file_stat.st_mtime,
                'extension': Path(file_path).suffix.lower()
            }
            
            # 尝试获取行数和列数
            try:
                if file_info['extension'] == '.csv':
                    df = pd.read_csv(file_path, nrows=1)
                    row_count = sum(1 for _ in open(file_path, 'r', encoding='utf-8-sig'))
                else:
                    df = pd.read_excel(file_path)
                    row_count = len(df)
                
                file_info['rows'] = row_count
                file_info['columns'] = len(df.columns)
                file_info['column_names'] = df.columns.tolist()
                
            except Exception:
                file_info['rows'] = 0
                file_info['columns'] = 0
                file_info['column_names'] = []
            
            return file_info
            
        except Exception as e:
            self.log(f"获取Excel文件信息失败: {str(e)}", "ERROR")
            return None
    
    def scan_document_folder(self, folder_path: str, extensions: List[str] = None) -> List[Dict[str, Any]]:
        """
        扫描文档文件夹中的文件
        
        Args:
            folder_path (str): 文档文件夹路径
            extensions (List[str], optional): 要扫描的文件扩展名列表，默认为PDF
            
        Returns:
            List[Dict[str, Any]]: 文件信息列表
        """
        if extensions is None:
            extensions = ['.pdf', '.doc', '.docx', '.txt']
            
        try:
            if not self.validate_document_folder(folder_path):
                return []
            
            files = []
            for root, dirs, filenames in os.walk(folder_path):
                for filename in filenames:
                    file_ext = Path(filename).suffix.lower()
                    if file_ext in extensions:
                        file_path = os.path.join(root, filename)
                        file_stat = os.stat(file_path)
                        
                        file_info = {
                            'name': filename,
                            'path': file_path,
                            'relative_path': os.path.relpath(file_path, folder_path),
                            'size': file_stat.st_size,
                            'size_mb': round(file_stat.st_size / (1024 * 1024), 2),
                            'extension': file_ext,
                            'modified_time': file_stat.st_mtime
                        }
                        files.append(file_info)
            
            self.log(f"扫描文档文件夹完成，发现 {len(files)} 个文件")
            return files
            
        except Exception as e:
            self.log(f"扫描文档文件夹失败: {str(e)}", "ERROR")
            return []
    
    # =================
    # 辅助方法
    # =================
    
    def get_file_size_str(self, size_bytes: int) -> str:
        """
        将字节大小转换为可读字符串
        
        Args:
            size_bytes (int): 字节大小
            
        Returns:
            str: 可读的大小字符串
        """
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
    
    def is_file_accessible(self, file_path: str) -> bool:
        """
        检查文件是否可访问
        
        Args:
            file_path (str): 文件路径
            
        Returns:
            bool: 文件是否可访问
        """
        try:
            return os.path.exists(file_path) and os.access(file_path, os.R_OK)
        except Exception:
            return False
    
    def get_current_paths(self) -> Dict[str, str]:
        """
        获取当前设置的路径
        
        Returns:
            Dict[str, str]: 包含excel_path和document_path的字典
        """
        return {
            'excel_path': self.excel_file_path,
            'document_path': self.document_folder_path
        }
    
    def set_paths(self, excel_path: str = "", document_path: str = ""):
        """
        设置文件路径
        
        Args:
            excel_path (str): Excel文件路径
            document_path (str): 文档文件夹路径
        """
        if excel_path:
            self.excel_file_path = excel_path
        if document_path:
            self.document_folder_path = document_path
    
    def clear_paths(self):
        """清空所有路径"""
        self.excel_file_path = ""
        self.document_folder_path = ""
        self.log("文件路径已清空")


# 创建全局文件管理器实例的工厂函数
def create_file_manager(log_callback: Optional[Callable[[str, str], None]] = None) -> FileManager:
    """
    创建文件管理器实例
    
    Args:
        log_callback: 日志回调函数
        
    Returns:
        FileManager: 文件管理器实例
    """
    return FileManager(log_callback)


# 便捷函数
def validate_file_paths(excel_path: str, document_path: str, 
                       log_callback: Optional[Callable[[str, str], None]] = None) -> bool:
    """
    快速验证文件路径的便捷函数
    
    Args:
        excel_path (str): Excel文件路径
        document_path (str): 文档文件夹路径
        log_callback: 日志回调函数
        
    Returns:
        bool: 路径是否都有效
    """
    manager = FileManager(log_callback)
    return manager.validate_all_paths(excel_path, document_path)


def quick_read_excel(file_path: str, 
                    log_callback: Optional[Callable[[str, str], None]] = None) -> Optional[List[Dict[str, Any]]]:
    """
    快速读取Excel文件的便捷函数
    
    Args:
        file_path (str): Excel文件路径
        log_callback: 日志回调函数
        
    Returns:
        Optional[List[Dict[str, Any]]]: 读取的数据列表
    """
    manager = FileManager(log_callback)
    return manager.read_excel_data(file_path) 