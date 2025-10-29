# Wisconsin Excise Tax XML Generator - User Guide

## Getting Started

### Installation

#### Windows Executable (Recommended for Non-Technical Users)

1. Download `WI_Excise_Tax_Generator.exe`
2. Double-click to run
3. Your web browser will open automatically
4. No Python installation required!

#### Running from Source (For Developers)

1. Ensure Python 3.8+ is installed
2. Open command prompt in the app folder
3. Run: `python app.py`
4. Browser opens to http://127.0.0.1:5000

## Understanding Report Types

### AB136 - Common Carrier Report

Use this report type if you are a **common carrier** (e.g., FedEx, UPS) shipping alcohol beverages on behalf of others.

**Required Information per Shipment:**
- Consignor (sender) information
- Consignee (recipient) information  
- Shipment date
- Weight of beverages
- Tracking number

### AB137 - Fulfillment House Report

Use this report type if you are a **fulfillment house** shipping wine to consumers.

**Required Information per Shipment:**
- Manufacturer (winery) information
- Consignee (recipient) information
- Shipment date
- Quantity of wine (in liters)
- Wine permit number
- Common carrier permit number

## Step-by-Step Guide

### Step 1: Select Your Report Type

Click on either:
- **AB136 - Common Carrier** - for shipping companies
- **AB137 - Fulfillment House** - for fulfillment operations

### Step 2: Enter Your Business Information

Fill in the "Filer Information" section:

1. **TIN Information:**
   - Select either FEIN or SSN
   - Enter your 9-digit tax ID number
   - Optionally enter State EIN (15 digits)

2. **Business Name:**
   - Line 1 is required (your legal business name)
   - Line 2 is optional (DBA or additional info)

3. **Business Address:**
   - All fields are required except Address Line 2
   - Use 2-letter state code (e.g., WI for Wisconsin)
   - ZIP can be 5 or 9 digits

4. **Save Your Information:**
   - Click "💾 Save Filer Info"
   - Your information will be saved for future use
   - You won't need to re-enter it each quarter

### Step 3: Set Tax Period and Contact

1. **Tax Period Begin:** First day of the reporting quarter (YYYY-MM-DD)
2. **Tax Period End:** Last day of the reporting quarter (YYYY-MM-DD)
3. **Acknowledgement Email:** Where you'll receive confirmation
4. **Amended Return:** Check this box only if correcting a previous submission

**Example Quarterly Dates:**
- Q1: January 1 to March 31
- Q2: April 1 to June 30
- Q3: July 1 to September 30
- Q4: October 1 to December 31

### Step 4: Configure Default Values

These values will be automatically used for all shipments to save time.

#### For Common Carrier:
Fill in your default **Consignor Information** (the typical sender):
- Name and address of the common consignor
- Permit number if applicable

#### For Fulfillment House:
Fill in your default **Manufacturer Information** (the winery):
- Manufacturer name and address
- Wine permit number (15 digits)
- Common carrier permit number (15 digits)

Click "💾 Save Defaults" to persist these values.

### Step 5: Enter Shipment Data

You have two options:

#### Option A: Import from CSV (Recommended)

1. **Prepare Your CSV File:**
   - You can use your existing Excel spreadsheet
   - Click "download a CSV template" to see the required format
   - Save your Excel file as CSV

2. **Copy Your Data:**
   - Open your CSV file in Excel or Notepad
   - Select all data (including headers)
   - Copy (Ctrl+C)

3. **Import:**
   - Click the "📄 Import from CSV" tab
   - Paste your data in the text box (Ctrl+V)
   - Click "📥 Import & Map CSV Data"
   - Your data will be automatically mapped to XML fields

4. **Review and Edit:**
   - Switch to "✍️ Manual Entry" tab
   - Review the imported data in the table
   - Make any necessary corrections
   - Add or delete rows as needed

#### Option B: Manual Entry

1. Click "✍️ Manual Entry" tab
2. Click "➕ Add Shipment" for each shipment
3. Fill in the table cells directly
4. Use "Delete" button to remove unwanted rows

**Editing Tips:**
- Click in any cell to edit
- Tab key moves to next cell
- Changes are saved automatically
- Use "🗑️ Clear All" to start over

### Step 6: Generate Your XML

1. **Review Everything:**
   - Check that all required fields are filled
   - Verify dates are correct
   - Ensure email address is accurate

2. **Generate:**
   - Click "🚀 Generate & Validate XML"
   - Wait for validation to complete

3. **Check Validation:**
   - ✅ **Green message:** XML is valid and ready to submit
   - ❌ **Red message:** There are errors that need fixing
   - Review any error messages carefully

4. **Preview:**
   - Scroll down to see the XML preview
   - Verify the data looks correct

5. **Download:**
   - Click "💾 Download XML File"
   - Save to your computer
   - Submit to Wisconsin DOR according to their instructions

## CSV Format Details

### Common Carrier CSV Format

**Required Columns:**
```
Ship To Company, Ship To Street, Ship To City, Ship To State, Ship To Zip,
Tracking Nos, Order Date, LB, TYPE
```

