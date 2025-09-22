from abc import ABC, abstractmethod
import logging

class BasePlugin(ABC):
    """Abstract base class for all data collection plugins"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def collect(self, **kwargs):
        """Collect data from the specified source"""
        pass
    
    @abstractmethod
    def transform(self, data, **kwargs):
        """Transform the collected data"""
        pass
    
    @abstractmethod
    def save(self, data, **kwargs):
        """Save the transformed data"""
        pass
    
    def execute(self, **kwargs):
        """Execute the complete data collection process"""
        try:
            raw_data = self.collect(**kwargs)
            transformed_data = self.transform(raw_data, **kwargs)
            self.save(transformed_data, **kwargs)
            self.logger.info("Plugin execution completed successfully")
            return transformed_data
        except Exception as e:
            self.logger.error(f"Plugin execution failed: {str(e)}")
            raise
