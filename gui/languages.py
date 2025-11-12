"""
PEDA自动化处理工具 - 多语言配置模块
支持英语、德语和中文三语言切换
"""

# 多语言配置字典
LANGUAGES = {
    'en': {
        'title': 'PEDA Automation Tool v1.0',
        'app_title': 'PEDA Automation Tool',
        'app_subtitle': 'Automated Document Processing v1.0',
        'language_label': 'Language:',
        'login_info': '🔐 Login Information',
        'username': 'Username:',
        'password': 'Password:',
        'login': '🔐 Login',
        'login_url': 'Login URL:',
        'save_settings': 'Save',
        'remember_password': 'Remember Password',
        'show_password': 'Show Password',
        'file_selection': '📁 File Selection',
        'excel_file': 'Excel File:',
        'document_path': 'Document Path:',
        'choose_file': '📄 Choose File...',
        'choose_folder': '📁 Choose Folder...',
        'system_settings': '🌐 System Settings',
        'ui_language': 'UI Language:',
        'system_language': 'System Language (after login):',
        'operation_control': '⚡ Operation Control',
        'start_processing': '▶️ Start Processing',
        'pause_processing': 'Pause Processing',
        'stop_processing': '⏹️ Stop',
        'reset': '🔄 Reset',
        'total_progress': 'Total Progress:',
        'current_status': 'Current:',
        'processing_status': '📊 Processing Status',
        'success': 'Success:',
        'failed': 'Failed:',
        'skipped': 'Skipped:',
        'total': 'Total:',
        'log_output': '📝 Log Output',
        'clear_log': 'Clear Log',
        'record_management': '💾 Record Management',
        'download_report': 'Download Report',
        'download_error_log': 'Download Error Log',
        'download_upload_record': 'Download Upload Record',
        'main_tab': 'Main',
        'logs_tab': 'Logs',
        'validate_inputs': 'Please fill in all required fields',
        'processing_complete': 'Processing Complete',
        'processing_started': 'Processing Started',
        'select_excel_first': 'Please select an Excel file first',
        'select_document_path': 'Please select document path first',
        'enter_credentials': 'Please enter username and password',
        'ready': 'Ready',
        'processing': 'Processing...',
        'idle': 'Idle',
        'processing_stopped': 'Processing stopped by user',
        'processing_reset': 'Processing reset',
        'error_occurred': 'Error occurred during processing',
        'processing_exception': 'Exception occurred during processing',
        'save_login': '💾 Save',
        'config_saved': 'Configuration saved'
    },
    'de': {
        'title': 'PEDA Automatisierungstool v1.0',
        'app_title': 'PEDA Automatisierungstool',
        'app_subtitle': 'Automatisierte Dokumentenverarbeitung v1.0',
        'language_label': 'Sprache:',
        'login_info': '🔐 Anmeldeinformationen',
        'username': 'Benutzername:',
        'password': 'Passwort:',
        'login': '🔐 Anmelden',
        'login_url': 'Anmelde-URL:',
        'save_settings': 'Speichern',
        'remember_password': 'Passwort merken',
        'show_password': 'Passwort anzeigen',
        'file_selection': '📁 Dateiauswahl',
        'excel_file': 'Excel-Datei:',
        'document_path': 'Dokumentenpfad:',
        'choose_file': '📄 Datei wählen...',
        'choose_folder': '📁 Ordner wählen...',
        'system_settings': '🌐 Systemeinstellungen',
        'ui_language': 'Oberflächensprache:',
        'system_language': 'Systemsprache (nach Anmeldung):',
        'operation_control': '⚡ Bediensteuerung',
        'start_processing': '▶️ Verarbeitung starten',
        'pause_processing': 'Verarbeitung pausieren',
        'stop_processing': '⏹️ Stoppen',
        'reset': '🔄 Zurücksetzen',
        'total_progress': 'Gesamtfortschritt:',
        'current_status': 'Aktuell:',
        'processing_status': '📊 Verarbeitungsstatus',
        'success': 'Erfolgreich:',
        'failed': 'Fehlgeschlagen:',
        'skipped': 'Übersprungen:',
        'total': 'Gesamt:',
        'log_output': '📝 Protokollausgabe',
        'clear_log': 'Protokoll löschen',
        'record_management': '💾 Datensatzverwaltung',
        'download_report': 'Bericht herunterladen',
        'download_error_log': 'Fehlerprotokoll herunterladen',
        'download_upload_record': 'Upload-Datensatz herunterladen',
        'main_tab': 'Haupt',
        'logs_tab': 'Logs',
        'validate_inputs': 'Bitte füllen Sie alle erforderlichen Felder aus',
        'processing_complete': 'Verarbeitung abgeschlossen',
        'processing_started': 'Verarbeitung gestartet',
        'select_excel_first': 'Bitte wählen Sie zuerst eine Excel-Datei',
        'select_document_path': 'Bitte wählen Sie zuerst den Dokumentenpfad',
        'enter_credentials': 'Bitte geben Sie Benutzername und Passwort ein',
        'ready': 'Bereit',
        'processing': 'Verarbeitung...',
        'idle': 'Leerlauf',
        'processing_stopped': 'Verarbeitung durch Benutzer gestoppt',
        'processing_reset': 'Verarbeitung zurückgesetzt',
        'error_occurred': 'Fehler während der Verarbeitung aufgetreten',
        'processing_exception': 'Fehler während der Verarbeitung aufgetreten',
        'save_login': '💾 Login speichern',
        'config_saved': 'Konfiguration gespeichert'
    },
    'zh': {
        'title': 'PEDA 自动化处理工具 v1.0',
        'app_title': 'PEDA 自动化处理工具',
        'app_subtitle': '自动化文档处理 v1.0',
        'language_label': '语言:',
        'login_info': '🔐 登录信息',
        'username': '用户名:',
        'password': '密码:',
        'login': '💾 保存',
        'login_url': '登录网址',
        'save_settings': '保存',
        'remember_password': '记住密码',
        'show_password': '显示密码',
        'file_selection': '📁 文件选择',
        'excel_file': 'Excel文件:',
        'document_path': '文档路径:',
        'choose_file': '📄 选择文件...',
        'choose_folder': '📁 选择文件夹...',
        'system_settings': '🌐 系统设置',
        'ui_language': '界面语言:',
        'system_language': '系统语言 (登录后):',
        'operation_control': '⚡ 操作控制',
        'start_processing': '▶️ 开始',
        'pause_processing': '暂停处理',
        'stop_processing': '⏹️ 停止',
        'reset': '🔄 重置',
        'total_progress': '总进度:',
        'current_status': '当前状态:',
        'processing_status': '📊 处理状态',
        'success': '成功:',
        'failed': '失败:',
        'skipped': '跳过:',
        'total': '总计:',
        'log_output': '📝 日志输出',
        'clear_log': '清空日志',
        'record_management': '💾 记录管理',
        'download_report': '文件上传报告',
        'download_error_log': '下载错误日志',
        'download_upload_record': '下载上传记录',
        'main_tab': '主页',
        'logs_tab': '日志',
        'validate_inputs': '请填写所有必需字段',
        'processing_complete': '处理完成',
        'processing_started': '开始处理',
        'select_excel_first': '请先选择Excel文件',
        'select_document_path': '请先选择文档路径',
        'enter_credentials': '请输入用户名和密码',
        'ready': '就绪',
        'processing': '处理中...',
        'idle': '空闲',
        'processing_stopped': '处理被用户停止',
        'processing_reset': '处理重置',
        'error_occurred': '处理期间发生错误',
        'processing_exception': '处理期间发生异常',
        'save_login': '💾 登录信息保存',
        'config_saved': '配置已保存'
    }
}

def get_text(language_code, key, default=None):
    """
    获取指定语言的文本
    
    Args:
        language_code (str): 语言代码 ('en', 'de', 'zh')
        key (str): 文本键名
        default (str, optional): 默认值，如果未找到则返回此值
    
    Returns:
        str: 对应的文本内容
    """
    if language_code not in LANGUAGES:
        language_code = 'zh'  # 默认中文
    
    return LANGUAGES[language_code].get(key, default or key)

def get_available_languages():
    """
    获取可用的语言列表
    
    Returns:
        list: 可用语言代码列表
    """
    return list(LANGUAGES.keys())

def get_language_display_name(language_code):
    """
    获取语言的显示名称
    
    Args:
        language_code (str): 语言代码
    
    Returns:
        str: 语言显示名称
    """
    display_names = {
        'en': 'English',
        'de': 'Deutsch',
        'zh': '中文'
    }
    return display_names.get(language_code, language_code)

def validate_language_code(language_code):
    """
    验证语言代码是否有效
    
    Args:
        language_code (str): 语言代码
    
    Returns:
        bool: 是否有效
    """
    return language_code in LANGUAGES