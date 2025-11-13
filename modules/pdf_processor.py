from datetime import datetime
from playwright.sync_api import Page
from pathlib import Path


def print_coversheet_pdf_v12(page: Page, part_number: str, save_dir: str) -> bool:
    """
    PDF_Print_V12: PDF导航模块
    
    专门负责查找PDF iframe和页面导航，实际PDF处理由Final模块完成
    
    Args:
        page: Playwright页面对象
        part_number: 零件号
        save_dir: 保存目录
        
    Returns:
        bool: 处理成功返回True，失败返回False
    """
    try:
        print(f"\n=== PDF_Print_V12: 开始为 {part_number} 下载PDF ===")
        print(f"保存目录: {save_dir}")
        # 确保保存目录存在
        Path(save_dir).mkdir(parents=True, exist_ok=True)
        
        # 步骤1: 查找PDF iframe并导航
        success = find_and_navigate_to_pdf(page)
        if not success:
            print("❌ 未找到PDF页面")
            return False
        
        # 步骤2: 调用Final模块处理PDF
        print("调用PDF_Print_Final模块处理PDF...")
        from .pdf_downloader import handle_pdf_final
        return handle_pdf_final(page, part_number, save_dir)
            
    except Exception as e:
        print(f"❌ PDF下载失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def find_and_navigate_to_pdf(page: Page) -> bool:
    """
    查找并导航到PDF页面
    """
    try:
        print("查找PDF iframe...")
        
        # 检查页面中的所有iframe
        iframes = page.query_selector_all("iframe")
        print(f"找到 {len(iframes)} 个iframe")
        
        pdf_iframe_src = None
        for i, iframe in enumerate(iframes):
            src = iframe.get_attribute("src")
            print(f"iframe {i}: src = {src}")
            
            if src and "publishing/proof/product" in src:
                pdf_iframe_src = src
                print(f"✅ 找到PDF iframe {i}: {src}")
                break
        
        if not pdf_iframe_src:
            print("❌ 未找到PDF iframe")
            return False
        
        # 构建完整的PDF URL
        if pdf_iframe_src.startswith("/"):
            base_url = f"{page.url.split('/webui')[0]}"
            pdf_url = f"{base_url}{pdf_iframe_src}"
        else:
            pdf_url = pdf_iframe_src
        
        print("直接导航到PDF页面...")
        print(f"PDF URL: {pdf_url}")
        
        page.goto(pdf_url)
        
        # 简单等待页面加载
        print("等待页面加载...")
        page.wait_for_timeout(8000)
        print("✅ 页面加载完成，准备交由Final模块处理")
        return True
        
    except Exception as e:
        print(f"❌ 导航到PDF页面失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("PDF_Print_V12 - PDF导航模块")
    print("负责查找PDF iframe和页面导航，调用Final模块进行PDF处理")