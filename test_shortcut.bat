@echo off
REM Test script to diagnose shortcut creation issue

cd /d %~dp0

echo Testing shortcut creation...
echo.

set SCRIPT_DIR=%~dp0
set SCRIPT_DIR=%SCRIPT_DIR:~0,-1%

echo Script Directory: %SCRIPT_DIR%
echo Desktop Path: %USERPROFILE%\Desktop
echo.

REM Check if icon file exists
if exist "%SCRIPT_DIR%\icon.ico" (
    echo [OK] icon.ico found
) else (
    echo [WARNING] icon.ico NOT found at: %SCRIPT_DIR%\icon.ico
)

REM Check if run_gui.bat exists
if exist "%SCRIPT_DIR%\run_gui.bat" (
    echo [OK] run_gui.bat found
) else (
    echo [ERROR] run_gui.bat NOT found
)
echo.

REM Try to create shortcut
echo Creating test shortcut...
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

echo.
echo VBScript content:
type CreateShortcut.vbs
echo.

echo Executing VBScript...
cscript //nologo CreateShortcut.vbs
set VBSCRIPT_ERROR=%errorlevel%

echo VBScript exit code: %VBSCRIPT_ERROR%
echo.

if exist "%USERPROFILE%\Desktop\PEDA V12.lnk" (
    echo [SUCCESS] Desktop shortcut created!
    echo Location: %USERPROFILE%\Desktop\PEDA V12.lnk
) else (
    echo [FAILED] Desktop shortcut was NOT created
    echo Please check if Desktop folder exists and you have write permissions
)

del CreateShortcut.vbs

pause
