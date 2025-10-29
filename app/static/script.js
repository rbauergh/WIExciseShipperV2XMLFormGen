// Wisconsin Excise Tax XML Generator - Frontend Logic

let currentShipments = [];
let generatedXML = '';

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadFilerConfig();
    loadDefaults();
    setupReportTypeListener();
    updateDefaultsPanel();
});

// ===== Report Type Management =====

function setupReportTypeListener() {
    const radioButtons = document.querySelectorAll('input[name="reportType"]');
    radioButtons.forEach(radio => {
        radio.addEventListener('change', function() {
            updateDefaultsPanel();
            updateTableHeaders();
            // Clear shipments silently when switching report types (no confirmation)
            if (currentShipments.length > 0) {
                if (confirm('Switching report type will clear your current shipments. Continue?')) {
                    currentShipments = [];
                    document.getElementById('shipmentsTableContainer').style.display = 'none';
                    // Switch to CSV import tab when clearing
                    switchTab('csv');
                } else {
                    // User cancelled - revert radio button
                    event.target.checked = false;
                    const otherType = event.target.value === 'CommonCarrier' ? 'FulfillmentHouse' : 'CommonCarrier';
                    document.querySelector(`input[name="reportType"][value="${otherType}"]`).checked = true;
                    updateDefaultsPanel();
                }
            }
        });
    });
}

function getReportType() {
    return document.querySelector('input[name="reportType"]:checked').value;
}

function updateDefaultsPanel() {
    const reportType = getReportType();
    document.getElementById('commonCarrierDefaults').style.display = 
        reportType === 'CommonCarrier' ? 'block' : 'none';
    document.getElementById('fulfillmentHouseDefaults').style.display = 
        reportType === 'FulfillmentHouse' ? 'block' : 'none';
}

// ===== Configuration Management =====

async function loadFilerConfig() {
    try {
        const response = await fetch('/api/config/filer');
        const config = await response.json();
        
        document.getElementById('tinType').value = config.tin_type || 'FEIN';
        document.getElementById('tinValue').value = config.tin_value || '';
        document.getElementById('stateEIN').value = config.state_ein || '';
        document.getElementById('businessName1').value = config.business_name_line1 || '';
        document.getElementById('businessName2').value = config.business_name_line2 || '';
        document.getElementById('address1').value = config.address_line1 || '';
        document.getElementById('address2').value = config.address_line2 || '';
        document.getElementById('city').value = config.city || '';
        document.getElementById('state').value = config.state || 'WI';
        document.getElementById('zip').value = config.zip || '';
    } catch (error) {
        console.error('Error loading filer config:', error);
    }
}

async function saveFilerConfig() {
    const config = getFilerData();
    
    try {
        const response = await fetch('/api/config/filer', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(config)
        });
        
        const result = await response.json();
        showStatus('Filer information saved successfully!', 'success');
    } catch (error) {
        showStatus('Error saving filer information: ' + error.message, 'error');
    }
}

async function loadDefaults() {
    try {
        const response = await fetch('/api/config/defaults');
        const defaults = await response.json();
        
        // Common Carrier defaults
        if (defaults.consignor) {
            document.getElementById('ccConsignorName').value = defaults.consignor.name || '';
            document.getElementById('ccConsignorAddress1').value = defaults.consignor.address_line1 || '';
            document.getElementById('ccConsignorCity').value = defaults.consignor.city || '';
            document.getElementById('ccConsignorState').value = defaults.consignor.state || 'WI';
            document.getElementById('ccConsignorZip').value = defaults.consignor.zip || '';
            document.getElementById('ccPermitNumber').value = defaults.consignor.permit_number || '';
        }
        
        // Fulfillment House defaults
        if (defaults.manufacturer) {
            document.getElementById('fhManufacturerName').value = defaults.manufacturer.name || '';
            document.getElementById('fhManufacturerAddress1').value = defaults.manufacturer.address_line1 || '';
            document.getElementById('fhManufacturerCity').value = defaults.manufacturer.city || '';
            document.getElementById('fhManufacturerState').value = defaults.manufacturer.state || 'WI';
            document.getElementById('fhManufacturerZip').value = defaults.manufacturer.zip || '';
            document.getElementById('fhWinePermitNumber').value = defaults.manufacturer.wine_permit_number || '';
        }
        
        if (defaults.common_carrier_permit) {
            document.getElementById('fhCCPermitNumber').value = defaults.common_carrier_permit;
        }
        
        if (defaults.ack_email) {
            document.getElementById('ackEmail').value = defaults.ack_email;
        }
    } catch (error) {
        console.error('Error loading defaults:', error);
    }
}

