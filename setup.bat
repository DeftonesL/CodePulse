@echo off
setlocal enabledelayedexpansion

:: CodePulse Setup Script for Windows
:: Auto-installs dependencies and sets up the environment

echo.
echo ========================================
echo   CodePulse Setup - Windows
echo ========================================
echo.

:: Check Python
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please install Python 3.9+ from https://python.org
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo [OK] Python %PYVER% detected
echo.

:: Check pip
echo [2/4] Checking pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip not found!
    echo Installing pip...
    python -m ensurepip --default-pip
)
echo [OK] pip is ready
echo.

:: Upgrade pip
echo [3/4] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo [OK] pip upgraded
echo.

:: Install dependencies
echo [4/4] Installing CodePulse dependencies...
echo This may take a minute...
echo.

python -m pip install --quiet ^
    click>=8.0.0 ^
    rich>=13.0.0 ^
    networkx>=3.0 ^
    jinja2>=3.1.0 ^
    pytest>=8.0.0

if errorlevel 1 (
    echo [ERROR] Failed to install dependencies!
    pause
    exit /b 1
)

echo [OK] All dependencies installed!
echo.

:: Create reports directory
if not exist "reports" mkdir reports

:: Check if AI dependencies needed
echo.
echo ========================================
echo   Optional: AI Features
echo ========================================
echo.
echo Would you like to install AI features?
echo (Requires Anthropic API key)
echo.
set /p INSTALL_AI="Install AI dependencies? (y/n): "

if /i "!INSTALL_AI!"=="y" (
    echo.
    echo Installing AI dependencies...
    python -m pip install --quiet anthropic>=0.40.0
    if errorlevel 1 (
        echo [WARNING] Failed to install AI dependencies
    ) else (
        echo [OK] AI dependencies installed!
        echo.
        echo To use AI features, set your API key:
        echo   set ANTHROPIC_API_KEY=your-key-here
        echo.
        echo Or create a .env file with:
        echo   ANTHROPIC_API_KEY=your-key-here
    )
)

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo CodePulse is ready to use!
echo.
echo Quick Start:
echo   codepulse           - Interactive mode
echo   codepulse --help    - Show all options
echo.
echo Example scans:
echo   codepulse           - Start interactive CLI
echo   python codepulse.py - Alternative way
echo.
pause
