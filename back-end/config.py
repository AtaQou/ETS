import json


def load_config():
    with open('appsettings.json', 'r') as f:
        config_data = json.load(f)
    return config_data
