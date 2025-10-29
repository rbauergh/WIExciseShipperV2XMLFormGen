"""
Configuration Manager for Wisconsin Excise Tax XML Generator
Manages filer information and application settings
"""

import json
import os
from typing import Dict, Optional


class ConfigManager:
    """Manage application configuration and filer information"""
    
    def __init__(self, config_dir: str = None):
        """
        Initialize configuration manager
        
        Args:
            config_dir: Directory to store configuration files
        """
        if config_dir is None:
            config_dir = os.path.join(os.path.dirname(__file__), 'config')
        
        self.config_dir = config_dir
        self.filer_config_file = os.path.join(config_dir, 'filer_config.json')
        self.defaults_config_file = os.path.join(config_dir, 'defaults.json')
        
        os.makedirs(config_dir, exist_ok=True)
    
    def save_filer_config(self, filer_data: Dict) -> None:
        """
        Save filer configuration
        
        Args:
            filer_data: Dictionary containing filer information
        """
        with open(self.filer_config_file, 'w', encoding='utf-8') as f:
            json.dump(filer_data, f, indent=2)
    
    def load_filer_config(self) -> Optional[Dict]:
        """
        Load filer configuration
        
        Returns:
            Dictionary with filer information or None if not found
        """
        if not os.path.exists(self.filer_config_file):
            return None
        
        try:
            with open(self.filer_config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return None
    
    def save_defaults(self, defaults: Dict) -> None:
        """
        Save default values for shipments
        
        Args:
            defaults: Dictionary containing default values
        """
        with open(self.defaults_config_file, 'w', encoding='utf-8') as f:
            json.dump(defaults, f, indent=2)
    
    def load_defaults(self) -> Optional[Dict]:
        """
        Load default values
        
        Returns:
            Dictionary with defaults or None if not found
        """
        if not os.path.exists(self.defaults_config_file):
            return None
        
        try:
            with open(self.defaults_config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return None
    
    def get_default_filer(self) -> Dict:
        """
        Get default filer configuration
        
        Returns:
            Dictionary with default/empty filer information
        """
        return {
            'tin_type': 'FEIN',
            'tin_value': '',
            'state_ein': '',
            'business_name_line1': '',
            'business_name_line2': '',
            'address_line1': '',
            'address_line2': '',
            'city': '',
            'state': 'WI',
            'zip': ''
        }
    
    def get_default_consignor(self) -> Dict:
        """
        Get default consignor information (for Common Carrier)
        
        Returns:
            Dictionary with default consignor information
        """
        return {
            'name': '',
            'address_line1': '',
            'address_line2': '',
            'city': '',
            'state': 'WI',
            'zip': '',
            'permit_number': ''
        }
    
    def get_default_manufacturer(self) -> Dict:
        """
        Get default manufacturer information (for Fulfillment House)
        
        Returns:
            Dictionary with default manufacturer information
        """
        return {
            'name': '',
            'address_line1': '',
            'address_line2': '',
            'city': '',
            'state': 'WI',
            'zip': '',
            'wine_permit_number': ''
        }