async function saveDefaults() {
    // Load existing defaults first to preserve both types
    let defaults = {};
    try {
        const response = await fetch('/api/config/defaults');
        defaults = await response.json();
    } catch (error) {
        console.error('Error loading existing defaults:', error);
    }
    
    // Update with current values
    defaults.ack_email = document.getElementById('ackEmail').value;
    
    const reportType = getReportType();
    
    if (reportType === 'CommonCarrier') {
        // Save Common Carrier defaults (preserve manufacturer if it exists)
        defaults.consignor = {
            name: document.getElementById('ccConsignorName').value,
            address_line1: document.getElementById('ccConsignorAddress1').value,
            city: document.getElementById('ccConsignorCity').value,
            state: document.getElementById('ccConsignorState').value,
            zip: document.getElementById('ccConsignorZip').value,
            permit_number: document.getElementById('ccPermitNumber').value
        };
    } else {
        // Save Fulfillment House defaults (preserve consignor if it exists)
        defaults.manufacturer = {
            name: document.getElementById('fhManufacturerName').value,
            address_line1: document.getElementById('fhManufacturerAddress1').value,
            city: document.getElementById('fhManufacturerCity').value,
            state: document.getElementById('fhManufacturerState').value,
            zip: document.getElementById('fhManufacturerZip').value,
            wine_permit_number: document.getElementById('fhWinePermitNumber').value
        };
        defaults.common_carrier_permit = document.getElementById('fhCCPermitNumber').value;
    }
    
    try {
        const response = await fetch('/api/config/defaults', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(defaults)
        });
        
        const result = await response.json();
        showStatus('Default values saved successfully!', 'success');
    } catch (error) {
        showStatus('Error saving defaults: ' + error.message, 'error');
    }
}

// ===== Tab Management =====

function switchTab(tabName, eventTarget = null) {
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // If called from a click event, highlight that button
    // If called programmatically, find and highlight the correct button
    if (eventTarget) {
        eventTarget.classList.add('active');
    } else {
        // Find the button corresponding to the tab
        const buttons = document.querySelectorAll('.tab-btn');
        buttons.forEach(btn => {
            if ((tabName === 'csv' && btn.textContent.includes('CSV')) ||
                (tabName === 'manual' && btn.textContent.includes('Manual'))) {
                btn.classList.add('active');
            }
        });
    }
    
    // Show/hide tab content
    document.getElementById('csvTab').style.display = tabName === 'csv' ? 'block' : 'none';
    document.getElementById('manualTab').style.display = tabName === 'manual' ? 'block' : 'none';
}

// ===== CSV Import =====

async function downloadTemplate() {
    const reportType = getReportType();
    window.location.href = `/api/csv/template/${reportType}`;
}

