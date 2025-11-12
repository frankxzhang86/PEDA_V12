import os
from playwright.sync_api import Playwright
from typing import List, Dict, Any, Optional, Callable

# 导入各模块的功能
from modules.document_manager import DocumentManager, process_document_upload
from modules.system_handler import handle_login_popup, set_language_after_login, enhanced_product_search
from modules.form_handler import fill_peda_form
from modules.browser_manager import BrowserManager
from modules.peda_processor import process_single_peda, validate_data_row, prepare_data_row


def run_batch_with_reuse(playwright: Playwright, data_rows: List[Dict[str, Any]], 
                        document_path: str,
                        username: str, password: str, system_language: str = 'en',
                        progress_callback: Optional[Callable] = None, 
                        log_callback: Optional[Callable] = None,
                        upload_record_callback: Optional[Callable] = None,
                        login_url: Optional[str] = None,
                        browser_path: Optional[str] = None,
                        preferred_browser: str = "auto",
                        browser_finder = None,
                        headless: bool = False) -> Dict[str, int]:
    """
    批量处理多行数据（浏览器复用版本）
    
    Args:
        playwright: Playwright实例
        data_rows: 数据行列表
        document_path: 文档主目录路径（从GUI传入）
        username: 用户名
        password: 密码
        system_language: 系统语言
        progress_callback: 进度回调函数
        log_callback: 日志回调函数
        upload_record_callback: 上传记录回调函数
        login_url: 登录网址
        browser_path: 自定义浏览器路径（可选）
        preferred_browser: 首选浏览器类型 ("chrome", "msedge", "auto")
        browser_finder: 预热的浏览器查找器实例（可选，用于加速启动）
        headless: 是否以Headless模式运行浏览器
        
    Returns:
        Dict[str, int]: 处理结果统计
    """
    def log(message: str, level: str = "INFO"):
        """内部日志函数"""
        if log_callback:
            log_callback(message, level)
        else:
            print(f"[{level}] {message}")
    
    # 初始化统计
    total_count = len(data_rows)
    success_count = 0
    failed_count = 0
    skipped_count = 0
    
    log("=== 开始批量处理PEDA（浏览器复用模式）===")
    log(f"总计: {total_count} 个件号")
    
    # 创建浏览器管理器
    browser_manager = BrowserManager()
    browser_manager.set_log_callback(log_callback)
    
    try:
        # 初始化浏览器并登录
        log("🚀 初始化浏览器管理器...")
        if not browser_manager.initialize(playwright, username, password, system_language, 
                                         login_url=login_url, browser_path=browser_path, 
                                         preferred_browser=preferred_browser,
                                         browser_finder=browser_finder,
                                         headless=headless):
            log("❌ 浏览器初始化失败，终止处理", "ERROR")
            return {
                'total': total_count,
                'success': 0,
                'failed': total_count,
                'skipped': 0
            }
        
        log("✅ 浏览器初始化成功，开始处理数据")
        
        # 遍历处理每行数据
        for index, row in enumerate(data_rows):
            current_part = row.get('part_number', f'未知件号_{index}')
            
            try:
                log(f"\n[{index+1}/{total_count}] 开始处理件号: {current_part}")
                
                # 更新进度
                if progress_callback:
                    progress = (index / total_count) * 100
                    progress_callback(progress, f"处理件号: {current_part} ({index+1}/{total_count})")
                
                # 验证数据行
                if not validate_data_row(row):
                    log(f"❌ 件号 {current_part} 数据不完整，跳过处理", "ERROR")
                    skipped_count += 1
                    continue
                
                # 预处理数据
                processed_row = prepare_data_row(row)
                
                # 重置页面状态（除了第一个件号）
                if index > 0:
                    if not browser_manager.reset_for_next_part():
                        log(f"❌ 页面状态重置失败，跳过件号 {current_part}", "ERROR")
                        failed_count += 1
                        continue
                
                # 获取页面对象
                page = browser_manager.get_page()
                if not page:
                    log(f"❌ 无法获取页面对象，跳过件号 {current_part}", "ERROR")
                    failed_count += 1
                    continue
                
                # 处理单个PEDA（传递document_path）
                if process_single_peda(page, processed_row, document_path, log_callback, upload_record_callback):
                    success_count += 1
                    log(f"✅ [{index+1}/{total_count}] 件号 {current_part} 处理完成", "SUCCESS")
                else:
                    failed_count += 1
                    log(f"❌ [{index+1}/{total_count}] 件号 {current_part} 处理失败", "ERROR")
                
            except Exception as e:
                failed_count += 1
                log(f"❌ [{index+1}/{total_count}] 件号 {current_part} 处理异常: {str(e)}", "ERROR")
                
                # 尝试截图
                try:
                    screenshot_path = os.path.join(os.getcwd(), f"error_batch_{current_part}_{index}.png")
                    browser_manager.take_screenshot(screenshot_path)
                    log(f"错误截图已保存: {screenshot_path}")
                except Exception:
                    pass
        
        # 最终进度更新
        if progress_callback:
            progress_callback(100, "批量处理完成")
        
        # 处理结果统计
        result = {
            'total': total_count,
            'success': success_count,
            'failed': failed_count,
            'skipped': skipped_count
        }
        
        log(f"\n=== 批量处理完成 ===")
        log(f"总计: {total_count} 个件号")
        log(f"成功: {success_count} 个")
        log(f"失败: {failed_count} 个")
        log(f"跳过: {skipped_count} 个")
        
        if failed_count == 0 and skipped_count == 0:
            log("🎉 所有件号处理成功！", "SUCCESS")
        elif success_count > 0:
            log(f"⚠️ 部分完成：{success_count}/{total_count} 个件号处理成功", "WARNING")
        else:
            log("❌ 批量处理失败，没有件号成功处理", "ERROR")
        
        return result
        
    except Exception as e:
        log(f"❌ 批量处理过程中发生严重错误: {str(e)}", "ERROR")
        return {
            'total': total_count,
            'success': success_count,
            'failed': total_count - success_count - skipped_count,
            'skipped': skipped_count
        }
        
    finally:
        # 清理浏览器资源
        log("🧹 正在清理浏览器资源...")
        browser_manager.cleanup()


