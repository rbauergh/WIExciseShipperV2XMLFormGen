"""
Test script to verify the Wisconsin Excise Tax XML Generator setup
Run this to ensure all components are working correctly
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    try:
        from lxml import etree
        print("  ✓ lxml")
    except ImportError as e:
        print(f"  ✗ lxml - {e}")
        return False
    
    try:
        from flask import Flask
        print("  ✓ Flask")
    except ImportError as e:
        print(f"  ✗ Flask - {e}")
        return False
    
    try:
        import xml_generator
        print("  ✓ xml_generator")
    except ImportError as e:
        print(f"  ✗ xml_generator - {e}")
        return False
    
    try:
        import csv_mapper
        print("  ✓ csv_mapper")
    except ImportError as e:
        print(f"  ✗ csv_mapper - {e}")
        return False
    
    try:
        import config_manager
        print("  ✓ config_manager")
    except ImportError as e:
        print(f"  ✗ config_manager - {e}")
        return False
    
    return True

def test_schemas():
    """Test that schema files exist"""
    print("\nTesting schema files...")
    schemas_dir = os.path.join(os.path.dirname(__file__), 'schemas')
    
    ab136 = os.path.join(schemas_dir, 'AB136.xsd')
    ab137 = os.path.join(schemas_dir, 'AB137.xsd')
    
    if os.path.exists(ab136):
        print("  ✓ AB136.xsd found")
    else:
        print("  ✗ AB136.xsd missing")
        return False
    
    if os.path.exists(ab137):
        print("  ✓ AB137.xsd found")
    else:
        print("  ✗ AB137.xsd missing")
        return False
    
    return True

def test_xml_generation():
    """Test basic XML generation"""
    print("\nTesting XML generation...")
    try:
        from xml_generator import XMLGenerator
        
        # Test Common Carrier
        gen = XMLGenerator('CommonCarrier')
        print("  ✓ Common Carrier generator initialized")
        
        # Test Fulfillment House
        gen = XMLGenerator('FulfillmentHouse')
        print("  ✓ Fulfillment House generator initialized")
        
        # Test basic XML generation
        filer_data = {
            'tin_type': 'FEIN',
            'tin_value': '123456789',
            'business_name_line1': 'Test Company',
            'address_line1': '123 Main St',
            'city': 'Madison',
            'state': 'WI',
            'zip': '53703'
        }
        
        shipments = [{
            'manufacturer_name': 'Test Winery',
            'manufacturer_address_line1': '123 Winery Rd',
            'manufacturer_city': 'Madison',
            'manufacturer_state': 'WI',
            'manufacturer_zip': '53703',
            'wine_permit_number': '123456789012345',
            'consignee_name': 'John Doe',
            'consignee_address_line1': '456 Oak Ave',
            'consignee_city': 'Milwaukee',
            'consignee_state': 'WI',
            'consignee_zip': '53202',
            'shipment_date': '2024-01-15',
            'tracking_number': '1Z12345',
            'common_carrier_permit_number': '123456789012345',
            'quantity_of_wine': '9.0'
        }]
        
        xml = gen.generate_xml(
            filer_data=filer_data,
            shipments=shipments,
            tax_period_begin='2024-01-01',
            tax_period_end='2024-03-31',
            ack_email='test@example.com'
        )
        
        print("  ✓ XML generation successful")
        
        # Test validation
        is_valid, error = gen.validate_xml(xml)
        if is_valid:
            print("  ✓ XML validation passed")
        else:
            print(f"  ✗ XML validation failed: {error}")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_directories():
    """Test that required directories exist"""
    print("\nTesting directories...")
    dirs = ['templates', 'static', 'schemas', 'config', 'output', 'docs']
    
    all_exist = True
    for dir_name in dirs:
        dir_path = os.path.join(os.path.dirname(__file__), dir_name)
        if os.path.exists(dir_path):
            print(f"  ✓ {dir_name}/")
        else:
            print(f"  ✗ {dir_name}/ missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print("=" * 60)
    print("Wisconsin Excise Tax XML Generator - Setup Test")
    print("=" * 60)
    print()
    
    all_passed = True
    
    # Run tests
    all_passed &= test_imports()
    all_passed &= test_directories()
    all_passed &= test_schemas()
    all_passed &= test_xml_generation()
    
    print()
    print("=" * 60)
    if all_passed:
        print("✅ All tests passed! Setup is complete.")
        print("You can now run: python app.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("Make sure all dependencies are installed:")
        print("  pip install -r requirements.txt")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())

