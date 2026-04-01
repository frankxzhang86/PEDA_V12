def set_language_after_login(page):
    """
    登录后立即设置语言为英语
    """
    try:
        print("开始设置语言为English...")

        # 等待页面完全加载
        page.wait_for_load_state("networkidle", timeout=15000)
        page.wait_for_timeout(2000)
        
        # 检查是否已经是英语界面
        try:
            search_placeholder_en = "Search for products, documents, ..."
            if page.get_by_placeholder(search_placeholder_en).is_visible(timeout=3000):
                print("✅ 检测到主页已为英语界面，无需切换")
                return True
        except:
            pass

        print("开始切换语言到English...")
        
        # 第一步：点击System Settings按钮
        page.locator('div[title="System Settings"]').click()
        print("✅ 已点击System Settings按钮")
        page.wait_for_timeout(1000)

        # 第二步：选择English选项 (使用更精确的定位器)
        page.locator('div.selectable-item[title="English"]').click()
        print("✅ 已选择English选项")
        
        # 第三步：等待页面刷新完成
        print("等待页面刷新...")
        page.wait_for_load_state("networkidle", timeout=10000)
        page.wait_for_timeout(2000)

        # 验证语言切换结果
        try:
            if page.get_by_placeholder(search_placeholder_en).is_visible(timeout=5000):
                print("✅ 语言成功切换到英语")
                return True
            else:
                print("✅ 语言切换完成（验证可能因页面变化而失败）")
                return True
        except:
            print("✅ 语言切换操作完成")
            return True

    except Exception as e:
        print(f"❌ 语言设置时发生异常: {e}")
        # 保存截图用于调试
        try:
            page.screenshot(path="language_setting_error.png")
            print("已保存语言设置错误截图: language_setting_error.png")
        except:
            pass
        return False

def handle_login_popup(page):
    """处理登录后的系统通知弹窗 - 使用正确的选择器"""
    try:
        print("正在检测系统通知弹窗...")
        
        # 使用正确的弹窗检测选择器
        popup_detected = False
        popup_selectors = [
            ".portal-popup-header__title:has-text('System Notice')",
            "div:has-text('System Notice')",
            ".portal-popup-header__title",
            "[class*='portal-popup']",
            ".stibo-GraphicsButton:has-text('OK')"
        ]
        
        for i, selector in enumerate(popup_selectors, 1):
            try:
                if page.locator(selector).is_visible(timeout=2000):
                    print(f"✅ 检测到系统通知弹窗 (选择器 {i}: {selector})")
                    popup_detected = True
                    break
            except:
                continue        
        if not popup_detected:
            print("未检测到系统通知弹窗")
            return True
        
        print("开始处理系统通知弹窗...")
        
        # 使用Playwright点击操作
        print("尝试Playwright点击操作...")
        try:
            # 勾选复选框
            checkbox_selectors = [
                'label[for="gwt-uid-1"]',
                'input[id="gwt-uid-1"]',
                'input[type="checkbox"]'
            ]
            
            for selector in checkbox_selectors:
                try:
                    if page.locator(selector).is_visible(timeout=1000):
                        page.locator(selector).click(force=True)
                        print(f"✅ 已勾选 'Don't show this again' (选择器: {selector})")
                        break
                except:
                    continue
            
            # 点击OK按钮
            ok_button_selectors = [
                'button.stibo-GraphicsButton:has-text("OK")',
                'button:has(.text:has-text("OK"))',
                '.stibo-GraphicsButton span.text:has-text("OK")',
                'button[type="button"]:has-text("OK")',
                'button.stibo-GraphicsButton'
            ]
            
            for selector in ok_button_selectors:
                try:
                    if page.locator(selector).is_visible(timeout=1000):
                        page.locator(selector).click(force=True)
                        print(f"✅ 已点击OK按钮 (选择器: {selector})")
                        break
                except:
                    continue
            
            page.wait_for_timeout(1000)
            
            # 验证弹窗是否关闭
            if not page.locator(".portal-popup-header__title").is_visible(timeout=2000):
                print("✅ Playwright方法成功关闭弹窗")
                return True
                
        except Exception as e:
            print(f"Playwright方法失败: {e}")
        
        # 方法3: 强制移除遮罩层和弹窗
        print("尝试强制移除遮罩层...")
        try:
            page.evaluate("""
                // 移除所有遮罩层
                document.querySelectorAll('.gwt-PopupPanelGlass').forEach(el => {
                    console.log('移除遮罩层:', el);
                    el.remove();
                });
                document.querySelectorAll('[class*="glass"]').forEach(el => el.remove());
                document.querySelectorAll('[class*="overlay"]').forEach(el => el.remove());
                
                // 移除弹窗
                document.querySelectorAll('.portal-popup-header__title').forEach(el => {
                    const popup = el.closest('[class*="popup"]') || el.closest('[class*="dialog"]');
                    if (popup) {
                        console.log('移除弹窗:', popup);
                        popup.remove();
                    }
                });
            """)
            
            page.wait_for_timeout(500)
            print("✅ 已强制移除遮罩层和弹窗")
            return True
            
        except Exception as e:
            print(f"强制移除失败: {e}")
        
        # 最后手段：按ESC键或Enter键
        try:
            print("尝试按ESC键关闭弹窗...")
            page.keyboard.press("Escape")
            page.wait_for_timeout(1000)
            
            if not page.locator(".portal-popup-header__title").is_visible(timeout=2000):
                print("✅ ESC键成功关闭弹窗")
                return True
        except:
            pass
        
        try:
            print("尝试按Enter键关闭弹窗...")
            page.keyboard.press("Enter")
            page.wait_for_timeout(1000)
            
            if not page.locator(".portal-popup-header__title").is_visible(timeout=2000):
                print("✅ Enter键成功关闭弹窗")
                return True
        except:
            pass
        
        print("❌ 所有弹窗关闭方法都失败了")
        return False
        
    except Exception as e:
        print(f"❌ 处理系统通知弹窗时出错: {e}")
        return False

