# Wisconsin Excise Tax XML Generator

A user-friendly web application for generating compliant XML reports for the Wisconsin Department of Revenue's excise tax requirements.

## Features

- **Two Report Types Supported:**
  - AB136 - Common Carrier Alcohol Beverage Shipment Report
  - AB137 - Fulfillment House Alcohol Beverage Shipment Report

- **Easy Data Entry:**
  - Import shipment data from CSV files
  - Manual data entry with intuitive web form
  - Paste data directly from Excel spreadsheets

- **Configuration Management:**
  - Save and reuse filer information
  - Store default values for common fields
  - Automatic data persistence

- **Validation:**
  - Real-time XSD schema validation
  - Clear error messages
  - Preview generated XML before downloading

- **User-Friendly:**
  - Clean, modern web interface
  - Works on Windows without Python installation (when built as .exe)
  - No technical knowledge required

## Quick Start

### For End Users (Windows .exe)

1. Double-click `WI_Excise_Tax_Generator.exe`
2. Your web browser will automatically open to the application
3. Fill in your information and generate XML files

### For Developers

#### Running from Source

1. Install Python 3.8 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
   Or on Windows, double-click `run.bat`

4. Open your browser to `http://127.0.0.1:5000/`

#### Building Windows Executable

On Windows:
1. Double-click `build.bat`
2. The executable will be created in the `dist` folder

Or manually:
```bash
pip install -r requirements.txt
pip install pyinstaller
pyinstaller build_exe.spec --clean
```

## Usage Guide

### Step 1: Select Report Type
Choose between Common Carrier (AB136) or Fulfillment House (AB137) based on your needs.

### Step 2: Enter Filer Information
- Fill in your business details (TIN, business name, address)
- Click "Save Filer Info" to reuse this information in future sessions

### Step 3: Set Tax Period & Contact
- Enter the tax period begin and end dates
- Provide an acknowledgement email address
- Check "Amended Return" if this is an amended filing

### Step 4: Configure Default Values
- Enter default consignor/manufacturer information that applies to all shipments
- Click "Save Defaults" to persist these values

### Step 5: Import or Enter Shipment Data

#### Option A: Import from CSV
1. Click "Import from CSV" tab
2. Download the CSV template or use your existing format
3. Paste your CSV data into the text area
4. Click "Import & Map CSV Data"
5. Review and edit the imported data as needed

#### Option B: Manual Entry
1. Click "Manual Entry" tab
2. Click "Add Shipment" to add rows
3. Fill in the shipment details in the table

### Step 6: Generate XML
1. Click "Generate & Validate XML"
2. Review the validation status
3. Preview the generated XML
4. Click "Download XML File" to save

## CSV Format

### Common Carrier CSV Format
```csv
Ship To Company,Ship To Street,Ship To City,Ship To State,Ship To Zip,Tracking Nos,Order Date,LB,TYPE
John Doe,123 Main St,Madison,WI,53703,1234567890,2024-01-15,25.5,Wine
```

### Fulfillment House CSV Format
```csv
Ship To Company,Ship To Street,Ship To City,Ship To State,Ship To Zip,Tracking Nos,Order Date,BOTTLE COUNT,SIZE
John Doe,123 Main St,Madison,WI,53703,1234567890,2024-01-15,12,750
```

**Note:** Bottle quantities are automatically converted to liters for Fulfillment House reports.

## File Structure

```
app/
├── app.py                  # Flask application
├── xml_generator.py        # XML generation and validation
├── csv_mapper.py           # CSV import and field mapping
├── config_manager.py       # Configuration management
├── requirements.txt        # Python dependencies
├── build_exe.spec          # PyInstaller configuration
├── build.bat               # Windows build script
├── run.bat                 # Windows run script
├── templates/
│   └── index.html         # Web interface
├── static/
│   ├── style.css          # Styling
│   └── script.js          # Frontend logic
├── schemas/
│   ├── AB136.xsd          # Common Carrier schema
│   └── AB137.xsd          # Fulfillment House schema
├── config/
│   └── filer_config.json  # Saved configurations
├── output/                # Generated XML files
└── docs/
    └── SCHEMA_UPDATE_GUIDE.md
```

## Configuration Files

Configuration files are stored in the `config/` directory:
- `filer_config.json` - Saved filer information
- `defaults.json` - Default values for shipments

These files are automatically created when you save your settings.

## Troubleshooting

### Application won't start
- Ensure Python 3.8+ is installed (for source version)
- Check that port 5000 is not in use by another application
- Try running as administrator (Windows .exe)

### XML validation fails
- Check that all required fields are filled
- Verify date format is YYYY-MM-DD
- Ensure TIN is exactly 9 digits
- Verify permit numbers are exactly 15 digits
- Check that state codes are valid 2-letter abbreviations

### CSV import fails
- Verify CSV has proper headers
- Check for special characters or encoding issues
- Ensure dates are in a recognizable format (MM/DD/YYYY or YYYY-MM-DD)

## Support

For issues or questions:
1. Check the documentation in the `docs/` folder
2. Review the schema documentation files
3. Verify your data matches the Wisconsin DOR requirements

## Version History

- **v1.0** (2024) - Initial release
  - Support for AB136 (Common Carrier) and AB137 (Fulfillment House)
  - CSV import functionality
  - Configuration management
  - XSD validation
  - Windows executable packaging

## License

This tool is provided for use with Wisconsin Department of Revenue excise tax reporting. 
Ensure compliance with all applicable state regulations.

