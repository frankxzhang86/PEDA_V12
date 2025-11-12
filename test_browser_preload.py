"""
测试浏览器预热功能
验证预热后启动浏览器的速度提升
"""
import time
from modules.browser_finder import BrowserFinder


def test_without_preload():
    """测试不预热的情况"""
    print("\n=== 测试1：不预热 ===")
    start = time.time()
    
    finder = BrowserFinder()
    path, browser_type = finder.find_browser()
    
    elapsed = time.time() - start
    print(f"✅ 找到浏览器: {browser_type}")
    print(f"⏱️  耗时: {elapsed:.3f} 秒")
    return elapsed


def test_with_preload():
    """测试预热的情况"""
    print("\n=== 测试2：预热模式 ===")
    
    # 模拟预热阶段
    print("1️⃣ 预热阶段：查找并缓存浏览器...")
    preload_start = time.time()
    finder = BrowserFinder()
    finder.find_browser()  # 第一次查找，会缓存结果
    preload_time = time.time() - preload_start
    print(f"   预热完成，耗时: {preload_time:.3f} 秒")
    
    # 模拟用户点击"开始处理"
    print("\n2️⃣ 处理阶段：使用缓存的浏览器路径...")
    process_start = time.time()
    path, browser_type = finder.find_browser()  # 第二次，直接返回缓存
    process_time = time.time() - process_start
    
    print(f"✅ 找到浏览器: {browser_type} (缓存)")
    print(f"⏱️  处理阶段耗时: {process_time:.3f} 秒")
    print(f"🚀 加速效果: {(preload_time - process_time) / preload_time * 100:.1f}%")
    
    return preload_time, process_time


def main():
    print("=" * 60)
    print("🧪 浏览器预热性能测试")
    print("=" * 60)
    
    # 测试不预热
    time_without = test_without_preload()
    
    # 测试预热
    time_preload, time_cached = test_with_preload()
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)
    print(f"不预热模式：{time_without:.3f} 秒")
    print(f"预热模式（预热阶段）：{time_preload:.3f} 秒")
    print(f"预热模式（处理阶段）：{time_cached:.3f} 秒 ⚡")
    print(f"\n用户体验提升：从 {time_without:.3f}秒 → {time_cached:.3f}秒")
    print(f"减少等待时间：{(time_without - time_cached):.3f} 秒")
    if time_without > time_cached:
        speedup = (time_without - time_cached) / time_without * 100
        print(f"🎯 速度提升：{speedup:.1f}%")


if __name__ == "__main__":
    main()
