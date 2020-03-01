import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import random

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1lsbQSm_gsb_CQNOnSuoZ4mZclxorLjsMj3V5CvstO_A'
SAMPLE_RANGE_NAME = 'Sheet1!A1:F10'

creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('sheets', 'v4', credentials=creds)

sheet = service.spreadsheets()

def clear_vals():
  # Clear values first
  request = sheet.values().clear(spreadsheetId = SAMPLE_SPREADSHEET_ID, range = SAMPLE_RANGE_NAME).execute()

def write_random_vals():
  # 10 rows
  # 6 columns
  random_vals = [[random.randint(1,101) for i in range(6)] for j in range(0,10)]

  new_values = {
    'values': random_vals
  }
  update = sheet.values().update(spreadsheetId = SAMPLE_SPREADSHEET_ID,
                                range = SAMPLE_RANGE_NAME,
                                valueInputOption='USER_ENTERED',
                                body = new_values
  ).execute()

  update = sheet.values().update(spreadsheetId = SAMPLE_SPREADSHEET_ID,
                                range = 'Sheet1!A1:F1',
                                valueInputOption = 'USER_ENTERED',
                                body = {'values': [[f'Field {i}' for i in range(6)]]}
  ).execute()

clear_vals()
write_random_vals()