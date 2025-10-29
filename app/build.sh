#!/bin/bash

# Build script for Mac/Linux (creates spec file, but CANNOT create Windows .exe)

echo "================================================"
echo "Wisconsin Excise Tax XML Generator"
echo "Build Script"
echo "================================================"
echo ""
echo "⚠️  WARNING: You are on Mac/Linux!"
echo "You CANNOT build a Windows .exe from Mac/Linux."
echo ""
echo "This script will prepare the build files, but to create"
echo "the Windows executable, you need to:"
echo "  1. Use a Windows VM (Parallels, VirtualBox, etc.)"
echo "  2. Run build.bat inside Windows"
echo "  3. Or use GitHub Actions to build in the cloud"
echo ""
echo "Press Ctrl+C to cancel, or Enter to continue anyway..."
read

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "Step 1: Installing dependencies..."
echo "This may take a few minutes..."
echo ""
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m pip install pyinstaller

echo ""
echo "Step 2: Attempting to build (will NOT create Windows .exe)..."
echo ""
python3 -m PyInstaller build_exe.spec --clean --noconfirm

if [ $? -eq 0 ]; then
    echo ""
    echo "================================================"
    echo "Build completed!"
    echo "================================================"
    echo ""
    echo "⚠️  HOWEVER: The output is for Mac, not Windows!"
    echo ""
    echo "To create a Windows .exe, you MUST:"
    echo "  1. Copy this project to a Windows machine"
    echo "  2. Run: build.bat"
    echo ""
    echo "Or see BUILD_INSTRUCTIONS.md for other options."
    echo ""
else
    echo ""
    echo "ERROR: Build failed!"
    echo ""
fi

