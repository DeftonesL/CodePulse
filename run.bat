@echo off
:: CodePulse Quick Launcher for Windows
:: Just double-click this file to run CodePulse

title CodePulse Scanner

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Python not found!
    echo Please run setup.bat first
    echo.
    pause
    exit /b 1
)

:: Run CodePulse
python codepulse.py

:: Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo [ERROR] CodePulse encountered an error
    echo.
    pause
)
