"""
Flask Web Application for Wisconsin Excise Tax XML Generator
"""

from flask import Flask, render_template, request, jsonify, send_file
from xml_generator import XMLGenerator
from csv_mapper import CSVMapper
from config_manager import ConfigManager
import os
import sys
from datetime import datetime
import traceback


# Determine the base directory
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    BASE_DIR = sys._MEIPASS
else:
    # Running as script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, 
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static'))

# Initialize managers
config_manager = ConfigManager(config_dir=os.path.join(BASE_DIR, 'config'))


@app.route('/')
def index():
    """Render main application page"""
    return render_template('index.html')


@app.route('/api/config/filer', methods=['GET', 'POST'])
def filer_config():
    """Get or save filer configuration"""
    if request.method == 'GET':
        config = config_manager.load_filer_config()
        if config is None:
            config = config_manager.get_default_filer()
        return jsonify(config)
    
    elif request.method == 'POST':
        data = request.json
        config_manager.save_filer_config(data)
        return jsonify({'success': True, 'message': 'Filer configuration saved'})


@app.route('/api/config/defaults', methods=['GET', 'POST'])
def defaults_config():
    """Get or save default values"""
    if request.method == 'GET':
        defaults = config_manager.load_defaults()
        if defaults is None:
            defaults = {
                'consignor': config_manager.get_default_consignor(),
                'manufacturer': config_manager.get_default_manufacturer(),
                'common_carrier_permit': '',
                'ack_email': ''
            }
        return jsonify(defaults)
    
    elif request.method == 'POST':
        data = request.json
        config_manager.save_defaults(data)
        return jsonify({'success': True, 'message': 'Defaults saved'})


@app.route('/api/csv/template/<report_type>')
def csv_template(report_type):
    """Generate CSV template for download"""
    try:
        template_csv = CSVMapper.generate_csv_template(report_type)
        
        # Create temporary file
        temp_file = os.path.join(BASE_DIR, 'output', f'{report_type}_template.csv')
        os.makedirs(os.path.dirname(temp_file), exist_ok=True)
        
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(template_csv)
        
        return send_file(
            temp_file,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'{report_type}_template.csv'
        )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/csv/parse', methods=['POST'])
