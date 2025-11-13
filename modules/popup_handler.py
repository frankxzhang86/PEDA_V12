"""
弹窗处理模块
用于处理PEDA系统中的各种弹窗，确保流程不被意外弹窗中断
"""

from playwright.sync_api import Page
from typing import Optional


def detect_popup(page: Page, timeout: int = 2000) -> bool:
    """
    检测页面是否存在弹窗
    
    Args:
        page: Playwright页面对象
        timeout: 检测超时时间（毫秒）
        
    Returns:
        bool: 存在弹窗返回True
    """
    try:
        # 检测遮罩层
        if page.locator('.gwt-PopupPanelGlass').is_visible(timeout=timeout):
            print("✅ 检测到遮罩层 (.gwt-PopupPanelGlass)")
            return True
        
        # 检测常见弹窗元素
        popup_selectors = [
            '.portal-popup-header__title',
            '[class*="popup"]',
            '[class*="dialog"]',
            '.stibo-GraphicsButton:has-text("OK")',
            '.stibo-GraphicsButton:has-text("Go back")'
        ]
        
        for selector in popup_selectors:
            if page.locator(selector).is_visible(timeout=500):
                print(f"✅ 检测到弹窗元素: {selector}")
                return True
        
        return False
    except Exception as e:
        print(f"检测弹窗时出错: {e}")
        return False


def handle_product_not_found_popup(page: Page) -> bool:
    """
    处理"Product Not Found"弹窗
    
    当产品搜索失败时，系统会弹出提示，需要点击"Go back"按钮返回主页
    
    Args:
        page: Playwright页面对象
        
    Returns:
        bool: 成功处理返回True
    """
    try:
        print("\n=== 检测产品未找到弹窗 ===")
        
        # 等待弹窗出现
        page.wait_for_timeout(2000)
        
        # 检测是否有弹窗
        if not detect_popup(page):
            print("未检测到弹窗，无需处理")
            return True
        
        print("检测到弹窗，开始处理...")
        
        # 方法1: 尝试点击 "Go back" 按钮
        print("尝试点击 'Go back' 按钮...")
        go_back_selectors = [
            'button.stibo-GraphicsButton:has-text("Go back")',
            'button:has-text("Go back")',
            'button[class*="Button"]:has-text("Go back")',
            '.stibo-GraphicsButton span.text:has-text("Go back")'
        ]
        
        for i, selector in enumerate(go_back_selectors, 1):
            try:
                button = page.locator(selector).first
                if button.is_visible(timeout=1000):
                    button.click(force=True)
                    print(f"✅ 成功点击 'Go back' 按钮 (选择器 {i})")
                    page.wait_for_timeout(1000)
                    
                    # 验证弹窗是否关闭
                    if not detect_popup(page, timeout=1000):
                        print("✅ 弹窗已关闭，页面恢复正常")
                        return True
                    else:
                        print("⚠️ 弹窗仍然存在，尝试其他方法")
            except Exception as e:
                print(f"选择器 {i} 失败: {e}")
                continue
        
        # 方法2: 尝试点击 "OK" 按钮（备用）
        print("尝试点击 'OK' 按钮...")
        ok_selectors = [
            'button.stibo-GraphicsButton:has-text("OK")',
            'button:has-text("OK")',
            'button[class*="Button"]:has-text("OK")'
        ]
        
        for i, selector in enumerate(ok_selectors, 1):
            try:
                button = page.locator(selector).first
                if button.is_visible(timeout=1000):
                    button.click(force=True)
                    print(f"✅ 成功点击 'OK' 按钮 (选择器 {i})")
                    page.wait_for_timeout(1000)
                    
                    if not detect_popup(page, timeout=1000):
                        print("✅ 弹窗已关闭")
                        return True
            except Exception as e:
                print(f"选择器 {i} 失败: {e}")
                continue
        
        # 方法3: 尝试按 ESC 键
        print("尝试按 ESC 键关闭弹窗...")
        try:
            page.keyboard.press("Escape")
            page.wait_for_timeout(1000)
            
            if not detect_popup(page, timeout=1000):
                print("✅ ESC 键成功关闭弹窗")
                return True
        except Exception as e:
            print(f"ESC 键失败: {e}")
        
        # 方法4: 强制清理遮罩层和弹窗
        print("尝试强制清理遮罩层和弹窗...")
        success = clear_all_popups(page)
        
        if success:
            print("✅ 产品未找到弹窗处理完成")
            return True
        else:
            print("❌ 产品未找到弹窗处理失败")
            return False
        
    except Exception as e:
        print(f"❌ 处理产品未找到弹窗时出错: {e}")
        # 尝试最后的清理
        clear_all_popups(page)
        return False


