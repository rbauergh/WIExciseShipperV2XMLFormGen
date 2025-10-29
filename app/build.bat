@echo off
REM Build script for Windows executable

echo ================================================
echo Wisconsin Excise Tax XML Generator
echo Build Script
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo Step 1: Installing dependencies...
echo This may take a few minutes...
echo.
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller

echo.
echo Step 2: Building executable with PyInstaller...
echo This may take 2-5 minutes...
echo.
python -m PyInstaller build_exe.spec --clean --noconfirm

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ================================================
echo Build completed successfully!
echo ================================================
echo.
echo Executable location: dist\WI_Excise_Tax_Generator.exe
echo.
echo You can now distribute the WI_Excise_Tax_Generator.exe file
echo to users who don't have Python installed.
echo.
pause

