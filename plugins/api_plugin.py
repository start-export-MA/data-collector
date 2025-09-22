import requests
from .base_plugin import BasePlugin

class APIPlugin(BasePlugin):
    """Plugin for collecting data from APIs"""
    
    def collect(self, **kwargs):
        url = self.config.get('url')
        headers = self.config.get('headers', {})
        params = self.config.get('params', {})
        
        self.logger.info(f"Collecting data from API: {url}")
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        return response.json()
    
    def transform(self, data, **kwargs):
        # Extract relevant data based on configuration
        data_path = self.config.get('data_path', [])
        transformed_data = data
        
        for path in data_path:
            if isinstance(transformed_data, dict) and path in transformed_data:
                transformed_data = transformed_data[path]
            else:
                self.logger.warning(f"Data path {path} not found in API response")
                return None
        
        return transformed_data
    
    def save(self, data, **kwargs):
        import json
        output_path = self.config.get('output_path', 'data/outputs/api_data.json')
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        self.logger.info(f"API data saved to: {output_path}")
