import os
from playwright.sync_api import Playwright, Browser, BrowserContext, Page
from typing import Optional, Callable
from start import get_chrome_executable

# 导入登录相关模块
from .system_handler import handle_login_popup, set_language_after_login


class BrowserManager:
    """
    浏览器管理器 - 实现浏览器会话复用
    
    功能：
    - 浏览器启动和关闭管理
    - 登录状态管理
    - 页面状态重置
    - 错误恢复机制
    """
    
    def __init__(self):
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.is_logged_in: bool = False
        self.username: str = ""
        self.password: str = ""
        self.system_language: str = "en"
        self.log_callback: Optional[Callable] = None
        
    def set_log_callback(self, callback: Callable):
        """设置日志回调函数"""
        self.log_callback = callback
        
    def log(self, message: str, level: str = "INFO"):
        """记录日志"""
        if self.log_callback:
            self.log_callback(message, level)
        else:
            print(f"[{level}] {message}")
    
    def initialize(self, playwright: Playwright, username: str, password: str, 
                   system_language: str = 'en', login_url: Optional[str] = None) -> bool:
        """
        初始化浏览器并登录
        
        Args:
            playwright: Playwright实例
            username: 用户名
            password: 密码
            system_language: 系统语言
            login_url: 登录网址
            
        Returns:
            bool: 初始化成功返回True
        """
        try:
            self.log("🚀 初始化浏览器管理器...")
            
            # 保存参数
            self.playwright = playwright
            self.username = username
            self.password = password
            self.system_language = system_language
            self.login_url = login_url or "https://frd-pim-app.emea.zf-world.com/webui/WebUI_2#deepLink=1&contextID=GL&workspaceID=Main&screen=homepage"
            
            # 启动浏览器
            self.log("启动浏览器...")
            self.browser = self.playwright.chromium.launch(headless=False, executable_path=get_chrome_executable())
            self.context = self.browser.new_context()
            self.page = self.context.new_page()
            
            # 执行登录
            if self._perform_login():
                self.is_logged_in = True
                self.log("✅ 浏览器初始化和登录完成", "SUCCESS")
                return True
            else:
                self.log("❌ 登录失败", "ERROR")
                self.cleanup()
                return False
                
        except Exception as e:
            self.log(f"❌ 浏览器初始化失败: {str(e)}", "ERROR")
            self.cleanup()
            return False
    
    def _perform_login(self) -> bool:
        """
        执行登录操作
        
        Returns:
            bool: 登录成功返回True
        """
        try:
            self.log(f"正在使用用户 '{self.username}' 登录到PEDA系统...")
            
            # 导航到登录页面
            self.page.goto(self.login_url)
            
            # 输入用户名和密码
            self.page.get_by_role("textbox", name="Username").click()
            self.page.get_by_role("textbox", name="Username").fill(self.username)
            self.page.get_by_role("textbox", name="Password").click()
            self.page.get_by_role("textbox", name="Password").fill(self.password)
            self.page.get_by_role("button", name="Login").click()
            
            # 等待登录完成
            self.log("等待登录完成...")
            self.log("正在等待页面加载，这可能需要较长时间...")
            
            # 等待登录成功的标志
            try:
                self.page.wait_for_selector(".stibo-HomePage, .mainArea, .primary-navigation-panel", timeout=60000)
                self.log("✅ 登录成功，主页面已加载")
            except Exception as e:
                self.log(f"⚠️ 等待主页面超时，但继续执行: {e}")
            
            # 额外等待确保页面稳定
            self.log("等待页面完全稳定...")
            self.page.wait_for_timeout(5000)
            
            # 处理系统通知弹窗
            self.log("开始检测系统通知弹窗...")
            if not handle_login_popup(self.page):
                self.log("继续执行，但可能存在未关闭的弹窗")
            
            # 等待弹窗处理完成
            self.log("等待弹窗处理完成...")
            self.page.wait_for_timeout(3000)
            
            # 设置语言
            if not set_language_after_login(self.page):
                self.log("⚠️ 语言设置失败，但继续执行（可能已经是英语界面）")
            
            return True
            
        except Exception as e:
            self.log(f"❌ 登录过程发生错误: {str(e)}", "ERROR")
            return False
    
    def reset_for_next_part(self) -> bool:
        """
        重置状态准备处理下一个件号
        
        Returns:
            bool: 重置成功返回True
        """
        try:
            if not self.is_logged_in or not self.page:
                self.log("❌ 浏览器未初始化或未登录", "ERROR")
                return False
            
            self.log("🔄 重置页面状态，准备处理下一个件号...")
            
            # 导航回主页面
            self.page.goto("https://frd-pim-app.emea.zf-world.com/webui/WebUI_2#deepLink=1&contextID=GL&workspaceID=Main&screen=homepage")
            
            # 等待页面加载
            self.page.wait_for_timeout(3000)
            
            # 检查是否还在登录状态
            if not self._check_login_status():
                self.log("⚠️ 检测到登录状态异常，尝试重新登录...")
                if self._perform_login():
                    self.is_logged_in = True
                    # 重新登录后也要切换语言
                    if not set_language_after_login(self.page):
                        self.log("⚠️ 语言设置失败，但继续执行（可能已经是英语界面）")
                    return True
                else:
                    self.log("❌ 重新登录失败", "ERROR")
                    return False
            
            self.log("✅ 页面状态重置完成")

            # 新增：每次重置后都强制切换语言为英语
            if not set_language_after_login(self.page):
                self.log("⚠️ 语言设置失败，但继续执行（可能已经是英语界面）")
            
            return True
            
        except Exception as e:
            self.log(f"❌ 页面状态重置失败: {str(e)}", "ERROR")
            return False
    
    def _check_login_status(self) -> bool:
        """
        检查登录状态
        
        Returns:
            bool: 已登录返回True
        """
        try:
            # 检查是否存在登录页面的元素
            login_elements = self.page.query_selector_all("input[name='Username'], input[name='Password']")
            if login_elements:
                return False  # 如果找到登录元素，说明未登录
            
            # 检查是否存在主页面的标志性元素
            home_elements = self.page.query_selector_all(".stibo-HomePage, .mainArea, .primary-navigation-panel")
            return len(home_elements) > 0
            
        except Exception:
            return False
    
    def get_page(self) -> Optional[Page]:
        """
        获取当前页面对象
        
        Returns:
            Page: 页面对象，如果未初始化返回None
        """
        if self.is_logged_in and self.page:
            return self.page
        return None
    
    def is_ready(self) -> bool:
        """
        检查管理器是否准备就绪
        
        Returns:
            bool: 准备就绪返回True
        """
        return (self.is_logged_in and 
                self.browser is not None and 
                self.context is not None and 
                self.page is not None)
    
    def take_screenshot(self, path: str) -> bool:
        """
        截图保存
        
        Args:
            path: 截图保存路径
            
        Returns:
            bool: 截图成功返回True
        """
        try:
            if self.page:
                self.page.screenshot(path=path)
                return True
            return False
        except Exception as e:
            self.log(f"❌ 截图失败: {str(e)}", "ERROR")
            return False
    
    def cleanup(self):
        """清理资源"""
        try:
            self.log("🧹 清理浏览器资源...")
            
            if self.context:
                self.context.close()
                self.context = None
                
            if self.browser:
                self.browser.close()
                self.browser = None
                
            self.page = None
            self.is_logged_in = False
            
            self.log("✅ 浏览器资源清理完成")
            
        except Exception as e:
            self.log(f"⚠️ 清理资源时发生错误: {str(e)}", "ERROR")
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.cleanup()