**Example:**
```csv
Ship To Company,Ship To Street,Ship To City,Ship To State,Ship To Zip,Tracking Nos,Order Date,LB,TYPE
John Doe,123 Main St,Madison,WI,53703,1Z12345,2024-01-15,25.5,Wine
Jane Smith,456 Oak Ave,Milwaukee,WI,53202,1Z67890,2024-01-16,30.2,Beer
```

**Notes:**
- Order Date can be MM/DD/YYYY or YYYY-MM-DD
- LB is weight in pounds (decimal allowed)
- TYPE must be: Beer, Wine, Spirits, or Unknown

### Fulfillment House CSV Format

**Required Columns:**
```
Ship To Company, Ship To Street, Ship To City, Ship To State, Ship To Zip,
Tracking Nos, Order Date, BOTTLE COUNT, SIZE
```

**Example:**
```csv
Ship To Company,Ship To Street,Ship To City,Ship To State,Ship To Zip,Tracking Nos,Order Date,BOTTLE COUNT,SIZE
John Doe,123 Main St,Madison,WI,53703,1Z12345,2024-01-15,12,750
Jane Smith,456 Oak Ave,Milwaukee,WI,53202,1Z67890,2024-01-16,6,750
```

**Notes:**
- BOTTLE COUNT is number of bottles
- SIZE is bottle size in milliliters (typically 750)
- Quantity is automatically converted to liters

## Tips and Best Practices

### Saving Time

1. **Save Your Filer Info:**
   - Do this once at the beginning
   - It will be pre-filled for all future reports

2. **Save Your Defaults:**
   - Set your common consignor or manufacturer info
   - It applies to all shipments automatically
   - Update only when needed

3. **Use CSV Import:**
   - Much faster than manual entry
   - Copy directly from your order management system
   - Review and make small edits after import

### Avoiding Errors

1. **Date Formats:**
   - Use YYYY-MM-DD format when possible
   - Or MM/DD/YYYY - the app will convert it

2. **Required Fields:**
   - Look for the red asterisk (*)
   - These must be filled in

3. **Number Formats:**
   - TIN: exactly 9 digits
   - Permit Numbers: exactly 15 digits
   - Weight/Quantity: decimal numbers allowed

4. **State Codes:**
   - Must be 2-letter codes (e.g., WI, IL, MN)
   - All uppercase

### Quarterly Workflow

1. **Week Before Quarter End:**
   - Verify your filer information is current
   - Update default values if anything changed

2. **After Quarter Ends:**
   - Export your shipment data to CSV
   - Run the generator
   - Review the XML preview carefully

3. **Submit to WI DOR:**
   - Follow their submission instructions
   - Keep a copy of the XML file
   - Save confirmation emails

## Troubleshooting

### Problem: XML Validation Fails

**Solution:**
1. Read the error message carefully
2. Common issues:
   - Missing required fields
   - Wrong date format
   - Invalid state code
   - TIN not 9 digits
   - Permit number not 15 digits
3. Fix the issues and try again

### Problem: CSV Import Fails

**Solution:**
1. Check that your CSV has headers
2. Ensure column names match expected format
3. Remove any special characters
4. Try copying just a few rows first to test

### Problem: Can't Download XML

**Solution:**
1. Check that XML validation passed first
2. Try a different browser
3. Check your download folder settings
4. Disable popup blockers temporarily

### Problem: Browser Doesn't Open

**Solution:**
1. Manually open browser
2. Navigate to: http://127.0.0.1:5000
3. Check that port 5000 isn't blocked by firewall

### Problem: Data Disappears

**Solution:**
1. Click "Save Filer Info" and "Save Defaults" regularly
2. Configuration is saved automatically
3. But shipment data is per-session only
4. Generate XML before closing browser

## Support and Resources

### Wisconsin DOR Resources
- Check Wisconsin DOR website for latest requirements
- Review their XML submission guidelines
- Contact DOR support for filing questions

### Application Help
- Review this guide
- Check README.md for technical details
- See SCHEMA_UPDATE_GUIDE.md for schema changes

### Best Practices
- Keep backups of your generated XML files
- Save your CSV files for each quarter
- Maintain a filing log with submission dates
- Test with sample data before quarter end

## Quick Reference

### File Locations
- **Generated XML:** Automatically downloaded to your Downloads folder
- **Configuration:** Stored in `config/` folder
- **Templates:** Available via "download a CSV template" link

### Keyboard Shortcuts
- **Tab:** Move to next field
- **Ctrl+C / Ctrl+V:** Copy and paste data
- **Enter:** Submit current form section

### Important Numbers
- **TIN:** 9 digits (no dashes)
- **State EIN:** 15 digits
- **Permit Numbers:** 15 digits
- **ZIP Code:** 5 or 9 digits

### Date Format
- **Preferred:** YYYY-MM-DD (2024-03-31)
- **Accepted:** MM/DD/YYYY (03/31/2024)
- **Quarter Ends:** 03-31, 06-30, 09-30, 12-31

