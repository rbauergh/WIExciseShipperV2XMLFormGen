# Wisconsin Excise Tax XML Form Generator

A user-friendly desktop application for generating Wisconsin Department of Revenue excise tax XML reports. Built with Flask, this application provides a web-based interface that can be packaged as a standalone Windows executable.

## 🎯 Features

- **Dual Report Support**: Generate both AB136 (Common Carrier) and AB137 (Fulfillment House) reports
- **CSV Import**: Easily import shipment data from spreadsheets
- **XSD Validation**: Built-in schema validation ensures compliance
- **Configuration Management**: Save and reuse filer information
- **Windows Executable**: No Python installation required for end users
- **User-Friendly Interface**: Clean, modern web UI designed for non-technical users

## 📋 Quick Start

### For End Users

1. Download `WI_Excise_Tax_Generator.exe`
2. Double-click to run
3. Your browser opens automatically
4. Generate compliant XML files!

See [INSTALLATION.md](INSTALLATION.md) for detailed instructions.

### For Developers

```bash
cd app/
pip install -r requirements.txt
python app.py
```

See [app/README.md](app/README.md) for full developer documentation.

## 📁 Project Structure

```
WIExciseShipperV2XMLFormGen/
├── README.md                    # This file
├── INSTALLATION.md              # Installation guide
│
├── app/                         # Main application
│   ├── app.py                   # Flask application
│   ├── xml_generator.py         # XML generation and validation
│   ├── csv_mapper.py            # CSV import logic
│   ├── config_manager.py        # Configuration management
│   ├── requirements.txt         # Python dependencies
│   ├── test_setup.py            # Setup verification script
│   │
│   ├── build_exe.spec           # PyInstaller configuration
│   ├── build.bat                # Windows build script
│   ├── run.bat                  # Windows run script
│   │
│   ├── templates/               # HTML templates
│   │   └── index.html
│   │
│   ├── static/                  # Frontend assets
│   │   ├── style.css
│   │   └── script.js
│   │
│   ├── schemas/                 # XSD schema files
│   │   ├── AB136.xsd            # Common Carrier schema
│   │   └── AB137.xsd            # Fulfillment House schema
│   │
│   ├── config/                  # Saved configurations
│   │   └── (auto-generated)
│   │
│   ├── output/                  # Generated XML files
│   │   └── (auto-generated)
│   │
│   └── docs/                    # Documentation
│       ├── USER_GUIDE.md        # End-user guide
│       └── SCHEMA_UPDATE_GUIDE.md
│
├── WIExciseShipperV0.2/         # Schema reference files
│   ├── AB136.xsd
│   ├── AB137.xsd
│   └── Documentation/
│
└── ref/                         # Reference data
    ├── Copy of FulfillmentHouse.csv
    └── WISCONSIN SHIPPING.csv
```

## 🚀 Usage Overview

### 1. Select Report Type
Choose between Common Carrier (AB136) or Fulfillment House (AB137)

### 2. Enter Filer Information
Fill in your business details once, save for future use

### 3. Configure Defaults
Set default consignor/manufacturer information

### 4. Import Data
- Paste CSV data directly from Excel
- Or download a template and fill it out
- Or enter data manually

### 5. Generate XML
Click generate, review validation, and download your compliant XML

See [app/docs/USER_GUIDE.md](app/docs/USER_GUIDE.md) for detailed instructions.

## 📊 CSV Format

### Common Carrier
```csv
Ship To Company,Ship To Street,Ship To City,Ship To State,Ship To Zip,Tracking Nos,Order Date,LB,TYPE
John Doe,123 Main St,Madison,WI,53703,1Z12345,2024-01-15,25.5,Wine
```

### Fulfillment House
```csv
Ship To Company,Ship To Street,Ship To City,Ship To State,Ship To Zip,Tracking Nos,Order Date,BOTTLE COUNT,SIZE
John Doe,123 Main St,Madison,WI,53703,1Z12345,2024-01-15,12,750
```

## 🔧 Building the Windows Executable

### Prerequisites
- **Windows machine** (or Windows VM)
- **Python 3.8+** installed
- **All dependencies** installed

### Build Steps

#### Option 1: Using the Build Script (Easiest)

1. Open Command Prompt or PowerShell
2. Navigate to the app directory:
   ```cmd
   cd app\
   ```
3. Run the build script:
   ```cmd
   build.bat
   ```
4. Wait for the build to complete (takes 1-3 minutes)
5. Find your executable in `app\dist\WI_Excise_Tax_Generator.exe`

#### Option 2: Manual Build

```bash
cd app/
pip install -r requirements.txt
pip install pyinstaller
pyinstaller build_exe.spec --clean --noconfirm
```

### What You Get

After building, you'll have a **single standalone .exe file** at:
```
app/dist/WI_Excise_Tax_Generator.exe
```

This file:
- ✅ Runs on any Windows machine (7, 10, 11+)
- ✅ **No Python installation required** on target machines
- ✅ Includes all dependencies bundled in
- ✅ Opens browser automatically when run
- ✅ Can be distributed to non-technical users

### Distributing to Users

Simply give them the `WI_Excise_Tax_Generator.exe` file. They:
1. Save it anywhere on their computer
2. Double-click to run
3. Start generating XML files!

**Optional:** Include the [QUICK_START.md](QUICK_START.md) guide for first-time users.

### Troubleshooting Build Issues

