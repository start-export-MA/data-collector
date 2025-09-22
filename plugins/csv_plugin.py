import pandas as pd
from .base_plugin import BasePlugin

class CSVPlugin(BasePlugin):
    """Plugin for collecting data from CSV files"""
    
    def collect(self, **kwargs):
        file_path = self.config.get('file_path')
        self.logger.info(f"Collecting data from CSV file: {file_path}")
        return pd.read_csv(file_path)
    
    def transform(self, data, **kwargs):
        # Apply transformations if specified in config
        transformations = self.config.get('transformations', {})
        
        if 'rename_columns' in transformations:
            data = data.rename(columns=transformations['rename_columns'])
        
        if 'filter' in transformations:
            for column, value in transformations['filter'].items():
                data = data[data[column] == value]
        
        return data
    
    def save(self, data, **kwargs):
        output_path = self.config.get('output_path', 'data/outputs/processed_data.csv')
        data.to_csv(output_path, index=False)
        self.logger.info(f"Data saved to: {output_path}")
