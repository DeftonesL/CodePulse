@echo off
REM ============================================
REM CodePulse - Complete Project Manager
REM ============================================

setlocal enabledelayedexpansion

REM Display menu if no arguments
if "%~1"=="" goto SHOW_MENU

REM Parse command
set CMD=%~1
shift

if /i "%CMD%"=="scan" goto CMD_SCAN
if /i "%CMD%"=="fast" goto CMD_FAST
if /i "%CMD%"=="full" goto CMD_FULL
if /i "%CMD%"=="json" goto CMD_JSON
if /i "%CMD%"=="comprehensive" goto CMD_COMPREHENSIVE
if /i "%CMD%"=="test" goto CMD_TEST
if /i "%CMD%"=="install" goto CMD_INSTALL
if /i "%CMD%"=="update" goto CMD_UPDATE
if /i "%CMD%"=="clean" goto CMD_CLEAN
if /i "%CMD%"=="benchmark" goto CMD_BENCHMARK
if /i "%CMD%"=="reports" goto CMD_REPORTS
if /i "%CMD%"=="help" goto SHOW_MENU
goto UNKNOWN_CMD

:SHOW_MENU
cls
echo.
echo  ========================================
echo    CodePulse v0.10.0 - Project Manager
echo  ========================================
echo.
echo  SCANNING COMMANDS:
echo    scan ^<path^>             - HTML scan + auto-open
echo    fast ^<path^>             - Fast scan (8 workers)
echo    full ^<path^>             - Full scan (no cache)
echo    json ^<path^>             - JSON output
echo    comprehensive ^<path^>    - Deep comprehensive scan
echo.
echo  PROJECT COMMANDS:
echo    install                 - Install dependencies
echo    update                  - Update CodePulse
echo    test                    - Run tests
echo    benchmark               - Performance test
echo    clean                   - Clean cache/reports
echo    reports                 - View reports folder
echo.
echo  EXAMPLES:
echo    .\codepulse scan C:\Users\xsll7\Desktop\discord
echo    .\codepulse comprehensive .\src
echo    .\codepulse install
echo    .\codepulse clean
echo.
echo  ========================================
echo.
pause
goto END

:CMD_SCAN
if "%~1"=="" (
    echo [ERROR] Project path required!
    echo Usage: .\codepulse scan ^<path^>
    pause
    goto END
)
cls
echo.
echo  ========================================
echo    CodePulse - HTML Scan
echo  ========================================
echo.
echo  [*] Project: %~1
echo  [*] Mode: HTML Report
echo.
python "%~dp0fast_scan.py" "%~1" --format html
if not errorlevel 1 (
    echo.
    echo  [SUCCESS] Report generated!
    echo  [*] Opening in browser...
    timeout /t 1 /nobreak >nul 2>&1
    for /f "delims=" %%i in ('dir /b /od "%~dp0reports\*.html" 2^>nul') do set "LATEST=%%i"
    if defined LATEST (
        start "" "%~dp0reports\!LATEST!"
    ) else (
        echo  [WARNING] Could not find report file
    )
)
pause
goto END

:CMD_FAST
if "%~1"=="" (
    echo [ERROR] Project path required!
    echo Usage: .\codepulse fast ^<path^>
    pause
    goto END
)
cls
echo.
echo  ========================================
echo    CodePulse - Fast Scan
echo  ========================================
echo.
echo  [*] Project: %~1
echo  [*] Mode: Fast (8 workers)
echo.
python "%~dp0fast_scan.py" "%~1" --format html --workers 8
if not errorlevel 1 (
    echo.
    echo  [SUCCESS] Report generated!
    echo  [*] Opening in browser...
    timeout /t 1 /nobreak >nul 2>&1
    for /f "delims=" %%i in ('dir /b /od "%~dp0reports\*.html" 2^>nul') do set "LATEST=%%i"
    if defined LATEST (
        start "" "%~dp0reports\!LATEST!"
    )
)
pause
goto END

:CMD_FULL
if "%~1"=="" (
    echo [ERROR] Project path required!
    echo Usage: .\codepulse full ^<path^>
    pause
    goto END
)
cls
echo.
echo  ========================================
echo    CodePulse - Full Scan
echo  ========================================
echo.
echo  [*] Project: %~1
echo  [*] Mode: Complete Analysis
echo.
python "%~dp0fast_scan.py" "%~1" --format html --no-cache --no-incremental
if not errorlevel 1 (
    echo.
    echo  [SUCCESS] Report generated!
    echo  [*] Opening in browser...
    timeout /t 1 /nobreak >nul 2>&1
    for /f "delims=" %%i in ('dir /b /od "%~dp0reports\*.html" 2^>nul') do set "LATEST=%%i"
    if defined LATEST (
        start "" "%~dp0reports\!LATEST!"
    )
)
pause
goto END

