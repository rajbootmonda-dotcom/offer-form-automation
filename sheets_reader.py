from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from typing import List, Dict
from config import GOOGLE_SHEET_ID, GOOGLE_SHEET_RANGE
import os
import pickle

class SheetsReader:
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    
    def __init__(self):
        self.sheet_id = GOOGLE_SHEET_ID
        self.sheet_range = GOOGLE_SHEET_RANGE
        self.service = self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Sheets API"""
        creds = None
        
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        return build('sheets', 'v4', credentials=creds)
    
    def read_sheet(self) -> List[Dict]:
        """Read data from Google Sheet"""
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range=self.sheet_range
            ).execute()
            
            rows = result.get('values', [])
            
            if not rows:
                print('No data found in sheet.')
                return []
            
            headers = rows[0]
            data = []
            
            for row in rows[1:]:
                row = row + [''] * (len(headers) - len(row))
                record = dict(zip(headers, row))
                data.append(record)
            
            return data
        
        except Exception as e:
            print(f"Error reading sheet: {e}")
            return []
    
    def get_next_batch(self, batch_size: int = 10) -> List[Dict]:
        """Get next batch of records to process"""
        return self.read_sheet()[:batch_size]
