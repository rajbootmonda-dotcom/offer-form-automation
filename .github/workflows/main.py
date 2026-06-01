import sys
from sheets_reader import SheetsReader
from browser_automation import BrowserAutomation
from proxy_manager import ProxyManager
from config import OFFER_URL
import random

def process_profiles(batch_size: int = 10):
    """Main function to process profiles from sheet"""
    
    print("="*50)
    print("OFFER FORM AUTOMATION - Starting...")
    print("="*50)
    
    sheets_reader = SheetsReader()
    proxy_manager = ProxyManager()
    browser_auto = BrowserAutomation(proxy_manager)
    
    try:
        print("\nReading data from Google Sheets...")
        profiles = sheets_reader.read_sheet()
        
        if not profiles:
            print("No profiles found in sheet")
            return
        
        print(f"Found {len(profiles)} profiles")
        
        successful = 0
        failed = 0
        
        for idx, profile in enumerate(profiles[:batch_size], 1):
            print(f"\n{'='*50}")
            print(f"Processing Profile {idx}/{len(profiles)}")
            print(f"{'='*50}")
            
            try:
                if not browser_auto.initialize_browser():
                    print("Failed to initialize browser")
                    failed += 1
                    continue
                
                if browser_auto.fill_form(profile, OFFER_URL):
                    print(f"✓ Profile {idx} processed successfully")
                    successful += 1
                else:
                    print(f"✗ Profile {idx} failed")
                    failed += 1
                
                browser_auto.close_browser()
                
                if idx < batch_size:
                    delay = random.randint(30, 120)
                    print(f"Waiting {delay} seconds before next profile...")
                    import time
                    time.sleep(delay)
            
            except Exception as e:
                print(f"Error processing profile {idx}: {e}")
                failed += 1
                try:
                    browser_auto.close_browser()
                except:
                    pass
        
        print(f"\n{'='*50}")
        print("PROCESSING COMPLETE")
        print(f"{'='*50}")
        print(f"Total Processed: {successful + failed}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {(successful/(successful+failed)*100):.1f}%" if (successful+failed) > 0 else "No profiles processed")
    
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        try:
            browser_auto.close_browser()
        except:
            pass

if __name__ == "__main__":
    batch_size = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    process_profiles(batch_size)