async function importCSV() {
    const csvContent = document.getElementById('csvInput').value.trim();
    
    if (!csvContent) {
        showStatus('⚠️ Please paste your CSV data in the text box first.\n\n' +
                   'STEPS:\n' +
                   '  1. Open your Excel file\n' +
                   '  2. Select all data (Ctrl+A or click top-left corner)\n' +
                   '  3. Copy (Ctrl+C)\n' +
                   '  4. Paste here (Ctrl+V)\n' +
                   '  5. Click Import button', 'warning');
        return;
    }
    
    const reportType = getReportType();
    const defaults = getDefaultsData();
    
    try {
        const response = await fetch('/api/csv/map', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                csv_content: csvContent,
                report_type: reportType,
                defaults: defaults
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            currentShipments = result.shipments;
            updateTable();
            
            // Show detailed feedback about the import
            showImportFeedback(result.feedback || `Successfully imported ${result.count} shipment(s)`);
            
            // Switch to manual tab to show the table
            switchTab('manual');
        } else {
            showStatus(result.error, 'error');
        }
    } catch (error) {
        const errorMsg = '❌ IMPORT FAILED\n\n' +
                        'Something went wrong while importing your data.\n\n' +
                        '💡 COMMON CAUSES:\n' +
                        '  • You might not have headers in your CSV\n' +
                        '  • The data might not be in CSV format\n' +
                        '  • There might be special characters causing issues\n\n' +
                        '💡 TRY THIS:\n' +
                        '  1. Open your Excel file\n' +
                        '  2. Make sure row 1 has column headers\n' +
                        '  3. Save the file as CSV (File → Save As → CSV)\n' +
                        '  4. Open the CSV in Notepad\n' +
                        '  5. Copy all the text from Notepad\n' +
                        '  6. Paste here and try again\n\n' +
                        'Technical error: ' + error.message;
        showStatus(errorMsg, 'error');
    }
}

function showImportFeedback(feedback) {
    // Show import feedback with details - stays visible!
    showStatus(feedback, 'info');
    // No timeout - message stays until user dismisses or takes next action
}

// ===== Table Management =====

function updateTableHeaders() {
    const reportType = getReportType();
    const thead = document.getElementById('shipmentsTableHead');
    
    let headers = [];
    
    if (reportType === 'CommonCarrier') {
        headers = [
            'Consignee Name', 'Address', 'City', 'State', 'ZIP',
            'Shipment Date', 'Weight (lbs)', 'Beverage Type', 'Tracking #', 'Actions'
        ];
    } else {
        headers = [
            'Consignee Name', 'Address', 'City', 'State', 'ZIP',
            'Shipment Date', 'Quantity (L)', 'Tracking #', 'Actions'
        ];
    }
    
    thead.innerHTML = '<tr>' + headers.map(h => `<th>${h}</th>`).join('') + '</tr>';
}

