"""
浏览器自动查找模块
负责在系统中查找可用的浏览器（Chrome、Edge等）
"""

import os
import platform
from typing import Optional, Tuple
from pathlib import Path


class BrowserFinder:
    """浏览器查找器 - 自动查找系统中的浏览器"""
    
    # Windows 常见浏览器路径
    WINDOWS_CHROME_PATHS = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    
    WINDOWS_EDGE_PATHS = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    
    def __init__(self, log_callback=None):
        """
        初始化浏览器查找器
        
        Args:
            log_callback: 日志回调函数，用于输出查找过程信息
        """
        self.log_callback = log_callback
        self._cached_browser_path = None
        self._cached_browser_type = None
    
    def log(self, message: str, level: str = "INFO"):
        """记录日志"""
        if self.log_callback:
            self.log_callback(message, level)
        else:
            print(f"[{level}] {message}")
    
    def find_browser(self, preferred_browser: Optional[str] = None, 
                     custom_path: Optional[str] = None) -> Tuple[Optional[str], Optional[str]]:
        """
        查找可用的浏览器
        
        优先级：
        1. 自定义路径（如果提供且有效）
        2. 环境变量 PEDA_BROWSER_PATH
        3. 注册表查找（Windows）
        4. 常见安装路径探测
        5. Playwright 内置浏览器
        
        Args:
            preferred_browser: 首选浏览器类型 ("chrome", "msedge", "auto")
            custom_path: 自定义浏览器路径
            
        Returns:
            Tuple[浏览器可执行路径, 浏览器类型] 或 (None, None) 如果未找到
        """
        # 如果已缓存，直接返回
        if self._cached_browser_path and self._cached_browser_type:
            self.log(f"使用缓存的浏览器: {self._cached_browser_type} - {self._cached_browser_path}")
            return self._cached_browser_path, self._cached_browser_type
        
        self.log("🔍 开始查找系统浏览器...")
        
        # 1. 检查自定义路径
        if custom_path:
            if self._validate_browser_path(custom_path):
                browser_type = self._identify_browser_type(custom_path)
                self.log(f"✅ 使用自定义浏览器: {browser_type} - {custom_path}")
                self._cache_result(custom_path, browser_type)
                return custom_path, browser_type
            else:
                self.log(f"⚠️ 自定义浏览器路径无效: {custom_path}", "WARNING")
        
        # 2. 检查环境变量
        env_path = os.environ.get('PEDA_BROWSER_PATH')
        if env_path:
            if self._validate_browser_path(env_path):
                browser_type = self._identify_browser_type(env_path)
                self.log(f"✅ 使用环境变量指定的浏览器: {browser_type} - {env_path}")
                self._cache_result(env_path, browser_type)
                return env_path, browser_type
            else:
                self.log(f"⚠️ 环境变量中的浏览器路径无效: {env_path}", "WARNING")
        
        # 3. 根据首选项查找
        if preferred_browser and preferred_browser.lower() != "auto":
            result = self._find_specific_browser(preferred_browser.lower())
            if result:
                self._cache_result(result[0], result[1])
                return result
        
        # 4. 自动查找（优先 Chrome，然后 Edge）
        result = self._auto_find_browser()
        if result:
            self._cache_result(result[0], result[1])
            return result
        
        self.log("❌ 未找到可用的浏览器", "ERROR")
        return None, None
    
    def _find_specific_browser(self, browser_type: str) -> Optional[Tuple[str, str]]:
        """
        查找特定类型的浏览器
        
        Args:
            browser_type: "chrome" 或 "msedge"
            
        Returns:
            (浏览器路径, 浏览器类型) 或 None
        """
        if browser_type == "chrome":
            return self._find_chrome()
        elif browser_type in ("edge", "msedge"):
            return self._find_edge()
        return None
    
    def _auto_find_browser(self) -> Optional[Tuple[str, str]]:
        """
        自动查找浏览器（优先 Chrome）
        
        Returns:
            (浏览器路径, 浏览器类型) 或 None
        """
        self.log("自动查找浏览器（优先级: Chrome > Edge）...")
        
        # 先尝试 Chrome
        result = self._find_chrome()
        if result:
            return result
        
        # 再尝试 Edge
        result = self._find_edge()
        if result:
            return result
        
        return None
    
    def _find_chrome(self) -> Optional[Tuple[str, str]]:
        """
        查找 Chrome 浏览器
        
        Returns:
            (Chrome路径, "chrome") 或 None
        """
        self.log("正在查找 Chrome 浏览器...")
        
        if platform.system() == "Windows":
            # 方法1: 尝试从注册表读取
            chrome_path = self._get_chrome_from_registry()
            if chrome_path and self._validate_browser_path(chrome_path):
                self.log(f"✅ 从注册表找到 Chrome: {chrome_path}")
                return chrome_path, "chrome"
            
            # 方法2: 尝试常见安装路径
            for path in self.WINDOWS_CHROME_PATHS:
                if self._validate_browser_path(path):
                    self.log(f"✅ 从常见路径找到 Chrome: {path}")
                    return path, "chrome"
        
        self.log("⚠️ 未找到 Chrome 浏览器", "WARNING")
        return None
    
    def _find_edge(self) -> Optional[Tuple[str, str]]:
        """
        查找 Edge 浏览器
        
        Returns:
            (Edge路径, "msedge") 或 None
        """
        self.log("正在查找 Edge 浏览器...")
        
        if platform.system() == "Windows":
            # 方法1: 尝试从注册表读取
            edge_path = self._get_edge_from_registry()
            if edge_path and self._validate_browser_path(edge_path):
                self.log(f"✅ 从注册表找到 Edge: {edge_path}")
                return edge_path, "msedge"
            
            # 方法2: 尝试常见安装路径
            for path in self.WINDOWS_EDGE_PATHS:
                if self._validate_browser_path(path):
                    self.log(f"✅ 从常见路径找到 Edge: {path}")
                    return path, "msedge"
        
        self.log("⚠️ 未找到 Edge 浏览器", "WARNING")
        return None
    
    def _get_chrome_from_registry(self) -> Optional[str]:
        """
        从 Windows 注册表获取 Chrome 路径
        
        Returns:
            Chrome 路径或 None
        """
        if platform.system() != "Windows":
            return None
        
        try:
            import winreg
            
            # 尝试从 HKEY_LOCAL_MACHINE
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"
                )
                chrome_path, _ = winreg.QueryValueEx(key, "")
                winreg.CloseKey(key)
                return chrome_path
            except FileNotFoundError:
                pass
            
            # 尝试从 HKEY_CURRENT_USER
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"
                )
                chrome_path, _ = winreg.QueryValueEx(key, "")
                winreg.CloseKey(key)
                return chrome_path
            except FileNotFoundError:
                pass
            
        except Exception as e:
            self.log(f"读取注册表时出错: {e}", "WARNING")
        
        return None
    
    def _get_edge_from_registry(self) -> Optional[str]:
        """
        从 Windows 注册表获取 Edge 路径
        
        Returns:
            Edge 路径或 None
        """
        if platform.system() != "Windows":
            return None
        
        try:
            import winreg
            
            # 尝试从 HKEY_LOCAL_MACHINE
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe"
                )
                edge_path, _ = winreg.QueryValueEx(key, "")
                winreg.CloseKey(key)
                return edge_path
            except FileNotFoundError:
                pass
            
            # 尝试从 HKEY_CURRENT_USER
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe"
                )
                edge_path, _ = winreg.QueryValueEx(key, "")
                winreg.CloseKey(key)
                return edge_path
            except FileNotFoundError:
                pass
            
        except Exception as e:
            self.log(f"读取注册表时出错: {e}", "WARNING")
        
        return None
    
    def _validate_browser_path(self, path: str) -> bool:
        """
        验证浏览器路径是否有效
        
        Args:
            path: 浏览器可执行文件路径
            
        Returns:
            路径有效返回 True
        """
        if not path:
            return False
        
        path_obj = Path(path)
        return path_obj.exists() and path_obj.is_file()
    
    def _identify_browser_type(self, path: str) -> str:
        """
        根据路径识别浏览器类型
        
        Args:
            path: 浏览器路径
            
        Returns:
            浏览器类型标识
        """
        path_lower = path.lower()
        if "chrome.exe" in path_lower:
            return "chrome"
        elif "msedge.exe" in path_lower:
            return "msedge"
        else:
            return "unknown"
    
    def _cache_result(self, path: str, browser_type: str):
        """
        缓存查找结果
        
        Args:
            path: 浏览器路径
            browser_type: 浏览器类型
        """
        self._cached_browser_path = path
        self._cached_browser_type = browser_type
    
    def clear_cache(self):
        """清除缓存的浏览器信息"""
        self._cached_browser_path = None
        self._cached_browser_type = None
        self.log("已清除浏览器缓存")
    
    def get_browser_info(self) -> dict:
        """
        获取当前浏览器信息
        
        Returns:
            包含浏览器信息的字典
        """
        return {
            "path": self._cached_browser_path,
            "type": self._cached_browser_type,
            "is_cached": bool(self._cached_browser_path)
        }
