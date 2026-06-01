import gspread
from google.oauth2.service_account import Credentials
from config import GOOGLE_SHEET_ID, GOOGLE_CREDENTIALS_FILE
import os
from typing import List, Dict

class SheetsReader:
    def __init__(self):
        self.sheet_id = GOOGLE_SHEET_ID
        self.credentials_file = GOOGLE_CREDENTIALS_FILE
        self.client = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Google Sheets API"""
        try:
            if not os.path.exists(self.credentials_file):
                print(f"Warning: {self.credentials_file} not found")
                return
            
            scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
            creds = Credentials.from_service_account_file(
                self.credentials_file,
                scopes=scopes
            )
            self.client = gspread.authorize(creds)
            print("✓ Authenticated with Google Sheets")
        except Exception as e:
            print(f"✗ Authentication failed: {e}")
    
    def read_sheet(self) -> List[Dict]:
        """Read data from Google Sheet"""
        try:
            if not self.client:
                print("Not authenticated")
                return []
            
            sheet = self.client.open_by_key(self.sheet_id).sheet1
            records = sheet.get_all_records()
            
            print(f"✓ Read {len(records)} records from sheet")
            return records
        except Exception as e:
            print(f"✗ Error reading sheet: {e}")
            return []
    
    def get_pending_profiles(self) -> List[Dict]:
        """Get profiles that haven't been processed yet"""
        try:
            records = self.read_sheet()
            pending = [r for r in records if r.get('status', '').lower() != 'completed']
            return pending
        except Exception as e:
            print(f"Error getting pending profiles: {e}")
            return []
