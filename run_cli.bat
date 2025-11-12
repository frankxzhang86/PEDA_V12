@echo off
REM PEDA V12 CLI Launcher
REM This script launches the PEDA V12 command-line interface in virtual environment

REM Change to the script's directory
cd /d %~dp0

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found
    echo Please run install.bat first to set up the environment
    pause
    exit /b 1
)

REM Activate virtual environment and launch CLI
echo Starting PEDA V12 CLI...
call venv\Scripts\activate.bat
python start.py

REM Pause at the end to see any output
pause
