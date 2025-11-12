"""
测试浏览器自动查找功能
"""

from modules.browser_finder import BrowserFinder


def main():
    print("=" * 70)
    print("测试浏览器自动查找功能")
    print("=" * 70)
    
    # 创建浏览器查找器
    finder = BrowserFinder(log_callback=lambda msg, level="INFO": print(f"[{level}] {msg}"))
    
    print("\n=== 测试 1: 自动查找（优先 Chrome）===")
    browser_path, browser_type = finder.find_browser(preferred_browser="auto")
    print(f"结果: {browser_type} - {browser_path}")
    
    print("\n=== 测试 2: 仅查找 Chrome ===")
    finder.clear_cache()
    browser_path, browser_type = finder.find_browser(preferred_browser="chrome")
    print(f"结果: {browser_type} - {browser_path}")
    
    print("\n=== 测试 3: 仅查找 Edge ===")
    finder.clear_cache()
    browser_path, browser_type = finder.find_browser(preferred_browser="msedge")
    print(f"结果: {browser_type} - {browser_path}")
    
    print("\n=== 测试 4: 使用缓存（应该很快）===")
    browser_path, browser_type = finder.find_browser(preferred_browser="auto")
    print(f"结果: {browser_type} - {browser_path}")
    
    print("\n=== 浏览器信息 ===")
    info = finder.get_browser_info()
    print(f"路径: {info['path']}")
    print(f"类型: {info['type']}")
    print(f"已缓存: {info['is_cached']}")
    
    print("\n" + "=" * 70)
    print("✅ 测试完成")
    print("=" * 70)


if __name__ == "__main__":
    main()
