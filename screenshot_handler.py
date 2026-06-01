import os
from datetime import datetime
from pathlib import Path

class ScreenshotHandler:
    def __init__(self, output_dir: str = "screenshots"):
        self.output_dir = output_dir
        self.success_dir = os.path.join(output_dir, "success")
        self.failure_dir = os.path.join(output_dir, "failure")
        
        # Create directories if they don't exist
        os.makedirs(self.success_dir, exist_ok=True)
        os.makedirs(self.failure_dir, exist_ok=True)
    
    def capture_success(self, driver, profile_id: str, email: str) -> str:
        """Capture screenshot when form is successfully submitted"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"success_{profile_id}_{email}_{timestamp}.png"
            filepath = os.path.join(self.success_dir, filename)
            
            driver.save_screenshot(filepath)
            print(f"✓ Success screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            print(f"Error capturing success screenshot: {e}")
            return None
    
    def capture_failure(self, driver, profile_id: str, email: str, error_msg: str = "") -> str:
        """Capture screenshot when form submission fails"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"failure_{profile_id}_{email}_{timestamp}.png"
            filepath = os.path.join(self.failure_dir, filename)
            
            driver.save_screenshot(filepath)
            print(f"✗ Failure screenshot saved: {filepath}")
            
            # Also save error log
            log_filename = filename.replace('.png', '.txt')
            log_filepath = os.path.join(self.failure_dir, log_filename)
            with open(log_filepath, 'w') as f:
                f.write(f"Profile ID: {profile_id}\n")
                f.write(f"Email: {email}\n")
                f.write(f"Timestamp: {timestamp}\n")
                f.write(f"Error: {error_msg}\n")
            
            return filepath
        except Exception as e:
            print(f"Error capturing failure screenshot: {e}")
            return None
    
    def capture_confirmation(self, driver, profile_id: str) -> str:
        """Capture confirmation/success page screenshot"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"confirmation_{profile_id}_{timestamp}.png"
            filepath = os.path.join(self.success_dir, filename)
            
            # Wait a moment for page to fully load
            import time
            time.sleep(2)
            
            driver.save_screenshot(filepath)
            print(f"✓ Confirmation screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            print(f"Error capturing confirmation screenshot: {e}")
            return None
    
    def get_page_source(self, driver, profile_id: str, filename_prefix: str = "page") -> str:
        """Save HTML page source for debugging"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            html_filename = f"{filename_prefix}_{profile_id}_{timestamp}.html"
            filepath = os.path.join(self.success_dir, html_filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            
            print(f"✓ Page source saved: {filepath}")
            return filepath
        except Exception as e:
            print(f"Error saving page source: {e}")
            return None
    
    def list_screenshots(self, status: str = "success") -> list:
        """List all screenshots of a given status"""
        if status == "success":
            directory = self.success_dir
        elif status == "failure":
            directory = self.failure_dir
        else:
            return []
        
        if not os.path.exists(directory):
            return []
        
        return os.listdir(directory)
    
    def cleanup_old_screenshots(self, days: int = 30):
        """Delete screenshots older than specified days"""
        import time
        current_time = time.time()
        cutoff_time = current_time - (days * 86400)
        
        for directory in [self.success_dir, self.failure_dir]:
            if not os.path.exists(directory):
                continue
            
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                if os.path.isfile(filepath):
                    file_time = os.path.getmtime(filepath)
                    if file_time < cutoff_time:
                        os.remove(filepath)
                        print(f"Deleted old file: {filepath}")
