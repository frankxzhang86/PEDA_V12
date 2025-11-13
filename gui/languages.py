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
        'headless_mode': 'Headless Mode',
        'file_selection': '📁 File Selection',
        'excel_file': 'Excel File:',
        'document_path': 'Document Path:',
        'choose_file': '📄 Choose File',
        'choose_folder': '📁 Choose Path',
        'generate_folders': '📁 Generate Folders',
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
        'config_saved': 'Configuration saved',
        'instructions_tab': 'Instructions',
        'instructions_title': '📖 User Manual',
        'instructions_op_title': '1. Operation Instructions',
        'instructions_op_content': """
1. Login: Enter the URL, username, and password, then click 'Save' to store the credentials.
2. File Selection: Click 'Choose File' to select the Excel file and 'Choose Folder' to select the document directory.
3. Generate Folders: After selecting the Excel file and document directory, click 'Generate Folders' to automatically create the required folder structure for each part number based on the Excel data. This will create sub-folders (Confidential, Image Documentation, Measurement Report, Other, Technical Datasheet, Technical Drawing) under each part number folder.
4. Headless Mode: Check the 'Headless Mode' option to run the browser in the background without displaying the browser window. This can improve performance and reduce visual distractions. Uncheck it if you want to observe the browser automation process.
5. Start: Click 'Start' to begin the automated processing.
6. Stop/Reset: 'Stop' halts the current process, and 'Reset' clears all progress and statistics.
7. Reports: After processing, you can download various reports for records.
""",
        'instructions_excel_title': '2. Excel Upload Instructions',
        'instructions_excel_content': """
The Excel file must contain specific columns for the program to read correctly.
Please download the template to see the required format.
""",
        'instructions_download_template': '📄 Download Template',
        'instructions_dir_title': '3. Document Directory Structure Requirements',
        'instructions_dir_content': """
1. The document directory must follow a specific structure.
2. Each sub-folder should be named with the 'Part Number' from the Excel file.
3. Inside each 'Part Number' folder, create sub-folders for different document types as shown below:

PEDA DOCUMENTS/
└───[PART NUMBER]/
    ├───Confidential/
    ├───Image Documentation/
    ├───Measurement Report/
    ├───Other/
    ├───Technical Datasheet/
    └───Technical Drawing/
"""
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
        'headless_mode': 'Headless-Modus',
        'file_selection': '📁 Dateiauswahl',
        'excel_file': 'Excel-Datei:',
        'document_path': 'Dokumentenpfad:',
        'choose_file': '📄 Datei wählen',
        'choose_folder': '📁 Pfad wählen',
        'generate_folders': '📁 Ordner erstellen',
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
        'config_saved': 'Konfiguration gespeichert',
        'instructions_tab': 'Anleitung',
        'instructions_title': '📖 Benutzerhandbuch',
        'instructions_op_title': '1. Bedienungsanleitung',
        'instructions_op_content': """
1. Anmelden: Geben Sie die URL, den Benutzernamen und das Passwort ein und klicken Sie auf "Speichern", um die Anmeldeinformationen zu sichern.
2. Dateiauswahl: Klicken Sie auf "Datei wählen", um die Excel-Datei auszuwählen, und auf "Ordner wählen", um das Dokumentenverzeichnis auszuwählen.
3. Ordner erstellen: Nachdem Sie die Excel-Datei und das Dokumentenverzeichnis ausgewählt haben, klicken Sie auf "Ordner erstellen", um automatisch die erforderliche Ordnerstruktur für jede Teilenummer basierend auf den Excel-Daten zu erstellen. Dies erstellt Unterordner (Confidential, Image Documentation, Measurement Report, Other, Technical Datasheet, Technical Drawing) unter jedem Teilenummer-Ordner.
4. Headless-Modus: Aktivieren Sie die Option "Headless-Modus", um den Browser im Hintergrund ohne Anzeige des Browserfensters auszuführen. Dies kann die Leistung verbessern und visuelle Ablenkungen reduzieren. Deaktivieren Sie es, wenn Sie den Browser-Automatisierungsprozess beobachten möchten.
5. Start: Klicken Sie auf "Start", um die automatische Verarbeitung zu beginnen.
6. Stopp/Zurücksetzen: "Stopp" hält den aktuellen Prozess an, und "Zurücksetzen" löscht den gesamten Fortschritt und die Statistiken.
7. Berichte: Nach der Verarbeitung können Sie verschiedene Berichte für Ihre Unterlagen herunterladen.
""",
        'instructions_excel_title': '2. Anleitung zum Hochladen von Excel-Dateien',
        'instructions_excel_content': """
Die Excel-Datei muss bestimmte Spalten enthalten, damit das Programm sie korrekt lesen kann.
Bitte laden Sie die Vorlage herunter, um das erforderliche Format zu sehen.
""",
        'instructions_download_template': '📄 Vorlage herunterladen',
        'instructions_dir_title': '3. Anforderungen an die Dokumentenverzeichnisstruktur',
        'instructions_dir_content': """
1. Das Dokumentenverzeichnis muss einer bestimmten Struktur folgen.
2. Jeder Unterordner sollte mit der 'PART NUMBER' aus der Excel-Datei benannt sein.
3. Innerhalb jedes 'PART NUMBER'-Ordners erstellen Sie Unterordner für verschiedene Dokumenttypen, wie unten gezeigt:

PEDA DOCUMENTS/
└───[PART NUMBER]/
    ├───Confidential/
    ├───Image Documentation/
    ├───Measurement Report/
    ├───Other/
    ├───Technical Datasheet/
    └───Technical Drawing/
"""
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
        'headless_mode': 'Headless 模式',
        'file_selection': '📁 文件选择',
        'excel_file': 'Excel文件:',
        'document_path': '文档路径:',
        'choose_file': '📄 选择文件',
        'choose_folder': '📁 选择路径',
        'generate_folders': '📁 生成文件夹',
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
        'config_saved': '配置已保存',
        'instructions_tab': '使用说明',
        'instructions_title': '📖 使用手册',
        'instructions_op_title': '1. 操作说明',
        'instructions_op_content': """
1. 登录：输入网址、用户名和密码，点击"保存"以存储凭据。
2. 文件选择：点击"选择文件"选择Excel文件，点击"选择文件夹"选择文档目录。
3. 生成文件夹：选择Excel文件和文档目录后，点击"生成文件夹"按钮，系统会根据Excel中的件号数据，自动创建所需的文件夹结构。程序会为每个件号创建子文件夹（Confidential、Image Documentation、Measurement Report、Other、Technical Datasheet、Technical Drawing）。
4. Headless模式：勾选"Headless模式"选项，浏览器将在后台运行，不显示浏览器窗口。这可以提高性能并减少视觉干扰。如果您想观察浏览器自动化过程，请取消勾选。
5. 开始：点击"开始"以启动自动化处理。
6. 停止/重置："停止"会暂停当前进程，"重置"会清除所有进度和统计信息。
7. 报告：处理完成后，您可以下载各种报告以供记录。
""",
        'instructions_excel_title': '2. 上传表格说明',
        'instructions_excel_content': """
Excel文件必须包含特定列，以便程序正确读取。
请下载模板以查看所需格式。
""",
        'instructions_download_template': '📄 下载模板',
        'instructions_dir_title': '3. 上传文档的目录结构要求',
        'instructions_dir_content': """
1. 文档目录必须遵循特定的结构。
2. 每个子文件夹都应以Excel文件中的"PART NUMBER"命名。
3. 在每个"PART NUMBER"文件夹内，为不同的文档类型创建子文件夹，如下所示：

PEDA DOCUMENTS/
└───[PART NUMBER]/
    ├───Confidential/
    ├───Image Documentation/
    ├───Measurement Report/
    ├───Other/
    ├───Technical Datasheet/
    └───Technical Drawing/
"""
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
