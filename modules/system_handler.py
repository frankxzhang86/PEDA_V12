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
      # 步骤5: 查找THP类型的建议项
    suggestion_selectors = [
        # 优先选择THP类型（这是我们需要的）
        f'text="{part_number} (THP_"',
        f'[title*="{part_number}"][title*="THP"]',
        
        # 备选方案：其他类型
        f'text="{part_number} (Product_"',
        f'[title*="{part_number}"]'
    ]
    
    print("开始查找搜索建议...")
    for i, selector in enumerate(suggestion_selectors, 1):
        try:
            print(f"尝试选择器 {i}: {selector}")
            element = page.locator(selector).first
            
            if element.is_visible(timeout=2000):
                # 获取元素文本确认是THP类型
                element_text = element.text_content()
                print(f"找到建议项: {element_text}")
                
                # 优先选择THP类型
                if "(THP_" in element_text:
                    element.click()
                    print(f"✅ 成功选择THP类型建议: {element_text}")
                    return True
                elif i <= 3:  # 前3个是THP相关的选择器
                    element.click()
                    print(f"✅ 选择了可能的THP项: {element_text}")
                    return True
                else:
                    print(f"⚠️ 找到非THP项，继续查找: {element_text}")
                    continue
            else:
                print(f"选择器 {i} 未找到可见元素")
        except Exception as e:
            print(f"选择器 {i} 失败: {e}")
            continue
      # 步骤6: 如果没有找到建议，尝试查看页面上的所有建议项
    print("未找到预期的建议项，查看所有可用选项...")
    try:
        # 查找所有可能的建议项
        all_suggestions = page.locator(f'[title*="{part_number}"]').all()
        if all_suggestions:
            print(f"找到 {len(all_suggestions)} 个建议项:")
            for i, suggestion in enumerate(all_suggestions):
                try:
                    text = suggestion.text_content()
                    print(f"  {i+1}. {text}")
                    # 如果找到THP类型，立即选择
                    if "(THP_" in text:
                        suggestion.click()
                        print(f"✅ 从所有建议中选择了THP项: {text}")
                        return True
                except Exception as e:
                    print(f"  {i+1}. 无法读取建议项: {e}")
            
            # 如果没有THP项，选择第一个
            print("⚠️ 未找到THP项，选择第一个建议")
            all_suggestions[0].click()
            return True
    except Exception as e:
        print(f"查看所有建议项失败: {e}")
    
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
    
    return False 