function updateTable() {
    updateTableHeaders();
    const tbody = document.getElementById('shipmentsTableBody');
    const reportType = getReportType();
    
    tbody.innerHTML = '';
    
    currentShipments.forEach((shipment, index) => {
        const row = tbody.insertRow();
        
        if (reportType === 'CommonCarrier') {
            row.innerHTML = `
                <td><input type="text" value="${shipment.consignee_name || ''}" onchange="updateShipment(${index}, 'consignee_name', this.value)"></td>
                <td><input type="text" value="${shipment.consignee_address_line1 || ''}" onchange="updateShipment(${index}, 'consignee_address_line1', this.value)"></td>
                <td><input type="text" value="${shipment.consignee_city || ''}" onchange="updateShipment(${index}, 'consignee_city', this.value)"></td>
                <td><input type="text" value="${shipment.consignee_state || ''}" maxlength="2" onchange="updateShipment(${index}, 'consignee_state', this.value)"></td>
                <td><input type="text" value="${shipment.consignee_zip || ''}" onchange="updateShipment(${index}, 'consignee_zip', this.value)"></td>
                <td><input type="date" value="${shipment.shipment_date || ''}" onchange="updateShipment(${index}, 'shipment_date', this.value)"></td>
                <td><input type="number" step="0.1" value="${shipment.weight_of_beverages || ''}" onchange="updateShipment(${index}, 'weight_of_beverages', this.value)"></td>
                <td>
                    <select onchange="updateShipment(${index}, 'beverage_type', this.value)">
                        <option value="">Select...</option>
                        <option value="Beer" ${shipment.beverage_type === 'Beer' ? 'selected' : ''}>Beer</option>
                        <option value="Wine" ${shipment.beverage_type === 'Wine' ? 'selected' : ''}>Wine</option>
                        <option value="Spirits" ${shipment.beverage_type === 'Spirits' ? 'selected' : ''}>Spirits</option>
                        <option value="Unknown" ${shipment.beverage_type === 'Unknown' ? 'selected' : ''}>Unknown</option>
                    </select>
                </td>
                <td><input type="text" value="${shipment.tracking_number || ''}" onchange="updateShipment(${index}, 'tracking_number', this.value)"></td>
                <td><button class="btn btn-secondary" onclick="deleteShipment(${index})">Delete</button></td>
            `;
        } else {
            row.innerHTML = `
                <td><input type="text" value="${shipment.consignee_name || ''}" onchange="updateShipment(${index}, 'consignee_name', this.value)"></td>
                <td><input type="text" value="${shipment.consignee_address_line1 || ''}" onchange="updateShipment(${index}, 'consignee_address_line1', this.value)"></td>
                <td><input type="text" value="${shipment.consignee_city || ''}" onchange="updateShipment(${index}, 'consignee_city', this.value)"></td>
                <td><input type="text" value="${shipment.consignee_state || ''}" maxlength="2" onchange="updateShipment(${index}, 'consignee_state', this.value)"></td>
                <td><input type="text" value="${shipment.consignee_zip || ''}" onchange="updateShipment(${index}, 'consignee_zip', this.value)"></td>
                <td><input type="date" value="${shipment.shipment_date || ''}" onchange="updateShipment(${index}, 'shipment_date', this.value)"></td>
                <td><input type="number" step="0.1" value="${shipment.quantity_of_wine || ''}" onchange="updateShipment(${index}, 'quantity_of_wine', this.value)"></td>
                <td><input type="text" value="${shipment.tracking_number || ''}" onchange="updateShipment(${index}, 'tracking_number', this.value)"></td>
                <td><button class="btn btn-secondary" onclick="deleteShipment(${index})">Delete</button></td>
            `;
        }
    });
    
    document.getElementById('shipmentCount').textContent = currentShipments.length;
    document.getElementById('shipmentsTableContainer').style.display = 'block';
}

function updateShipment(index, field, value) {
    currentShipments[index][field] = value;
}

function deleteShipment(index) {
    if (confirm('Delete this shipment?')) {
        currentShipments.splice(index, 1);
        updateTable();
    }
}

function clearShipments() {
    if (confirm('Clear all shipments?')) {
        currentShipments = [];
        updateTable();
        document.getElementById('shipmentsTableContainer').style.display = 'none';
    }
}

function addShipmentRow() {
    const reportType = getReportType();
    const defaults = getDefaultsData();
    
    let newShipment = {};
    
    if (reportType === 'CommonCarrier') {
        newShipment = {
            consignor_name: defaults.consignor?.name || '',
            consignor_address_line1: defaults.consignor?.address_line1 || '',
            consignor_city: defaults.consignor?.city || '',
            consignor_state: defaults.consignor?.state || 'WI',
            consignor_zip: defaults.consignor?.zip || '',
            permit_number: defaults.consignor?.permit_number || '',
            consignee_name: '',
            consignee_address_line1: '',
            consignee_city: '',
            consignee_state: '',
            consignee_zip: '',
            shipment_date: '',
            beverage_type: '',
            weight_of_beverages: '',
            tracking_number: ''
        };
    } else {
        newShipment = {
            manufacturer_name: defaults.manufacturer?.name || '',
            manufacturer_address_line1: defaults.manufacturer?.address_line1 || '',
            manufacturer_city: defaults.manufacturer?.city || '',
            manufacturer_state: defaults.manufacturer?.state || 'WI',
            manufacturer_zip: defaults.manufacturer?.zip || '',
            wine_permit_number: defaults.manufacturer?.wine_permit_number || '',
            common_carrier_permit_number: defaults.common_carrier_permit || '',
            consignee_name: '',
            consignee_address_line1: '',
            consignee_city: '',
            consignee_state: '',
            consignee_zip: '',
            shipment_date: '',
            quantity_of_wine: '',
            tracking_number: ''
        };
    }
    
    currentShipments.push(newShipment);
    updateTable();
}

// ===== Data Extraction =====

