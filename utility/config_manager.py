import os
import json

# Set default appearance mode and color theme
default_appearance = "System"
config_file = os.path.join(os.path.dirname(__file__), "config.json")

def load_config():
    """Load saved appearance mode if it exists"""
    config = load_full_config()
    return config.get("appearance_mode", default_appearance)

def save_config(appearance_mode):
    """Save appearance mode preference"""
    config = load_full_config()
    config["appearance_mode"] = appearance_mode
    save_full_config(config)

def load_full_config():
    """Load the complete configuration file"""
    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as f:
                config = json.load(f)
                return config
        except Exception as e:
            print(f"Error loading config: {e}")
    return {"appearance_mode": default_appearance, "deepl_api_key": ""}

def save_full_config(config):
    """Save the complete configuration file"""
    try:
        with open(config_file, "w") as f:
            json.dump(config, f)
    except Exception as e:
        print(f"Error saving config: {e}")

def get_api_key():
    """Get the DeepL API key from config"""
    config = load_full_config()
    return config.get("deepl_api_key", "")

def save_api_key(api_key):
    """Save DeepL API key to config"""
    config = load_full_config()
    config["deepl_api_key"] = api_key
    save_full_config(config)

