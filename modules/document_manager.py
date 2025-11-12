import os
from pathlib import Path
from typing import Dict, List, Optional

# 导入配置常量
from config.constants import DOCUMENT_CATEGORIES, FILE_TYPE_FILTERS

# 导入表单处理模块（用于save_and_validate_peda函数调用）
from modules.form_handler import save_and_validate_peda


class DocumentManager:
    """文档管理类，负责扫描和处理文档文件"""
    
    def __init__(self, base_path: str, part_number: str):
        self.base_path = Path(base_path)
        self.part_number = part_number
        self.part_folder = self.base_path / part_number
        self.scan_results = {}
        
    def validate_structure(self) -> bool:
        """验证件号文件夹结构是否正确"""
        if not self.part_folder.exists():
            print(f"错误: 件号文件夹不存在: {self.part_folder}")
            return False
            
        if not self.part_folder.is_dir():
            print(f"错误: {self.part_folder} 不是一个目录")
            return False
            
        print(f"件号文件夹验证通过: {self.part_folder}")
        return True
    
    def scan_documents(self) -> Dict[str, List[str]]:
        """扫描所有文档类别下的文件"""
        self.scan_results = {}
        
        for category in DOCUMENT_CATEGORIES:
            category_path = self.part_folder / category
            files = self._scan_category_files(category, category_path)
            self.scan_results[category] = files
            
        return self.scan_results
    
    def _scan_category_files(self, category: str, category_path: Path) -> List[str]:
        """扫描指定类别下的所有文件"""
        files = []
        
        if not category_path.exists():
            print(f"信息: 类别目录不存在: {category_path}")
            return files
            
        if not category_path.is_dir():
            print(f"警告: {category_path} 不是一个目录")
            return files
        
        try:
            # 获取所有文件
            all_files = [f for f in category_path.iterdir() if f.is_file()]
            
            for file_path in all_files:
                # 验证文件是否有效（检查权限、大小等）
                if self._validate_file(file_path):
                    files.append(str(file_path))
                else:
                    print(f"警告: 文件验证失败: {file_path}")
            
            # 按文件名排序
            files.sort()
            print(f"{category}: 找到 {len(files)} 个有效文件")
            
        except Exception as e:
            print(f"错误: 扫描类别 {category} 时出错: {e}")
            
        return files
    
    def _validate_file(self, file_path: Path) -> bool:
        """验证单个文件是否有效"""
        try:
            # 检查文件是否可读
            if not os.access(file_path, os.R_OK):
                print(f"警告: 文件无读取权限: {file_path}")
                return False
                
            # 检查文件大小（避免过大文件，这里设置为200MB）
            file_size = file_path.stat().st_size
            max_size = 200 * 1024 * 1024  # 200MB
            if file_size > max_size:
                print(f"警告: 文件过大 ({file_size / 1024 / 1024:.1f}MB): {file_path}")
                print(f"⚠️ 建议将文件压缩或分割后再上传")
                return False
                
            return True
            
        except Exception as e:
            print(f"错误: 验证文件时出错 {file_path}: {e}")
            return False
    
    def get_upload_summary(self) -> Dict:
        """获取上传摘要信息"""
        total_files = sum(len(files) for files in self.scan_results.values())
        categories_with_files = sum(1 for files in self.scan_results.values() if files)
        
        return {
            "part_number": self.part_number,
            "total_files": total_files,
            "categories_with_files": categories_with_files,
            "total_categories": len(DOCUMENT_CATEGORIES),
            "scan_results": self.scan_results
        }


