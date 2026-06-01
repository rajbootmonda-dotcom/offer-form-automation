import os
from dotenv import load_dotenv

load_dotenv()

# Proxy Configuration
PROXY_SERVER = os.getenv('PROXY_SERVER', 'proxy-jet.io')
PROXY_PORT = os.getenv('PROXY_PORT', '1010')
PROXY_USERNAME = os.getenv('PROXY_USERNAME', '250729XnnNO')
PROXY_PASSWORD = os.getenv('PROXY_PASSWORD', 'AzI23456789abcd')

# IP Quality Score API
IP_QUALITY_API_KEY = os.getenv('IP_QUALITY_API_KEY', '')

# Google Sheets
GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID', '')
GOOGLE_CREDENTIALS_FILE = 'credentials.json'

# Offer Form URL
OFFER_URL = 'https://example.com/offer'  # Replace with actual URL

# Browser Configuration
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
]

# Automation Behavior
DELAY_MIN = 2  # Minimum delay between actions (seconds)
DELAY_MAX = 8  # Maximum delay between actions (seconds)
MOUSE_MOVEMENT_ENABLED = True  # Enable random mouse movements
RANDOM_SCROLL_ENABLED = True  # Enable random scrolling

# Logging
LOG_DIR = 'logs'
SCREENSHOT_DIR = 'screenshots'
