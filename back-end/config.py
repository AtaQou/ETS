import os
import json
from dotenv import load_dotenv

# Load .env file
load_dotenv()

def load_config():
    with open('appsettings.json', 'r') as f:
        config_data = json.load(f)
    return config_data

# Google API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
