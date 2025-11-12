@echo off
REM PEDA V12 Windows Installation Script
REM This script installs Python dependencies and sets up Playwright browsers in a virtual environment

REM Ensure script runs in its own directory
cd /d %~dp0

echo ========================================
echo PEDA V12 Installation Script
echo ========================================
echo.
echo This script will:
echo   [1/6] Verify Python environment
echo   [2/6] Create virtual environment
echo   [3/6] Upgrade pip package manager
echo   [4/6] Install Python dependencies
echo   [5/6] Install Playwright browsers
echo   [6/6] Create desktop shortcut
echo.
echo ========================================
echo.

REM Check if Python is installed
echo [1/5] Verifying Python environment...
echo.
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

REM Check Python version is 3.8 or higher
echo Checking Python version...
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
for /f "tokens=1,2 delims=." %%a in ("%PYVER%") do (
    set PYMAJOR=%%a
    set PYMINOR=%%b
)

if %PYMAJOR% LSS 3 (
    echo ERROR: Python version %PYVER% is too old
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)
if %PYMAJOR% EQU 3 if %PYMINOR% LSS 8 (
    echo ERROR: Python version %PYVER% is too old
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo Python version %PYVER% is compatible
echo.

REM Check if pip is available
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available
    echo Please reinstall Python with pip included
    pause
    exit /b 1
)

echo pip found:
python -m pip --version
echo.
echo [STEP 1/6 COMPLETED] Python environment verified successfully!
echo.

REM Create or verify virtual environment
echo ========================================
echo [2/6] Setting up virtual environment...
echo ========================================
echo.

if exist "venv\Scripts\activate.bat" (
    echo Virtual environment already exists, skipping creation...
) else (
    echo Creating new virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
)

echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo.
echo [STEP 2/6 COMPLETED] Virtual environment is ready!
echo.

REM Upgrade pip to latest version
echo ========================================
echo [3/6] Upgrading pip package manager...
echo ========================================
echo.
python -m pip install --upgrade pip
if errorlevel 1 (
    echo WARNING: Failed to upgrade pip, continuing anyway...
)
echo.
echo [STEP 3/6 COMPLETED] pip upgraded successfully!
echo.

REM Install Python dependencies from requirements.txt
echo ========================================
echo [4/6] Installing Python dependencies...
echo ========================================
echo This may take several minutes, please wait...
echo.

python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo [STEP 4/6 COMPLETED] Python dependencies installed successfully!
echo.

REM Install Playwright browsers
echo ========================================
echo [5/6] Installing Playwright browsers...
echo ========================================
echo This will download Chromium, Firefox, and WebKit
echo This may take several minutes depending on your internet speed...
echo Please be patient...
echo.

python -m playwright install
if errorlevel 1 (
    echo ERROR: Failed to install Playwright browsers
    pause
    exit /b 1
)

echo.
echo [STEP 5/6 COMPLETED] Playwright browsers installed successfully!
echo.

REM Create shortcuts for GUI version
echo ========================================
echo [6/6] Creating shortcuts...
echo ========================================
echo.
set SCRIPT_DIR=%~dp0
set SCRIPT_DIR=%SCRIPT_DIR:~0,-1%

REM Create shortcut in project directory (always works)
echo Creating shortcut in project directory...
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%SCRIPT_DIR%\启动 PEDA V12.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%SCRIPT_DIR%\run_gui.bat" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%SCRIPT_DIR%" >> CreateShortcut.vbs
echo oLink.Description = "PEDA V12 Document Management System" >> CreateShortcut.vbs
if exist "%SCRIPT_DIR%\icon.ico" (
    echo oLink.IconLocation = "%SCRIPT_DIR%\icon.ico" >> CreateShortcut.vbs
)
echo oLink.Save >> CreateShortcut.vbs

cscript //nologo CreateShortcut.vbs >nul 2>&1

if exist "%SCRIPT_DIR%\启动 PEDA V12.lnk" (
    echo [OK] Project directory shortcut created: "启动 PEDA V12.lnk"
) else (
    echo [WARNING] Failed to create project directory shortcut
)

REM Try to create desktop shortcut
echo.
echo Creating desktop shortcut...
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = oWS.SpecialFolders("Desktop") ^& "\PEDA V12.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%SCRIPT_DIR%\run_gui.bat" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%SCRIPT_DIR%" >> CreateShortcut.vbs
echo oLink.Description = "PEDA V12 Document Management System" >> CreateShortcut.vbs
if exist "%SCRIPT_DIR%\icon.ico" (
    echo oLink.IconLocation = "%SCRIPT_DIR%\icon.ico" >> CreateShortcut.vbs
)
echo oLink.Save >> CreateShortcut.vbs

cscript //nologo CreateShortcut.vbs >nul 2>&1
del CreateShortcut.vbs

if exist "%USERPROFILE%\Desktop\PEDA V12.lnk" (
    echo [OK] Desktop shortcut created successfully!
) else (
    echo [WARNING] Failed to create desktop shortcut
    echo          You can use the shortcut in the project directory instead
)

echo.
echo [STEP 6/6 COMPLETED] Shortcuts created!
echo.
echo ========================================
echo ALL STEPS COMPLETED SUCCESSFULLY!
echo ========================================
echo.
echo Installation complete! You can now run the application by:
echo.
echo   [Recommended] Double-click "启动 PEDA V12.lnk" in this folder
echo   [Alternative] Double-click "PEDA V12" on your desktop (if created)
echo   [Manual]      Run run_gui.bat for GUI version
echo   [Manual]      Run run_cli.bat for CLI version
echo.
echo ========================================
echo.

pause
