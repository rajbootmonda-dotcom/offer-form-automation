import os
from dotenv import load_dotenv

load_dotenv()

# Proxy Configuration
PROXY_SERVER = os.getenv('PROXY_SERVER', 'proxy-jet.io')
PROXY_PORT = os.getenv('PROXY_PORT', '1010')
PROXY_USERNAME = os.getenv('PROXY_USERNAME', '250729XnnNO')
PROXY_PASSWORD = os.getenv('PROXY_PASSWORD', 'AzI23456789abcd')

# IP Quality Score
IP_QUALITY_API_KEY = os.getenv('IP_QUALITY_API_KEY')

# Google Sheets
GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID', '197jkMk3MC5_KD7n6rT459RJQC0K_F3cI8k4ShSO7TMk')
GOOGLE_SHEET_RANGE = os.getenv('GOOGLE_SHEET_RANGE', 'Sheet1!A:M')

# Offer
OFFER_URL = os.getenv('OFFER_URL', 'https://getmyoffer.app/MY8KJ3Yv')

# Behavior
DELAY_MIN = int(os.getenv('DELAY_MIN', '3'))
DELAY_MAX = int(os.getenv('DELAY_MAX', '8'))
MOUSE_MOVEMENT_ENABLED = os.getenv('MOUSE_MOVEMENT_ENABLED', 'true').lower() == 'true'
RANDOM_SCROLL_ENABLED = os.getenv('RANDOM_SCROLL_ENABLED', 'true').lower() == 'true'

# User Agents (Facebook/TikTok)
USER_AGENTS = [
    'Mozilla/5.0 (Linux; Android 16; CPH2449 Build/UKQ1.230924.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/147.0.7727.55 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/553.0;]',
    'Mozilla/5.0 (Linux; Android 14; SM-A135F Build/TP1A.220624.014) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.7727.55 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/552.0;]',
    'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.7727.55 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/551.0;]',
    'Mozilla/5.0 (Linux; Android 15; SM-G991B Build/UP1A.231005.007) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.7727.55 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/550.0;]',
    'Mozilla/5.0 (Linux; Android 16; RMX3461 Build/S) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.7727.55 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/549.0;]'
]

FORM_FIELDS = {
    'header': 'header',
    'email': 'email',
    'fst': 'first_name',
    'last': 'last_name',
    'address': 'address',
    'zip': 'zip_code',
    'cellphone': 'phone',
    'city': 'city',
    'state': 'state',
    'month': 'month',
    'day': 'day',
    'year': 'year',
    'gender': 'gender'
}