def process_document_upload(page, document_manager: DocumentManager, part_number: str = None, data_row = None, upload_record_callback=None) -> Dict:
    """处理文档上传的主要逻辑，支持上传记录回调"""
    upload_results = {
        "success_count": 0,
        "failed_count": 0,
        "category_results": {},
        "errors": []
    }
    
    scan_results = document_manager.scan_documents()
    
    # 点击Document maintenance标签
    if not click_document_maintenance_tab(page):
        upload_results["errors"].append("无法点击Document maintenance标签")
        return upload_results
    
    # 等待页面加载
    page.wait_for_timeout(2000)
    
    # 遍历所有文档类别
    for category in DOCUMENT_CATEGORIES:
        files = scan_results.get(category, [])
        category_result = {
            "total_files": len(files),
            "uploaded_files": 0,
            "failed_files": 0,
            "errors": []
        }
        
        if not files:
            print(f"跳过类别 {category}: 没有文件")
            category_result["status"] = "skipped_no_files"
        else:
            print(f"开始上传类别 {category}: {len(files)} 个文件")
            category_result = upload_category_files(
                page, category, files, part_number=part_number, upload_record_callback=upload_record_callback
            )
        
        upload_results["category_results"][category] = category_result
        upload_results["success_count"] += category_result.get("uploaded_files", 0)
        upload_results["failed_count"] += category_result.get("failed_files", 0)
    
    # 执行保存和验证
    if upload_results['success_count'] > 0:
        print(f"\n成功上传了 {upload_results['success_count']} 个文件，开始保存、验证和跳转...")
        
        # 如果有上传失败的文件，给出提示但继续尝试保存
        if upload_results['failed_count'] > 0:
            print(f"⚠️ 注意：有 {upload_results['failed_count']} 个文件上传失败")
            print("将尝试保存已上传的文件...")
        
        # 导入表单处理模块（这里使用动态导入避免循环依赖）
        from modules.form_handler import save_and_validate_peda
        save_and_validate_success = save_and_validate_peda(page, part_number, document_manager, data_row)
        upload_results['save_and_validate'] = save_and_validate_success
        upload_results['pdf_saved'] = save_and_validate_success
    else:
        print("⚠️ 没有成功上传的文件，跳过保存和验证")
        upload_results['save_and_validate'] = False
    
    return upload_results


def click_document_maintenance_tab(page) -> bool:
    """点击Document maintenance标签并等待内容加载"""
    try:
        print("尝试点击Document maintenance标签...")
        
        # 先检查当前状态
        try:
            if page.locator("#stibo_tab_Document_maintenance.tabs-panel-tab--selected").is_visible(timeout=1000):
                print("✅ Document maintenance标签已经是选中状态")
                return True
        except:
            print("Document maintenance标签当前未选中，需要点击")
            
        # 使用多种点击方法，优先使用最稳定的方法
        click_methods = [
            # 方法1: 强制点击（最稳定）
            lambda: page.locator("#stibo_tab_Document_maintenance").click(force=True),
            # 方法2: JavaScript强制点击
            lambda: page.evaluate("document.querySelector('#stibo_tab_Document_maintenance').click()"),
            # 方法3: 标准点击
            lambda: page.locator("#stibo_tab_Document_maintenance").click(),
            # 方法4: 使用class和文本组合
            lambda: page.locator("div.tabs-panel-tab:has-text('Document maintenance')").click(),
        ]
        
        clicked = False
        for i, method in enumerate(click_methods, 1):
            try:
                print(f"尝试点击方法 {i}...")
                method()
                
                # 等待标签状态改变
                page.wait_for_timeout(1500)
                
                # 验证是否成功切换 - 恢复原版本的简单有效验证
                if page.locator("#stibo_tab_Document_maintenance.tabs-panel-tab--selected").is_visible(timeout=3000):
                    print(f"✅ Document maintenance标签点击成功 (方法 {i})")
                    print("✅ 已成功切换到Document maintenance标签页")
                    clicked = True
                    break
                else:
                    print(f"⚠️ 方法 {i} 点击后标签页未正确切换")
                    
            except Exception as e:
                print(f"点击方法 {i} 失败: {e}")
        
        if not clicked:
            print("❌ 无法成功切换到Document maintenance标签")
            return False
        
        # 等待页面内容加载
        print("等待Document maintenance页面内容加载...")
        page.wait_for_timeout(3000)
        
        # 等待文档上传按钮出现
        print("等待文档上传按钮出现...")
        try:
            # 等待任意一个上传按钮变为可见
            page.wait_for_selector("i.material-icons:has-text('add_circle')", timeout=10000)
            print("✅ 文档上传按钮已出现")
            return True
        except Exception as e:
            print(f"⚠️ 等待上传按钮超时: {e}")
            # 即使上传按钮检测超时，如果标签切换成功就继续
            print("标签切换成功，继续尝试文档上传...")
            return True
            
    except Exception as e:
        print(f"❌ 点击Document maintenance标签失败: {e}")
        return False


