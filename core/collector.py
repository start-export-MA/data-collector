import yaml
import logging
from .plugin_manager import PluginManager

class DataCollector:
    """Main data collection framework"""
    
    def __init__(self, config_path="config/config.yaml", plugins_config_path="config/plugins.yaml"):
        self.config = self._load_config(config_path)
        self.plugins_config = self._load_config(plugins_config_path)
        self.plugin_manager = PluginManager()
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Set up logging
        logging.basicConfig(
            level=getattr(logging, self.config.get('log_level', 'INFO')),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def _load_config(self, config_path):
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise Exception(f"Failed to load config from {config_path}: {str(e)}")
    
    def initialize(self):
        """Initialize the data collector"""
        self.logger.info("Initializing Data Collector")
        self.plugin_manager.discover_plugins()
        self.logger.info(f"Available plugins: {', '.join(self.plugin_manager.list_plugins())}")
    
    def run(self):
        """Run the data collection process"""
        self.logger.info("Starting data collection process")
        
        for plugin_name, plugin_config in self.plugins_config.items():
            if plugin_config.get('enabled', False):
                try:
                    self.logger.info(f"Executing plugin: {plugin_name}")
                    result = self.plugin_manager.execute_plugin(
                        plugin_name, 
                        plugin_config, 
                        **self.config.get('global_settings', {})
                    )
                    self.logger.info(f"Plugin {plugin_name} completed successfully")
                except Exception as e:
                    self.logger.error(f"Plugin {plugin_name} failed: {str(e)}")
                    if not self.config.get('continue_on_error', True):
                        raise
            else:
                self.logger.info(f"Plugin {plugin_name} is disabled, skipping")
        
        self.logger.info("Data collection process completed")
