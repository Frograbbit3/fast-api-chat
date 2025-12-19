@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

if not exist tools (
    echo [ERROR] tools directory not found!
    pause
    exit /b 1
)

cd tools
echo Installing python if not installed...
if exist install-python.bat (
    call install-python.bat
) else (
    echo [WARNING] install-python.bat not found in tools!
)
cd ..

rem Try to detect Python install path from registry (3.12 version; adjust if needed)
set "pyInstallPath="

for /f "tokens=2*" %%A in ('reg query "HKCU\Software\Python\PythonCore\3.12\InstallPath" /ve 2^>nul') do (
    set "pyInstallPath=%%B"
)

if not defined pyInstallPath (
    for /f "tokens=2*" %%A in ('reg query "HKLM\Software\Python\PythonCore\3.12\InstallPath" /ve 2^>nul') do (
        set "pyInstallPath=%%B"
    )
)

if defined pyInstallPath (
    rem Remove trailing backslash if present
    if "!pyInstallPath:~-1!"=="\" set "pyInstallPath=!pyInstallPath:~0,-1!"
    echo Found Python install path: !pyInstallPath!
    set "pyExe=!pyInstallPath!\python.exe"
    if exist "!pyExe!" (
        echo Python executable found at !pyExe!
        rem Add Python directory to PATH temporarily
        set "PATH=!pyInstallPath!;!PATH!"
    ) else (
        echo Python executable not found at !pyExe!
    )
) else (
    echo Python install path not found in registry.
    echo Will try to use python from PATH.
)

if not exist requirements.txt (
    echo [ERROR] requirements.txt not found!
    pause
    exit /b 1
)

echo Installing libs...
python -m pip install -r requirements.txt

echo Wiping..
python tools/wipe.py
echo Testing script...
python serve.py

pause
endlocal
