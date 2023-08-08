import json

config_filename = '/home/kali/AMP-Tools/config.json'

def load_config():
    try:
        with open(config_filename, "r") as config_file:
            config = json.load(config_file)
            return config
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    
def save_config(config):
    with open(config_filename, "w") as config_file:
        json.dump(config, config_file, indent=4)