def run(playwright: Playwright, data_row=None, username=None, password=None, system_language='en', login_url=None, headless: bool = False) -> None:
    """
    原有的单次处理函数（保持向后兼容）
    
    Args:
        playwright: Playwright实例
        data_row: 单行数据
        username: 用户名
        password: 密码
        system_language: 系统语言
        login_url: 登录网址
        headless: 是否以Headless模式运行浏览器
    """
    # 检查是否提供了数据行
    if data_row is None:
        print("错误: 没有提供数据行，无法执行操作")
        print("请确保Excel文件存在并包含必要的数据列：")
        print("- part_number: 产品编号")
        print("- contact: 联系人名称")
        print("- project_type: 项目类型")
        print("- reason: 原因代码")
        print("- sample_quantity: 样品数量")
        print("- decision_region: 决策区域")
        print("- decision_value: 决策值")
        print("- document_maintenance_path: 文档维护路径")
        return
    
    # 检查是否提供了登录凭据
    if not username or not password:
        print("错误: 没有提供用户名或密码")
        print("请在GUI界面中输入用户名和密码")
        return
    
    # 从data_row中提取数据
    part_number = data_row.get('part_number', '34359074D')
    contact = data_row.get('contact', 'Pipar Pan')
    project_type = data_row.get('project_type', '2')
    reason = data_row.get('reason', '250')
    sample_quantity = data_row.get('sample_quantity', '10')
    decision_region = data_row.get('decision_region', 'Asia')
    decision_value = data_row.get('decision_value', '10')
    document_maintenance_path = data_row.get('document_maintenance_path', 'C:/PEDA_Documents/')
    
    print(f"开始处理件号: {part_number}")
    print(f"文档路径: {document_maintenance_path}")
    
    # 初始化文档管理器
    doc_manager = DocumentManager(document_maintenance_path, part_number)
    
    # 验证文档结构
    if not doc_manager.validate_structure():
        print(f"件号 {part_number} 的文档结构验证失败，跳过处理")
        return
    
    # 扫描文档并获取摘要
    doc_manager.scan_documents()  # 先扫描文档
    summary = doc_manager.get_upload_summary()
    print(f"文档扫描完成: 共 {summary['total_files']} 个文件在 {summary['categories_with_files']} 个类别中")
    
    browser = playwright.chromium.launch(headless=headless)
    context = browser.new_context()
    page = context.new_page()
    
    try:
        # 登录系统
        print(f"正在使用用户 '{username}' 登录到PEDA系统...")
        # 使用提供的登录URL，如果没有则使用默认值
        if not login_url:
            login_url = "https://frd-pim-app.emea.zf-world.com/webui/WebUI_2#deepLink=1&contextID=GL&workspaceID=Main&screen=homepage"
            print("⚠️ 未提供登录URL，使用默认URL")
        
        page.goto(login_url)
        page.get_by_role("textbox", name="Username").click()
        page.get_by_role("textbox", name="Username").fill(username)
        page.get_by_role("textbox", name="Password").click()
        page.get_by_role("textbox", name="Password").fill(password)
        page.get_by_role("button", name="Login").click()
        
        # 等待登录完成
        print("等待登录完成...")
        print("正在等待页面加载，这可能需要较长时间...")
        
        # 等待登录成功的标志 - 等待主页面元素出现
        try:
            # 等待主页面的标志性元素出现，表示登录成功
            page.wait_for_selector(".stibo-HomePage, .mainArea, .primary-navigation-panel", timeout=60000)  # 60秒超时
            print("✅ 登录成功，主页面已加载")
        except Exception as e:
            print(f"⚠️ 等待主页面超时，但继续执行: {e}")
        
        # 额外等待，确保页面完全稳定
        print("等待页面完全稳定...")
        page.wait_for_timeout(5000)  # 5秒额外等待
        
        # 现在检测和处理系统通知弹窗
        print("开始检测系统通知弹窗...")
        if not handle_login_popup(page):
            print("继续执行，但可能存在未关闭的弹窗")
        
        # 等待弹窗处理完成
        print("等待弹窗处理完成...")
        page.wait_for_timeout(3000)
        
        # 登录后立即设置语言
        if not set_language_after_login(page):
            print("⚠️ 语言设置失败，但继续执行（可能已经是英语界面）")
            # 不抛出异常，继续执行
            
        # 搜索产品
        if not enhanced_product_search(page, part_number):
            raise Exception(f"产品 {part_number} 搜索失败")
        
        # 创建PEDA
        try:
            page.get_by_role("button", name="more_horiz").click()
            page.get_by_role("button", name="Create new PEDA").click()
            
            print("等待PEDA页面加载...")
            page.wait_for_timeout(5000)
            
            if not fill_peda_form(page, data_row):
                raise Exception("PEDA表单填写失败")

            print("开始文档上传流程...")
            upload_results = process_document_upload(page, doc_manager, part_number, data_row)
            
            print("\n=== 文档上传完成 ===")
            print(f"成功上传: {upload_results['success_count']} 个文件")
            print(f"上传失败: {upload_results['failed_count']} 个文件")
            
            # 详细显示每个类别的上传结果
            for category, result in upload_results.get('category_results', {}).items():
                if result.get('total_files', 0) > 0:
                    success = result.get('uploaded_files', 0)
                    failed = result.get('failed_files', 0)
                    print(f"  {category}: {success}/{success + failed} 个文件成功")
            
            # 显示保存和验证结果
            if upload_results.get('save_and_validate'):
                print("✅ PEDA保存、验证和Cover Sheet跳转成功")
                # PDF功能由独立模块处理，这里不再显示PDF状态
            else:
                print("❌ PEDA保存、验证或Cover Sheet跳转失败或被跳过")
                if upload_results['failed_count'] > 0:
                    print(f"   可能原因：有 {upload_results['failed_count']} 个文件未成功上传")
            
            print(f"✅ 件号 {part_number} PEDA创建完成")
            
        except Exception as e:
            print(f"❌ 创建或处理PEDA时失败: {e}")
            screenshot_path = os.path.join(os.getcwd(), f"error_screenshot_{part_number}.png")
            page.screenshot(path=screenshot_path)
            print(f"截图已保存到: {screenshot_path}")
            
            # 发生错误时，保持浏览器打开以便用户观察
            print("⚠️ 发生错误，浏览器将保持打开状态以便观察问题")
            print("请手动检查问题后关闭浏览器，或按 Ctrl+C 结束程序")
            
            # 等待用户操作，不自动关闭浏览器
            try:
                input("按 Enter 键继续（这将关闭浏览器）...")
            except KeyboardInterrupt:
                print("\n用户中断，保持浏览器打开")
                return
        
        # 不自动关闭浏览器，让用户手动检查结果
        print(f"\n🎉 件号 {part_number} PEDA处理流程完成！")
        print("浏览器将保持打开状态，您可以:")
        print("1. 检查PEDA是否创建成功")
        print("2. 手动点击Cover Sheet标签（如果需要）")
        print("3. 检查所有文档是否正确上传")
        print("4. 完成后手动关闭浏览器")
        
        try:
            input("\n按 Enter 键关闭浏览器并继续...")
        except KeyboardInterrupt:
            print("\n用户中断，浏览器将保持打开")
            return
        
        print(f"正在关闭浏览器...")
        if context:
            context.close()
        if browser:
            browser.close()
        print(f"件号 {part_number} 处理流程结束\n")

    except Exception as final_e:
        print(f"❌ 程序执行时发生未预期错误: {final_e}")
        try:
            if context:
                context.close()
            if browser:
                browser.close()
        except:
            pass
