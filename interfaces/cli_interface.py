import os
from playwright.sync_api import sync_playwright

# 导入所需模块
from modules.data_processor import read_excel_data, select_excel_file
from core.workflow_engine import run


def main():
    """主函数，读取Excel数据并处理每一行"""
    print("=== PEDA 自动化处理工具 ===")
    print("请选择包含PEDA数据的Excel文件...")
    
    # 使用文件选择对话框
    excel_path = select_excel_file()
    
    if not excel_path:
        print("未选择文件，程序退出")
        return
    
    print(f"选择的文件: {excel_path}")
    
    # 验证文件是否存在（双重检查）
    if not os.path.exists(excel_path):
        print(f"错误: 文件不存在 - {excel_path}")
        return
    
    try:
        print("正在读取Excel数据...")
        data = read_excel_data(excel_path)
        if data is None:
            print("错误: 无法读取Excel数据")
            return
            
        if data.empty:
            print("错误: Excel文件为空，没有数据可处理")
            return
            
        # 验证必要的列是否存在
        required_columns = ['part_number', 'contact', 'project_type', 'reason', 
                          'sample_quantity', 'decision_region', 'decision_value', 
                          'document_maintenance_path']
        missing_columns = [col for col in required_columns if col not in data.columns]
        
        if missing_columns:
            print(f"错误: Excel文件缺少必要的列: {missing_columns}")
            print(f"必需的列: {required_columns}")
            print("请检查Excel文件的列名是否正确")
            return
        
        print(f"Excel数据验证通过，共 {len(data)} 行数据")
        print("开始处理PEDA数据...")
        print("-" * 50)
        
        # 遍历每行数据执行操作
        with sync_playwright() as playwright:
            for index, row in data.iterrows():
                print(f"\n[{index+1}/{len(data)}] 开始处理件号: {row['part_number']}")
                # 使用默认的硬编码凭据（旧版本兼容）
                run(playwright, row, "lulm", "=LML1234567890lml", "en")
                print(f"[{index+1}/{len(data)}] 件号 {row['part_number']} 处理完成")
                
        print("-" * 50)
        print("所有PEDA数据处理完成！")
                
    except Exception as e:
        print(f"执行过程中发生错误: {e}")
        print("请检查Excel文件格式和数据完整性")


if __name__ == "__main__":
    main()