"""GUI 接口适配层。
注意：为加快GUI冷启动，避免在模块导入阶段加载重量级依赖。
所有重量级依赖（playwright/pandas 等）均在函数体内按需导入。"""


def run_with_gui_params_v2(excel_path: str, document_path: str, username: str, password: str, 
                          system_language: str = 'en', progress_callback=None, log_callback=None, upload_record_callback=None, login_url=None):
    print(f"[DEBUG] run_with_gui_params_v2 called with excel_path={excel_path}, document_path={document_path}, username={username}, password={password}, system_language={system_language}, login_url={login_url}")
    """
    从GUI调用的主要处理函数（浏览器复用版本）
    
    Args:
        excel_path: Excel文件路径
        document_path: 文档根目录路径
        username: 用户名
        password: 密码
        system_language: 系统语言 ('en' 或 'de')
        progress_callback: 进度回调函数
        log_callback: 日志回调函数
        upload_record_callback: 上传记录回调函数
        login_url: 登录页面URL
    """
    try:
        # 延迟导入，避免主GUI启动变慢
        from playwright.sync_api import sync_playwright
        from modules.data_processor import read_excel_data
        from core.workflow_engine import run_batch_with_reuse
        if log_callback:
            log_callback("=== PEDA 自动化处理开始（浏览器复用模式）===")
            log_callback(f"Excel文件: {excel_path}")
            log_callback(f"文档路径: {document_path}")
            log_callback(f"用户: {username}")
            log_callback(f"系统语言: {system_language}")
        
        # 读取Excel数据
        if log_callback:
            log_callback("正在读取Excel数据...")
        
        data = read_excel_data(excel_path)
        print(f"[DEBUG] read_excel_data returned: {type(data)}")
        if data is None:
            print("[DEBUG] Excel数据读取失败，data is None")
            if log_callback:
                log_callback("错误: 无法读取Excel数据", "ERROR")
            return False
            
        if data.empty:
            print("[DEBUG] Excel数据为空，data.empty is True")
            if log_callback:
                log_callback("错误: Excel文件为空，没有数据可处理", "ERROR")
            return False
        
        # 验证必要的列是否存在
        required_columns = ['part_number', 'contact', 'project_type', 'reason', 
                          'sample_quantity', 'decision_region', 'decision_value', 
                          'document_maintenance_path']
        missing_columns = [col for col in required_columns if col not in data.columns]
        
        if missing_columns:
            error_msg = f"Excel文件缺少必要的列: {missing_columns}"
            if log_callback:
                log_callback(f"错误: {error_msg}", "ERROR")
                log_callback(f"必需的列: {required_columns}", "ERROR")
            return False
        
        total_rows = len(data)
        if log_callback:
            log_callback(f"Excel数据验证通过，共 {total_rows} 行数据")
        
        # 转换DataFrame为字典列表
        data_rows = data.to_dict('records')
        
        # 调用批量处理函数（浏览器复用）
        print("[DEBUG] about to call run_batch_with_reuse")
        with sync_playwright() as playwright:
            result = run_batch_with_reuse(
                playwright=playwright,
                data_rows=data_rows,
                username=username,
                password=password,
                system_language=system_language,
                progress_callback=progress_callback,
                log_callback=log_callback,
                upload_record_callback=upload_record_callback,
                login_url=login_url
            )
        print(f"[DEBUG] run_batch_with_reuse returned: {result}")
        
        # 分析处理结果
        success_rate = result['success'] / result['total'] * 100 if result['total'] > 0 else 0
        
        if log_callback:
            log_callback(f"\n=== 最终处理结果 ===")
            log_callback(f"成功率: {success_rate:.1f}% ({result['success']}/{result['total']})")
            
            if result['success'] == result['total']:
                log_callback("🎉 所有件号处理成功！", "SUCCESS")
            elif result['success'] > 0:
                log_callback(f"⚠️ 部分完成，建议检查失败的件号", "WARNING")
            else:
                log_callback("❌ 处理失败，请检查配置和数据", "ERROR")
        
        # 返回完整统计字典，供GUI显示
        return result
    except Exception as e:
        print(f"[DEBUG] Exception in run_with_gui_params_v2: {e}")
        import traceback
        traceback.print_exc()
        if log_callback:
            log_callback(f"❌ 处理过程中发生严重错误: {str(e)}", "ERROR")
        return False


