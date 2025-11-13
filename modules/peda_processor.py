import os
from playwright.sync_api import Page
from typing import Dict, Any, Optional, Callable

# 导入相关处理模块
from .document_manager import DocumentManager, process_document_upload
from .system_handler import enhanced_product_search
from .form_handler import fill_peda_form
from .pdf_processor import print_coversheet_pdf_v12


def process_single_peda(page: Page, data_row: Dict[str, Any], 
                       document_maintenance_path: str,
                       log_callback: Optional[Callable] = None,
                       upload_record_callback: Optional[Callable] = None) -> bool:
    """
    处理单个PEDA（不包含浏览器管理）
    
    Args:
        page: 已登录的页面对象
        data_row: 单行数据
        document_maintenance_path: 文档主目录路径（从GUI传入）
        log_callback: 日志回调函数
        upload_record_callback: 上传记录回调函数
        
    Returns:
        bool: 处理成功返回True
    """
    def log(message: str, level: str = "INFO"):
        """内部日志函数"""
        if log_callback:
            log_callback(message, level)
        else:
            print(f"[{level}] {message}")
    
    try:
        # 从data_row中提取数据（必填字段）
        part_number = data_row.get('part_number', '')
        reason = data_row.get('reason', '')
        decision_region = data_row.get('decision_region', '')
        decision_value = data_row.get('decision_value', '')
        
        # 选填字段（提供默认值）
        contact = data_row.get('contact', 'Pipar Pan')
        project_type = data_row.get('project_type', '2')
        sample_quantity = data_row.get('sample_quantity', '10')
        
        if not part_number:
            log("❌ 件号为空，跳过处理", "ERROR")
            return False
        
        log(f"开始处理件号: {part_number}")
        log(f"文档路径: {document_maintenance_path}")
        
        # 初始化文档管理器
        doc_manager = DocumentManager(document_maintenance_path, part_number)
        
        # 验证文档结构
        if not doc_manager.validate_structure():
            log(f"件号 {part_number} 的文档结构验证失败，跳过处理", "ERROR")
            return False
        
        # 扫描文档并获取摘要
        doc_manager.scan_documents()
        summary = doc_manager.get_upload_summary()
        log(f"文档扫描完成: 共 {summary['total_files']} 个文件在 {summary['categories_with_files']} 个类别中")
        
        # 步骤1: 搜索产品
        log(f"搜索产品: {part_number}")
        if not enhanced_product_search(page, part_number):
            log(f"❌ 产品 {part_number} 搜索失败", "ERROR")
            return False
        
        log("✅ 产品搜索成功")
        
        # 步骤2: 创建PEDA
        log("创建新的PEDA...")
        try:
            # 等待more_horiz按钮出现（确保页面加载完成）
            page.get_by_role("button", name="more_horiz").wait_for(state="visible", timeout=10000)
            
            # 检查THP审批状态
            from .approval_checker import check_thp_approval_status
            if not check_thp_approval_status(page, part_number):
                log(f"⚠️ 件号 {part_number} 的THP未批准，跳过处理", "WARNING")
                return False
            
            log("✅ THP审批状态检查通过")
            
            # 点击创建PEDA
            page.get_by_role("button", name="more_horiz").click()
            page.get_by_role("button", name="Create new PEDA").click()
            
            log("等待PEDA页面加载...")
            page.wait_for_timeout(5000)
            
            # 新增：确保在PEDA Detail页
            try:
                if not page.get_by_text("PEDA Details", exact=True).is_visible(timeout=2000):
                    page.get_by_text("PEDA Details", exact=True).click()
                    page.wait_for_timeout(1000)
            except Exception as e:
                log(f"切换到PEDA Detail页失败: {e}", "WARNING")
        
        except Exception as e:
            log(f"❌ 创建PEDA页面失败: {str(e)}", "ERROR")
            return False
        
        # 步骤3: 填写PEDA表单
        log("填写PEDA表单...")
        if not fill_peda_form(page, data_row):
            log("❌ PEDA表单填写失败", "ERROR")
            return False
        
        log("✅ PEDA表单填写完成")
        
        # 步骤4: 文档上传
        log("开始文档上传流程...")
        upload_results = process_document_upload(page, doc_manager, part_number, data_row, upload_record_callback=upload_record_callback)
        
        # 显示上传结果
        log("\n=== 文档上传完成 ===")
        log(f"成功上传: {upload_results['success_count']} 个文件")
        log(f"上传失败: {upload_results['failed_count']} 个文件")
        
        # 详细显示每个类别的上传结果
        for category, result in upload_results.get('category_results', {}).items():
            if result.get('total_files', 0) > 0:
                success = result.get('uploaded_files', 0)
                failed = result.get('failed_files', 0)
                log(f"  {category}: {success}/{success + failed} 个文件成功")
        
        # 显示保存和验证结果
        if upload_results.get('save_and_validate'):
            log("✅ PEDA保存、验证和Cover Sheet跳转成功", "SUCCESS")
            # === 新增：Cover Sheet PDF 导出 ===
            save_dir = os.path.join(document_maintenance_path, part_number)
            log(f"=== 开始为 {part_number} 导出Cover Sheet PDF ===")
            pdf_success = print_coversheet_pdf_v12(page, part_number, save_dir)
            if pdf_success:
                log(f"✅ {part_number} 的Cover Sheet PDF导出成功", "SUCCESS")
            else:
                log(f"❌ {part_number} 的Cover Sheet PDF导出失败", "ERROR")
        else:
            log("❌ PEDA保存、验证或Cover Sheet跳转失败或被跳过", "ERROR")
            if upload_results['failed_count'] > 0:
                log(f"   可能原因：有 {upload_results['failed_count']} 个文件未成功上传")
        # 判断整体处理结果
        if upload_results['failed_count'] == 0 and upload_results.get('save_and_validate'):
            log(f"✅ 件号 {part_number} PEDA创建完成", "SUCCESS")
            return True
        else:
            log(f"⚠️ 件号 {part_number} PEDA创建部分失败", "ERROR")
            return False
            
    except Exception as e:
        log(f"❌ 处理件号 {part_number} 时发生异常: {str(e)}", "ERROR")
        
        # 截图保存错误状态
        try:
            # 创建错误截图目录
            error_screenshot_dir = os.path.join(os.getcwd(), "error_screenshot")
            os.makedirs(error_screenshot_dir, exist_ok=True)
            
            # 生成带时间戳的截图文件名
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(error_screenshot_dir, f"error_{part_number}_{timestamp}.png")
            
            page.screenshot(path=screenshot_path)
            log(f"错误截图已保存到: {screenshot_path}")
        except Exception as screenshot_error:
            log(f"保存错误截图失败: {str(screenshot_error)}", "WARNING")
        
        return False


