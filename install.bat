@echo off
REM PEDA V12 Windows Installation Script
REM This script installs Python dependencies and sets up Playwright browsers

REM Ensure script runs in its own directory
cd /d %~dp0

echo ========================================
echo PEDA V12 Installation Script
echo ========================================
echo.
echo This script will:
echo   [1/5] Verify Python environment
echo   [2/5] Upgrade pip package manager
echo   [3/5] Install Python dependencies
echo   [4/5] Install Playwright browsers
echo   [5/5] Create desktop shortcut
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
echo [STEP 1/5 COMPLETED] Python environment verified successfully!
echo.

REM Upgrade pip to latest version
echo ========================================
echo [2/5] Upgrading pip package manager...
echo ========================================
echo.
python -m pip install --upgrade pip
if errorlevel 1 (
    echo WARNING: Failed to upgrade pip, continuing anyway...
)
echo.
echo [STEP 2/5 COMPLETED] pip upgraded successfully!
echo.

REM Install Python dependencies from requirements.txt
echo ========================================
echo [3/5] Installing Python dependencies...
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
echo [STEP 3/5 COMPLETED] Python dependencies installed successfully!
echo.

REM Install Playwright browsers
echo ========================================
echo [4/5] Installing Playwright browsers...
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
echo [STEP 4/5 COMPLETED] Playwright browsers installed successfully!
echo.

REM Create desktop shortcut for GUI version
echo ========================================
echo [5/5] Creating desktop shortcut...
echo ========================================
echo.
set SCRIPT_DIR=%~dp0
set SCRIPT_DIR=%SCRIPT_DIR:~0,-1%

REM Create VBScript to generate shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = oWS.SpecialFolders("Desktop") ^& "\PEDA V12.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%SCRIPT_DIR%\run_gui.bat" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%SCRIPT_DIR%" >> CreateShortcut.vbs
echo oLink.Description = "PEDA V12 Document Management System" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs

REM Execute VBScript
cscript //nologo CreateShortcut.vbs
del CreateShortcut.vbs

if exist "%USERPROFILE%\Desktop\PEDA V12.lnk" (
    echo Desktop shortcut created successfully!
) else (
    echo Warning: Failed to create desktop shortcut
)

echo.
echo [STEP 5/5 COMPLETED] Desktop shortcut created!
echo.
echo ========================================
echo ALL STEPS COMPLETED SUCCESSFULLY!
echo ========================================
echo.
echo You can now run the application by:
echo   1. Double-clicking "PEDA V12" on your desktop
echo   2. Running run_gui.bat for GUI version
echo   3. Running run_cli.bat for CLI version
echo.

pause
