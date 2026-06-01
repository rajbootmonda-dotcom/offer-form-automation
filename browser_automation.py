import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
from typing import Dict
from config import USER_AGENTS, DELAY_MIN, DELAY_MAX, MOUSE_MOVEMENT_ENABLED, RANDOM_SCROLL_ENABLED
from proxy_manager import ProxyManager
from screenshot_handler import ScreenshotHandler

class BrowserAutomation:
    def __init__(self, proxy_manager: ProxyManager):
        self.proxy_manager = proxy_manager
        self.driver = None
        self.wait = None
        self.screenshot_handler = ScreenshotHandler()
    
    def _random_delay(self):
        """Add random delay for human behavior"""
        delay = random.uniform(DELAY_MIN, DELAY_MAX)
        time.sleep(delay)
    
    def _random_mouse_movement(self):
        """Simulate random mouse movements"""
        if not MOUSE_MOVEMENT_ENABLED:
            return
        
        actions = ActionChains(self.driver)
        for _ in range(random.randint(2, 5)):
            x = random.randint(0, 1920)
            y = random.randint(0, 1080)
            actions.move_by_offset(x, y)
            actions.pause(random.uniform(0.1, 0.5))
        actions.perform()
    
    def _random_scroll(self):
        """Simulate random scrolling"""
        if not RANDOM_SCROLL_ENABLED:
            return
        
        for _ in range(random.randint(2, 4)):
            scroll_amount = random.randint(100, 500)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            self._random_delay()
    
    def initialize_browser(self) -> bool:
        """Initialize undetected Chrome browser with proxy"""
        try:
            proxy_url = self.proxy_manager.get_proxy_url()
            
            if not self.proxy_manager.validate_proxy():
                print("Proxy validation failed")
                return False
            
            options = uc.ChromeOptions()
            options.add_argument(f"--proxy-server={proxy_url}")
            options.add_argument(f'user-agent={random.choice(USER_AGENTS)}')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--no-first-run')
            options.add_argument('--no-default-browser-check')
            options.add_argument('--disable-extensions')
            
            self.driver = uc.Chrome(options=options, version_main=None)
            self.wait = WebDriverWait(self.driver, 15)
            
            print("Browser initialized successfully")
            return True
        
        except Exception as e:
            print(f"Error initializing browser: {e}")
            return False
    
    def fill_form(self, form_data: Dict, offer_url: str) -> bool:
        """Fill and submit form with data"""
        try:
            email = form_data.get('email', 'unknown')
            
            print(f"Opening: {offer_url}")
            self.driver.get(offer_url)
            self._random_delay()
            self._random_scroll()
            
            self.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "input")))
            self._random_delay()
            
            field_selectors = {
                'header': ['[name="header"]', '[id="header"]'],
                'email': ['[name="email"]', '[id="email"]', '[type="email"]'],
                'fst': ['[name="first_name"]', '[name="firstName"]', '[id="first_name"]'],
                'last': ['[name="last_name"]', '[name="lastName"]', '[id="last_name"]'],
                'address': ['[name="address"]', '[id="address"]'],
                'zip': ['[name="zip"]', '[name="zip_code"]', '[id="zip"]'],
                'cellphone': ['[name="phone"]', '[name="cellphone"]', '[id="phone"]'],
                'city': ['[name="city"]', '[id="city"]'],
                'state': ['[name="state"]', '[id="state"]'],
                'month': ['[name="month"]', '[id="month"]'],
                'day': ['[name="day"]', '[id="day"]'],
                'year': ['[name="year"]', '[id="year"]'],
                'gender': ['[name="gender"]', '[id="gender"]']
            }
            
            for field_key, value in form_data.items():
                if not value:
                    continue
                
                if field_key in field_selectors:
                    filled = False
                    for selector in field_selectors[field_key]:
                        try:
                            element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                            
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                            self._random_delay()
                            
                            if element.tag_name == 'select':
                                Select(element).select_by_value(str(value))
                            else:
                                element.clear()
                                for char in str(value):
                                    element.send_keys(char)
                                    time.sleep(random.uniform(0.05, 0.15))
                            
                            self._random_delay()
                            filled = True
                            print(f"Filled {field_key}: {value}")
                            break
                        except:
                            continue
                    
                    if not filled:
                        print(f"Could not fill {field_key}")
            
            self._random_mouse_movement()
            self._random_scroll()
            self._random_delay()
            
            submit_selectors = ['[type="submit"]', 'button[type="submit"]', '[onclick*="submit"]']
            for selector in submit_selectors:
                try:
                    submit_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
                    self._random_delay()
                    submit_btn.click()
                    print("Form submitted")
                    
                    # Wait for page to load after submission
                    time.sleep(3)
                    
                    # Take screenshot of completion page
                    screenshot_path = self.screenshot_handler.take_page_screenshot(
                        self.driver, 
                        email, 
                        "completion"
                    )
                    
                    if screenshot_path:
                        print(f"✓ Completion screenshot saved: {screenshot_path}")
                    
                    return True
                except:
                    continue
            
            return False
        
        except Exception as e:
            print(f"Error filling form: {e}")
            return False
    
    def take_screenshot(self, profile_email: str) -> str:
        """Take screenshot of current page"""
        return self.screenshot_handler.take_screenshot(self.driver, profile_email)
    
    def close_browser(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()
            print("Browser closed")