:CMD_JSON
if "%~1"=="" (
    echo [ERROR] Project path required!
    echo Usage: .\codepulse json ^<path^>
    pause
    goto END
)
cls
echo.
echo  ========================================
echo    CodePulse - JSON Export
echo  ========================================
echo.
echo  [*] Project: %~1
echo  [*] Mode: JSON Output
echo.
python "%~dp0fast_scan.py" "%~1" --format json
pause
goto END

:CMD_COMPREHENSIVE
if "%~1"=="" (
    echo [ERROR] Project path required!
    echo Usage: .\codepulse comprehensive ^<path^>
    pause
    goto END
)
cls
echo.
echo  ========================================
echo    CodePulse - Comprehensive Scan
echo  ========================================
echo.
echo  [*] Project: %~1
echo  [*] Mode: Deep Analysis
echo.
echo  [*] Running comprehensive scan...
echo  [*] This may take a while...
echo.
python "%~dp0comprehensive_scan.py" "%~1"
if not errorlevel 1 (
    echo.
    echo  [SUCCESS] Comprehensive scan complete!
    echo  [*] Check reports folder for results
    timeout /t 2 /nobreak >nul 2>&1
    start "" "%~dp0reports\"
)
pause
goto END

:CMD_TEST
cls
echo.
echo  ========================================
echo    CodePulse - Running Tests
echo  ========================================
echo.
if not exist "%~dp0tests\" (
    echo [ERROR] Tests directory not found!
    pause
    goto END
)
echo  [*] Running pytest...
echo.
python -m pytest tests/ -v
echo.
echo  [*] Tests complete!
pause
goto END

:CMD_INSTALL
cls
echo.
echo  ========================================
echo    CodePulse - Install Dependencies
echo  ========================================
echo.
echo  [*] Checking Python...
python --version
if errorlevel 1 (
    echo [ERROR] Python not found!
    pause
    goto END
)
echo.
echo  [*] Installing requirements...
echo.
python -m pip install -r requirements.txt --upgrade
echo.
echo  [SUCCESS] Dependencies installed!
pause
goto END

:CMD_UPDATE
cls
echo.
echo  ========================================
echo    CodePulse - Update
echo  ========================================
echo.
echo  [*] Pulling latest changes...
echo.
git pull origin main
if errorlevel 1 (
    echo [ERROR] Git pull failed!
    echo Make sure you're in a git repository.
    pause
    goto END
)
echo.
echo  [*] Updating dependencies...
python -m pip install -r requirements.txt --upgrade
echo.
echo  [SUCCESS] CodePulse updated!
pause
goto END

:CMD_CLEAN
cls
echo.
echo  ========================================
echo    CodePulse - Clean
echo  ========================================
echo.
echo  [*] Cleaning cache...
if exist ".codepulse_cache\" (
    rmdir /s /q .codepulse_cache
    echo     [OK] Cache cleared
) else (
    echo     [INFO] No cache found
)
echo.
echo  [*] Cleaning state...
if exist ".codepulse_state.json" (
    del .codepulse_state.json
    echo     [OK] State cleared
) else (
    echo     [INFO] No state found
)
echo.
echo  [*] Cleaning Python cache...
for /d /r . %%d in (__pycache__) do @if exist "%%d" (
    echo     [OK] Removing %%d
    rd /s /q "%%d"
)
echo.
set /p CLEAN_REPORTS="  Clean old reports? (Y/N): "
if /i "%CLEAN_REPORTS%"=="Y" (
    if exist "reports\" (
        echo     [*] Cleaning reports...
        del /q reports\*.html 2>nul
        del /q reports\*.json 2>nul
        echo     [OK] Reports cleared
    )
)
echo.
echo  [SUCCESS] Cleanup complete!
pause
goto END

:CMD_BENCHMARK
cls
echo.
echo  ========================================
echo    CodePulse - Performance Benchmark
echo  ========================================
echo.
echo  [*] Running benchmark...
echo.
python "%~dp0benchmark.py"
echo.
pause
goto END

:CMD_REPORTS
cls
echo.
echo  ========================================
echo    CodePulse - Reports
echo  ========================================
echo.
if not exist "reports\" (
    echo [ERROR] Reports folder not found!
    mkdir reports
    echo [INFO] Created reports folder
    pause
    goto END
)
echo  [*] Opening reports folder...
start "" "%~dp0reports\"
echo.
echo  [*] Recent reports:
echo.
dir /b /od reports\*.html reports\*.json 2>nul
if errorlevel 1 (
    echo     [INFO] No reports found
)
echo.
pause
goto END

:UNKNOWN_CMD
cls
echo.
echo  [ERROR] Unknown command: %CMD%
echo.
echo  Use: .\codepulse help
echo.
pause
goto END

:END
endlocal
