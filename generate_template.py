import pandas as pd
import os

def create_peda_upload_template():
    """
    生成 PEDA V12 的 Excel 上传模板文件。
    该文件包含一个数据输入表和一个使用说明表。
    """
    template_filename = "PEDA_Upload_Template.xlsx"
    
    # --- 1. 创建数据模板工作表 (Data Sheet) ---
    # 根据 peda_processor.py 中的实际数据期待字段
    data_template = {
        "part_number": ["PN-001-A", "PN-002-B", "PN-003-C"],
        "contact": ["Pipar Pan", "Pipar Pan", "Pipar Pan"],
        "project_type": ["2", "2", "2"],
        "reason": ["250", "250", "250"],
        "sample_quantity": ["10", "20", "15"],
        "decision_region": ["Asia", "Asia", "Europe"],
        "decision_value": ["10", "10", "10"],
        "document_maintenance_path": ["C:/PEDA_Documents/", "C:/PEDA_Documents/", "C:/PEDA_Documents/"]
    }
    df_template = pd.DataFrame(data_template)
    
    # --- 2. 创建使用说明工作表 (Instruction Sheet) ---
    instructions_data = {
        "字段名 (Field Name)": [
            "part_number",
            "contact",
            "project_type",
            "reason",
            "sample_quantity",
            "decision_region",
            "decision_value",
            "document_maintenance_path"
        ],
        "说明 (Description)": [
            "【必填】产品料号，系统会根据此料号搜索产品并创建PEDA。示例：PN-001-A",
            
            "【必填】联系人名称。示例：Pipar Pan",
            
            "【必填】项目类型，通常填写数字代码。示例：2",
            
            "【必填】原因代码，系统预定义的值。示例：250",
            
            "【必填】样品数量，整数值。示例：10",
            
            "【必填】决策区域，产品适用的地区。示例：Asia, Europe",
            
            "【必填】决策值，整数。示例：10",
            
            "【必填】文档维护路径，系统会在此路径下查找 <part_number> 子文件夹中的所有文档类别文件夹进行上传。示例：C:/PEDA_Documents/ 或 D:\\PEDA_Files\\"
        ],
        "示例值 (Example)": [
            "PN-001-A",
            "Pipar Pan",
            "2",
            "250",
            "10",
            "Asia",
            "10",
            "C:/PEDA_Documents/"
        ]
    }
    df_instructions = pd.DataFrame(instructions_data)

    # --- 3. 将两个 DataFrame 写入同一个 Excel 文件 ---
    try:
        with pd.ExcelWriter(template_filename, engine='openpyxl') as writer:
            # 写入数据模板工作表
            df_template.to_excel(writer, sheet_name='PEDA Upload Data', index=False)
            
            # 写入使用说明工作表
            df_instructions.to_excel(writer, sheet_name='Instructions', index=False)
            
            # 获取工作簿对象以便进行格式调整
            workbook = writer.book
            
            # 调整 Instructions 工作表的列宽
            instructions_sheet = workbook['Instructions']
            instructions_sheet.column_dimensions['A'].width = 25
            instructions_sheet.column_dimensions['B'].width = 100
            instructions_sheet.column_dimensions['C'].width = 20
            
            # 调整 PEDA Upload Data 工作表的列宽
            data_sheet = workbook['PEDA Upload Data']
            data_sheet.column_dimensions['A'].width = 15
            data_sheet.column_dimensions['B'].width = 15
            data_sheet.column_dimensions['C'].width = 12
            data_sheet.column_dimensions['D'].width = 12
            data_sheet.column_dimensions['E'].width = 15
            data_sheet.column_dimensions['F'].width = 15
            data_sheet.column_dimensions['G'].width = 12
            data_sheet.column_dimensions['H'].width = 30
        
        print("=" * 60)
        print("✅ 成功！PEDA V12 上传模板文件已创建")
        print("=" * 60)
        print(f"📄 文件名：{template_filename}")
        print(f"📁 完整路径：{os.path.abspath(template_filename)}")
        print("\n📊 文件包含以下工作表：")
        print("  1. PEDA Upload Data - 数据输入工作表（包含3行示例数据）")
        print("  2. Instructions - 使用说明工作表（详细字段说明）")
        print("\n📋 Excel 期待的列（字段）：")
        print("  • part_number - 产品料号（必填）")
        print("  • contact - 联系人（必填）")
        print("  • project_type - 项目类型（必填）")
        print("  • reason - 原因代码（必填）")
        print("  • sample_quantity - 样品数量（必填）")
        print("  • decision_region - 决策区域（必填）")
        print("  • decision_value - 决策值（必填）")
        print("  • document_maintenance_path - 文档路径（必填）")
        print("\n💡 提示：请在 'PEDA Upload Data' 工作表中填写您的数据")
        print("=" * 60)
        
    except Exception as e:
        print("=" * 60)
        print("❌ 创建模板文件失败")
        print("=" * 60)
        print(f"错误信息：{e}")
        print("\n请确保：")
        print("  1. 已安装必要的库：pip install pandas openpyxl")
        print("  2. 当前目录有写入权限")
        print("  3. 文件未被其他程序打开")
        print("  4. PEDA_Upload_Template.xlsx 文件不存在或未被占用")
        print("=" * 60)

if __name__ == "__main__":
    create_peda_upload_template()