def parse_csv():
    """Parse CSV data"""
    try:
        data = request.json
        csv_content = data.get('csv_content', '')
        report_type = data.get('report_type', 'CommonCarrier')
        
        # Parse CSV
        rows = CSVMapper.parse_csv_data(csv_content)
        
        return jsonify({
            'success': True,
            'rows': rows,
            'count': len(rows)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 400


@app.route('/api/xml/generate', methods=['POST'])
def generate_xml():
    """Generate XML from shipment data with automatic date normalization"""
    try:
        data = request.json
        
        report_type = data.get('report_type', 'CommonCarrier')
        filer_data = data.get('filer_data')
        shipments = data.get('shipments', [])
        tax_period_begin = data.get('tax_period_begin')
        tax_period_end = data.get('tax_period_end')
        ack_email = data.get('ack_email')
        amended = data.get('amended', False)
        
        # Auto-normalize dates in all data
        tax_period_begin = CSVMapper.normalize_date(tax_period_begin) if tax_period_begin else ''
        tax_period_end = CSVMapper.normalize_date(tax_period_end) if tax_period_end else ''
        
        # Get defaults from the request data (current form values, not saved file)
        # This allows users to update defaults and generate without saving first
        defaults = data.get('defaults', {})
        
        # Re-apply defaults and normalize dates in shipments
        for shipment in shipments:
            # Normalize shipment date
            if 'shipment_date' in shipment and shipment['shipment_date']:
                shipment['shipment_date'] = CSVMapper.normalize_date(shipment['shipment_date'])
            
            # Re-apply current defaults for Common Carrier
            if report_type == 'CommonCarrier':
                consignor = defaults.get('consignor', {})
                
                # ALWAYS overwrite with current defaults (this ensures fresh values)
                # Use .get() with empty string default to handle missing fields
                shipment['consignor_name'] = consignor.get('name', shipment.get('consignor_name', ''))
                shipment['consignor_address_line1'] = consignor.get('address_line1', shipment.get('consignor_address_line1', ''))
                shipment['consignor_address_line2'] = consignor.get('address_line2', shipment.get('consignor_address_line2', ''))
                shipment['consignor_city'] = consignor.get('city', shipment.get('consignor_city', ''))
                shipment['consignor_state'] = consignor.get('state', shipment.get('consignor_state', ''))
                shipment['consignor_zip'] = consignor.get('zip', shipment.get('consignor_zip', ''))
                shipment['permit_number'] = consignor.get('permit_number', shipment.get('permit_number', ''))
            
            # Re-apply current defaults for Fulfillment House
            elif report_type == 'FulfillmentHouse' and defaults.get('manufacturer'):
                manufacturer = defaults['manufacturer']
                shipment['manufacturer_name'] = manufacturer.get('name', shipment.get('manufacturer_name', ''))
                shipment['manufacturer_address_line1'] = manufacturer.get('address_line1', shipment.get('manufacturer_address_line1', ''))
                shipment['manufacturer_address_line2'] = manufacturer.get('address_line2', shipment.get('manufacturer_address_line2', ''))
                shipment['manufacturer_city'] = manufacturer.get('city', shipment.get('manufacturer_city', ''))
                shipment['manufacturer_state'] = manufacturer.get('state', shipment.get('manufacturer_state', ''))
                shipment['manufacturer_zip'] = manufacturer.get('zip', shipment.get('manufacturer_zip', ''))
                if manufacturer.get('wine_permit_number'):
                    shipment['wine_permit_number'] = manufacturer['wine_permit_number']
                if defaults.get('common_carrier_permit'):
                    shipment['common_carrier_permit_number'] = defaults['common_carrier_permit']
        
        # Validate required fields
        if not filer_data:
            return jsonify({'success': False, 'error': 'Filer data is required'}), 400
        if not shipments:
            return jsonify({'success': False, 'error': 'At least one shipment is required'}), 400
        if not tax_period_begin or not tax_period_end:
            return jsonify({'success': False, 'error': 'Tax period dates are required'}), 400
        if not ack_email:
            return jsonify({'success': False, 'error': 'Acknowledgement email is required'}), 400
        
        # Generate XML
        generator = XMLGenerator(report_type)
        xml_string = generator.generate_xml(
            filer_data=filer_data,
            shipments=shipments,
            tax_period_begin=tax_period_begin,
            tax_period_end=tax_period_end,
            ack_email=ack_email,
            amended=amended
        )
        
        # Validate XML
        is_valid, error_message = generator.validate_xml(xml_string)
        
        if not is_valid:
            return jsonify({
                'success': False,
                'error': 'XML validation failed',
                'validation_error': error_message,
                'xml': xml_string  # Return XML anyway so user can see it
            }), 400
        
        return jsonify({
            'success': True,
            'xml': xml_string,
            'validation': 'passed'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/xml/save', methods=['POST'])
def save_xml():
    """Save generated XML to file"""
    try:
        data = request.json
        xml_string = data.get('xml')
        report_type = data.get('report_type', 'CommonCarrier')
        
        if not xml_string:
            return jsonify({'success': False, 'error': 'No XML provided'}), 400
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'{report_type}_{timestamp}.xml'
        
        # Save file
        generator = XMLGenerator(report_type)
        output_dir = os.path.join(BASE_DIR, 'output')
        filepath = generator.save_xml(xml_string, filename, output_dir)
        
        return send_file(
            filepath,
            mimetype='application/xml',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/csv/map', methods=['POST'])
def map_csv():
    """Map CSV data to XML shipment format with helpful feedback"""
    try:
        data = request.json
        
        csv_content = data.get('csv_content', '')
        report_type = data.get('report_type', 'CommonCarrier')
        defaults = data.get('defaults', {})
        
        # Parse CSV
        rows = CSVMapper.parse_csv_data(csv_content)
        
        # Generate mapping report
        mapping_report = CSVMapper.get_mapping_report(rows, report_type)
        
        # Map to shipment format
        if report_type == 'CommonCarrier':
            consignor = defaults.get('consignor', config_manager.get_default_consignor())
            shipments = CSVMapper.map_to_common_carrier(rows, consignor)
        else:  # FulfillmentHouse
            manufacturer = defaults.get('manufacturer', config_manager.get_default_manufacturer())
            common_carrier_permit = defaults.get('common_carrier_permit', '')
            shipments = CSVMapper.map_to_fulfillment_house(
                rows, manufacturer, common_carrier_permit
            )
        
        # Build user-friendly feedback message
        feedback = "✅ CSV IMPORT SUCCESSFUL!\n\n"
        feedback += f"📊 Imported {len(shipments)} shipment(s)\n\n"
        
        if mapping_report['mapped_columns']:
            feedback += "🔗 SUCCESSFULLY MAPPED:\n"
            for mapping in mapping_report['mapped_columns']:
                feedback += f"  ✓ {mapping}\n"
            feedback += "\n"
        
        if mapping_report['unmapped_columns']:
            feedback += f"⚠️  IGNORED COLUMNS (not needed for this report):\n"
            for col in mapping_report['unmapped_columns']:
                feedback += f"  • {col}\n"
            feedback += "\n"
        
        if mapping_report['missing_recommended']:
            feedback += "⚠️  MISSING RECOMMENDED FIELDS:\n"
            field_tips = {
                'consignee_name': 'Add "Name" or "Ship To Company" column',
                'consignee_address_line1': 'Add "Address" or "Ship To Street" column',
                'consignee_city': 'Add "City" or "Ship To City" column',
                'consignee_state': 'Add "State" or "Ship To State" column',
                'consignee_zip': 'Add "ZIP" or "Ship To Zip" column',
                'shipment_date': 'Add "Date" or "Order Date" column',
                'weight_of_beverages': 'Add "LB" or "Weight" column',
                'bottle_count': 'Add "Bottle Count" or "Quantity" column',
                'bottle_size_ml': 'Add "Size" or "SIZE" column (in milliliters)'
            }
            for field in mapping_report['missing_recommended']:
                tip = field_tips.get(field, f'Add column for {field}')
                feedback += f"  ⚠ {field}: {tip}\n"
            feedback += "\n  TIP: You can add these manually in Step 5, or update your CSV and re-import\n\n"
        
        return jsonify({
            'success': True,
            'shipments': shipments,
            'count': len(shipments),
            'mapping_report': mapping_report,
            'feedback': feedback
        })
        
    except Exception as e:
        error_msg = "❌ CSV IMPORT FAILED\n\n"
        error_msg += f"Error: {str(e)}\n\n"
        error_msg += "💡 COMMON FIXES:\n"
        error_msg += "  • Make sure your CSV has headers in the first row\n"
        error_msg += "  • Check that you copied the entire data (including headers)\n"
        error_msg += "  • Try removing any special formatting from Excel before copying\n"
        error_msg += "  • Save as CSV file first, then copy from there\n\n"
        error_msg += f"Technical details:\n{traceback.format_exc()}\n"
        
        return jsonify({
            'success': False,
            'error': error_msg
        }), 400


def open_browser():
    """Open the default web browser to the application"""
    import webbrowser
    import time
    
    time.sleep(1.5)  # Give the server time to start
    webbrowser.open('http://127.0.0.1:5000/')


if __name__ == '__main__':
    import threading
    
    # Open browser in a separate thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run Flask app
    print("=" * 60)
    print("Wisconsin Excise Tax XML Generator")
    print("=" * 60)
    print("\nStarting web server...")
    print("Opening browser at http://127.0.0.1:5000/")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    
    app.run(debug=False, host='127.0.0.1', port=5000)

