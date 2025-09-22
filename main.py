#!/usr/bin/env python3
"""
Automated Data Collection Framework
A flexible, plugin-based system for collecting data from various sources.
"""

import argparse
from core.collector import DataCollector

def main():
    parser = argparse.ArgumentParser(description="Automated Data Collection Framework")
    parser.add_argument('--config', default='config/config.yaml', help='Path to main configuration file')
    parser.add_argument('--plugins-config', default='config/plugins.yaml', help='Path to plugins configuration file')
    parser.add_argument('--list-plugins', action='store_true', help='List available plugins and exit')
    
    args = parser.parse_args()
    
    collector = DataCollector(args.config, args.plugins_config)
    
    if args.list_plugins:
        collector.initialize()
        print("Available plugins:")
        for plugin in collector.plugin_manager.list_plugins():
            print(f"  - {plugin}")
        return
    
    try:
        collector.initialize()
        collector.run()
    except Exception as e:
        print(f"Data collection failed: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
