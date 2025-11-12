# 文档类别映射
DOCUMENT_CATEGORIES = [
    "Image Documentation",
    "Other", 
    "Technical Datasheet",
    "Confidential",
    "Measurement Report",
    "Technical Drawing"
]

# 文件类型过滤配置
FILE_TYPE_FILTERS = {
    "Image Documentation": ['.jpg', '.png', '.bmp', '.gif', '.tiff', '.jpeg'],
    "Technical Datasheet": ['.pdf', '.doc', '.docx', '.xlsx', '.xls'],
    "Technical Drawing": ['.dwg', '.dxf', '.pdf'],
    "Measurement Report": ['.xlsx', '.pdf', '.csv', '.xls'],
    "Other": [],  # 允许所有类型
    "Confidential": ['.pdf', '.doc', '.docx']
} 