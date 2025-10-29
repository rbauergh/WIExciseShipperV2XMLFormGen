"""
XML Generator for Wisconsin Department of Revenue Excise Tax Reports
Supports AB136 (Common Carrier) and AB137 (Fulfillment House) schemas
"""

from lxml import etree
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import os
import re


class XMLGenerator:
    """Generate and validate XML files for WI DOR excise tax reports"""
    
    SCHEMA_DIR = os.path.join(os.path.dirname(__file__), 'schemas')
    
    SCHEMA_TYPES = {
        'CommonCarrier': 'AB136.xsd',
        'FulfillmentHouse': 'AB137.xsd'
    }
    
    def __init__(self, report_type: str):
        """
        Initialize XML generator
        
        Args:
            report_type: 'CommonCarrier' or 'FulfillmentHouse'
        """
        if report_type not in self.SCHEMA_TYPES:
            raise ValueError(f"Invalid report type. Must be one of {list(self.SCHEMA_TYPES.keys())}")
        
        self.report_type = report_type
        self.schema_file = os.path.join(self.SCHEMA_DIR, self.SCHEMA_TYPES[report_type])
        
        # Load and parse the XSD schema
        with open(self.schema_file, 'rb') as f:
            schema_doc = etree.parse(f)
            self.schema = etree.XMLSchema(schema_doc)
    
    def generate_xml(self, filer_data: Dict, shipments: List[Dict], 
                     tax_period_begin: str, tax_period_end: str,
                     ack_email: str, amended: bool = False) -> str:
        """
        Generate XML document
        
        Args:
            filer_data: Dictionary with filer information
            shipments: List of shipment dictionaries
            tax_period_begin: Tax period begin date (YYYY-MM-DD)
            tax_period_end: Tax period end date (YYYY-MM-DD)
            ack_email: Acknowledgement email address
            amended: Whether this is an amended return
            
        Returns:
            XML string
        """
        # Create root element
        root_tag = self.report_type
        root = etree.Element(root_tag)
        
        # Add tax period dates
        etree.SubElement(root, 'TaxPeriodBeginDate').text = tax_period_begin
        etree.SubElement(root, 'TaxPeriodEndDate').text = tax_period_end
        
        # Add filer information
        filer = etree.SubElement(root, 'Filer')
        
        # TIN
        tin = etree.SubElement(filer, 'TIN')
        etree.SubElement(tin, 'TypeTIN').text = filer_data.get('tin_type', 'FEIN')
        etree.SubElement(tin, 'TINTypeValue').text = filer_data['tin_value']
        
        # State EIN (optional)
        if filer_data.get('state_ein'):
            etree.SubElement(filer, 'StateEIN').text = filer_data['state_ein']
        
        # Business Name
        name = etree.SubElement(filer, 'Name')
        etree.SubElement(name, 'BusinessNameLine1').text = filer_data['business_name_line1']
        if filer_data.get('business_name_line2'):
            etree.SubElement(name, 'BusinessNameLine2').text = filer_data['business_name_line2']
        
        # Address
        address = etree.SubElement(filer, 'Address')
        etree.SubElement(address, 'AddressLine1').text = filer_data['address_line1']
        if filer_data.get('address_line2'):
            etree.SubElement(address, 'AddressLine2').text = filer_data['address_line2']
        etree.SubElement(address, 'City').text = filer_data['city']
        etree.SubElement(address, 'State').text = filer_data['state']
        etree.SubElement(address, 'ZIP').text = filer_data['zip']
        
        # Acknowledgement email
        etree.SubElement(root, 'AckAddress').text = ack_email
        
        # Amended return indicator
        if amended:
            etree.SubElement(root, 'AmendedReturnIndicator').text = 'X'
        
        # Add shipments
        for shipment_data in shipments:
            if self.report_type == 'CommonCarrier':
                self._add_common_carrier_shipment(root, shipment_data)
            else:
                self._add_fulfillment_house_shipment(root, shipment_data)
        
        return self._to_xml_string(root)
    
    def _add_common_carrier_shipment(self, root, data: Dict):
        """Add a Common Carrier shipment element"""
        shipment = etree.SubElement(root, 'Shipment')
        
        # Consignor Name and Address
        etree.SubElement(shipment, 'ConsignorName').text = data['consignor_name']
        consignor_addr = etree.SubElement(shipment, 'ConsignorAddress')
        etree.SubElement(consignor_addr, 'AddressLine1').text = data['consignor_address_line1']
        if data.get('consignor_address_line2'):
            etree.SubElement(consignor_addr, 'AddressLine2').text = data['consignor_address_line2']
        etree.SubElement(consignor_addr, 'City').text = data['consignor_city']
        etree.SubElement(consignor_addr, 'State').text = data['consignor_state']
        etree.SubElement(consignor_addr, 'ZIP').text = data['consignor_zip']
        
        # Permit Number (optional)
        if data.get('permit_number'):
            etree.SubElement(shipment, 'PermitNumber').text = data['permit_number']
        
        # Consignee Name and Address
        etree.SubElement(shipment, 'ConsigneeName').text = data['consignee_name']
        consignee_addr = etree.SubElement(shipment, 'ConsigneeAddress')
        etree.SubElement(consignee_addr, 'AddressLine1').text = data['consignee_address_line1']
        if data.get('consignee_address_line2'):
            etree.SubElement(consignee_addr, 'AddressLine2').text = data['consignee_address_line2']
        etree.SubElement(consignee_addr, 'City').text = data['consignee_city']
        etree.SubElement(consignee_addr, 'State').text = data['consignee_state']
        etree.SubElement(consignee_addr, 'ZIP').text = data['consignee_zip']
        
        # Shipment Date
        etree.SubElement(shipment, 'ShipmentDate').text = data['shipment_date']
        
        # Beverage Type (optional)
        if data.get('beverage_type'):
            etree.SubElement(shipment, 'BeverageType').text = data['beverage_type']
        
        # Weight of Beverages
        etree.SubElement(shipment, 'WeightOfBeverages').text = str(data['weight_of_beverages'])
        
        # Tracking Number
        etree.SubElement(shipment, 'TrackingNumber').text = data.get('tracking_number', '')
        
        # Bill of Lading Number (optional)
        if data.get('bill_of_lading_number'):
            etree.SubElement(shipment, 'BillOfLadingNumber').text = data['bill_of_lading_number']
    
    def _add_fulfillment_house_shipment(self, root, data: Dict):
        """Add a Fulfillment House shipment element"""
        shipment = etree.SubElement(root, 'Shipment')
        
        # Manufacturer Address
        mfr_addr = etree.SubElement(shipment, 'ManufacturerAddress')
        etree.SubElement(mfr_addr, 'AddressLine1').text = data['manufacturer_address_line1']
        if data.get('manufacturer_address_line2'):
            etree.SubElement(mfr_addr, 'AddressLine2').text = data['manufacturer_address_line2']
        etree.SubElement(mfr_addr, 'City').text = data['manufacturer_city']
        etree.SubElement(mfr_addr, 'State').text = data['manufacturer_state']
        etree.SubElement(mfr_addr, 'ZIP').text = data['manufacturer_zip']
        
        # Wine Permit Number
        etree.SubElement(shipment, 'WinePermitNumber').text = data['wine_permit_number']
        
        # Manufacturer Name
        etree.SubElement(shipment, 'ManufacturerName').text = data['manufacturer_name']
        
        # Consignee Name and Address
        etree.SubElement(shipment, 'ConsigneeName').text = data['consignee_name']
        consignee_addr = etree.SubElement(shipment, 'ConsigneeAddress')
        etree.SubElement(consignee_addr, 'AddressLine1').text = data['consignee_address_line1']
        if data.get('consignee_address_line2'):
            etree.SubElement(consignee_addr, 'AddressLine2').text = data['consignee_address_line2']
        etree.SubElement(consignee_addr, 'City').text = data['consignee_city']
        etree.SubElement(consignee_addr, 'State').text = data['consignee_state']
        etree.SubElement(consignee_addr, 'ZIP').text = data['consignee_zip']
        
        # Shipment Date
        etree.SubElement(shipment, 'ShipmentDate').text = data['shipment_date']
        
        # Tracking Number
        etree.SubElement(shipment, 'TrackingNumber').text = data.get('tracking_number', '')
        
        # Common Carrier Permit Number
        etree.SubElement(shipment, 'CommonCarrierPermitNumber').text = data['common_carrier_permit_number']
        
        # Quantity of Wine (in liters)
        etree.SubElement(shipment, 'QuantityOfWine').text = str(data['quantity_of_wine'])
        
        # Different Consignor (optional)
        if data.get('different_consignor_name'):
            diff_consignor = etree.SubElement(shipment, 'DifferentConsignor')
            etree.SubElement(diff_consignor, 'ConsignorName').text = data['different_consignor_name']
            
            diff_addr = etree.SubElement(diff_consignor, 'ConsignorAddress')
            etree.SubElement(diff_addr, 'AddressLine1').text = data['different_consignor_address_line1']
            if data.get('different_consignor_address_line2'):
                etree.SubElement(diff_addr, 'AddressLine2').text = data['different_consignor_address_line2']
            etree.SubElement(diff_addr, 'City').text = data['different_consignor_city']
            etree.SubElement(diff_addr, 'State').text = data['different_consignor_state']
            etree.SubElement(diff_addr, 'ZIP').text = data['different_consignor_zip']
    
    def _to_xml_string(self, root) -> str:
        """Convert XML element to formatted string"""
        return etree.tostring(
            root,
            pretty_print=True,
            xml_declaration=True,
            encoding='UTF-8'
        ).decode('utf-8')
    
    def validate_xml(self, xml_string: str) -> Tuple[bool, Optional[str]]:
        """
        Validate XML against the schema with enhanced error messages
        
        Args:
            xml_string: XML document as string
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            doc = etree.fromstring(xml_string.encode('utf-8'))
            self.schema.assertValid(doc)
            return True, None
        except etree.DocumentInvalid as e:
            # Enhance error message with context and tips
            error_msg = str(e)
            enhanced_msg = self._enhance_validation_error(error_msg, xml_string)
            return False, enhanced_msg
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    def _enhance_validation_error(self, error_msg: str, xml_string: str) -> str:
        """
        Enhance validation error messages with context and helpful tips for non-technical users
        
        Args:
            error_msg: Original error message
            xml_string: The XML being validated
            
        Returns:
            Enhanced error message with clear, actionable tips
        """
        enhanced = "❌ VALIDATION FAILED - Please Fix the Following:\n\n"
        enhanced += "═" * 60 + "\n\n"
        enhanced += "⚠️  NOTE: Fixing one error at a time - there may be more after you fix this one.\n"
        enhanced += "    Just fix this issue and click 'Generate & Validate' again to check for others.\n\n"
        enhanced += "═" * 60 + "\n\n"
        
        # Add context about where the error occurred
        if "AddressLine1" in error_msg:
            # Extract the problematic value and line number
            invalid_value = ""
            line_number = None
            value_match = re.search(r"value '([^']*)'", error_msg)
            if value_match:
                invalid_value = value_match.group(1)
            line_match = re.search(r"line (\d+)", error_msg)
            if line_match:
                line_number = int(line_match.group(1))
            
            # Determine which address is missing by looking at the XML context
            # We'll search for the invalid value to see where it appears
            location = ""
            step_num = ""
            section = ""
            
            # Split XML into lines to analyze context around the error
            xml_lines = xml_string.split('\n')
            
            # Find the context by looking at what comes BEFORE the AddressLine1 in the XML
            if line_number and line_number <= len(xml_lines):
                # Look backwards from error line to find which section we're in
                for i in range(line_number - 1, max(0, line_number - 20), -1):
                    if i < len(xml_lines):
                        line = xml_lines[i]
                        if '<Filer>' in line:
                            location = "YOUR BUSINESS ADDRESS"
                            step_num = "2"
                            section = "Filer Information"
                            break
                        elif '<ConsignorAddress>' in line:
                            location = "SENDER'S ADDRESS (Consignor)"
                            step_num = "4"
                            section = "Default Consignor Information"
                            break
                        elif '<ManufacturerAddress>' in line:
                            location = "MANUFACTURER'S ADDRESS (Winery)"
                            step_num = "4"
                            section = "Default Manufacturer Information"
                            break
                        elif '<ConsigneeAddress>' in line:
                            location = "RECIPIENT'S ADDRESS (Consignee)"
                            step_num = "5"
                            section = "shipment data (from CSV or table)"
                            break
            
            # Fallback if we couldn't determine from line number
            if not location:
                if "<ConsignorAddress>" in xml_string:
                    location = "SENDER'S ADDRESS (Consignor)"
                    step_num = "4"
                    section = "Default Consignor Information"
                elif "<ManufacturerAddress>" in xml_string:
                    location = "MANUFACTURER'S ADDRESS (Winery)"
                    step_num = "4"
                    section = "Default Manufacturer Information"
                elif "<ConsigneeAddress>" in xml_string:
                    location = "RECIPIENT'S ADDRESS (Consignee)"
                    step_num = "5"
                    section = "shipment data (from CSV or table)"
                else:
                    location = "YOUR BUSINESS ADDRESS"
                    step_num = "2"
                    section = "Filer Information"
            
            # Show the invalid value if we found one
            if invalid_value:
                enhanced += f"🔍 PROBLEM: Invalid street address in {location}\n\n"
                enhanced += f"❌ INVALID ADDRESS: \"{invalid_value}\"\n\n"
                
                # Check for periods (most common issue)
                if '.' in invalid_value:
                    clean_addr = invalid_value.replace('.', '')
                    enhanced += f"⚠️  Issue: Contains period (.)\n"
                    enhanced += f"💡 Quick Fix: Change \"{invalid_value}\" to \"{clean_addr}\"\n\n"
            else:
                enhanced += f"🔍 PROBLEM: Missing or empty street address in {location}\n\n"
            
            enhanced += f"📋 WHERE TO FIX: Go to Step {step_num} - {section}\n\n"
            enhanced += "✅ HOW TO FIX:\n\n"
            
            if "Consignor" in location or "Manufacturer" in location:
                enhanced += "  1. Scroll up to Step 4: Default Values\n"
                enhanced += f"  2. Find the '{section}' section\n"
                enhanced += "  3. Fill in the 'Address Line 1' field (REQUIRED)\n"
                enhanced += "     Example: 123 Main Street\n"
                enhanced += "  4. Click '💾 Save Defaults'\n"
                enhanced += "  5. Scroll back down and click 'Generate & Validate' again\n\n"
                enhanced += "⚠️  IMPORTANT: This address will be used for ALL shipments in your report.\n"
                enhanced += "    Make sure it's the correct sender/manufacturer address!\n"
            elif "Consignee" in location or "RECIPIENT" in location:
                if invalid_value and '.' in invalid_value:
                    # Specific issue with period
                    enhanced += "  The recipient address has a PERIOD (.) which isn't allowed!\n\n"
                    clean_addr = invalid_value.replace('.', '')
                    enhanced += f"  EASIEST FIX - Re-import your CSV (periods will be auto-removed):\n"
                    enhanced += "     1. Go to Step 5\n"
                    enhanced += "     2. Click 'Import from CSV' tab\n"
                    enhanced += "     3. Paste your CSV data again\n"
                    enhanced += "     4. Click Import (addresses will be automatically cleaned)\n"
                    enhanced += "     5. Click Generate again\n\n"
                    enhanced += f"  OR manually edit the address in the table:\n"
                    enhanced += f"     1. Go to Step 5, look at the shipment table\n"
                    enhanced += f"     2. Find the address: \"{invalid_value}\"\n"
                    enhanced += f"     3. Change it to: \"{clean_addr}\" (remove the period)\n"
                    enhanced += f"     4. Click Generate again\n"
                elif invalid_value == "" or not invalid_value:
                    enhanced += "  A recipient address is empty!\n\n"
                    enhanced += "  Option 1 - If using CSV import:\n"
                    enhanced += "     • Your CSV file has a blank 'Address' field for one of the rows\n"
                    enhanced += "     • Fix it in your CSV and re-import\n\n"
                    enhanced += "  Option 2 - If entering manually:\n"
                    enhanced += "     • Look at the shipment table in Step 5\n"
                    enhanced += "     • Find the row with blank 'Address'\n"
                    enhanced += "     • Fill it in\n"
                else:
                    enhanced += "  Option 1 - Re-import CSV (easiest - auto-cleans addresses):\n"
                    enhanced += "     • Go to Step 5, click 'Import from CSV' tab\n"
                    enhanced += "     • Paste your CSV again\n"
                    enhanced += "     • Click Import\n\n"
                    enhanced += "  Option 2 - Edit manually:\n"
                    enhanced += "     • Look at the shipment table in Step 5\n"
                    enhanced += f"     • Find and fix the address: \"{invalid_value}\"\n"
                    enhanced += "     • Remove any special characters except - and /\n"
            else:
                enhanced += "  1. Go to Step 2: Filer Information\n"
                enhanced += "  2. Fill in 'Address Line 1' (REQUIRED)\n"
                enhanced += "     This is YOUR company's street address\n"
                enhanced += "     Example: 456 Business Blvd\n"
                enhanced += "  3. Click '💾 Save Filer Info'\n"
        
        elif "TIN" in error_msg or "TINTypeValue" in error_msg:
            enhanced += "🔍 PROBLEM: Tax ID Number (TIN) is missing or incorrect\n\n"
            enhanced += "📋 WHERE TO FIX: Step 2 - Filer Information\n\n"
            enhanced += "✅ HOW TO FIX:\n\n"
            enhanced += "  1. Go to Step 2: Filer Information\n"
            enhanced += "  2. Find the 'TIN Value' field\n"
            enhanced += "  3. Enter your 9-digit Tax ID Number\n\n"
            enhanced += "  IMPORTANT FORMATTING RULES:\n"
            enhanced += "     ✓ Must be EXACTLY 9 digits\n"
            enhanced += "     ✓ NO dashes or spaces\n"
            enhanced += "     ✓ Numbers only\n\n"
            enhanced += "  Examples:\n"
            enhanced += "     ❌ WRONG: 12-3456789 (has dashes)\n"
            enhanced += "     ❌ WRONG: 123456 (too short)\n"
            enhanced += "     ✅ CORRECT: 123456789\n\n"
            enhanced += "  4. Click '💾 Save Filer Info'\n"
        
        elif "PermitNumber" in error_msg or "WinePermitNumber" in error_msg or "CommonCarrierPermitNumber" in error_msg:
            enhanced += "🔍 PROBLEM: Permit Number is missing or incorrect\n\n"
            enhanced += "📋 WHERE TO FIX: Step 4 - Default Values\n\n"
            enhanced += "✅ HOW TO FIX:\n\n"
            enhanced += "  1. Go to Step 4: Default Values\n"
            if "Wine" in error_msg:
                enhanced += "  2. Find 'Wine Permit Number'\n"
            elif "CommonCarrier" in error_msg:
                enhanced += "  2. Find 'Common Carrier Permit Number'\n"
            else:
                enhanced += "  2. Find the permit number field\n"
            enhanced += "  3. Enter the 15-digit permit number\n\n"
            enhanced += "  IMPORTANT FORMATTING RULES:\n"
            enhanced += "     ✓ Must be EXACTLY 15 digits\n"
            enhanced += "     ✓ Add zeros at the start if needed\n"
            enhanced += "     ✓ Numbers only, no letters or symbols\n\n"
            enhanced += "  Examples:\n"
            enhanced += "     ❌ WRONG: 123456 (too short)\n"
            enhanced += "     ✅ CORRECT: 000000000123456 (padded with zeros)\n"
            enhanced += "     ✅ CORRECT: 123456789012345 (already 15 digits)\n\n"
            enhanced += "  4. Click '💾 Save Defaults'\n"
        
        elif "Date" in error_msg or "YYYY-MM-DD" in error_msg:
            # Try to extract the invalid date value from the error message
            invalid_date = ""
            match = re.search(r"value '([^']*)'", error_msg)
            if match:
                invalid_date = match.group(1)
            
            # Try to determine which date field
            date_field = "Unknown date field"
            if "TaxPeriodBeginDate" in error_msg:
                date_field = "📍 TAX PERIOD BEGIN DATE (Step 3)"
            elif "TaxPeriodEndDate" in error_msg:
                date_field = "📍 TAX PERIOD END DATE (Step 3)"
            elif "ShipmentDate" in error_msg or "<Shipment>" in xml_string:
                date_field = "📍 SHIPMENT DATE (in your shipment data)"
            
            enhanced += "🔍 PROBLEM: Date could not be understood or is invalid\n\n"
            
            if invalid_date:
                enhanced += f"❌ INVALID DATE: \"{invalid_date}\"\n\n"
            
            enhanced += f"{date_field}\n\n"
            
            enhanced += "ℹ️  NOTE: The app automatically converts most date formats for you!\n"
            enhanced += "   Common formats like 10/29/2025, 3/31/24, Oct 29 2025 all work.\n"
            enhanced += "   This error usually means the date is blank or truly unreadable.\n\n"
            enhanced += "✅ HOW TO FIX:\n\n"
            
            if invalid_date:
                if not invalid_date or invalid_date.strip() == "":
                    enhanced += "  The date is EMPTY - you need to fill it in!\n\n"
                    enhanced += "  For Tax Period dates:\n"
                    enhanced += "     • Go to Step 3\n"
                    enhanced += "     • Click the calendar icon\n"
                    enhanced += "     • Select the correct date\n\n"
                    enhanced += "  For Shipment dates:\n"
                    enhanced += "     • Check your CSV file - make sure the Date column isn't blank\n"
                    enhanced += "     • Or edit the shipment table in Step 5\n"
                else:
                    enhanced += f"  The value \"{invalid_date}\" is not a recognizable date.\n\n"
                    enhanced += "  What to do:\n"
                    enhanced += "     1. Check if this is really a date (not random text)\n"
                    enhanced += "     2. Use a standard format like: 10/29/2025 or 2025-10-29\n"
                    enhanced += "     3. Or use the date picker (calendar icon) for guaranteed format\n\n"
            
            enhanced += "  The app accepts these formats (and auto-converts them):\n"
            enhanced += "     ✓ 10/29/2025 (American format)\n"
            enhanced += "     ✓ 10/29/25 (short year)\n"
            enhanced += "     ✓ 2024-03-31 (official format)\n"
            enhanced += "     ✓ October 29, 2025 (with month name)\n"
            enhanced += "     ✓ Oct 29 2025 (abbreviated)\n\n"
            enhanced += "  Only these cause errors:\n"
            enhanced += "     ❌ (blank/empty)\n"
            enhanced += "     ❌ 2025 (year only)\n"
            enhanced += "     ❌ random text that's not a date\n\n"
            enhanced += "  💡 BEST TIP: Use the calendar picker - click the calendar icon next to the date field!\n"
        
        elif "Email" in error_msg or "AckAddress" in error_msg:
            enhanced += "🔍 PROBLEM: Email address is missing or invalid\n\n"
            enhanced += "📋 WHERE TO FIX: Step 3 - Tax Period & Contact\n\n"
            enhanced += "✅ HOW TO FIX:\n\n"
            enhanced += "  1. Go to Step 3: Tax Period & Contact\n"
            enhanced += "  2. Find 'Acknowledgement Email'\n"
            enhanced += "  3. Enter a valid email address\n\n"
            enhanced += "  Email format must include:\n"
            enhanced += "     • Username before the @\n"
            enhanced += "     • @ symbol in the middle\n"
            enhanced += "     • Domain name after the @\n\n"
            enhanced += "  Examples:\n"
            enhanced += "     ❌ WRONG: john.doe (missing @domain.com)\n"
            enhanced += "     ❌ WRONG: @company.com (missing username)\n"
            enhanced += "     ✅ CORRECT: john.doe@company.com\n"
            enhanced += "     ✅ CORRECT: reports@business.org\n"
        
        elif "State" in error_msg:
            # Try to extract the invalid state value
            invalid_state = ""
            match = re.search(r"value '([^']*)'", error_msg)
            if match:
                invalid_state = match.group(1)
            
            enhanced += "🔍 PROBLEM: State code is invalid or missing\n\n"
            
            if invalid_state:
                enhanced += f"❌ INVALID STATE CODE: \"{invalid_state}\"\n\n"
            
            # Determine which state field
            location = "Unknown location"
            if "<Filer>" in xml_string and xml_string.find("<Filer>") < xml_string.find("</Filer>"):
                location = "📍 YOUR BUSINESS STATE (Step 2: Filer Information)"
            elif "<ConsignorAddress>" in xml_string:
                location = "📍 CONSIGNOR STATE (Step 4: Default Consignor Information)"
            elif "<ManufacturerAddress>" in xml_string:
                location = "📍 MANUFACTURER STATE (Step 4: Default Manufacturer Information)"
            elif "<ConsigneeAddress>" in xml_string:
                location = "📍 RECIPIENT STATE (from your CSV data or Step 5 table)"
            
            enhanced += f"{location}\n\n"
            enhanced += "✅ HOW TO FIX:\n\n"
            enhanced += "  State codes MUST be 2 uppercase letters\n\n"
            
            if invalid_state and len(invalid_state) > 2:
                enhanced += f"  Quick Fix: \"{invalid_state}\" is spelled out - use just the 2-letter code\n"
                # Try to guess the state
                state_map = {
                    'WISCONSIN': 'WI', 'ILLINOIS': 'IL', 'MINNESOTA': 'MN',
                    'IOWA': 'IA', 'MICHIGAN': 'MI', 'CALIFORNIA': 'CA'
                }
                suggestion = state_map.get(invalid_state.upper())
                if suggestion:
                    enhanced += f"  Try: {suggestion}\n\n"
                else:
                    enhanced += "\n"
            
            enhanced += "  Common Wisconsin area states:\n"
            enhanced += "     ✓ WI = Wisconsin\n"
            enhanced += "     ✓ IL = Illinois\n"
            enhanced += "     ✓ MN = Minnesota\n"
            enhanced += "     ✓ IA = Iowa\n"
            enhanced += "     ✓ MI = Michigan\n"
            enhanced += "     ✓ CA = California\n\n"
            enhanced += "  Common mistakes:\n"
            enhanced += "     ❌ WRONG: Wisconsin (spelled out)\n"
            enhanced += "     ❌ WRONG: wi (lowercase)\n"
            enhanced += "     ❌ WRONG: W (only 1 letter)\n"
            enhanced += "     ❌ WRONG: WIS (3 letters)\n"
            enhanced += "     ✅ CORRECT: WI\n\n"
            enhanced += "  WHERE TO CHECK:\n"
            enhanced += "     • Step 2: Your business state\n"
            enhanced += "     • Step 4: Consignor or Manufacturer state\n"
            enhanced += "     • Step 5: Recipient states in shipment table\n"
            enhanced += "     • Your CSV file's State column\n"
        
        elif "City" in error_msg:
            # Try to extract the invalid city value from the error message
            invalid_city = ""
            match = re.search(r"value '([^']*)'", error_msg)
            if match:
                invalid_city = match.group(1)
            
            enhanced += "🔍 PROBLEM: City name contains invalid characters\n\n"
            
            if invalid_city:
                enhanced += f"❌ INVALID CITY: \"{invalid_city}\"\n\n"
                
                # Identify what's wrong with this specific city
                issues = []
                if re.search(r'[0-9]', invalid_city):
                    issues.append("Contains numbers")
                if re.search(r'[.,;:]', invalid_city):
                    issues.append("Contains punctuation (.,;:)")
                if re.search(r'[^A-Za-z\s]', invalid_city):
                    issues.append("Contains special characters")
                
                if issues:
                    enhanced += f"⚠️  Issues found: {', '.join(issues)}\n\n"
            
            # Determine which city field has the problem
            location = "Unknown location"
            if "<Filer>" in xml_string and xml_string.find("<Filer>") < xml_string.find(error_msg if "<City>" in error_msg else "xxxxx"):
                location = "📍 YOUR BUSINESS CITY (Step 2: Filer Information)"
            elif "<ConsignorAddress>" in xml_string:
                location = "📍 CONSIGNOR CITY (Step 4: Default Consignor Information)"
            elif "<ManufacturerAddress>" in xml_string:
                location = "📍 MANUFACTURER CITY (Step 4: Default Manufacturer Information)"
            elif "<ConsigneeAddress>" in xml_string:
                location = "📍 RECIPIENT CITY (from your CSV data or Step 5 table)"
            
            enhanced += f"{location}\n\n"
            enhanced += "✅ HOW TO FIX:\n\n"
            
            if invalid_city:
                # Give specific fix for this city
                suggestion = re.sub(r'[0-9]', '', invalid_city)  # Remove numbers
                suggestion = re.sub(r'[.,;:]', '', suggestion)    # Remove common punctuation
                suggestion = suggestion.strip()
                
                if suggestion and suggestion != invalid_city:
                    enhanced += f"  Quick Fix: Change \"{invalid_city}\" to \"{suggestion}\"\n\n"
            
            enhanced += "  City names can ONLY contain:\n"
            enhanced += "     ✓ Letters (A-Z, a-z)\n"
            enhanced += "     ✓ Spaces\n\n"
            enhanced += "  City names CANNOT contain:\n"
            enhanced += "     ✗ Numbers (0-9)\n"
            enhanced += "     ✗ Punctuation (periods, commas, etc.)\n"
            enhanced += "     ✗ Special characters\n\n"
            enhanced += "  Examples:\n"
            enhanced += "     ❌ WRONG: Fake2 (has number)\n"
            enhanced += "     ✅ CORRECT: Fake\n\n"
            enhanced += "     ❌ WRONG: Madison, WI (has comma)\n"
            enhanced += "     ✅ CORRECT: Madison\n\n"
            enhanced += "     ❌ WRONG: St. Paul (has period)\n"
            enhanced += "     ✅ CORRECT: Saint Paul (spell out 'Saint')\n\n"
            enhanced += "     ✅ CORRECT: Eau Claire (spaces OK)\n\n"
            enhanced += "  WHERE TO CHECK:\n"
            enhanced += "     • Step 2: Your business city (Filer Information)\n"
            enhanced += "     • Step 4: Consignor or Manufacturer city (Default Values)\n"
            enhanced += "     • Step 5: Recipient cities in your shipment table\n"
            enhanced += "     • Your original CSV file's City column\n"
        
        elif "BusinessNameLine1" in error_msg:
            enhanced += "🔍 PROBLEM: Business name is missing or has invalid characters\n\n"
            enhanced += "📋 WHERE TO FIX: Step 2 - Filer Information\n\n"
            enhanced += "✅ HOW TO FIX:\n\n"
            enhanced += "  1. Go to Step 2: Filer Information\n"
            enhanced += "  2. Fill in 'Business Name Line 1' (REQUIRED)\n\n"
            enhanced += "  Business names can contain:\n"
            enhanced += "     ✓ Letters and numbers\n"
            enhanced += "     ✓ # - ( ) & '\n"
            enhanced += "     ✓ Single spaces (not multiple spaces in a row)\n\n"
            enhanced += "  Business names CANNOT contain:\n"
            enhanced += "     ✗ Most special characters (@, !, $, %, etc.)\n"
            enhanced += "     ✗ Leading or trailing spaces\n\n"
            enhanced += "  Examples:\n"
            enhanced += "     ❌ WRONG:   ABC Company  (extra spaces)\n"
            enhanced += "     ❌ WRONG: ABC@Company (@ symbol)\n"
            enhanced += "     ✅ CORRECT: ABC Company Inc\n"
            enhanced += "     ✅ CORRECT: Smith & Sons #3\n"
            enhanced += "     ✅ CORRECT: O'Brien's Wine (apostrophe OK)\n"
        
        elif "ZIP" in error_msg or "Zip" in error_msg:
            # Extract the invalid ZIP value from error message
            invalid_zip = ""
            line_number = None
            
            # Try different patterns to extract the value
            value_match = re.search(r"value '([^']*)'", error_msg)
            if value_match:
                invalid_zip = value_match.group(1)
            else:
                # Try alternate pattern
                value_match = re.search(r'value "([^"]*)"', error_msg)
                if value_match:
                    invalid_zip = value_match.group(1)
            
            line_match = re.search(r"line (\d+)", error_msg)
            if line_match:
                line_number = int(line_match.group(1))
            
            # If we couldn't extract from error, try to find it in the XML at that line
            if not invalid_zip and line_number:
                xml_lines = xml_string.split('\n')
                if line_number <= len(xml_lines):
                    line_content = xml_lines[line_number - 1]
                    zip_match = re.search(r'<ZIP>([^<]*)</ZIP>', line_content)
                    if zip_match:
                        invalid_zip = zip_match.group(1)
            
            # Determine which ZIP field by looking at XML context
            location = "Unknown location"
            xml_lines = xml_string.split('\n')
            
            if line_number and line_number <= len(xml_lines):
                for i in range(line_number - 1, max(0, line_number - 20), -1):
                    if i < len(xml_lines):
                        line = xml_lines[i]
                        if '<Filer>' in line:
                            location = "📍 YOUR BUSINESS ZIP (Step 2: Filer Information)"
                            break
                        elif '<ConsignorAddress>' in line:
                            location = "📍 CONSIGNOR ZIP (Step 4: Default Consignor Information)"
                            break
                        elif '<ManufacturerAddress>' in line:
                            location = "📍 MANUFACTURER ZIP (Step 4: Default Manufacturer Information)"
                            break
                        elif '<ConsigneeAddress>' in line:
                            location = "📍 RECIPIENT ZIP (from your CSV data or Step 5 table)"
                            break
            
            enhanced += "🔍 PROBLEM: ZIP code is invalid\n\n"
            
            if invalid_zip:
                enhanced += f"❌ INVALID ZIP: \"{invalid_zip}\"\n\n"
                
                # Analyze what's wrong
                issues = []
                if len(invalid_zip) < 5:
                    issues.append(f"Too short (only {len(invalid_zip)} characters, need 5 or 9)")
                elif len(invalid_zip) > 9:
                    issues.append(f"Too long ({len(invalid_zip)} characters, max is 9)")
                elif 5 < len(invalid_zip) < 9:
                    issues.append(f"Wrong length ({len(invalid_zip)} characters, must be exactly 5 or 9)")
                
                if re.search(r'[^0-9A-Z]', invalid_zip):
                    issues.append("Contains invalid characters (only numbers and letters allowed)")
                
                if issues:
                    enhanced += f"⚠️  Issues found: {', '.join(issues)}\n\n"
            
            enhanced += f"{location}\n\n"
            enhanced += "✅ HOW TO FIX:\n\n"
            enhanced += "  ZIP codes must be:\n"
            enhanced += "     • EXACTLY 5 digits (12345)\n"
            enhanced += "     • OR EXACTLY 9 digits (123456789)\n"
            enhanced += "     • Numbers only (or letters for Canadian postal codes)\n\n"
            enhanced += "  Examples:\n"
            enhanced += "     ✅ CORRECT: 53703\n"
            enhanced += "     ✅ CORRECT: 537031234\n"
            enhanced += "     ❌ WRONG: 53703-1234 (has dash - app should auto-remove this)\n"
            enhanced += "     ❌ WRONG: 5370 (too short)\n"
            enhanced += "     ❌ WRONG: 5370312345 (too long)\n\n"
            enhanced += "  WHERE TO CHECK:\n"
            enhanced += "     • Step 2: Your business ZIP\n"
            enhanced += "     • Step 4: Consignor or Manufacturer ZIP\n"
            enhanced += "     • Step 5: Recipient ZIPs in shipment table\n"
            enhanced += "     • Your CSV file's ZIP column\n"
        
        elif "Weight" in error_msg or "WeightOfBeverages" in error_msg:
            enhanced += "🔍 PROBLEM: Weight value is missing or invalid\n\n"
            enhanced += "📋 WHERE TO FIX: Check your shipment data (Step 5)\n\n"
            enhanced += "✅ HOW TO FIX:\n\n"
            enhanced += "  Weight must be:\n"
            enhanced += "     • A number (can have decimals)\n"
            enhanced += "     • In pounds (lbs)\n\n"
            enhanced += "  Examples:\n"
            enhanced += "     ✅ CORRECT: 25.5\n"
            enhanced += "     ✅ CORRECT: 30\n"
            enhanced += "     ❌ WRONG: (blank)\n"
            enhanced += "     ❌ WRONG: 25 lbs (remove 'lbs')\n"
        
        elif "pattern" in error_msg.lower() or "not accepted" in error_msg.lower():
            enhanced += "🔍 PROBLEM: A field has invalid characters or is empty when it's required\n\n"
            enhanced += "✅ GENERAL TIPS:\n\n"
            enhanced += "  1. Check that all REQUIRED fields (marked with *) are filled in\n"
            enhanced += "  2. Remove any special characters or symbols\n"
            enhanced += "  3. Make sure there are no extra spaces at the beginning or end\n"
            enhanced += "  4. Check that dates are in YYYY-MM-DD format\n"
            enhanced += "  5. Verify numbers don't have letters mixed in\n\n"
            enhanced += "  If you're still stuck, review the original error message above\n"
            enhanced += "  and look for field names mentioned.\n"
        
        else:
            enhanced += "🔍 PROBLEM: " + error_msg + "\n\n"
            enhanced += "✅ GENERAL TIPS:\n\n"
            enhanced += "  • Double-check all REQUIRED fields (marked with red *)\n"
            enhanced += "  • Make sure dates use YYYY-MM-DD format\n"
            enhanced += "  • Verify permit numbers are 15 digits\n"
            enhanced += "  • Check that your TIN is 9 digits\n"
        
        enhanced += "\n" + "═" * 60 + "\n"
        enhanced += "\n🔄 AFTER FIXING:\n\n"
        enhanced += "  1. Make the changes described above\n"
        enhanced += "  2. Click '💾 Save Filer Info' or '💾 Save Defaults' if you changed those sections\n"
        enhanced += "  3. Scroll back to Step 6\n"
        enhanced += "  4. Click '🚀 Generate & Validate XML' again\n"
        enhanced += "  5. The app will check for MORE errors (if any)\n"
        enhanced += "  6. Repeat until you see the green SUCCESS message!\n\n"
        enhanced += "💡 Each click checks your work and finds the next issue (if any).\n"
        enhanced += "   Don't worry - you're making progress with each fix!\n"
        
        return enhanced
    
    def save_xml(self, xml_string: str, filename: str, output_dir: str = None) -> str:
        """
        Save XML to file
        
        Args:
            xml_string: XML document as string
            filename: Output filename
            output_dir: Output directory (default: ./output)
            
        Returns:
            Full path to saved file
        """
        if output_dir is None:
            output_dir = os.path.join(os.path.dirname(__file__), 'output')
        
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(xml_string)
        
        return filepath

