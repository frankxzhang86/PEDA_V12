# PEDA自动化处理工具 - 工作流程说明

## 🚀 新版本：浏览器复用模式（V2推荐）

1. 用户点击 start.py
   ↓
2. start.py 调用 gui.peda_gui_complete.main()
   ↓
3. 启动GUI界面，等待用户输入
   ↓
4. 用户在GUI中设置：
   - 用户名/密码
   - Excel文件路径
   - 文档存储路径
   - 语言选择
   ↓
5. 用户点击"开始处理"按钮
   ↓
6. function_controller 检测到 use_browser_reuse = True
   ↓
7. 调用 interfaces.gui_interface.run_with_gui_params_v2()（浏览器复用版本）
   ↓
8. 读取Excel文件 (modules.data_processor.read_excel_data())
   ↓
9. 验证Excel数据格式和必要列
   ↓
10. 转换DataFrame为字典列表
    ↓
11. 调用 core.workflow_engine.run_batch_with_reuse() 批量处理
    ↓
12. **【一次性浏览器初始化】**
    - 创建 BrowserManager 实例
    - 启动浏览器（browser = playwright.chromium.launch()）
    - 创建上下文和页面
    - **执行一次登录PEDA系统**
    - 处理系统弹窗
    - 设置语言
    ↓
13. **【循环处理每行数据】**
    for index, row in enumerate(data_rows):
        ↓
14. 验证和预处理数据行
        ↓
15. **【页面状态重置】**（除第一行外）
    - browser_manager.reset_for_next_part()
    - 导航回主页面
    - 检查登录状态
    - 如需要则重新登录
        ↓
16. 调用 modules.peda_processor.process_single_peda() 处理当前行
    - 搜索产品
    - 创建PEDA
    - 填写表单
    - 上传文档
    - 保存验证
    - 导出PDF
        ↓
17. 记录处理结果，更新进度
        ↓
18. 继续下一行（回到步骤14）
    ↓
19. **【统一资源清理】**
    - 所有行处理完成后
    - browser_manager.cleanup()
    - 关闭浏览器
    - 显示最终统计结果

### PDF处理链（与原版相同）：
```
form_handler.save_and_validate_peda()
    ↓
调用 pdf_processor.print_coversheet_pdf_v12()
    ↓
查找PDF iframe并导航
    ↓
调用 pdf_downloader.handle_pdf_final()
    ↓
下载PDF文件到指定目录
```

---

## 🔄 原版本：兼容模式（每行重启浏览器）

1. 用户点击 start.py
   ↓
2. start.py 调用 gui.peda_gui_complete.main()
   ↓
3. 启动GUI界面，等待用户输入
   ↓
4. 用户在GUI中设置：
   - 用户名/密码
   - Excel文件路径
   - 文档存储路径
   - 语言选择
   ↓
5. 用户点击"开始处理"按钮
   ↓
6. function_controller 检测到 use_browser_reuse = False
   ↓
7. 调用 interfaces.gui_interface.run_with_gui_params()（原版本）
   ↓
8. 读取Excel文件 (modules.data_processor.read_excel_data())
   ↓
9. 验证Excel数据格式和必要列
   ↓
10. 计算总行数，初始化计数器
    ↓
11. **【每行数据独立处理】**
    for index, row in data.iterrows():
        ↓
12. 调用 core.workflow_engine.run() 处理当前行
        ↓
13. **【每行都重新启动浏览器】**
    - browser = playwright.chromium.launch()
    - context = browser.new_context()
    - page = context.new_page()
    - **每次都重新登录PEDA系统**
    - 处理系统弹窗
    - 设置语言
    - 搜索产品
    - 创建PEDA
    - 填写表单
    - 上传文档
    - 保存验证
    - 导出PDF
        ↓
14. **【每行都关闭浏览器】**
    - context.close()
    - browser.close()
    - 记录处理结果
        ↓
15. 继续下一行（回到步骤11）

---

## 📊 两种模式对比

| 特性 | 浏览器复用模式 | 兼容模式 |
|------|----------------|----------|
| **浏览器启动次数** | 1次 | N次（N=行数） |
| **登录次数** | 1次 | N次（N=行数） |
| **处理效率** | 高 | 低 |
| **内存使用** | 中等（持续） | 低（峰值） |
| **稳定性** | 高（有重试机制） | 高（每行独立） |
| **适用场景** | 批量处理（推荐） | 网络不稳定环境 |
| **时间节省** | 60-80% | 基准 |

## ⚙️ 模式切换

在 `gui/function_controller.py` 中：

```python
def __init__(self, parent_app):
    self.app = parent_app
    # True = 浏览器复用模式（推荐）
    # False = 兼容模式（每行重启）
    self.use_browser_reuse = True
```

## 🎯 推荐使用场景

### 浏览器复用模式（默认）
- ✅ 正常网络环境
- ✅ 批量处理多行数据
- ✅ 追求高效率
- ✅ 内存充足的系统

### 兼容模式
- ✅ 网络不稳定环境
- ✅ 单行或少量数据处理
- ✅ 调试和故障排除
- ✅ 内存受限的系统

---

*更新时间: 2024年*  
*版本: V12 浏览器复用版*