function getFilerData() {
    return {
        tin_type: document.getElementById('tinType').value,
        tin_value: document.getElementById('tinValue').value,
        state_ein: document.getElementById('stateEIN').value,
        business_name_line1: document.getElementById('businessName1').value,
        business_name_line2: document.getElementById('businessName2').value,
        address_line1: document.getElementById('address1').value,
        address_line2: document.getElementById('address2').value,
        city: document.getElementById('city').value,
        state: document.getElementById('state').value,
        zip: document.getElementById('zip').value
    };
}

function getDefaultsData() {
    const reportType = getReportType();
    
    if (reportType === 'CommonCarrier') {
        return {
            consignor: {
                name: document.getElementById('ccConsignorName').value,
                address_line1: document.getElementById('ccConsignorAddress1').value,
                city: document.getElementById('ccConsignorCity').value,
                state: document.getElementById('ccConsignorState').value,
                zip: document.getElementById('ccConsignorZip').value,
                permit_number: document.getElementById('ccPermitNumber').value
            }
        };
    } else {
        return {
            manufacturer: {
                name: document.getElementById('fhManufacturerName').value,
                address_line1: document.getElementById('fhManufacturerAddress1').value,
                city: document.getElementById('fhManufacturerCity').value,
                state: document.getElementById('fhManufacturerState').value,
                zip: document.getElementById('fhManufacturerZip').value,
                wine_permit_number: document.getElementById('fhWinePermitNumber').value
            },
            common_carrier_permit: document.getElementById('fhCCPermitNumber').value
        };
    }
}

// ===== XML Generation =====

