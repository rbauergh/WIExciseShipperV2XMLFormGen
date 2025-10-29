# Schema Update Guide

This guide explains how to update the Wisconsin Excise Tax XML Generator to support new schema versions from the Wisconsin Department of Revenue.

## Quick Update Process

When the Wisconsin DOR releases a new schema version:

1. **Replace Schema Files:**
   - Copy the new `.xsd` files to the `schemas/` directory
   - Keep the same filenames: `AB136.xsd` and `AB137.xsd`

2. **Test with Sample Data:**
   - Run the application
   - Generate test XML files
   - Verify validation passes

3. **Update Version Number:**
   - Update the version in the footer of `templates/index.html`

## Detailed Update Instructions

### If Schema Structure Remains Similar

If the new schema only has minor changes (new optional fields, updated enumerations, etc.):

1. **Update Schema Files Only:**
   ```
   app/schemas/AB136.xsd  (replace with new version)
   app/schemas/AB137.xsd  (replace with new version)
   ```

2. **Test the Application:**
   - The XML generator will automatically use the new schema
   - Validation will enforce new rules automatically
   - Test with your CSV import to ensure fields still map correctly

### If Schema Structure Changed Significantly

If the new schema has structural changes (new required fields, renamed elements, etc.):

1. **Update XML Generator (`xml_generator.py`):**
   
   Look for these methods:
   - `_add_common_carrier_shipment()` - Update for AB136 changes
   - `_add_fulfillment_house_shipment()` - Update for AB137 changes
   
   Add or modify field mappings as needed.

2. **Update CSV Mapper (`csv_mapper.py`):**
   
   Update these dictionaries:
   - `COMMON_CARRIER_MAPPINGS` - Map CSV columns to new XML fields
   - `FULFILLMENT_HOUSE_MAPPINGS` - Map CSV columns to new XML fields

3. **Update Web Interface (`templates/index.html`):**
   
   If new required fields were added:
   - Add form inputs in the appropriate sections
   - Add table columns for shipment data

4. **Update JavaScript (`static/script.js`):**
   
   Update these functions if new fields were added:
   - `updateTableHeaders()` - Add new column headers
   - `updateTable()` - Add new table cells
   - `getFilerData()` - Include new filer fields
   - `addShipmentRow()` - Include new shipment fields

## Using an LLM for Updates

If you need to use an LLM (like ChatGPT or Claude) to help with updates, provide:

### Context to Share

```
I need to update the Wisconsin Excise Tax XML Generator to support a new schema version.

Current Schema Version: 0.2
New Schema Version: [VERSION]

The application is a Flask web app that:
- Generates XML from user input
- Validates against XSD schemas
- Imports data from CSV files
- Supports two report types: AB136 (Common Carrier) and AB137 (Fulfillment House)

Key files that may need updating:
1. xml_generator.py - XML generation and structure
2. csv_mapper.py - CSV field mappings
3. templates/index.html - Web form fields
4. static/script.js - Frontend data handling

I'm attaching the new XSD file(s). Please analyze the changes and tell me:
1. What fields were added, removed, or renamed?
2. Which Python files need updates?
3. What specific code changes are required?
```

### Attach These Files

1. The new XSD file(s)
2. Your current `xml_generator.py`
3. Your current `csv_mapper.py`
4. Sample XML from the new schema (if available)

### Example Prompt for Major Changes

```
The Wisconsin DOR released a new schema (attached: AB137_v0.3.xsd).

Comparing to the old schema (v0.2):
- New required field: <LicenseNumber>
- Renamed field: <QuantityOfWine> → <VolumeInLiters>
- New optional field: <WineryLicense>

Please update these files:

1. xml_generator.py - Add the new fields to _add_fulfillment_house_shipment()
2. csv_mapper.py - Update FULFILLMENT_HOUSE_MAPPINGS to include these fields
3. templates/index.html - Add form inputs for the new fields
4. static/script.js - Update the table to display the new fields

Show me exactly what code to change in each file.
```

## Testing Changes

