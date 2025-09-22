import pytest
from plugins.csv_plugin import CSVPlugin
from plugins.api_plugin import APIPlugin

def test_csv_plugin_initialization():
    config = {
        'file_path': 'data/inputs/sample_data.csv',
        'output_path': 'data/outputs/test_output.csv'
    }
    plugin = CSVPlugin(config)
    assert plugin.config == config

def test_api_plugin_initialization():
    config = {
        'url': 'https://api.example.com/data',
        'output_path': 'data/outputs/test_api_output.json'
    }
    plugin = APIPlugin(config)
    assert plugin.config == config

# Add more tests as needed