def handle_fatal_error_popup(page: Page) -> bool:
    """
    处理"Fatal Error"弹窗
    
    当系统出现致命错误时，需要关闭弹窗并可能需要重置状态
    
    Args:
        page: Playwright页面对象
        
    Returns:
        bool: 成功处理返回True
    """
    try:
        print("\n=== 检测Fatal Error弹窗 ===")
        
        # 检测Fatal Error关键词
        error_keywords = ["Fatal", "Error", "error had occurred"]
        has_error = False
        
        for keyword in error_keywords:
            try:
                if page.locator(f'text="{keyword}"').is_visible(timeout=1000):
                    print(f"✅ 检测到错误弹窗: 包含关键词 '{keyword}'")
                    has_error = True
                    break
            except:
                continue
        
        if not has_error:
            print("未检测到Fatal Error弹窗")
            return True
        
        print("开始处理Fatal Error弹窗...")
        
        # 尝试点击OK或Close按钮
        close_selectors = [
            'button:has-text("OK")',
            'button:has-text("Close")',
            'button.stibo-GraphicsButton'
        ]
        
        for selector in close_selectors:
            try:
                button = page.locator(selector).first
                if button.is_visible(timeout=1000):
                    button.click(force=True)
                    print(f"✅ 点击关闭按钮: {selector}")
                    page.wait_for_timeout(1000)
                    break
            except:
                continue
        
        # 强制清理
        clear_all_popups(page)
        print("✅ Fatal Error弹窗处理完成")
        return True
        
    except Exception as e:
        print(f"❌ 处理Fatal Error弹窗时出错: {e}")
        clear_all_popups(page)
        return False


def clear_all_popups(page: Page) -> bool:
    """
    强制清理所有弹窗和遮罩层
    
    当正常方法无法关闭弹窗时，使用JavaScript强制移除
    
    Args:
        page: Playwright页面对象
        
    Returns:
        bool: 清理成功返回True
    """
    try:
        print("执行强制清理...")
        
        # 执行JavaScript清理
        page.evaluate("""
            () => {
                // 清理所有遮罩层
                const glassPanels = document.querySelectorAll('.gwt-PopupPanelGlass, [class*="glass"], [class*="overlay"]');
                glassPanels.forEach(el => {
                    console.log('移除遮罩层:', el.className);
                    el.remove();
                });
                
                // 清理所有弹窗
                const popups = document.querySelectorAll('[class*="popup"], [class*="dialog"], [class*="modal"]');
                popups.forEach(el => {
                    // 只移除可能的弹窗，不移除整个应用的容器
                    if (el.style.zIndex && parseInt(el.style.zIndex) > 1000) {
                        console.log('移除弹窗:', el.className);
                        el.remove();
                    }
                });
                
                // 恢复body的滚动
                document.body.style.overflow = '';
                
                console.log('清理完成');
            }
        """)
        
        page.wait_for_timeout(500)
        
        # 验证清理结果
        if not detect_popup(page, timeout=500):
            print("✅ 强制清理成功，页面恢复正常")
            return True
        else:
            print("⚠️ 清理后仍检测到弹窗元素")
            return False
        
    except Exception as e:
        print(f"❌ 强制清理失败: {e}")
        return False


def handle_any_popup(page: Page) -> bool:
    """
    通用弹窗处理函数
    
    自动检测并尝试关闭任何类型的弹窗
    
    Args:
        page: Playwright页面对象
        
    Returns:
        bool: 成功处理返回True
    """
    try:
        if not detect_popup(page):
            return True
        
        print("\n=== 检测到弹窗，尝试通用处理 ===")
        
        # 尝试各种常见的关闭方式
        close_actions = [
            ('button:has-text("Go back")', "Go back"),
            ('button:has-text("OK")', "OK"),
            ('button:has-text("Close")', "Close"),
            ('button:has-text("Cancel")', "Cancel"),
            ('[aria-label="Close"]', "Close icon")
        ]
        
        for selector, name in close_actions:
            try:
                button = page.locator(selector).first
                if button.is_visible(timeout=500):
                    button.click(force=True)
                    print(f"✅ 点击 '{name}' 按钮")
                    page.wait_for_timeout(1000)
                    
                    if not detect_popup(page, timeout=500):
                        print("✅ 弹窗已关闭")
                        return True
            except:
                continue
        
        # 如果常规方法失败，强制清理
        print("常规方法失败，执行强制清理...")
        return clear_all_popups(page)
        
    except Exception as e:
        print(f"❌ 通用弹窗处理失败: {e}")
        clear_all_popups(page)
        return False
