import requests
import random
from typing import Dict, Optional
from config import PROXY_SERVER, PROXY_PORT, PROXY_USERNAME, PROXY_PASSWORD, IP_QUALITY_API_KEY

class ProxyManager:
    def __init__(self):
        self.proxy_server = PROXY_SERVER
        self.proxy_port = PROXY_PORT
        self.proxy_username = PROXY_USERNAME
        self.proxy_password = PROXY_PASSWORD
        self.ip_quality_api = IP_QUALITY_API_KEY
        self.used_ips = set()
        self.ip_scores = {}

    def get_proxy_url(self) -> str:
        """Generate proxy URL with authentication"""
        return f"http://{self.proxy_username}:{self.proxy_password}@{self.proxy_server}:{self.proxy_port}"

    def get_proxy_dict(self) -> Dict[str, str]:
        """Return proxy as dictionary for requests"""
        proxy_url = self.get_proxy_url()
        return {
            'http': proxy_url,
            'https': proxy_url
        }

    def check_ip_quality(self, ip: str) -> Dict:
        """Check IP quality score using Fraudlogix/IP Quality Score"""
        if not self.ip_quality_api:
            return {'score': None, 'is_valid': True}
        
        try:
            url = f"https://api.abuseipdb.com/api/v2/check"
            headers = {'Key': self.ip_quality_api, 'Accept': 'application/json'}
            params = {'ipAddress': ip, 'maxAgeInDays': 90}
            
            response = requests.get(url, headers=headers, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                abuse_score = data.get('data', {}).get('abuseConfidenceScore', 0)
                return {
                    'score': abuse_score,
                    'is_valid': abuse_score < 75,
                    'ip': ip
                }
        except Exception as e:
            print(f"Error checking IP quality: {e}")
        
        return {'score': None, 'is_valid': True, 'ip': ip}

    def is_duplicate_ip(self, ip: str) -> bool:
        """Check if IP has been used before"""
        return ip in self.used_ips

    def register_ip(self, ip: str):
        """Register IP as used"""
        self.used_ips.add(ip)

    def validate_proxy(self) -> bool:
        """Test proxy connectivity"""
        try:
            response = requests.get(
                'http://httpbin.org/ip',
                proxies=self.get_proxy_dict(),
                timeout=5
            )
            if response.status_code == 200:
                ip = response.json().get('origin')
                print(f"Proxy validated. Current IP: {ip}")
                
                quality = self.check_ip_quality(ip)
                print(f"IP Quality Score: {quality}")
                
                if self.is_duplicate_ip(ip):
                    print(f"WARNING: IP {ip} has been used before!")
                    return False
                
                self.register_ip(ip)
                return quality['is_valid']
        except Exception as e:
            print(f"Proxy validation failed: {e}")
        
        return False
