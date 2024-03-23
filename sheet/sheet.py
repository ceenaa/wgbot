from __future__ import print_function

import os

from google.oauth2 import service_account
from googleapiclient.discovery import build
from service.peer import get_short_all_peers

sheet_id = os.environ.get("SHEET_ID")


def main():
    SERVICE_ACCOUNT_FILE = 'keys.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # The ID spreadsheet.
    SAMPLE_SPREADSHEET_ID = sheet_id

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()

    peers = get_short_all_peers()

    body = {
        'values': peers
    }

    sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="peers" + "!A2", body=body,
                          valueInputOption="USER_ENTERED").execute()
