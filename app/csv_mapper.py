"""
CSV Mapper for Wisconsin Excise Tax Reports
Maps CSV data to XML structure
"""

import csv
import re
from datetime import datetime
from typing import List, Dict, Optional
from io import StringIO


class CSVMapper:
    """Map CSV data to XML structure for WI DOR reports"""
    
    # Common Carrier field mappings
    # Multiple column name variations can map to the same field
    COMMON_CARRIER_MAPPINGS = {
        # Consignee Name variations
        'Ship To Company': 'consignee_name',
        'Consignee Name': 'consignee_name',
        'Company': 'consignee_name',
        'Name': 'consignee_name',
        
        # Address variations
        'Ship To Street': 'consignee_address_line1',
        'Ship To Address': 'consignee_address_line1',
        'Address': 'consignee_address_line1',
        'Street': 'consignee_address_line1',
        'Address Line 1': 'consignee_address_line1',
        'AddressLine1': 'consignee_address_line1',
        
        # City variations
        'Ship To City': 'consignee_city',
        'City': 'consignee_city',
        
        # State variations
        'Ship To State': 'consignee_state',
        'State': 'consignee_state',
        
        # ZIP variations
        'Ship To Zip': 'consignee_zip',
        'Zip': 'consignee_zip',
        'ZIP': 'consignee_zip',
        'Zip Code': 'consignee_zip',
        'ZipCode': 'consignee_zip',
        
        # Tracking Number variations
        'Tracking Nos': 'tracking_number',
        'Tracking Number': 'tracking_number',
        'Tracking #': 'tracking_number',
        'Tracking': 'tracking_number',
        'TrackingNumber': 'tracking_number',
        
        # Date variations
        'Order Date': 'shipment_date',
        'Shipment Date': 'shipment_date',
        'Date': 'shipment_date',
        'Ship Date': 'shipment_date',
        
        # Weight variations
        'LB': 'weight_of_beverages',
        'Weight': 'weight_of_beverages',
        'Weight (lbs)': 'weight_of_beverages',
        'Pounds': 'weight_of_beverages',
        
        # Beverage Type variations
        'TYPE': 'beverage_type',
        'Type': 'beverage_type',
        'Beverage Type': 'beverage_type',
        'BeverageType': 'beverage_type',
    }
    
    # Fulfillment House field mappings
    # Multiple column name variations can map to the same field
    FULFILLMENT_HOUSE_MAPPINGS = {
        # Consignee Name variations (same as Common Carrier)
        'Ship To Company': 'consignee_name',
        'Consignee Name': 'consignee_name',
        'Company': 'consignee_name',
        'Name': 'consignee_name',
        
        # Address variations
        'Ship To Street': 'consignee_address_line1',
        'Ship To Address': 'consignee_address_line1',
        'Address': 'consignee_address_line1',
        'Street': 'consignee_address_line1',
        'Address Line 1': 'consignee_address_line1',
        'AddressLine1': 'consignee_address_line1',
        
        # City variations
        'Ship To City': 'consignee_city',
        'City': 'consignee_city',
        
        # State variations
        'Ship To State': 'consignee_state',
        'State': 'consignee_state',
        
        # ZIP variations
        'Ship To Zip': 'consignee_zip',
        'Zip': 'consignee_zip',
        'ZIP': 'consignee_zip',
        'Zip Code': 'consignee_zip',
        'ZipCode': 'consignee_zip',
        
        # Tracking Number variations
        'Tracking Nos': 'tracking_number',
        'Tracking Number': 'tracking_number',
        'Tracking #': 'tracking_number',
        'Tracking': 'tracking_number',
        'TrackingNumber': 'tracking_number',
        
        # Date variations
        'Order Date': 'shipment_date',
        'Shipment Date': 'shipment_date',
        'Date': 'shipment_date',
        'Ship Date': 'shipment_date',
        
        # Bottle Count variations (will be converted to liters)
        'BOTTLE COUNT': 'bottle_count',
        'Bottle Count': 'bottle_count',
        'BottleCount': 'bottle_count',
        'Bottles': 'bottle_count',
        'Count': 'bottle_count',
        'Qty': 'bottle_count',
        'Quantity': 'bottle_count',
        
        # Bottle Size variations
        'SIZE': 'bottle_size_ml',
        'Size': 'bottle_size_ml',
        'Bottle Size': 'bottle_size_ml',
        'BottleSize': 'bottle_size_ml',
        'ML': 'bottle_size_ml',
        'Size (ml)': 'bottle_size_ml',
    }
    
    @staticmethod
    def parse_csv_data(csv_content: str, has_header: bool = True) -> List[Dict]:
        """
        Parse CSV content into list of dictionaries
        
        Args:
            csv_content: CSV data as string
            has_header: Whether the first row contains headers
            
        Returns:
            List of dictionaries representing rows
        """
        reader = csv.DictReader(StringIO(csv_content))
        return list(reader)
    
    @staticmethod
    def normalize_date(date_str: str) -> str:
        """
        Convert various date formats to YYYY-MM-DD
        Handles most common date formats automatically
        
        Args:
            date_str: Date string in various formats
            
        Returns:
            Date string in YYYY-MM-DD format
        """
        if not date_str or not str(date_str).strip():
            return ''
        
        date_str = str(date_str).strip()
        
        # If already in correct format, return as-is
        if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            return date_str
        
        # Try many common date formats
        formats = [
            # ISO format
            '%Y-%m-%d',
            
            # American formats (most common in US)
            '%m/%d/%Y',      # 10/29/2025
            '%m/%d/%y',      # 10/29/25
            '%m-%d-%Y',      # 10-29-2025
            '%m-%d-%y',      # 10-29-25
            
            # With single digit day/month
            '%m/%d/%Y',      # 3/5/2024
            '%m/%d/%y',      # 3/5/24
            
            # European formats
            '%d/%m/%Y',      # 29/10/2025
            '%d/%m/%y',      # 29/10/25
            '%d-%m-%Y',      # 29-10-2025
            '%d-%m-%y',      # 29-10-25
            
            # Year first formats
            '%Y/%m/%d',      # 2025/10/29
            '%Y.%m.%d',      # 2025.10.29
            
            # With month names
            '%B %d, %Y',     # October 29, 2025
            '%b %d, %Y',     # Oct 29, 2025
            '%d %B %Y',      # 29 October 2025
            '%d %b %Y',      # 29 Oct 2025
            '%B %d %Y',      # October 29 2025 (no comma)
            '%b %d %Y',      # Oct 29 2025 (no comma)
            
            # Compact formats
            '%Y%m%d',        # 20251029
            '%m%d%Y',        # 10292025
            '%m%d%y',        # 102925
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                # Sanity check: year should be reasonable (1900-2100)
                if 1900 <= dt.year <= 2100:
                    return dt.strftime('%Y-%m-%d')
            except ValueError:
                continue
        
        # Try to parse with dateutil if available (more flexible)
        try:
            from dateutil import parser
            dt = parser.parse(date_str, fuzzy=False)
            if 1900 <= dt.year <= 2100:
                return dt.strftime('%Y-%m-%d')
        except:
            pass
        
        # If no format matches, return as-is and let validation catch it
        return date_str
    
    @staticmethod
    def clean_street_address(address: str) -> str:
        """
        Clean street address to remove invalid characters
        
        Schema allows: A-Z, a-z, 0-9, hyphen, slash, single spaces
        Common issue: Periods in abbreviations (N. Main St.)
        
        Args:
            address: Street address that may contain periods or other invalid chars
            
        Returns:
            Cleaned address
        """
        if not address:
            return ''
        
        address = str(address)
        
        # Remove periods (common in "N. Main St." or "St. Paul St.")
        address = address.replace('.', '')
        
        # Remove other invalid characters (keep only allowed chars)
        # Allowed: A-Z, a-z, 0-9, hyphen, slash, space
        address = re.sub(r'[^A-Za-z0-9\-/\s]', '', address)
        
        # Normalize multiple spaces to single space
        address = re.sub(r'\s+', ' ', address)
        
        # Trim leading/trailing spaces
        address = address.strip()
        
        return address
    
    @staticmethod
    def clean_zip_code(zip_code: str) -> str:
        """Clean and format ZIP code"""
        # Remove any non-alphanumeric characters
        zip_code = re.sub(r'[^0-9A-Z]', '', str(zip_code).upper())
        # Ensure it's at least 5 characters
        return zip_code.zfill(5) if zip_code.isdigit() else zip_code
    
    @staticmethod
    def clean_tin(tin: str) -> str:
        """Clean TIN/SSN/FEIN to 9 digits"""
        return re.sub(r'[^0-9]', '', str(tin))[:9].zfill(9)
    
    @staticmethod
    def clean_permit_number(permit: str) -> str:
        """Clean permit number to 15 digits"""
        return re.sub(r'[^0-9]', '', str(permit))[:15].zfill(15)
    
    @staticmethod
    def bottles_to_liters(bottle_count: int, bottle_size_ml: int) -> float:
        """
        Convert bottle count and size to liters
        
        Args:
            bottle_count: Number of bottles
            bottle_size_ml: Size of each bottle in milliliters
            
        Returns:
            Total volume in liters
        """
        total_ml = bottle_count * bottle_size_ml
        return round(total_ml / 1000, 1)
    
    @staticmethod
    def get_mapping_report(csv_rows: List[Dict], report_type: str) -> Dict:
        """
        Generate a report of which CSV columns were mapped
        
        Args:
            csv_rows: List of CSV row dictionaries
            report_type: 'CommonCarrier' or 'FulfillmentHouse'
            
        Returns:
            Dictionary with mapping statistics and suggestions
        """
        if not csv_rows:
            return {
                'mapped_columns': [],
                'unmapped_columns': [],
                'missing_recommended': [],
                'warnings': []
            }
        
        csv_columns = set(csv_rows[0].keys())
        mappings = CSVMapper.COMMON_CARRIER_MAPPINGS if report_type == 'CommonCarrier' else CSVMapper.FULFILLMENT_HOUSE_MAPPINGS
        
        mapped_columns = []
        unmapped_columns = []
        
        for col in csv_columns:
            if col in mappings:
                mapped_columns.append(f"{col} → {mappings[col]}")
            else:
                unmapped_columns.append(col)
        
        # Determine what's missing
        if report_type == 'CommonCarrier':
            recommended = ['consignee_name', 'consignee_address_line1', 'consignee_city', 
                          'consignee_state', 'consignee_zip', 'shipment_date', 'weight_of_beverages']
        else:
            recommended = ['consignee_name', 'consignee_address_line1', 'consignee_city',
                          'consignee_state', 'consignee_zip', 'shipment_date', 'bottle_count', 'bottle_size_ml']
        
        mapped_fields = set(mappings.get(col) for col in csv_columns if col in mappings)
        missing_recommended = [field for field in recommended if field not in mapped_fields]
        
        warnings = []
        if unmapped_columns:
            warnings.append(f"Found {len(unmapped_columns)} unmapped columns that will be ignored")
        if missing_recommended:
            warnings.append(f"Missing {len(missing_recommended)} recommended fields")
        
        return {
            'mapped_columns': mapped_columns,
            'unmapped_columns': unmapped_columns,
            'missing_recommended': missing_recommended,
            'warnings': warnings
        }
    
    @classmethod
    def map_to_common_carrier(cls, csv_rows: List[Dict], 
                              default_consignor: Dict) -> List[Dict]:
        """
        Map CSV rows to Common Carrier shipment format
        
        Args:
            csv_rows: List of CSV row dictionaries
            default_consignor: Default consignor information to use for all shipments
            
        Returns:
            List of shipment dictionaries ready for XML generation
        """
        shipments = []
        
        for row in csv_rows:
            shipment = {
                # Consignor (sender) - use defaults
                'consignor_name': default_consignor.get('name', ''),
                'consignor_address_line1': default_consignor.get('address_line1', ''),
                'consignor_address_line2': default_consignor.get('address_line2', ''),
                'consignor_city': default_consignor.get('city', ''),
                'consignor_state': default_consignor.get('state', ''),
                'consignor_zip': default_consignor.get('zip', ''),
                'permit_number': default_consignor.get('permit_number', ''),
            }
            
            # Map CSV fields to shipment fields
            for csv_field, xml_field in cls.COMMON_CARRIER_MAPPINGS.items():
                if csv_field in row and row[csv_field]:
                    value = row[csv_field]
                    
                    # Apply transformations and assign
                    if xml_field == 'shipment_date':
                        shipment[xml_field] = cls.normalize_date(value)
                    elif xml_field == 'consignee_zip':
                        shipment[xml_field] = cls.clean_zip_code(value)
                    elif xml_field == 'consignee_address_line1' or xml_field == 'consignee_address_line2':
                        shipment[xml_field] = cls.clean_street_address(value)
                    elif xml_field == 'weight_of_beverages':
                        shipment[xml_field] = float(value)
                    elif xml_field == 'beverage_type':
                        # Normalize beverage type
                        value = value.capitalize()
                        if value.upper() not in ['BEER', 'WINE', 'SPIRITS', 'UNKNOWN']:
                            value = 'Unknown'
                        shipment[xml_field] = value
                    else:
                        shipment[xml_field] = value
            
            # Set defaults for optional fields
            shipment.setdefault('tracking_number', '')
            shipment.setdefault('bill_of_lading_number', '')
            shipment.setdefault('consignee_address_line2', '')
            
            shipments.append(shipment)
        
        return shipments
    
    @classmethod
    def map_to_fulfillment_house(cls, csv_rows: List[Dict], 
                                  default_manufacturer: Dict,
                                  common_carrier_permit: str) -> List[Dict]:
        """
        Map CSV rows to Fulfillment House shipment format
        
        Args:
            csv_rows: List of CSV row dictionaries
            default_manufacturer: Default manufacturer information
            common_carrier_permit: Common carrier permit number
            
        Returns:
            List of shipment dictionaries ready for XML generation
        """
        shipments = []
        
        for row in csv_rows:
            shipment = {
                # Manufacturer info - use defaults
                'manufacturer_name': default_manufacturer.get('name', ''),
                'manufacturer_address_line1': default_manufacturer.get('address_line1', ''),
                'manufacturer_address_line2': default_manufacturer.get('address_line2', ''),
                'manufacturer_city': default_manufacturer.get('city', ''),
                'manufacturer_state': default_manufacturer.get('state', ''),
                'manufacturer_zip': default_manufacturer.get('zip', ''),
                'wine_permit_number': default_manufacturer.get('wine_permit_number', ''),
                'common_carrier_permit_number': common_carrier_permit,
            }
            
            # Map CSV fields to shipment fields
            for csv_field, xml_field in cls.FULFILLMENT_HOUSE_MAPPINGS.items():
                if csv_field in row and row[csv_field]:
                    value = row[csv_field]
                    
                    # Apply transformations and assign
                    if xml_field == 'shipment_date':
                        shipment[xml_field] = cls.normalize_date(value)
                    elif xml_field == 'consignee_zip':
                        shipment[xml_field] = cls.clean_zip_code(value)
                    elif xml_field == 'consignee_address_line1' or xml_field == 'consignee_address_line2':
                        shipment[xml_field] = cls.clean_street_address(value)
                    elif xml_field in ['bottle_count', 'bottle_size_ml']:
                        # Store temporarily for conversion
                        shipment[xml_field] = int(value)
                    else:
                        shipment[xml_field] = value
            
            # Convert bottles to liters
            if 'bottle_count' in shipment and 'bottle_size_ml' in shipment:
                shipment['quantity_of_wine'] = cls.bottles_to_liters(
                    shipment.pop('bottle_count'),
                    shipment.pop('bottle_size_ml')
                )
            
            # Set defaults for optional fields
            shipment.setdefault('tracking_number', '')
            shipment.setdefault('consignee_address_line2', '')
            shipment.setdefault('different_consignor_name', '')
            
            shipments.append(shipment)
        
        return shipments
    
    @staticmethod
    def generate_csv_template(report_type: str) -> str:
        """
        Generate a CSV template for manual data entry
        
        Args:
            report_type: 'CommonCarrier' or 'FulfillmentHouse'
            
        Returns:
            CSV template as string
        """
        if report_type == 'CommonCarrier':
            headers = [
                'Ship To Company',
                'Ship To Street',
                'Ship To City',
                'Ship To State',
                'Ship To Zip',
                'Tracking Nos',
                'Order Date',
                'LB',
                'TYPE'
            ]
        else:  # FulfillmentHouse
            headers = [
                'Ship To Company',
                'Ship To Street',
                'Ship To City',
                'Ship To State',
                'Ship To Zip',
                'Tracking Nos',
                'Order Date',
                'BOTTLE COUNT',
                'SIZE'
            ]
        
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(headers)
        return output.getvalue()

