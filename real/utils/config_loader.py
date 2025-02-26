import json

class ConfigLoader:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config_data = self.load_config()

    def load_config(self):
        with open(self.config_file, 'r') as file:
            return json.load(file)

    def get(self, section, key, default=None):
        return self.config_data.get(section, {}).get(key, default)

