import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog
from config.constants import REQUIRED_COLUMNS

def read_excel_data(file_path):
    """从Excel文件读取数据"""
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            print(f"错误: 文件不存在 - {file_path}")
            return None
        
        # 检查文件权限
        if not os.access(file_path, os.R_OK):
            print(f"错误: 文件无读取权限 - {file_path}")
            return None
        
        print(f"正在读取文件: {os.path.basename(file_path)}")
        
        # 根据文件扩展名选择读取方式
        if file_path.lower().endswith('.csv'):
            df = pd.read_csv(file_path, encoding='utf-8')
            print("文件类型: CSV")
        elif file_path.lower().endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
            print("文件类型: Excel")
        else:
            print(f"警告: 未知文件类型，尝试按Excel格式读取")
            df = pd.read_excel(file_path)
        
        # 显示基本信息
        print(f"数据读取成功: {len(df)} 行, {len(df.columns)} 列")
        
        if len(df) == 0:
            print("警告: 文件中没有数据行")
            return None
        
        return df
        
    except pd.errors.EmptyDataError:
        print(f"错误: 文件为空或没有数据 - {file_path}")
        return None
    except pd.errors.ParserError as e:
        print(f"错误: 文件格式解析失败 - {e}")
        return None
    except PermissionError:
        print(f"错误: 文件被其他程序占用或权限不足 - {file_path}")
        return None
    except FileNotFoundError:
        print(f"错误: 文件未找到 - {file_path}")
        return None
    except Exception as e:
        print(f"错误: 读取Excel文件时发生未知错误 - {e}")
        print(f"文件路径: {file_path}")
        return None

def validate_excel_data(df: pd.DataFrame):
    """
    验证DataFrame是否符合要求。

    1. 检查所有必需的列是否存在。
    2. 检查必填字段（part_number, reason, decision_region, decision_value）是否为空，筛选出"合格"的数据行。
       - "合格"定义：4个必填字段都不能为空。
       - 选填字段（contact, project_type, sample_quantity）可以为空。

    Args:
        df (pd.DataFrame): 从Excel读取的DataFrame。

    Returns:
        dict: 包含验证结果的字典，格式如下：
              {
                  'headers_valid': bool,      # 表头是否有效
                  'missing_columns': list,    # 缺少的必填列名
                  'total_rows': int,          # 总行数
                  'qualified_rows_count': int,# 合格行数（必填字段不为空）
                  'qualified_df': pd.DataFrame # 只包含合格行的DataFrame
              }
    """
    if df is None or df.empty:
        return {
            'headers_valid': False,
            'missing_columns': REQUIRED_COLUMNS,
            'total_rows': 0,
            'qualified_rows_count': 0,
            'qualified_df': pd.DataFrame()
        }

    # 1. 检查表头 - 只检查必填列
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        return {
            'headers_valid': False,
            'missing_columns': missing_columns,
            'total_rows': len(df),
            'qualified_rows_count': 0,
            'qualified_df': pd.DataFrame()
        }

    # 2. 筛选合格行 - 只检查4个必填字段不为空
    # 丢弃必填字段中有任何空值的行
    qualified_df = df.dropna(subset=REQUIRED_COLUMNS)
    
    qualified_rows_count = len(qualified_df)

    return {
        'headers_valid': True,
        'missing_columns': [],
        'total_rows': len(df),
        'qualified_rows_count': qualified_rows_count,
        'qualified_df': qualified_df
    }


def select_excel_file():
    """打开文件选择对话框，让用户选择Excel文件"""
    try:
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        
        file_path = filedialog.askopenfilename(
            title="选择Excel数据文件",
            filetypes=[
                ("Excel文件", "*.xlsx *.xls"),
                ("CSV文件", "*.csv"), 
                ("所有文件", "*.*")
            ],
            initialdir="."  # 从当前目录开始
        )
        
        root.destroy()  # 销毁隐藏的窗口
        return file_path
        
    except Exception as e:
        print(f"打开文件选择对话框时出错: {e}")
        return None 