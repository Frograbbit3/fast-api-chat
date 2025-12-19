@echo off
setlocal

echo Checking for Python...

where python >nul 2>&1
if %errorlevel%==0 (
    echo Python is already installed.
    python --version
    goto :eof
)

echo Python not found. Downloading installer...

:: Set temp download location
set "PYTHON_INSTALLER=%TEMP%\python_installer.exe"

:: Download Python (change version if needed)
powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe -OutFile '%PYTHON_INSTALLER%'"

if not exist "%PYTHON_INSTALLER%" (
    echo Failed to download installer.
    exit /b 1
)

echo Installing Python silently...

:: Silent install with Add to PATH enabled and pip
"%PYTHON_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

:: Wait a bit just in case
timeout /t 5 >nul

:: Check again
where python >nul 2>&1
if %errorlevel%==0 (
    echo Python installed successfully!
    python --version
) else (
    echo Python installation failed.
    exit /b 1
)

:: Cleanup
del "%PYTHON_INSTALLER%"

endlocal
