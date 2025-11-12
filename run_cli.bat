@echo off
REM PEDA V12 CLI Launcher
REM This script launches the PEDA V12 command-line interface

REM Change to the script's directory
cd /d %~dp0

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please run install.bat first
    pause
    exit /b 1
)

REM Launch the CLI application
echo Starting PEDA V12 CLI...
python start.py

REM Pause at the end to see any output
pause