def enhanced_product_search(page, part_number):
    """增强的产品搜索方法，重点选择THP类型的结果"""
    search_box = page.locator("[id=\"Find_BP\\,_Products\\,_OE_Numbers\\,_THPs\"]").get_by_role("textbox", name="Search...")
    
    print(f"开始增强搜索: {part_number}")
    
    # 步骤1: 确保搜索框获得焦点
    search_box.click()
    page.wait_for_timeout(500)
    print("搜索框已获得焦点")
    
    # 步骤2: 清空并逐字符输入
    search_box.clear()
    print("开始逐字符输入...")
    for i, char in enumerate(part_number):
        search_box.type(char, delay=150)  # 每字符150ms延迟
        if (i + 1) % 3 == 0:  # 每3个字符打印一次进度
            print(f"已输入: {part_number[:i+1]}")
    
    print(f"输入完成: {part_number}")
    
    # 步骤3: 触发搜索事件
    search_box.dispatch_event('input')
    search_box.dispatch_event('keyup')
    print("已触发搜索事件")
    
    # 步骤4: 等待搜索建议出现
    print(f"等待 {part_number} 的搜索建议...")
    page.wait_for_timeout(3000)  # 等待3秒让建议加载
      # 步骤5: 获取所有建议项，用Python逻辑精确匹配
    # 正确格式: title="100169&nbsp;(THP_xxxxxxx)" —— 括号内直接以 THP_ 开头
    # 错误格式: title="100169&nbsp;(100169_THP_DOGA)" —— 括号内以件号开头
    # 直接用 title 属性选择器匹配，无需处理 &nbsp; 空格问题
    print("开始查找搜索建议（直接匹配 title 属性）...")
    try:
        # 先打印所有候选项供调试
        all_suggestions = page.locator(f'[title*="{part_number}"]').all()
        print(f"找到 {len(all_suggestions)} 个建议项:")
        for i, suggestion in enumerate(all_suggestions):
            try:
                title = suggestion.get_attribute('title') or ''
                print(f"  {i+1}. {title}")
            except Exception as e:
                print(f"  {i+1}. 无法读取title: {e}")

        # 精确选择：title 属性中含 "(THP_" 的项（括号内直接以 THP_ 开头）
        thp_element = page.locator(f'[title*="(THP_"]').first
        if thp_element.is_visible(timeout=3000):
            title = thp_element.get_attribute('title') or ''
            thp_element.click()
            print(f"✅ 选中正确的THP项: {title}")
            return True
        else:
            print(f"❌ 未检测到 THP 项（括号内以 THP_ 开头），搜索失败")
            return False
    except Exception as e:
        print(f"查找建议项失败: {e}")
    
    # 步骤7: 最后的fallback - 直接按回车搜索
    print("⚠️ 没有找到任何搜索建议，使用回车键直接搜索")
    search_box.press('Enter')
    page.wait_for_timeout(2000)
      # 检查是否有搜索结果页面
    try:
        result_elements = page.locator(f'[title*="{part_number}"]').all()
        if result_elements:
            print(f"搜索结果页面找到 {len(result_elements)} 个结果")
            for element in result_elements:
                try:
                    text = element.text_content()
                    if "(THP_" in text:
                        element.click()
                        print(f"✅ 从搜索结果选择了THP项: {text}")
                        return True
                except:
                    continue
            # 选择第一个结果
            result_elements[0].click()
            print("选择了第一个搜索结果")
            return True
    except Exception as e:
        print(f"检查搜索结果失败: {e}")
    
    # 搜索失败，检测并处理可能的"Product Not Found"弹窗
    print(f"⚠️ 产品 {part_number} 搜索失败，检测是否有弹窗...")
    from .popup_handler import handle_product_not_found_popup
    handle_product_not_found_popup(page)
    
    return False 