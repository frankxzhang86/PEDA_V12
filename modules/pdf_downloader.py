import requests
from datetime import datetime
from playwright.sync_api import Page
from pathlib import Path
import urllib3

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def handle_pdf_final(page: Page, part_number: str, save_dir: str) -> bool:
    """
    PDF_Print_Final: PDF最终处理模块
    
    直接从URL下载原始PDF文件
    """
    print("🎯 PDF_Print_Final: 开始处理PDF页面...")
    
    # 确保保存目录存在
    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)
    
    # 构建文件保存路径
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{part_number}_CoverSheet_{timestamp}.pdf"
    full_file_path = save_path / file_name

    # 直接HTTP请求下载原始PDF
    try:
        print("\n--- 尝试直接下载原始PDF文件 ---")
        pdf_url = page.url
        print(f"从URL下载: {pdf_url}")

        # 从Playwright获取当前页面的cookies，用于身份验证
        cookies_list = page.context.cookies()
        cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies_list}
        print("已获取浏览器Cookies用于请求认证。")

        # 使用requests库发送带有cookies的GET请求，禁用SSL验证
        response = requests.get(
            pdf_url, 
            cookies=cookies_dict, 
            timeout=60, 
            verify=False  # 禁用SSL证书验证
        )
        response.raise_for_status()

        # 先尝试保存文件
        with open(full_file_path, 'wb') as f:
            f.write(response.content)
        
        # 检查文件是否成功保存且大小合理
        if full_file_path.exists() and full_file_path.stat().st_size > 100:
            print(f"✅ PDF文件已成功下载到: {full_file_path}")
            print(f"   文件大小: {full_file_path.stat().st_size} 字节")
            return True
        else:
            print("❌ 文件写入失败或文件为空")
            return False

    except Exception as e:
        print(f"❌ PDF下载失败: {e}")
        return False

if __name__ == "__main__":
    print("PDF_Print_Final - PDF最终处理模块")
    print("直接从URL下载原始PDF文件") 