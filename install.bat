@echo off
chcp 65001 >nul
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
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
set "SHORTCUT_TARGET=%SCRIPT_DIR%\run_gui.bat"
set "SHORTCUT_DESCRIPTION=PEDA V12 Document Management System"
set "SHORTCUT_ICON="
if exist "%SCRIPT_DIR%\icon.ico" (
    set "SHORTCUT_ICON=%SCRIPT_DIR%\icon.ico"
)

REM Create shortcut in project directory (always works)
set "PROJECT_SHORTCUT=%SCRIPT_DIR%\启动 PEDA V12.lnk"
echo Creating shortcut in project directory...
call :CreateShortcut "%PROJECT_SHORTCUT%" "%SHORTCUT_TARGET%" "%SCRIPT_DIR%" "%SHORTCUT_DESCRIPTION%" "%SHORTCUT_ICON%"

if exist "%PROJECT_SHORTCUT%" (
    echo [OK] Project directory shortcut created: "启动 PEDA V12.lnk"
) else (
    echo [WARNING] Failed to create project directory shortcut
)

REM Determine candidate desktop paths (handles Desktop redirection/OneDrive)
set "PRIMARY_DESKTOP="
for /f "delims=" %%D in ('powershell -NoProfile -Command "[Environment]::GetFolderPath(^"Desktop^")"') do (
    if not defined PRIMARY_DESKTOP set "PRIMARY_DESKTOP=%%D"
)

set "COMMON_DESKTOP="
for /f "delims=" %%D in ('powershell -NoProfile -Command "[Environment]::GetFolderPath(^"CommonDesktopDirectory^")"') do (
    if not defined COMMON_DESKTOP set "COMMON_DESKTOP=%%D"
)

echo.
echo Creating desktop shortcut...
set "DESKTOP_SHORTCUT_DONE="
call :TryDesktopShortcut "%PRIMARY_DESKTOP%"
call :TryDesktopShortcut "%USERPROFILE%\Desktop"
call :TryDesktopShortcut "%HOMEDRIVE%%HOMEPATH%\Desktop"
if defined OneDrive call :TryDesktopShortcut "%OneDrive%\Desktop"
if defined OneDriveConsumer call :TryDesktopShortcut "%OneDriveConsumer%\Desktop"
if defined COMMON_DESKTOP call :TryDesktopShortcut "%COMMON_DESKTOP%"
if defined PUBLIC call :TryDesktopShortcut "%PUBLIC%\Desktop"

if defined DESKTOP_SHORTCUT_DONE (
    echo [OK] Desktop shortcut created successfully!
    echo      Location: %DESKTOP_SHORTCUT_DONE%
) else (
    echo [WARNING] Failed to create desktop shortcut
    echo          You can copy "启动 PEDA V12.lnk" to your desktop manually if it is redirected or locked
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
goto :EOF

:CreateShortcut
set "CS_SHORTCUT_PATH=%~1"
set "CS_SHORTCUT_TARGET=%~2"
set "CS_SHORTCUT_WORKDIR=%~3"
set "CS_SHORTCUT_DESC=%~4"
set "CS_SHORTCUT_ICON=%~5"

if "%CS_SHORTCUT_PATH%"=="" exit /b 1
if "%CS_SHORTCUT_TARGET%"=="" exit /b 1

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$shell = New-Object -ComObject WScript.Shell; " ^
    "$shortcut = $shell.CreateShortcut($env:CS_SHORTCUT_PATH); " ^
    "$shortcut.TargetPath = $env:CS_SHORTCUT_TARGET; " ^
    "if ($env:CS_SHORTCUT_WORKDIR) { $shortcut.WorkingDirectory = $env:CS_SHORTCUT_WORKDIR }; " ^
    "if ($env:CS_SHORTCUT_DESC) { $shortcut.Description = $env:CS_SHORTCUT_DESC }; " ^
    "$iconPath = $env:CS_SHORTCUT_ICON; " ^
    "if ($iconPath -and (Test-Path $iconPath)) { $shortcut.IconLocation = $iconPath }; " ^
    "$shortcut.Save()" >nul 2>&1

set "LAST_SHORTCUT_ERROR=%errorlevel%"
set CS_SHORTCUT_PATH=
set CS_SHORTCUT_TARGET=
set CS_SHORTCUT_WORKDIR=
set CS_SHORTCUT_DESC=
set CS_SHORTCUT_ICON=
exit /b %LAST_SHORTCUT_ERROR%

:TryDesktopShortcut
if defined DESKTOP_SHORTCUT_DONE exit /b
set "TARGET_FOLDER=%~1"
if "%TARGET_FOLDER%"=="" exit /b
if not exist "%TARGET_FOLDER%" exit /b

if "%TARGET_FOLDER:~-1%"=="\" set "TARGET_FOLDER=%TARGET_FOLDER:~0,-1%"

set "CURRENT_DESKTOP_LINK=%TARGET_FOLDER%\PEDA V12.lnk"
call :CreateShortcut "%CURRENT_DESKTOP_LINK%" "%SHORTCUT_TARGET%" "%SCRIPT_DIR%" "%SHORTCUT_DESCRIPTION%" "%SHORTCUT_ICON%"
if exist "%CURRENT_DESKTOP_LINK%" (
    set "DESKTOP_SHORTCUT_DONE=%CURRENT_DESKTOP_LINK%"
)
exit /b
