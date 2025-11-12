"""
PEDA自动化处理工具 - UI组件模块
包含所有界面组件的创建和管理功能
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
from .languages import get_text


class UIComponentManager:
    """UI组件管理器 - 负责创建和管理所有界面组件"""
    
    def __init__(self, parent_app):
        """
        初始化UI组件管理器
        
        Args:
            parent_app: 父应用程序实例（PEDAAutomationGUI）
        """
        self.app = parent_app
        self.root = parent_app.root
        self.colors = parent_app.colors
        
    def create_main_container(self):
        """创建主容器"""
        self.app.main_container = tk.Frame(self.root, bg=self.colors['white'])
        self.app.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
    def create_header(self):
        """创建现代化顶部标题栏"""
        header_frame = tk.Frame(self.app.main_container, bg=self.colors['primary'], height=70)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        header_frame.pack_propagate(False)
        
        # 左侧标题区域
        title_container = tk.Frame(header_frame, bg=self.colors['primary'])
        title_container.pack(side=tk.LEFT, fill=tk.Y, padx=25, pady=10)
        
        title_label = tk.Label(title_container, 
                              text="PEDA Automation Tool",
                              bg=self.colors['primary'],
                              fg=self.colors['white'],
                              font=('微软雅黑', 18, 'bold'))
        title_label.pack(anchor='w')
        
        subtitle_label = tk.Label(title_container, 
                                 text="Automated Document Processing v1.0",
                                 bg=self.colors['primary'],
                                 fg=self.colors['primary_pale'],
                                 font=('微软雅黑', 10))
        subtitle_label.pack(anchor='w', pady=(2, 0))
        
        # 右侧语言切换区域
        lang_container = tk.Frame(header_frame, bg=self.colors['primary'])
        lang_container.pack(side=tk.RIGHT, fill=tk.Y, padx=25, pady=15)
        
        tk.Label(lang_container, text="Language:", 
                bg=self.colors['primary'], fg=self.colors['primary_pale'],
                font=('微软雅黑', 9)).pack(anchor='e')
        
        lang_frame = tk.Frame(lang_container, bg=self.colors['primary'])
        lang_frame.pack(anchor='e', pady=(5, 0))
        
        # 语言切换按钮 - 使用新的色彩系统
        self.app.en_btn = tk.Button(lang_frame, text="English", 
                               bg=self.colors['primary_pale'], fg=self.colors['primary'],
                               font=('微软雅黑', 9),
                               relief='flat', padx=12, pady=4,
                               cursor='hand2',
                               command=lambda: self.app.switch_language('en'))
        self.app.en_btn.pack(side=tk.LEFT, padx=(0, 2))
        
        self.app.de_btn = tk.Button(lang_frame, text="Deutsch", 
                               bg=self.colors['primary_pale'], fg=self.colors['primary'],
                               font=('微软雅黑', 9),
                               relief='flat', padx=12, pady=4,
                               cursor='hand2',
                               command=lambda: self.app.switch_language('de'))
        self.app.de_btn.pack(side=tk.LEFT, padx=(2, 2))
        
        self.app.zh_btn = tk.Button(lang_frame, text="中文", 
                               bg=self.colors['white'], fg=self.colors['primary'],
                               font=('微软雅黑', 9, 'bold'),
                               relief='flat', padx=12, pady=4,
                               cursor='hand2',
                               command=lambda: self.app.switch_language('zh'))
        self.app.zh_btn.pack(side=tk.LEFT, padx=(2, 0))

    def create_content_area(self):
        """创建内容区域"""
        self.app.notebook = ttk.Notebook(self.app.main_container)
        self.app.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 主要配置页面
        self.app.main_tab = tk.Frame(self.app.notebook, bg=self.colors['white'])
        self.app.notebook.add(self.app.main_tab, text="Main")
        self.create_main_tab_content()
        
        # 日志页面
        self.app.log_tab = tk.Frame(self.app.notebook, bg=self.colors['white'])
        self.app.notebook.add(self.app.log_tab, text="Logs")
        self.create_log_tab_content()
        
    def create_main_tab_content(self):
        """创建主页面内容"""
        # 直接在主页面创建内容，不使用滚动区域
        content_frame = tk.Frame(self.app.main_tab, bg=self.colors['white'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=5)
        
        # 创建各个区域，优化间距
        self.create_login_section(content_frame)
        self.create_file_selection_section(content_frame)
        self.create_operation_control_section(content_frame)
        self.create_progress_section(content_frame)
        self.create_record_management_section(content_frame)
        
    def create_login_section(self, parent):
        """创建登录信息区域"""
        self.app.login_frame = ttk.LabelFrame(parent, text="🔐 Login Information", 
                                         style='Title.TLabelframe', padding=15)
        self.app.login_frame.pack(fill=tk.X, pady=(0, 10))
        
        login_grid = tk.Frame(self.app.login_frame, bg=self.colors['neutral_100'])
        login_grid.pack(fill=tk.X)
        
        # 登录网址输入（移到最上面）
        self.app.login_url_label = tk.Label(login_grid, text="登录网址", 
                bg=self.colors['neutral_100'], fg=self.colors['neutral_700'],
                font=('微软雅黑', 9, 'bold'))
        self.app.login_url_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 8), padx=(0, 10))

        login_url_frame = tk.Frame(login_grid, bg=self.colors['neutral_100'])
        login_url_frame.grid(row=0, column=1, sticky=tk.W+tk.E, pady=(0, 8))

        self.app.login_url_entry = tk.Entry(login_url_frame, textvariable=self.app.login_url_var, 
                                      font=('微软雅黑', 9), width=50, relief='solid',
                                      borderwidth=1, bg=self.colors['white'],
                                      fg=self.colors['neutral_700'],
                                      highlightbackground=self.colors['neutral_300'],
                                      highlightcolor=self.colors['primary_light'])
        self.app.login_url_entry.pack(fill=tk.X, ipady=4)

        # 用户名输入
        self.app.username_label = tk.Label(login_grid, text=get_text(self.app.current_language, 'username'), 
                bg=self.colors['neutral_100'], fg=self.colors['neutral_700'],
                font=('微软雅黑', 9, 'bold'))
        self.app.username_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 8), padx=(0, 10))
        username_frame = tk.Frame(login_grid, bg=self.colors['neutral_100'])
        username_frame.grid(row=1, column=1, sticky=tk.W+tk.E, pady=(0, 8))
        self.app.username_entry = tk.Entry(username_frame, textvariable=self.app.username_var, 
                                      font=('微软雅黑', 9), width=30, relief='solid',
                                      borderwidth=1, bg=self.colors['white'],
                                      fg=self.colors['neutral_700'],
                                      highlightbackground=self.colors['neutral_300'],
                                      highlightcolor=self.colors['primary_light'])
        self.app.username_entry.pack(fill=tk.X, ipady=4)
        
        # 密码输入
        self.app.password_label = tk.Label(login_grid, text=get_text(self.app.current_language, 'password'), 
                bg=self.colors['neutral_100'], fg=self.colors['neutral_700'],
                font=('微软雅黑', 9, 'bold'))
        self.app.password_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 8), padx=(0, 10))
        
        password_frame = tk.Frame(login_grid, bg=self.colors['neutral_100'])
        password_frame.grid(row=2, column=1, sticky=tk.W+tk.E, pady=(0, 8))
        
        self.app.password_entry = tk.Entry(password_frame, textvariable=self.app.password_var, 
                                      show="*", font=('微软雅黑', 9), width=30, 
                                      relief='solid', borderwidth=1, bg=self.colors['white'],
                                      fg=self.colors['neutral_700'],
                                      highlightbackground=self.colors['neutral_300'],
                                      highlightcolor=self.colors['primary_light'])
        self.app.password_entry.pack(fill=tk.X, ipady=4)
        
        # 选项行
        options_frame = tk.Frame(login_grid, bg=self.colors['neutral_100'])
        options_frame.grid(row=3, column=0, columnspan=3, sticky=tk.W+tk.E, pady=(10, 0))
        
        # 左侧选项
        left_options = tk.Frame(options_frame, bg=self.colors['neutral_100'])
        left_options.pack(side=tk.LEFT)
        
        self.app.remember_cb = tk.Checkbutton(left_options, text=get_text(self.app.current_language, 'remember_password'),
                                         variable=self.app.remember_password_var,
                                         bg=self.colors['neutral_100'], fg=self.colors['neutral_600'],
                                         font=('微软雅黑', 9), activebackground=self.colors['neutral_100'],
                                         selectcolor=self.colors['white'])
        self.app.remember_cb.pack(side=tk.LEFT, padx=(0, 15))
        
        self.app.show_password_cb = tk.Checkbutton(left_options, text=get_text(self.app.current_language, 'show_password'),
                                                  variable=self.app.show_password_var,
                                                  bg=self.colors['neutral_100'], fg=self.colors['neutral_600'],
                                                  font=('微软雅黑', 9), activebackground=self.colors['neutral_100'],
                                                  selectcolor=self.colors['white'],
                                                  command=self.app.toggle_password_visibility)
        self.app.show_password_cb.pack(side=tk.LEFT)
        
        # 登录按钮 - 统一按钮样式，设置固定宽度
        self.app.save_settings_btn = tk.Button(options_frame, text=get_text(self.app.current_language, 'login'),
                                          font=('微软雅黑', 9, 'bold'), 
                                          bg=self.colors['primary'],
                                          fg=self.colors['white'], relief='flat',
                                          padx=20, pady=8, cursor='hand2',
                                          command=self.app.save_config,
                                          activebackground=self.colors['primary_light'],
                                          height=1, width=15)
        self.app.save_settings_btn.pack(side=tk.RIGHT)
        
        login_grid.columnconfigure(1, weight=1)
        
    def create_file_selection_section(self, parent):
        """创建文件选择区域"""
        self.app.file_frame = ttk.LabelFrame(parent, text=get_text(self.app.current_language, 'file_selection'), 
                                        style='Title.TLabelframe', padding=15)
        self.app.file_frame.pack(fill=tk.X, pady=(0, 8))
        
        file_grid = tk.Frame(self.app.file_frame, bg=self.colors['neutral_100'])
        file_grid.pack(fill=tk.X)
        
        # Excel文件选择
        self.app.excel_file_label = tk.Label(file_grid, text=get_text(self.app.current_language, 'excel_file'), 
                bg=self.colors['neutral_100'], fg=self.colors['neutral_700'],
                font=('微软雅黑', 9, 'bold'))
        self.app.excel_file_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 6), padx=(0, 10))
        
        excel_frame = tk.Frame(file_grid, bg=self.colors['neutral_100'])
        excel_frame.grid(row=0, column=1, sticky=tk.W+tk.E, pady=(0, 6))
        
        self.app.excel_entry = tk.Entry(excel_frame, textvariable=self.app.excel_file_var, 
                                   font=('微软雅黑', 9), state='readonly',
                                   relief='solid', borderwidth=1, bg=self.colors['neutral_50'],
                                   fg=self.colors['neutral_600'])
        self.app.excel_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        
        self.app.excel_btn = tk.Button(excel_frame, text=get_text(self.app.current_language, 'choose_file'),
                                  font=('微软雅黑', 9, 'bold'), bg=self.colors['primary'],
                                  fg=self.colors['white'], relief='flat',
                                  padx=20, pady=8, cursor='hand2',
                                  command=self.app.choose_excel_file,
                                  activebackground=self.colors['primary_light'],
                                  height=1, width=15)
        self.app.excel_btn.pack(side=tk.RIGHT, padx=(8, 0))
        
        # 文档路径选择
        self.app.document_path_label = tk.Label(file_grid, text=get_text(self.app.current_language, 'document_path'),
                bg=self.colors['neutral_100'], fg=self.colors['neutral_700'],
                font=('微软雅黑', 9, 'bold'))
        self.app.document_path_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 6), padx=(0, 10))
        
        document_frame = tk.Frame(file_grid, bg=self.colors['neutral_100'])
        document_frame.grid(row=1, column=1, sticky=tk.W+tk.E, pady=(0, 6))
        
        self.app.document_entry = tk.Entry(document_frame, textvariable=self.app.document_path_var, 
                                      font=('微软雅黑', 9), state='readonly',
                                      relief='solid', borderwidth=1, bg=self.colors['neutral_50'],
                                      fg=self.colors['neutral_600'])
        self.app.document_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        
        self.app.document_btn = tk.Button(document_frame, text=get_text(self.app.current_language, 'choose_folder'),
                                     font=('微软雅黑', 9, 'bold'), bg=self.colors['primary'],
                                     fg=self.colors['white'], relief='flat',
                                     padx=20, pady=8, cursor='hand2',
                                     command=self.app.choose_document_folder,
                                     activebackground=self.colors['primary_light'],
                                     height=1, width=15)
        self.app.document_btn.pack(side=tk.RIGHT, padx=(8, 0))
        
        file_grid.columnconfigure(1, weight=1)
        
    def create_operation_control_section(self, parent):
        """创建操作控制区域"""
        self.app.control_frame = ttk.LabelFrame(parent, text=get_text(self.app.current_language, 'operation_control'), 
                                          style='Title.TLabelframe', padding=15)
        self.app.control_frame.pack(fill=tk.X, pady=(0, 8))
        
        button_container = tk.Frame(self.app.control_frame, bg=self.colors['neutral_100'])
        button_container.pack(fill=tk.X)
        
        # 计算按钮宽度 - 三等分减去间距
        button_width = 25  # 固定宽度，确保等宽
        btn_font = ('微软雅黑', 10, 'bold')
        btn_padx = 10
        btn_pady = 8

        # 三等分按钮布局 - 使用固定宽度
        self.app.start_btn = tk.Button(button_container, text=get_text(self.app.current_language, 'start_processing'),
                                       command=self.app.run_processing,
                                       font=btn_font,
                                       bg=self.colors['primary'], fg=self.colors['white'],
                                       relief='flat', padx=btn_padx, pady=btn_pady, cursor='hand2',
                                       activebackground=self.colors['primary_dark'],
                                       activeforeground=self.colors['white'],
                                       height=1, width=button_width)
        self.app.start_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.app.stop_btn = tk.Button(button_container, text=get_text(self.app.current_language, 'stop_processing'),
                                 font=btn_font, bg=self.colors['danger'],
                                 fg=self.colors['white'], relief='flat',
                                 padx=btn_padx, pady=btn_pady, cursor='hand2',
                                 command=self.app.stop_processing,
                                 state='disabled',
                                 activebackground=self.colors['danger_light'],
                                 height=1, width=button_width)
        self.app.stop_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))

        self.app.reset_btn = tk.Button(button_container, text=get_text(self.app.current_language, 'reset'),
                                  font=btn_font, bg=self.colors['warning'],
                                  fg=self.colors['white'], relief='flat',
                                  padx=btn_padx, pady=btn_pady, cursor='hand2',
                                  command=self.app.reset_processing,
                                  activebackground=self.colors['warning_light'],
                                  height=1, width=button_width)
        self.app.reset_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
    def create_progress_section(self, parent):
        """创建进度显示区域"""
        self.app.progress_frame = ttk.LabelFrame(parent, text=get_text(self.app.current_language, 'processing_status'), 
                                           style='Title.TLabelframe', padding=12)
        self.app.progress_frame.pack(fill=tk.X, pady=(0, 8))
        
        # 进度条
        progress_container = tk.Frame(self.app.progress_frame, bg=self.colors['neutral_100'])
        progress_container.pack(fill=tk.X, pady=(0, 6))
        
        self.app.total_progress_label = tk.Label(progress_container, text=get_text(self.app.current_language, 'total_progress'), 
                bg=self.colors['neutral_100'], fg=self.colors['neutral_700'],
                font=('微软雅黑', 9, 'bold'))
        self.app.total_progress_label.pack(side=tk.LEFT)
        
        self.app.progress_bar = ttk.Progressbar(progress_container, variable=self.app.progress_var,
                                          maximum=100, style='Custom.Horizontal.TProgressbar')
        self.app.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 8))
        
        self.app.progress_label = tk.Label(progress_container, text="0%", 
                                      bg=self.colors['neutral_100'], fg=self.colors['neutral_700'],
                                      font=('微软雅黑', 9, 'bold'))
        self.app.progress_label.pack(side=tk.RIGHT)
        
        # 状态统计
        stats_frame = tk.Frame(self.app.progress_frame, bg=self.colors['neutral_100'])
        stats_frame.pack(fill=tk.X)
        
        self.app.stats_labels = {}
        self.app.stats_text_labels = {}
        stats = [('success', 'success'), ('failed', 'failed'), ('total', 'total')]
        for i, (key, text_key) in enumerate(stats):
            frame = tk.Frame(stats_frame, bg=self.colors['neutral_100'])
            frame.pack(side=tk.LEFT, padx=(0, 15))
            
            self.app.stats_text_labels[key] = tk.Label(frame, text=get_text(self.app.current_language, text_key), 
                                                      bg=self.colors['neutral_100'], 
                                                      fg=self.colors['neutral_600'],
                                                      font=('微软雅黑', 9))
            self.app.stats_text_labels[key].pack(side=tk.LEFT)
            
            self.app.stats_labels[key] = tk.Label(frame, text="0", 
                                             bg=self.colors['neutral_100'], 
                                             fg=self.colors['neutral_700'],
                                             font=('微软雅黑', 9, 'bold'))
            self.app.stats_labels[key].pack(side=tk.LEFT, padx=(3, 0))
        
        # 当前状态
        status_frame = tk.Frame(self.app.progress_frame, bg=self.colors['neutral_100'])
        status_frame.pack(fill=tk.X, pady=(6, 0))
        
        self.app.current_label = tk.Label(status_frame, text=get_text(self.app.current_language, 'current_status'), 
                                         bg=self.colors['neutral_100'], fg=self.colors['neutral_600'],
                                         font=('微软雅黑', 9))
        self.app.current_label.pack(side=tk.LEFT)
        
        self.app.status_label = tk.Label(status_frame, textvariable=self.app.current_status_var,
                                    bg=self.colors['neutral_100'], fg=self.colors['primary'],
                                    font=('微软雅黑', 9, 'bold'))
        self.app.status_label.pack(side=tk.LEFT, padx=(3, 0))
        
    def create_record_management_section(self, parent):
        """创建记录管理区域"""
        self.app.record_frame = ttk.LabelFrame(parent, text=get_text(self.app.current_language, 'record_management'), 
                                         style='Title.TLabelframe', padding=12)
        self.app.record_frame.pack(fill=tk.X, pady=(0, 5))
        
        download_frame = tk.Frame(self.app.record_frame, bg=self.colors['neutral_100'])
        download_frame.pack(fill=tk.X)
        
        # 固定宽度，确保等宽
        button_width = 25
        
        # 三等分按钮布局 - 使用固定宽度
        self.app.download_report_btn = tk.Button(download_frame, text="文件上传报告",
                                               font=('微软雅黑', 9, 'bold'), bg=self.colors['secondary'],
                                               fg=self.colors['white'], relief='flat',
                                               pady=8, cursor='hand2', 
                                               command=self.app.download_report,
                                               activebackground=self.colors['secondary_light'],
                                               height=1, width=button_width)
        self.app.download_report_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.app.download_error_btn = tk.Button(download_frame, text=get_text(self.app.current_language, 'download_error_log'),
                                              font=('微软雅黑', 9, 'bold'), bg=self.colors['secondary'],
                                              fg=self.colors['white'], relief='flat',
                                              pady=8, cursor='hand2', 
                                              command=self.app.download_error_log,
                                              activebackground=self.colors['secondary_light'],
                                              height=1, width=button_width)
        self.app.download_error_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        
        self.app.download_upload_btn = tk.Button(download_frame, text=get_text(self.app.current_language, 'download_upload_record'),
                                               font=('微软雅黑', 9, 'bold'), bg=self.colors['secondary'],
                                               fg=self.colors['white'], relief='flat',
                                               pady=8, cursor='hand2', 
                                               command=self.app.download_upload_record,
                                               activebackground=self.colors['secondary_light'],
                                               height=1, width=button_width)
        self.app.download_upload_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
    def create_log_tab_content(self):
        """创建日志页面内容"""
        log_container = tk.Frame(self.app.log_tab, bg=self.colors['white'])
        log_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 日志控制栏
        log_control = tk.Frame(log_container, bg=self.colors['white'])
        log_control.pack(fill=tk.X, pady=(0, 10))
        
        self.app.log_title_label = tk.Label(log_control, text=get_text(self.app.current_language, 'log_output'), 
                bg=self.colors['white'], font=('微软雅黑', 12, 'bold'))
        self.app.log_title_label.pack(side=tk.LEFT)
        
        self.app.clear_log_btn = tk.Button(log_control, text=get_text(self.app.current_language, 'clear_log'),
                 font=('微软雅黑', 9), bg=self.colors['danger'],
                 fg=self.colors['white'], relief='flat',
                 padx=15, pady=5, command=self.app.clear_log)
        self.app.clear_log_btn.pack(side=tk.RIGHT)
        
        # 日志文本区域
        log_frame = tk.Frame(log_container, bg=self.colors['white'], relief='solid', bd=1)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.app.log_text = tk.Text(log_frame, font=('微软雅黑', 9), 
                               bg=self.colors['white'], fg=self.colors['dark'],
                               wrap=tk.WORD, state='disabled')
        
        log_scrollbar = ttk.Scrollbar(log_frame, command=self.app.log_text.yview)
        self.app.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.app.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_status_bar(self):
        """创建状态栏"""
        self.app.status_bar = tk.Frame(self.root, bg=self.colors['light'], height=25)
        self.app.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        self.app.status_bar.pack_propagate(False)
        
        self.app.status_text = tk.Label(self.app.status_bar, text=get_text(self.app.current_language, 'ready'), 
                                   bg=self.colors['light'], fg=self.colors['dark'],
                                   font=('微软雅黑', 9))
        self.app.status_text.pack(side=tk.LEFT, padx=10, pady=3)
        
        # 时间显示
        self.app.time_label = tk.Label(self.app.status_bar, text="", 
                                  bg=self.colors['light'], fg=self.colors['dark'],
                                  font=('微软雅黑', 9))
        self.app.time_label.pack(side=tk.RIGHT, padx=10, pady=3)

    def save_login_info(self):
        """保存登录信息到配置文件"""
        if hasattr(self.app, 'save_config'):
            self.app.save_config()
            tk.messagebox.showinfo("保存成功", "登录信息已保存，下次将自动填充。")