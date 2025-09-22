import importlib
import pkgutil
import logging
from pathlib import Path

class PluginManager:
    """Manages the loading and execution of plugins"""
    
    def __init__(self, plugin_dir="plugins"):
        self.plugins = {}
        self.plugin_dir = plugin_dir
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def discover_plugins(self):
        """Discover all available plugins in the plugins directory"""
        plugin_path = Path(self.plugin_dir)
        
        for finder, name, ispkg in pkgutil.iter_modules([str(plugin_path)]):
            if name.startswith('_'):
                continue
                
            try:
                module = importlib.import_module(f"{self.plugin_dir}.{name}")
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type) and 
                        issubclass(attr, __import__(f"{self.plugin_dir}.base_plugin").BasePlugin) and
                        attr != __import__(f"{self.plugin_dir}.base_plugin").BasePlugin):
                        self.plugins[name] = attr
                        self.logger.info(f"Discovered plugin: {name}")
            except ImportError as e:
                self.logger.error(f"Failed to import plugin {name}: {str(e)}")
    
    def get_plugin(self, name):
        """Get a plugin instance by name"""
        if name not in self.plugins:
            raise ValueError(f"Plugin '{name}' not found")
        return self.plugins[name]
    
    def execute_plugin(self, name, config, **kwargs):
        """Execute a specific plugin"""
        plugin_class = self.get_plugin(name)
        plugin_instance = plugin_class(config)
        return plugin_instance.execute(**kwargs)
    
    def list_plugins(self):
        """List all available plugins"""
        return list(self.plugins.keys())
