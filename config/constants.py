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
    "Image Documentation": [],
    "Technical Datasheet": [],
    "Technical Drawing": [],
    "Measurement Report": [],
    "Other": [],
    "Confidential": []
} 

# Excel模板中必需的列名（必填字段）
REQUIRED_COLUMNS = [
    'part_number',
    'reason',
    'decision_region',
    'decision_value'
]

# Excel模板中需要保持唯一性的列
PART_NUMBER_COLUMN = 'part_number'

# Excel模板中所有可选的列名（包含必填和选填）
ALL_COLUMNS = [
    'part_number',      # 必填
    'reason',           # 必填
    'decision_region',  # 必填
    'decision_value',   # 必填
    'contact',          # 选填
    'project_type',     # 选填
    'sample_quantity'   # 选填
]
