import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials


CREDENTIALS_FILE = 'game-whish-list-174a4b364e4b.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

spreadsheet = service.spreadsheets().create(body={
    'properties': {'title': 'Game List', 'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': 'Games',
                               'gridProperties': {'rowCount': 100, 'columnCount': 15}}}]
}).execute()
spreadsheetId = spreadsheet['spreadsheetId']
# print('https://docs.google.com/spreadsheets/d/' + spreadsheetId)

driveService = apiclient.discovery.build('drive', 'v3', http=httpAuth)
access = driveService.permissions().create(
    fileId=spreadsheetId,
    body={'type': 'user', 'role': 'writer', 'emailAddress': 'furthertwoant@gmail.com'},
    fields='id'
).execute()

print('https://docs.google.com/spreadsheets/d/' + spreadsheetId)