def upload_category_files(page, category: str, files: List[str], part_number=None, upload_record_callback=None) -> Dict:
    """上传指定类别的所有文件，支持上传记录回调"""
    result = {
        "total_files": len(files),
        "uploaded_files": 0,
        "failed_files": 0,
        "errors": [],
        "status": "processing"
    }
    
    for file_path in files:
        file_name = os.path.basename(file_path)
        try:
            if upload_single_file(page, category, file_path):
                result["uploaded_files"] += 1
                print(f"上传成功: {category} - {file_name}")
                if upload_record_callback:
                    upload_record_callback(part_number, file_name, "成功", "")
            else:
                result["failed_files"] += 1
                error_msg = f"上传失败: {category} - {file_name}"
                result["errors"].append(error_msg)
                print(error_msg)
                if upload_record_callback:
                    upload_record_callback(part_number, file_name, "失败", error_msg)
        except Exception as e:
            result["failed_files"] += 1
            error_msg = f"上传异常: {category} - {file_name}: {e}"
            result["errors"].append(error_msg)
            print(error_msg)
            if upload_record_callback:
                upload_record_callback(part_number, file_name, "失败", error_msg)
    
    if result["failed_files"] == 0:
        result["status"] = "success"
    elif result["uploaded_files"] == 0:
        result["status"] = "failed"
    else:
        result["status"] = "partial_success"
    
    return result


def upload_single_file(page, category: str, file_path: str) -> bool:
    """上传单个文件到指定类别"""
    try:
        print(f"准备上传文件: {Path(file_path).name} 到 {category}")
        
        # 转换类别名称为ID格式
        category_id = category.replace(" ", "_")
        
        # 快速滚动到目标区域（增加等待时间）
        try:
            page.locator(f"#{category_id}").scroll_into_view_if_needed()
            page.wait_for_timeout(800)  # 增加到800ms
        except:
            pass
        
        # 优化的上传按钮定位（恢复原来的逻辑，增加等待时间）
        upload_button_selectors = [
            f"#{category_id} i.material-icons:has-text('add_circle')",  # 最常用的
            f"#{category_id} .stb-Button-Add-Small",                   # 备用1
            f"#{category_id} i:has-text('add_circle')",                # 备用2
        ]
        
        button_clicked = False
        for i, selector in enumerate(upload_button_selectors, 1):
            try:
                upload_button = page.locator(selector)
                if upload_button.is_visible(timeout=1000):  # 增加到1秒
                    upload_button.click()
                    button_clicked = True
                    print(f"✅ 上传按钮点击成功 (方法 {i})")
                    break
            except Exception as e:
                print(f"上传按钮选择器 {i} 失败: {e}")
        
        if not button_clicked:
            print(f"❌ 无法点击 {category} 的上传按钮")
            return False
        
        # 增加文件选择等待时间
        page.wait_for_timeout(800)  # 增加到800ms
        
        # 优化的文件上传方法（恢复原来的逻辑，增加等待时间）
        upload_success = False
        
        # 方法1: 直接查找文件输入框（最快）
        try:
            file_input = page.locator("input[type='file']")
            if file_input.is_visible(timeout=2000):  # 增加到2秒
                file_input.set_input_files(file_path)
                upload_success = True
                print(f"✅ 直接文件输入成功: {Path(file_path).name}")
        except Exception as e:
            print(f"直接文件输入失败: {e}")
        
        # 方法2: 尝试file_chooser（增加超时时间）
        if not upload_success:
            try:
                with page.expect_file_chooser(timeout=8000) as fc_info:  # 增加到8秒
                    pass
                file_chooser = fc_info.value
                file_chooser.set_files(file_path)
                upload_success = True
                print(f"✅ file_chooser方法成功: {Path(file_path).name}")
            except Exception as e:
                print(f"file_chooser方法失败: {e}")
        
        # 方法3: Choose File按钮方法
        if not upload_success:
            try:
                choose_file_btn = page.get_by_role("button", name="Choose File")
                if choose_file_btn.is_visible(timeout=2000):  # 增加到2秒
                    choose_file_btn.set_input_files(file_path)
                    upload_success = True
                    print(f"✅ Choose File按钮方法成功: {Path(file_path).name}")
            except Exception as e:
                print(f"Choose File按钮方法失败: {e}")
        
        if not upload_success:
            print(f"❌ 所有文件上传方法都失败")
            return False
        
        # 快速处理Insert按钮
        try:
            insert_button = page.get_by_role("button", name="Insert")
            if insert_button.is_visible(timeout=2000):  # 增加到2秒
                insert_button.click()
                print("✅ 已点击Insert按钮")
        except:
            pass  # Insert按钮可能不存在，继续
        
        # 增加上传完成等待时间（特别是大文件）
        page.wait_for_timeout(1500)  # 增加到1.5秒
        return True
            
    except Exception as e:
        print(f"❌ 上传文件 {Path(file_path).name} 到 {category} 失败: {e}")
        return False