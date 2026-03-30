import os
# PDF打印功能导入
from .pdf_processor import print_coversheet_pdf_v12

def fill_peda_form(page, data_row):
    """填写PEDA表单 (假设已为英语界面)"""
    try:
        # 新增：确保在PEDA Detail页
        try:
            if not page.locator("#stibo_tab_PEDA_Details.tabs-panel-tab--selected").is_visible(timeout=2000):
                print("当前不在PEDA Detail页，尝试切换...")
                page.locator("#stibo_tab_PEDA_Details").click(force=True)
                page.wait_for_timeout(1000)
                if not page.locator("#stibo_tab_PEDA_Details.tabs-panel-tab--selected").is_visible(timeout=3000):
                    print("⚠️ 切换到PEDA Detail页失败，后续表单填写可能异常")
                else:
                    print("✅ 已成功切换到PEDA Detail页")
            else:
                print("已在PEDA Detail页")
        except Exception as e:
            print(f"切换到PEDA Detail页异常: {e}")
        
        # 提取数据并确保所有值都是字符串类型
        contact = data_row.get('contact', '')
        project_type = str(data_row.get('project_type', '2'))  # 确保是字符串
        reason = str(data_row.get('reason', '250'))  # 确保是字符串
        sample_quantity = data_row.get('sample_quantity', '')
        decision_region = data_row.get('decision_region', 'Asia')
        decision_value = str(data_row.get('decision_value', '10'))  # 确保是字符串

        import pandas as pd
        # 清理 NaN 值
        external_info = data_row.get('external_info', '')
        if pd.isna(external_info):
            external_info = ''
        else:
            external_info = str(external_info).strip()

        internal_comment = data_row.get('internal_comment', '')
        if pd.isna(internal_comment):
            internal_comment = ''
        else:
            internal_comment = str(internal_comment).strip()
            
        # 清理 contact 和 sample_quantity 的 NaN
        if pd.isna(contact):
            contact = ''
        else:
            contact = str(contact).strip()
            
        if pd.isna(sample_quantity):
            sample_quantity = ''
        else:
            sample_quantity = str(sample_quantity).strip()
        # print("[调试] data_row keys:", list(data_row.keys()))
        # print(f"[调试] external_info: '{external_info}' | internal_comment: '{internal_comment}'")
        # print("开始填写PEDA表单 (英语界面)...")
        # print(f"表单数据: contact={contact}, project_type={project_type}, reason={reason}")
        # print(f"样品数量: {sample_quantity}, 决策区域: {decision_region}, 决策值: {decision_value}")
        
        # 填写联系人（选填，有值才填）
        try:
            if contact:  # 只在有值时填写
                contact_field = page.locator("#Contact").get_by_role("combobox")
                contact_field.select_option(contact)
                # 触发change事件确保表单检测到变更
                contact_field.dispatch_event("change")
                page.wait_for_timeout(500)
                print(f"✅ 联系人填写成功: {contact}")
            else:
                print("⏭️ 联系人为空，跳过填写")
        except Exception as e:
            print(f"⚠️ 联系人填写失败（选填项，继续执行）: {e}")

        # 填写 External Info（选填，有值才填）
        try:
            if external_info:  # 只在有值时填写
                external_info_field = page.locator("#External_Info textarea")
                external_info_field.wait_for(state="visible", timeout=3000)
                external_info_field.fill(external_info)
                external_info_field.dispatch_event("input")
                external_info_field.dispatch_event("change")
                page.wait_for_timeout(500)
                print(f"✅ External Info 填写成功: {external_info}")
            else:
                print("⏭️ External Info 为空，跳过填写")
        except Exception as e:
            print(f"⚠️ External Info 填写失败（选填项，继续执行）: {e}")

        # 填写 Internal Comment（选填，有值才填）
        try:
            if internal_comment:  # 只在有值时填写
                internal_comment_field = page.locator("#Internal_Comment textarea")
                internal_comment_field.wait_for(state="visible", timeout=3000)
                internal_comment_field.fill(internal_comment)
                internal_comment_field.dispatch_event("input")
                internal_comment_field.dispatch_event("change")
                page.wait_for_timeout(500)
                print(f"✅ Internal Comment 填写成功: {internal_comment}")
            else:
                print("⏭️ Internal Comment 为空，跳过填写")
        except Exception as e:
            print(f"⚠️ Internal Comment 填写失败（选填项，继续执行）: {e}")
        
        # 填写项目类型
        try:
            project_type_field = page.locator("#Project_Type").get_by_role("combobox")
            project_type_field.select_option(project_type)
            # 触发change事件
            project_type_field.dispatch_event("change")
            page.wait_for_timeout(500)
            print(f"✅ 项目类型填写成功: {project_type}")
        except Exception as e:
            print(f"❌ 项目类型填写失败: {e}")
            raise
        
        # 填写原因
        try:
            reason_field = page.locator("#Reason").get_by_role("combobox")
            reason_field.select_option(reason)
            # 触发change事件
            reason_field.dispatch_event("change")
            page.wait_for_timeout(500)
            print(f"✅ 原因填写成功: {reason}")
        except Exception as e:
            print(f"❌ 原因填写失败: {e}")
            raise
        
        # 填写样品数量（选填，有值才填）
        try:
            if sample_quantity:  # 只在有值时填写
                quantity_field = page.locator(".gwt-TextBox.validator-number")
                quantity_field.fill(sample_quantity)
                # 触发input和change事件
                quantity_field.dispatch_event("input")
                quantity_field.dispatch_event("change")
                page.wait_for_timeout(500)
                print(f"✅ 样品数量填写成功: {sample_quantity}")
            else:
                print("⏭️ 样品数量为空，跳过填写")
        except Exception as e:
            print(f"⚠️ 样品数量填写失败（选填项，继续执行）: {e}")
        
        # 填写决策值
        try:
            decision_field = page.locator(f"#Decision_{decision_region}").get_by_role("combobox")
            decision_field.select_option(decision_value)
            # 触发change事件
            decision_field.dispatch_event("change")
            page.wait_for_timeout(500)
            print(f"✅ {decision_region} 决策值填写成功: {decision_value}")
        except Exception as e:
            print(f"❌ {decision_region} 决策值填写失败: {e}")
            raise
        
        # 等待表单状态更新
        print("等待表单状态更新...")
        page.wait_for_timeout(2000)
        
        # 保存表单
        try:
            print("等待保存按钮变为可用状态...")
            
            # 直接选择第一个可用的保存按钮（从调试信息可知第1个按钮是可用的）
            save_buttons = page.locator("button:has-text('Save')")
            
            # 检查第一个按钮是否可用
            first_button = save_buttons.first
            if first_button.is_enabled():
                print("找到可用的保存按钮，准备点击...")
                first_button.click()
                page.wait_for_load_state("networkidle", timeout=10000)
                print("✅ 表单保存成功")
                return True
            else:
                # 如果第一个不可用，尝试找到可用的按钮
                count = save_buttons.count()
                for i in range(count):
                    button = save_buttons.nth(i)
                    if button.is_enabled():
                        print(f"使用第 {i+1} 个可用的保存按钮...")
                        button.click()
                        page.wait_for_load_state("networkidle", timeout=10000)
                        print("✅ 表单保存成功")
                        return True
                
                print("❌ 没有找到可用的保存按钮")
                return False
                    
        except Exception as e:
            print(f"❌ 表单保存失败: {e}")
            # 显示所有保存按钮的状态以便调试
            try:
                save_buttons = page.locator("button:has-text('Save')")
                count = save_buttons.count()
                print(f"找到 {count} 个保存按钮:")
                for i in range(count):
                    button = save_buttons.nth(i)
                    is_enabled = button.is_enabled()
                    title = button.get_attribute("title") or "无title"
                    class_attr = button.get_attribute("class") or "无class"
                    print(f"  按钮 {i+1}: 可用={is_enabled}, title='{title}', class='{class_attr}'")
            except Exception as debug_e:
                print(f"调试信息获取失败: {debug_e}")
            return False
        
    except Exception as e:
        print(f"❌ 填写PEDA表单时发生错误: {e}")
        import traceback
        print(f"详细错误信息: {traceback.format_exc()}")
        return False