async function generateXML() {
    // Pre-flight checks with helpful messages
    if (currentShipments.length === 0) {
        showStatus('⚠️ NO SHIPMENTS FOUND\n\n' +
                   'You need to add shipment data first!\n\n' +
                   'WHAT TO DO:\n' +
                   '  Option 1: Import from CSV\n' +
                   '    • Go to Step 5\n' +
                   '    • Click "Import from CSV" tab\n' +
                   '    • Paste your data and click Import\n\n' +
                   '  Option 2: Add manually\n' +
                   '    • Go to Step 5\n' +
                   '    • Click "Manual Entry" tab\n' +
                   '    • Click "Add Shipment" button\n' +
                   '    • Fill in the table', 'warning');
        return;
    }
    
    const reportType = getReportType();
    const filerData = getFilerData();
    const taxPeriodBegin = document.getElementById('taxPeriodBegin').value;
    const taxPeriodEnd = document.getElementById('taxPeriodEnd').value;
    const ackEmail = document.getElementById('ackEmail').value;
    const amended = document.getElementById('amendedReturn').checked;
    
    // Detailed validation with specific guidance
    let missingFields = [];
    
    if (!filerData.tin_value) missingFields.push('• Step 2: TIN Value (9 digits required)');
    if (!filerData.business_name_line1) missingFields.push('• Step 2: Business Name Line 1');
    if (!filerData.address_line1) missingFields.push('• Step 2: Address Line 1');
    if (!filerData.city) missingFields.push('• Step 2: City');
    if (!filerData.state) missingFields.push('• Step 2: State (2 letters)');
    if (!filerData.zip) missingFields.push('• Step 2: ZIP Code');
    
    if (missingFields.length > 0) {
        showStatus('⚠️ MISSING REQUIRED INFORMATION\n\n' +
                   'Please fill in these REQUIRED fields:\n\n' +
                   missingFields.join('\n') + '\n\n' +
                   'TIP: Look for fields marked with a red asterisk (*)', 'warning');
        return;
    }
    
    if (!taxPeriodBegin || !taxPeriodEnd || !ackEmail) {
        let missing = [];
        if (!taxPeriodBegin) missing.push('• Tax Period Begin date');
        if (!taxPeriodEnd) missing.push('• Tax Period End date');
        if (!ackEmail) missing.push('• Acknowledgement Email');
        
        showStatus('⚠️ MISSING REQUIRED INFORMATION IN STEP 3\n\n' +
                   'Please fill in:\n\n' +
                   missing.join('\n') + '\n\n' +
                   'Go to Step 3: Tax Period & Contact', 'warning');
        return;
    }
    
    // Check defaults are filled (most common issue!)
    const defaults = getDefaultsData();
    let defaultWarnings = [];
    
    if (reportType === 'CommonCarrier') {
        if (!defaults.consignor?.name) defaultWarnings.push('• Consignor Name');
        if (!defaults.consignor?.address_line1) defaultWarnings.push('• Consignor Address Line 1');
        if (!defaults.consignor?.city) defaultWarnings.push('• Consignor City');
        if (!defaults.consignor?.state) defaultWarnings.push('• Consignor State');
        if (!defaults.consignor?.zip) defaultWarnings.push('• Consignor ZIP');
    } else {
        if (!defaults.manufacturer?.name) defaultWarnings.push('• Manufacturer Name');
        if (!defaults.manufacturer?.address_line1) defaultWarnings.push('• Manufacturer Address Line 1');
        if (!defaults.manufacturer?.city) defaultWarnings.push('• Manufacturer City');
        if (!defaults.manufacturer?.state) defaultWarnings.push('• Manufacturer State');
        if (!defaults.manufacturer?.zip) defaultWarnings.push('• Manufacturer ZIP');
        if (!defaults.manufacturer?.wine_permit_number) defaultWarnings.push('• Wine Permit Number (15 digits)');
        if (!defaults.common_carrier_permit) defaultWarnings.push('• Common Carrier Permit Number (15 digits)');
    }
    
    if (defaultWarnings.length > 0) {
        const section = reportType === 'CommonCarrier' ? 'Default Consignor Information' : 'Default Manufacturer Information';
        showStatus('⚠️ MISSING SENDER/MANUFACTURER INFORMATION\n\n' +
                   'Please fill in Step 4: Default Values\n\n' +
                   `Missing fields in "${section}":\n\n` +
                   defaultWarnings.join('\n') + '\n\n' +
                   '📋 WHAT TO DO:\n' +
                   '  1. Scroll up to Step 4: Default Values\n' +
                   `  2. Fill in the ${section} section\n` +
                   '  3. Click "💾 Save Defaults"\n' +
                   '  4. Come back here and try again\n\n' +
                   '⚠️  This information is used for ALL shipments!', 'warning');
        
        // Scroll to defaults section
        document.getElementById('defaultsSection').scrollIntoView({ behavior: 'smooth', block: 'center' });
        return;
    }
    
    // Clear previous results and show loading state
    generatedXML = '';
    document.getElementById('xmlPreviewSection').style.display = 'none';
    document.getElementById('xmlPreview').textContent = '';
    document.getElementById('validationStatus').textContent = '';
    
    // Show loading message
    showStatus('⏳ Generating and validating your file...\n\nPlease wait...', 'info');
    
    // Get current defaults from the form (not saved file)
    const currentDefaults = getDefaultsData();
    
    try {
        const response = await fetch('/api/xml/generate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                report_type: reportType,
                filer_data: filerData,
                shipments: currentShipments,
                tax_period_begin: taxPeriodBegin,
                tax_period_end: taxPeriodEnd,
                ack_email: ackEmail,
                amended: amended,
                defaults: currentDefaults  // Send current form values
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            generatedXML = result.xml;
            document.getElementById('xmlPreview').textContent = generatedXML;
            
            // Success message with next steps
            const successMsg = '✅ SUCCESS! YOUR FILE IS READY!\n\n' +
                             '═══════════════════════════════════════════════════\n\n' +
                             `✓ Generated ${reportType} report\n` +
                             `✓ Included ${currentShipments.length} shipment(s)\n` +
                             '✓ Passed all Wisconsin DOR validation checks\n\n' +
                             'NEXT STEPS:\n' +
                             '  1. Review the file preview below (optional)\n' +
                             '  2. Click "💾 Download XML File" button\n' +
                             '  3. Save the file to your computer\n' +
                             '  4. Submit to Wisconsin DOR per their instructions\n\n' +
                             '💡 TIP: Keep a copy of this file for your records!';
            
            document.getElementById('validationStatus').className = 'status-message success';
            document.getElementById('validationStatus').innerHTML = 
                '<pre style="white-space: pre-wrap; font-family: inherit; margin: 0;">' + successMsg + '</pre>';
            document.getElementById('xmlPreviewSection').style.display = 'block';
            
            // Scroll to preview
            document.getElementById('xmlPreviewSection').scrollIntoView({ behavior: 'smooth' });
        } else {
            // Validation failed - show enhanced error message
            generatedXML = result.xml || '';  // Save it anyway so user can see what was generated
            
            // Hide status message to make error stand out
            document.getElementById('statusMessage').style.display = 'none';
            
            const errorMsg = result.validation_error || result.error;
            document.getElementById('validationStatus').className = 'status-message error';
            document.getElementById('validationStatus').innerHTML = 
                '<pre style="white-space: pre-wrap; font-family: inherit; margin: 0;">' + errorMsg + '</pre>';
            
            // Show XML preview collapsed by default on error
            document.getElementById('xmlPreview').textContent = generatedXML;
            document.getElementById('xmlPreviewSection').style.display = 'block';
            
            // Scroll to the error message so user sees it immediately
            document.getElementById('validationStatus').scrollIntoView({ behavior: 'smooth', block: 'start' });
            
            // Add a visual flash to indicate new error
            document.getElementById('validationStatus').style.animation = 'none';
            setTimeout(() => {
                document.getElementById('validationStatus').style.animation = 'fadeIn 0.5s';
            }, 10);
        }
    } catch (error) {
        showStatus('❌ UNEXPECTED ERROR\n\n' +
                   'Something went wrong while generating the file.\n\n' +
                   '💡 WHAT TO TRY:\n' +
                   '  1. Make sure all fields are filled in\n' +
                   '  2. Try clicking "Generate & Validate" again\n' +
                   '  3. If it keeps failing, try refreshing the page (F5)\n' +
                   '     and starting over\n\n' +
                   'Technical error: ' + error.message, 'error');
    }
}

