# Building the Windows Executable

## 🎯 Goal

Create a standalone Windows `.exe` file that your colleagues can run **without having Python installed**.

## ⚠️ Important

**You MUST build on a Windows machine!**

You cannot build a Windows .exe from Mac or Linux. You need:
- A Windows computer, OR
- A Windows virtual machine, OR
- Access to a Windows cloud instance

## 📋 Prerequisites

Before building, ensure you have:

1. ✅ **Windows** (7, 10, or 11)
2. ✅ **Python 3.8 or higher** installed
   - Download from https://python.org
   - During installation, check **"Add Python to PATH"**
3. ✅ **This project's code** on the Windows machine

## 🚀 Build Steps (Simple Method)

### Step 1: Open Command Prompt

1. Press `Windows Key + R`
2. Type `cmd` and press Enter

### Step 2: Navigate to the App Folder

```cmd
cd path\to\WIExciseShipperV2XMLFormGen\app
```

Example:
```cmd
cd C:\Users\YourName\Documents\WIExciseShipperV2XMLFormGen\app
```

### Step 3: Run the Build Script

```cmd
build.bat
```

### Step 4: Wait

The build process will:
1. Install dependencies (30 seconds - 1 minute)
2. Install PyInstaller
3. Build the executable (1-3 minutes)
4. Show "Build completed successfully!"

### Step 5: Get Your Executable

Find it at:
```
app\dist\WI_Excise_Tax_Generator.exe
```

**That's it!** 🎉

## 🔧 Build Steps (Manual Method)

If the batch file doesn't work, do it manually:

```cmd
cd app\

REM Install dependencies
pip install -r requirements.txt
pip install pyinstaller

REM Build the executable
pyinstaller build_exe.spec --clean --noconfirm
```

The `.exe` will be in `dist\WI_Excise_Tax_Generator.exe`

## 📦 What Gets Built

The build process creates:

```
app/
├── build/          # Temporary build files (can delete)
├── dist/
│   └── WI_Excise_Tax_Generator.exe  # ← THIS IS WHAT YOU WANT!
└── ...
```

The **dist/WI_Excise_Tax_Generator.exe** file is:
- About 30-50 MB
- Completely standalone
- Contains Python + all libraries + your code
- Ready to distribute

## ✅ Testing the Executable

After building:

1. **Navigate to the dist folder:**
   ```cmd
   cd dist\
   ```

2. **Double-click** `WI_Excise_Tax_Generator.exe`

3. **Browser should open** automatically to the app

4. **Try generating an XML** with test data

5. **If it works**, you're done!

## 📤 Distributing to Users

### Simple Distribution

Just give them the single .exe file:
```
WI_Excise_Tax_Generator.exe
```

### Recommended Distribution Package

Create a folder with:
```
WI_Excise_Tax_Package/
├── WI_Excise_Tax_Generator.exe
├── QUICK_START.md (or PDF version)
└── README.txt (simple instructions)
```

Zip it up and send to your colleagues!

## 🐛 Troubleshooting

### Python Not Found

**Error:** `'python' is not recognized...`

**Fix:**
1. Install Python from https://python.org
2. During installation, CHECK the box "Add Python to PATH"
3. Restart Command Prompt
4. Try again

### Build Fails

**Error:** Various build errors

**Fix:**
```cmd
REM Clean everything and start over
rmdir /s /q build
rmdir /s /q dist
pip install -r requirements.txt --upgrade
pip install pyinstaller --upgrade
pyinstaller build_exe.spec --clean --noconfirm
```

### Executable Won't Run

**Error:** Windows SmartScreen blocks it

**Fix:**
1. Click "More info" on the warning
2. Click "Run anyway"
3. (Optional) Code-sign the exe to avoid this

### Module Not Found During Build

**Error:** `ModuleNotFoundError: No module named 'xyz'`

**Fix:**
```cmd
pip install xyz
pip install -r requirements.txt
pyinstaller build_exe.spec --clean --noconfirm
```

### Build is Slow

This is normal! PyInstaller takes 1-5 minutes to:
- Analyze dependencies
- Bundle Python interpreter
- Include all libraries
- Create the executable

Be patient!

## 📂 What to Keep

After building successfully:

**Keep:**
- ✅ `dist/WI_Excise_Tax_Generator.exe` - This is what you distribute!
- ✅ Source code (for future updates)

**Can Delete:**
- ❌ `build/` folder - Temporary build files
- ❌ `__pycache__/` folders - Python cache

## 🔄 Rebuilding After Changes

If you make changes to the code:

1. Edit your Python files
2. Test with `python app.py`
3. Run `build.bat` again
4. New .exe will be in `dist/` folder
5. Distribute the new version to users

## 🌐 Don't Have Windows?

### Option 1: Use a Windows VM

**On Mac (Parallels Desktop):**
1. Install Parallels Desktop
2. Create a Windows 11 VM
3. Copy project to the VM
4. Build inside the VM

**On Mac (VirtualBox - Free):**
1. Download VirtualBox
2. Download Windows 10/11 ISO
3. Create VM, install Windows
4. Build inside the VM

### Option 2: Use GitHub Actions

Create `.github/workflows/build-windows.yml`:
```yaml
name: Build Windows Executable

on:
  workflow_dispatch:

jobs:
  build:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        cd app
        pip install -r requirements.txt
        pip install pyinstaller
    
    - name: Build executable
      run: |
        cd app
        pyinstaller build_exe.spec --clean --noconfirm
    
    - name: Upload artifact
      uses: actions/upload-artifact@v3
      with:
        name: WI_Excise_Tax_Generator
        path: app/dist/WI_Excise_Tax_Generator.exe
```

Then click "Actions" → "Build Windows Executable" → "Run workflow"  
Download the built .exe from the artifacts!

### Option 3: Ask a Colleague

Send them:
1. The entire project folder (zip it up)
2. This BUILD_INSTRUCTIONS.md file
3. Ask them to run `build.bat`
4. Have them send back the .exe from `dist/` folder

## 📋 Build Checklist

Before distributing:

- [ ] Built on Windows machine
- [ ] Tested the .exe on the build machine
- [ ] Tested the .exe on a **clean** Windows machine (no Python)
- [ ] Generated a test XML successfully
- [ ] Validated the XML passes
- [ ] Downloaded the XML file
- [ ] Verified file opens in notepad/browser
- [ ] Created Quick Start guide for users
- [ ] Documented any known issues

## 🎉 Success!

Once built, you have a **single file** that:
- Works on any Windows computer
- Requires no installation
- Bundles everything needed
- Your colleagues can use immediately

**Distribute the .exe and watch the magic happen!** ✨

---

**Need help?** See [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) for the full deployment process.