def validate_data_row(data_row: Dict[str, Any]) -> bool:
    """
    验证单行数据的完整性（只验证必填字段）
    
    Args:
        data_row: 数据行
        
    Returns:
        bool: 数据有效返回True
    """
    # 只验证4个必填字段
    required_fields = [
        'part_number', 'reason', 'decision_region', 'decision_value'
    ]
    
    for field in required_fields:
        if field not in data_row or not str(data_row[field]).strip():
            return False
    
    return True


def prepare_data_row(data_row: Dict[str, Any]) -> Dict[str, Any]:
    """
    预处理数据行，确保数据格式正确，并为选填字段提供默认值
    
    Args:
        data_row: 原始数据行
        
    Returns:
        Dict: 处理后的数据行
    """
    processed_row = data_row.copy()
    
    # 确保必填字段为字符串格式
    required_fields = ['part_number', 'reason', 'decision_region', 'decision_value']
    for field in required_fields:
        if field in processed_row:
            processed_row[field] = str(processed_row[field]).strip()
    
    # 选填字段，提供默认值
    optional_defaults = {
        'contact': 'Pipar Pan',
        'project_type': '2',
        'sample_quantity': '10'
    }
    
    for field, default_value in optional_defaults.items():
        if field not in processed_row or not str(processed_row[field]).strip():
            processed_row[field] = default_value
        else:
            processed_row[field] = str(processed_row[field]).strip()
    
    return processed_row