**"PyInstaller not found":**
```bash
pip install pyinstaller
```

**"Module not found" errors:**
```bash
pip install -r requirements.txt --upgrade
```

**Build fails:**
```bash
# Clean and try again
pyinstaller build_exe.spec --clean --noconfirm
```

### Cross-Platform Note

⚠️ **You must build on Windows to create a Windows .exe**

If you're on Mac/Linux and need a Windows executable:
- Use a Windows VM (VirtualBox, Parallels, VMware)
- Use a Windows cloud instance (AWS, Azure)
- Ask a colleague with Windows to build it
- Use GitHub Actions (can automate Windows builds)

The executable will be in `app/dist/WI_Excise_Tax_Generator.exe`

## 📝 Testing

Verify your installation:
```bash
cd app/
python test_setup.py
```

This will check:
- Required Python packages
- Schema files
- Directory structure  
- XML generation functionality

## 🔄 Updating to New Schemas

When Wisconsin DOR releases new schema versions:

1. Replace schema files in `app/schemas/`
2. Test with sample data
3. See [app/docs/SCHEMA_UPDATE_GUIDE.md](app/docs/SCHEMA_UPDATE_GUIDE.md) for detailed instructions

For major schema changes, the guide includes prompts for using LLMs (ChatGPT, Claude) to assist with updates.

## 📚 Documentation

- **[INSTALLATION.md](INSTALLATION.md)** - Installation instructions
- **[app/README.md](app/README.md)** - Developer documentation
- **[app/docs/USER_GUIDE.md](app/docs/USER_GUIDE.md)** - End-user guide
- **[app/docs/SCHEMA_UPDATE_GUIDE.md](app/docs/SCHEMA_UPDATE_GUIDE.md)** - Schema update instructions

## 🛠 Technology Stack

- **Backend**: Python 3.8+, Flask
- **XML Processing**: lxml with XSD validation
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Packaging**: PyInstaller for Windows executable
- **Schemas**: Wisconsin DOR AB136 & AB137 (v0.2)

## ✅ System Requirements

**Minimum:**
- Windows 7+ (for .exe) or any OS with Python 3.8+
- 512 MB RAM
- 50 MB disk space
- Modern web browser

**Recommended:**
- Windows 10+
- 2 GB RAM
- Chrome or Firefox

## 🎨 Recent Improvements

### Automatic Data Cleaning
- ✅ **15+ date formats** accepted and auto-converted (10/29/2025, Oct 29 2025, etc.)
- ✅ **40+ column name variations** recognized (Address, Ship To Street, etc.)
- ✅ **Periods auto-removed** from street addresses (N. Main St → N Main St)
- ✅ **ZIP codes auto-cleaned** (removes dashes, pads with zeros)
- ✅ **Bottles to liters** calculated automatically
- ✅ **Beverage types** normalized (wine → Wine)

### Enhanced Error Messages
- 📍 **Exact field location** (which step, which section)
- ❌ **Shows invalid value** when possible
- ⚠️ **Identifies specific issues** (too short, has period, etc.)
- 💡 **Quick fix suggestions** with examples
- ✅ **Step-by-step instructions** to resolve
- 🔄 **Iterative workflow** clearly explained

### Schema Bug Fixes
- 🐛 **October date bug fixed** - Original schema rejected month 10
- 📝 **Documented for Wisconsin DOR** to fix upstream
- ✅ **All quarters now supported** (Q1-Q4)

See [AUTO_CONVERSIONS.md](AUTO_CONVERSIONS.md) and [HELP_FEATURES.md](HELP_FEATURES.md) for details.

## 🐛 Troubleshooting

**Application won't start:**
- Check Python version (3.8+)
- Verify port 5000 is available
- Run as administrator if needed

**Validation fails:**
- Read the error message carefully - it tells you exactly what to fix!
- Error messages show the exact field and step number
- Follow the numbered instructions to resolve
- Click Generate again after each fix

**CSV import issues:**
- Make sure row 1 has column headers
- The app accepts many column name variations
- Periods in addresses are auto-removed
- Dates are auto-converted from common formats

**Re-importing doesn't help:**
- Fill in Step 4 (Default Values) completely
- Defaults are re-applied each time you Generate
- Use the error message to find the specific field

See [app/docs/USER_GUIDE.md](app/docs/USER_GUIDE.md) for comprehensive troubleshooting.

## 📄 License

This tool is provided for use with Wisconsin Department of Revenue excise tax reporting requirements. Ensure compliance with all applicable state regulations.

## 🤝 Support

For technical issues with the application:
- Review the documentation in `/app/docs/`
- Check the troubleshooting sections
- Verify your data matches schema requirements

For Wisconsin DOR reporting requirements:
- Visit the Wisconsin Department of Revenue website
- Review their official documentation
- Contact their support for filing questions

## 🔮 Future Enhancements

Potential improvements for future versions:
- Batch processing of multiple CSV files
- Export to multiple formats
- Automated submission to WI DOR (if API becomes available)
- Support for additional report types
- Multi-language support
- Cloud-based version

## 📋 Version History

**v1.0** (2024)
- Initial release
- Support for AB136 and AB137 schemas (v0.2)
- CSV import functionality
- Configuration management
- XSD validation
- Windows executable packaging
- Comprehensive documentation

---

**Built for the Wisconsin Department of Revenue excise tax reporting requirements**

**Schema Version:** 0.2 (April 30, 2024)