async function downloadXML() {
    if (!generatedXML) {
        showStatus('Please generate XML first', 'warning');
        return;
    }
    
    const reportType = getReportType();
    
    try {
        const response = await fetch('/api/xml/save', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                xml: generatedXML,
                report_type: reportType
            })
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
            a.download = `${reportType}_${timestamp}.xml`;
            
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            showStatus('XML file downloaded successfully!', 'success');
        } else {
            showStatus('Error downloading XML file', 'error');
        }
    } catch (error) {
        showStatus('Error: ' + error.message, 'error');
    }
}

function copyXML() {
    if (!generatedXML) {
        showStatus('Please generate XML first', 'warning');
        return;
    }
    
    navigator.clipboard.writeText(generatedXML).then(() => {
        showStatus('XML copied to clipboard!', 'success');
    }).catch(err => {
        showStatus('Error copying to clipboard: ' + err.message, 'error');
    });
}

// ===== UI Utilities =====

function showStatus(message, type = 'info') {
    const statusEl = document.getElementById('statusMessage');
    
    // Add a close button (×) for all message types
    const closeBtn = '<button onclick="document.getElementById(\'statusMessage\').style.display=\'none\'" ' +
                    'style="float: right; background: none; border: none; font-size: 1.5em; ' +
                    'cursor: pointer; padding: 0 10px; color: inherit; opacity: 0.7; ' +
                    'line-height: 1;" title="Close this message">&times;</button>';
    
    statusEl.innerHTML = closeBtn + '<div style="clear: both;"><pre style="white-space: pre-wrap; font-family: inherit; margin: 0;">' + message + '</pre></div>';
    statusEl.className = 'status-message ' + type;
    statusEl.style.display = 'block';
    
    // ALL messages stay visible until:
    // - User clicks the X button to close
    // - User clicks Generate again (which clears and shows new status)
    // - User takes action that triggers new status
    // NO AUTO-HIDE! Users need time to read and act on all messages.
}