from typing import Optional, Callable

def save_and_validate_peda(page, part_number: str = None, document_manager = None, data_row = None, log_callback: Optional[Callable] = None) -> bool:
    """保存PEDA、验证并跳转到Cover Sheet"""
    try:
        print("\n=== 开始保存、验证和跳转到Cover Sheet ===")
        # ====== 新增调试日志，检查data_row字段读取情况 ======
        if data_row is not None:
            print(f"[调试] data_row.keys(): {list(data_row.keys())}")
            print(f"[调试] external_info: {data_row.get('external_info', None)}")
            print(f"[调试] internal_comment: {data_row.get('internal_comment', None)}")
        else:
            print("[调试] data_row is None!")
        
        # 第一步：点击Save按钮
        print("1. 查找并点击Save按钮...")
        
        # 首先等待页面处理完成（等待遮罩层消失）
        print("等待页面处理完成...")
        try:
            page.wait_for_function(
                """() => {
                    const overlay = document.querySelector('#waitScreenOverlayGlass, .waitscreenoverlayglass');
                    return !overlay || overlay.style.display === 'none' || !overlay.offsetParent;
                }""",
                timeout=20000
            )
            print("✅ 页面处理完成")
        except Exception as e:
            print(f"⚠️ 等待页面处理超时: {e}")
            # 强制清除遮罩层
            page.evaluate("""
                const overlays = document.querySelectorAll('#waitScreenOverlayGlass, .waitscreenoverlayglass, #waitScreenOverlay');
                overlays.forEach(overlay => {
                    if (overlay) {
                        overlay.style.display = 'none';
                        overlay.style.visibility = 'hidden';
                        overlay.remove();
                    }
                });
            """)
        
        # 等待Save按钮变为可用状态（这需要所有文件都上传完成）
        print("等待所有文件上传完成，Save按钮变为可用状态...")
        print("⚠️ 注意：只有当所有文件都成功上传后，Save按钮才会变为可用")
        
        save_button_available = False
        max_wait_time = 60  # 最多等待60秒
        wait_interval = 3   # 每3秒检查一次
        
        for attempt in range(max_wait_time // wait_interval):
            try:
                # 检查是否有可用的Save按钮
                result = page.evaluate("""
                    () => {
                        const saveButtons = document.querySelectorAll('button[class*="SaveButton"]');
                        let availableButton = null;
                        let totalButtons = saveButtons.length;
                        let enabledButtons = 0;
                        
                        for (let button of saveButtons) {
                            if (!button.disabled && !button.classList.contains('stibo-GraphicsButton-disabled')) {
                                availableButton = button;
                                enabledButtons++;
                            }
                        }
                        
                        return {
                            hasAvailableButton: availableButton !== null,
                            totalButtons: totalButtons,
                            enabledButtons: enabledButtons
                        };
                    }
                """)
                
                print(f"检查第 {attempt + 1} 次: 总按钮数={result['totalButtons']}, 可用按钮数={result['enabledButtons']}")
                
                if result['hasAvailableButton']:
                    print("✅ 检测到可用的Save按钮，所有文件上传完成")
                    save_button_available = True
                    break
                else:
                    print(f"Save按钮仍不可用，等待 {wait_interval} 秒...")
                    page.wait_for_timeout(wait_interval * 1000)
                    
            except Exception as e:
                print(f"检查Save按钮状态时出错: {e}")
                page.wait_for_timeout(wait_interval * 1000)
        
        if not save_button_available:
            print("⚠️ 等待Save按钮可用超时")
            print("可能的原因：")
            print("1. 仍有文件正在上传中")
            print("2. 有文件上传失败")
            print("3. 页面存在其他问题")
            print("将尝试强制操作...")
        else:
            print("✅ Save按钮已可用，准备保存")
        
        # 使用第一个选择器点击Save按钮（根据日志验证有效）
        try:
            save_button = page.locator("button.SaveButton:has-text('Save'):not([disabled])").first
            if save_button.is_visible(timeout=2000) and save_button.is_enabled():
                save_button.click(force=True)
                print("✅ Save按钮点击成功 (选择器 1)")
                save_clicked = True
            else:
                print("Save按钮不可用")
                save_clicked = False
        except Exception as e:
            print(f"Save按钮点击失败: {e}")
            save_clicked = False
        
        if not save_clicked:
            print("❌ 无法找到或点击Save按钮")
            return False
        
        # 第二步：等待Save按钮变灰（disabled状态）
        print("2. 等待Save按钮变为禁用状态...")
        try:
            # 等待Save按钮变为disabled状态，最多等待30秒
            page.wait_for_function(
                """() => {
                    const saveButton = document.querySelector('button.SaveButton, button[class*="SaveButton"]');
                    return saveButton && (saveButton.disabled || saveButton.classList.contains('stibo-GraphicsButton-disabled'));
                }""",
                timeout=30000
            )
            print("✅ Save按钮已变为禁用状态，保存完成")
        except Exception as e:
            print(f"⚠️ 等待Save按钮禁用超时，但可能已保存成功: {e}")
            # 继续执行，不中断流程
        
        # 额外等待确保保存完全完成
        page.wait_for_timeout(2000)
        
        # 第三步：点击Validate按钮（使用第一个选择器，根据日志验证有效）
        print("3. 查找并点击Validate PEDA按钮...")
        try:
            validate_button = page.locator("button.RunBusinessActionButton:has-text('Validate PEDA')")
            if validate_button.is_visible() and validate_button.is_enabled():
                validate_button.click()
                print("✅ Validate PEDA按钮点击成功 (选择器 1)")
                validate_clicked = True
            else:
                print("Validate PEDA按钮不可用")
                validate_clicked = False
        except Exception as e:
            print(f"Validate PEDA按钮点击失败: {e}")
            validate_clicked = False
        
        if not validate_clicked:
            print("❌ 无法找到或点击Validate PEDA按钮")
            return False
        
        # 第四步：等待验证完成和页面跳转
        print("4. 等待PEDA验证完成和页面跳转...")
        page.wait_for_timeout(8000)  # 等待验证过程和页面跳转
        
        # 第五步：点击Cover Sheet标签
        print("5. 点击Cover Sheet标签...")
        try:
            # 等待页面跳转完成
            page.wait_for_load_state("networkidle", timeout=10000)
            page.wait_for_timeout(2000)
            
            # 先检查Cover Sheet标签是否已经选中
            try:
                if page.locator("#stibo_tab_Cover_Sheet.tabs-panel-tab--selected").is_visible(timeout=1000):
                    print("✅ Cover Sheet标签已经是选中状态")
                    return True
            except:
                print("Cover Sheet标签当前未选中，需要点击")
            
            # 使用强制点击方法（根据日志验证有效）
            try:
                print("尝试Cover Sheet标签点击方法 1...")
                page.locator("#stibo_tab_Cover_Sheet").click(force=True)
                
                # 等待标签状态改变
                page.wait_for_timeout(1500)
                
                # 验证是否成功切换
                if page.locator("#stibo_tab_Cover_Sheet.tabs-panel-tab--selected").is_visible(timeout=3000):
                    print("✅ Cover Sheet标签点击成功 (方法 1)")
                    print("✅ 已成功切换到Cover Sheet标签页")
                    clicked = True
                else:
                    print("⚠️ 标签页切换失败")
                    clicked = False
                        
            except Exception as e:
                print(f"Cover Sheet点击失败: {e}")
                clicked = False
            
            if not clicked:
                print("❌ 无法成功切换到Cover Sheet标签")
                print("⚠️ 未能自动点击Cover Sheet标签")
                print("请手动点击Cover Sheet标签查看相关信息")
                print("常见原因：页面结构变化、元素被遮挡或网络延迟")
                return False
            else:
                # 等待Cover Sheet页面内容加载
                print("等待Cover Sheet页面内容加载...")
                page.wait_for_timeout(3000)
        
        except Exception as e:
            print(f"⚠️ 点击Cover Sheet标签时出错: {e}")
            print("这通常不影响PEDA的保存和验证，请手动点击Cover Sheet标签")
        
        print("=== PEDA保存、验证和Cover Sheet流程完成 ===\n")
        
        # 新增：自动导出Cover Sheet PDF
        if part_number:
            print(f"\n=== 开始为 {part_number} 导出Cover Sheet PDF ===")
            if log_callback:
                try:
                    log_callback(f"=== 开始为 {part_number} 导出Cover Sheet PDF ===", "INFO")
                except Exception:
                    pass
            
            # 修改：使用件号文件夹作为PDF保存目录，而不是单独的PDF_Downloads文件夹
            if document_manager and hasattr(document_manager, 'part_folder'):
                # 直接保存到件号文件夹内，与上传文件在一起
                pdf_save_dir = str(document_manager.part_folder)
                print(f"=== PDF_Print_V12: 开始为 {part_number} 下载PDF ===")
                print(f"保存目录: {pdf_save_dir}")
            else:
                # 备选方案：使用默认路径（document_maintenance_path 不再从Excel读取）
                print("⚠️ 警告：document_manager 不可用，使用默认路径")
                base_path = "C:\\OES\\AI\\PIMS_Automation\\IAM\\PEDA\\PEDA_Ducuments"
                pdf_save_dir = os.path.join(base_path, part_number)
                print(f"=== 使用默认路径保存PDF ===")
                print(f"保存目录: {pdf_save_dir}")
                
                # 确保目录存在
                os.makedirs(pdf_save_dir, exist_ok=True)
            
            # 调用PDF打印功能
            pdf_success = print_coversheet_pdf_v12(page, part_number, pdf_save_dir)

            if pdf_success:
                print(f"✅ {part_number} 的Cover Sheet PDF导出成功")
                if log_callback:
                    try:
                        log_callback(f"✅ {part_number} 的Cover Sheet PDF导出成功", "SUCCESS")
                    except Exception:
                        pass
            else:
                print(f"❌ {part_number} 的Cover Sheet PDF导出失败")
                if log_callback:
                    try:
                        log_callback(f"❌ {part_number} 的Cover Sheet PDF导出失败", "ERROR")
                    except Exception:
                        pass
                # 不让PDF导出失败影响整个流程
        
        return True
        
    except Exception as e:
        print(f"❌ 保存和验证PEDA时发生错误: {e}")
        return False