def run_with_gui_params(excel_path: str, document_path: str, username: str, password: str, 
                       system_language: str = 'en', progress_callback=None, log_callback=None):
    """
    从GUI调用的主要处理函数（原版本，保持向后兼容）
    
    Args:
        excel_path: Excel文件路径
        document_path: 文档根目录路径
        username: 用户名
        password: 密码
        system_language: 系统语言 ('en' 或 'de')
        progress_callback: 进度回调函数
        log_callback: 日志回调函数
    """
    try:
        # 延迟导入，避免主GUI启动变慢
        from playwright.sync_api import sync_playwright
        from modules.data_processor import read_excel_data
        from core.workflow_engine import run
        if log_callback:
            log_callback("=== PEDA 自动化处理开始 ===")
            log_callback(f"Excel文件: {excel_path}")
            log_callback(f"文档路径: {document_path}")
            log_callback(f"用户: {username}")
            log_callback(f"系统语言: {system_language}")
        
        # 读取Excel数据
        if log_callback:
            log_callback("正在读取Excel数据...")
        
        data = read_excel_data(excel_path)
        if data is None:
            if log_callback:
                log_callback("错误: 无法读取Excel数据", "ERROR")
            return False
            
        if data.empty:
            if log_callback:
                log_callback("错误: Excel文件为空，没有数据可处理", "ERROR")
            return False
        
        # 验证必要的列是否存在
        required_columns = ['part_number', 'contact', 'project_type', 'reason', 
                          'sample_quantity', 'decision_region', 'decision_value', 
                          'document_maintenance_path']
        missing_columns = [col for col in required_columns if col not in data.columns]
        
        if missing_columns:
            error_msg = f"Excel文件缺少必要的列: {missing_columns}"
            if log_callback:
                log_callback(f"错误: {error_msg}", "ERROR")
                log_callback(f"必需的列: {required_columns}", "ERROR")
            return False
        
        total_rows = len(data)
        if log_callback:
            log_callback(f"Excel数据验证通过，共 {total_rows} 行数据")
        
        success_count = 0
        failed_count = 0
        
        # 遍历每行数据执行操作
        with sync_playwright() as playwright:
            for index, row in data.iterrows():
                current_part = row['part_number']
                
                if log_callback:
                    log_callback(f"\n[{index+1}/{total_rows}] 开始处理件号: {current_part}")
                
                # 更新进度
                if progress_callback:
                    progress = (index / total_rows) * 100
                    progress_callback(progress, f"处理件号: {current_part}")
                
                try:
                    # 调用处理函数，传入GUI参数
                    result = run(playwright, row, username, password, system_language)
                    
                    if result is not False: # 如果没有明确返回False，认为成功
                        success_count += 1
                        if log_callback:
                            log_callback(f"✅ [{index+1}/{total_rows}] 件号 {current_part} 处理完成", "SUCCESS")
                    else:
                        failed_count += 1
                        if log_callback:
                            log_callback(f"❌ [{index+1}/{total_rows}] 件号 {current_part} 处理失败", "ERROR")
                            
                except Exception as e:
                    failed_count += 1
                    if log_callback:
                        log_callback(f"❌ [{index+1}/{total_rows}] 件号 {current_part} 处理异常: {str(e)}", "ERROR")
        
        # 最终进度更新
        if progress_callback:
            progress_callback(100, "处理完成")
        
        # 最终结果
        if log_callback:
            log_callback(f"\n=== 处理完成 ===")
            log_callback(f"总计: {total_rows} 个件号")
            log_callback(f"成功: {success_count} 个")
            log_callback(f"失败: {failed_count} 个")
            
            if failed_count == 0:
                log_callback("🎉 所有件号处理成功！", "SUCCESS")
            else:
                log_callback(f"⚠️ 有 {failed_count} 个件号处理失败，请检查日志", "ERROR")
        
        return failed_count == 0  # 如果没有失败的，返回True
        
    except Exception as e:
        if log_callback:
            log_callback(f"❌ 处理过程中发生严重错误: {str(e)}", "ERROR")
        return False