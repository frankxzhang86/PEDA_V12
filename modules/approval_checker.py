"""
THP审批状态检查模块
用于在创建PEDA前检查THP是否已批准，避免触发错误
"""

from playwright.sync_api import Page
from typing import Optional


def check_thp_approval_status(page: Page, part_number: str) -> bool:
    """
    检查THP的审批状态
    
    在产品搜索成功后、创建PEDA前调用此函数
    检查页面上是否显示"Never Approved"状态
    
    Args:
        page: Playwright页面对象
        part_number: 件号（用于日志记录）
        
    Returns:
        bool: 已批准返回True，未批准返回False
    """
    try:
        print(f"\n=== 检查THP {part_number} 的审批状态 ===")
        
        # 方法1: 查找"Never Approved"文本
        print("方法1: 查找 'Never Approved' 文本...")
        try:
            never_approved_element = page.locator('text="Never Approved"').first
            if never_approved_element.is_visible(timeout=2000):
                print(f"❌ 检测到THP {part_number} 状态为: Never Approved")
                return False
        except Exception as e:
            print(f"方法1未找到: {e}")
        
        # 方法2: 查找特定的CSS类"NotInApproved"
        print("方法2: 查找 '.approval.NotInApproved' 元素...")
        try:
            not_approved_element = page.locator('span.approval.NotInApproved').first
            if not_approved_element.is_visible(timeout=2000):
                text = not_approved_element.text_content()
                print(f"❌ 检测到THP {part_number} 审批状态为: {text}")
                return False
        except Exception as e:
            print(f"方法2未找到: {e}")
        
        # 方法3: 查找包含"approval"类且包含"NotInApproved"的元素
        print("方法3: 查找 '[class*=\"approval\"][class*=\"NotInApproved\"]' 元素...")
        try:
            approval_element = page.locator('[class*="approval"][class*="NotInApproved"]').first
            if approval_element.is_visible(timeout=2000):
                text = approval_element.text_content()
                print(f"❌ 检测到THP {part_number} 审批状态为: {text}")
                return False
        except Exception as e:
            print(f"方法3未找到: {e}")
        
        # 方法4: 查找"Approved"或其他批准状态，反向确认
        print("方法4: 查找批准状态元素...")
        try:
            approved_selectors = [
                'span.approval.InApproved',
                'span.approval:has-text("Approved")',
                '[class*="approval"][class*="Approved"]:not([class*="NotInApproved"])'
            ]
            
            for selector in approved_selectors:
                try:
                    approved_element = page.locator(selector).first
                    if approved_element.is_visible(timeout=1000):
                        text = approved_element.text_content()
                        print(f"✅ 检测到THP {part_number} 已批准: {text}")
                        return True
                except:
                    continue
        except Exception as e:
            print(f"方法4检查失败: {e}")
        
        # 如果无法确定状态，假设已批准（允许继续）
        print(f"⚠️ 无法检测到明确的审批状态，假设THP {part_number} 已批准，继续处理")
        return True
        
    except Exception as e:
        print(f"❌ 检查THP审批状态时出错: {e}")
        # 出错时允许继续，让后续流程来处理
        print(f"⚠️ 出错，假设THP {part_number} 已批准，继续处理")
        return True


def get_approval_status_text(page: Page) -> Optional[str]:
    """
    获取当前页面的THP审批状态文本
    
    用于调试和日志记录
    
    Args:
        page: Playwright页面对象
        
    Returns:
        str: 审批状态文本（如"Never Approved", "Approved"等），无法获取返回None
    """
    try:
        # 尝试获取审批状态元素
        status_selectors = [
            'span.approval',
            '[class*="approval"]'
        ]
        
        for selector in status_selectors:
            try:
                elements = page.locator(selector).all()
                for element in elements:
                    if element.is_visible(timeout=500):
                        text = element.text_content()
                        if text and text.strip():
                            return text.strip()
            except:
                continue
        
        return None
        
    except Exception as e:
        print(f"获取审批状态文本时出错: {e}")
        return None
