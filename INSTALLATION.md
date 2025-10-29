# Installation Guide

## For End Users (Windows)

### Option 1: Using the Executable (Easiest)

1. **Download** the `WI_Excise_Tax_Generator.exe` file
2. **Double-click** the executable
3. **Wait** for your web browser to open automatically
4. **Start using** the application!

**That's it!** No Python installation required.

**Note:** Windows may show a security warning the first time you run it. Click "More info" then "Run anyway" to proceed.

### Option 2: Running from Source (Requires Python)

1. **Install Python 3.8 or higher**
   - Download from https://python.org
   - During installation, check "Add Python to PATH"

2. **Open the app folder**
   - Navigate to the `app/` directory

3. **Run the application**
   - Double-click `run.bat`
   - OR open command prompt and run: `python app.py`

4. **Use the application**
   - Browser will open automatically
   - Navigate to http://127.0.0.1:5000 if it doesn't

## For Developers

### Initial Setup

```bash
cd app/
python -m venv venv
venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On Mac/Linux

pip install -r requirements.txt
```

### Running the Application

```bash
python app.py
```

Browser will open to http://127.0.0.1:5000

### Building Windows Executable

**On Windows:**

```bash
# Install build dependencies
pip install -r requirements.txt
pip install pyinstaller

# Build the executable
pyinstaller build_exe.spec --clean --noconfirm
```

The executable will be in `dist/WI_Excise_Tax_Generator.exe`

**Or simply:**

Double-click `build.bat`

### Project Structure

```
app/
├── app.py                  # Main Flask application
├── xml_generator.py        # XML generation and validation
├── csv_mapper.py           # CSV import and mapping
├── config_manager.py       # Configuration management
├── requirements.txt        # Python dependencies
├── build_exe.spec          # PyInstaller spec file
├── build.bat               # Windows build script
├── run.bat                 # Windows run script
├── templates/              # HTML templates
│   └── index.html
├── static/                 # CSS and JavaScript
│   ├── style.css
│   └── script.js
├── schemas/                # XSD schema files
│   ├── AB136.xsd
│   └── AB137.xsd
├── config/                 # Configuration storage
├── output/                 # Generated XML files
└── docs/                   # Documentation
    ├── USER_GUIDE.md
    └── SCHEMA_UPDATE_GUIDE.md
```

## System Requirements

### Minimum Requirements
- **OS:** Windows 7 or later (for .exe), or any OS with Python 3.8+
- **RAM:** 512 MB
- **Disk Space:** 50 MB
- **Browser:** Any modern browser (Chrome, Firefox, Edge, Safari)

### Recommended
- **OS:** Windows 10 or later
- **RAM:** 2 GB
- **Browser:** Chrome or Firefox (latest version)

## Troubleshooting

### "Python is not recognized..."

**Solution:** Python is not installed or not in PATH
- Reinstall Python and check "Add Python to PATH" during installation
- Or manually add Python to system PATH

### Port 5000 Already in Use

**Solution:** Another application is using port 5000
- Close other applications using that port
- Or modify `app.py` to use a different port (change `port=5000`)

### PyInstaller Build Fails

**Solution:** Missing dependencies
```bash
pip install --upgrade pip
pip install --upgrade setuptools wheel
pip install -r requirements.txt
pip install pyinstaller
```

### Executable Won't Run

**Solution:** Windows SmartScreen blocking
- Click "More info" on the warning dialog
- Click "Run anyway"
- Add to antivirus exceptions if needed

### Browser Doesn't Open Automatically

**Solution:** Manual navigation
- Open your web browser
- Go to: http://127.0.0.1:5000

## Uninstallation

### For Executable Users
Simply delete the `WI_Excise_Tax_Generator.exe` file

### For Source Users
1. Delete the entire `app/` folder
2. Remove Python virtual environment if created

## Updates

To update to a new version:

1. **Backup your config files** (optional, to preserve settings):
   - Copy `app/config/filer_config.json`
   - Copy `app/config/defaults.json`

2. **Download the new version**

3. **Replace the old files** with new ones

4. **Restore your config files** (if backed up):
   - Copy back to `app/config/`

5. **Test the application**

## Getting Help

- Review the [User Guide](app/docs/USER_GUIDE.md)
- Check the [README](app/README.md)
- For schema updates, see [Schema Update Guide](app/docs/SCHEMA_UPDATE_GUIDE.md)

