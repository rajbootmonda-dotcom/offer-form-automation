import requests
from config import PROXY_SERVER, PROXY_PORT, PROXY_USERNAME, PROXY_PASSWORD, IP_QUALITY_API_KEY
import time

class ProxyManager:
    def __init__(self):
        self.proxy_server = PROXY_SERVER
        self.proxy_port = PROXY_PORT
        self.proxy_username = PROXY_USERNAME
        self.proxy_password = PROXY_PASSWORD
        self.ip_quality_key = IP_QUALITY_API_KEY
    
    def get_proxy_url(self) -> str:
        """Build proxy URL with authentication"""
        if self.proxy_username and self.proxy_password:
            return f'http://{self.proxy_username}:{self.proxy_password}@{self.proxy_server}:{self.proxy_port}'
        return f'http://{self.proxy_server}:{self.proxy_port}'
    
    def validate_proxy(self) -> bool:
        """Validate proxy is working"""
        try:
            proxy_url = self.get_proxy_url()
            proxies = {'http': proxy_url, 'https': proxy_url}
            
            response = requests.get(
                'http://httpbin.org/ip',
                proxies=proxies,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✓ Proxy validated. IP: {response.json()['origin']}")
                return True
            return False
        except Exception as e:
            print(f"✗ Proxy validation failed: {e}")
            return False
    
    def check_ip_reputation(self, ip: str) -> dict:
        """Check IP reputation using IP Quality Score"""
        if not self.ip_quality_key:
            print("IP Quality API key not configured")
            return {}
        
        try:
            url = f'https://api.abuseipdb.com/api/v2/check'
            headers = {'Key': self.ip_quality_key, 'Accept': 'application/json'}
            params = {'ipAddress': ip, 'maxAgeInDays': '90'}
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            print(f"Error checking IP reputation: {e}")
            return {}