After making updates:

1. **Test with Sample Data:**
   ```python
   python app.py
   ```

2. **Verify Each Report Type:**
   - Generate a Common Carrier XML
   - Generate a Fulfillment House XML
   - Check validation passes

3. **Test CSV Import:**
   - Import sample CSV data
   - Verify fields map correctly
   - Check for any missing mappings

4. **Test Edge Cases:**
   - Optional fields (should work when blank)
   - Required fields (should show error when missing)
   - Date format conversion
   - Number format validation

## Common Schema Changes and Solutions

### New Required Field Added

**Problem:** Schema requires a new field like `<NewField>`

**Solution:**
1. Add to `xml_generator.py`:
   ```python
   etree.SubElement(shipment, 'NewField').text = data['new_field']
   ```

2. Add to form in `index.html`:
   ```html
   <div class="form-group">
       <label>New Field <span class="required">*</span></label>
       <input type="text" id="newField" required>
   </div>
   ```

3. Add to JavaScript `getFilerData()` or `getDefaultsData()`:
   ```javascript
   new_field: document.getElementById('newField').value,
   ```

### Field Renamed

**Problem:** `<OldName>` changed to `<NewName>`

**Solution:**
1. Update XML element name in `xml_generator.py`
2. Update field name in CSV mappings in `csv_mapper.py`
3. Update variable names in JavaScript
4. Update label text in HTML

### Enumeration Values Changed

**Problem:** `<BeverageType>` now allows "Cider" in addition to Beer/Wine/Spirits

**Solution:**
1. XSD automatically allows new values
2. Update dropdown in `index.html`:
   ```html
   <option value="Cider">Cider</option>
   ```

### New Optional Section

**Problem:** Schema adds optional `<Certifications>` section

**Solution:**
1. Add section to XML generator (check if data exists before adding)
2. Add collapsible section in HTML form
3. Make all inputs optional (no `required` attribute)

## Rollback Process

If the update causes issues:

1. **Restore Old Schema Files:**
   ```bash
   cp schemas_backup/AB136.xsd schemas/
   cp schemas_backup/AB137.xsd schemas/
   ```

2. **Restore Old Code:**
   - Use git to revert changes
   - Or restore from backup files

3. **Test Thoroughly:**
   - Ensure application works with old schema
   - Document what went wrong for next attempt

## Version Control Best Practices

1. **Before Making Changes:**
   - Backup current `schemas/` directory
   - Commit all current changes to git
   - Create a new branch for schema update

2. **During Updates:**
   - Commit each file change separately
   - Write clear commit messages
   - Test after each change

3. **After Updates:**
   - Update version number in README
   - Document changes in changelog
   - Rebuild Windows executable

## Getting Help

If you're stuck:

1. **Check Wisconsin DOR Documentation:**
   - Look for migration guides
   - Check for sample XML files
   - Review change logs

2. **Compare Schemas:**
   - Use an XML diff tool to compare old vs new XSD
   - Identify all structural changes
   - List all new/removed/renamed elements

3. **Test Incrementally:**
   - Update one file at a time
   - Test after each change
   - Isolate issues to specific changes

## Maintaining Forward Compatibility

To make future updates easier:

1. **Use Configuration:**
   - Store field mappings in config files where possible
   - Avoid hardcoding field lists

2. **Document Custom Logic:**
   - Comment why specific transformations are needed
   - Note any Wisconsin-specific requirements

3. **Keep Test Data:**
   - Save sample CSV files
   - Keep generated XML examples
   - Maintain validation test cases

## Schema Validation Testing

Create a test script to validate samples:

```python
from xml_generator import XMLGenerator

def test_schema():
    generator = XMLGenerator('FulfillmentHouse')
    
    # Your test data here
    xml = generator.generate_xml(...)
    
    is_valid, error = generator.validate_xml(xml)
    print(f"Valid: {is_valid}")
    if not is_valid:
        print(f"Error: {error}")

if __name__ == '__main__':
    test_schema()
```

Run before and after schema updates to catch regressions.

