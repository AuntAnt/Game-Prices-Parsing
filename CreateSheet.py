import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date


CREDENTIALS_FILE = 'game-wish-list-174a4b364e4b.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
)

httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)


def creating_spreadsheet():
    spreadsheet = service.spreadsheets().create(body={
        'properties': {'title': 'Game List', 'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Games',
                                   'gridProperties': {'rowCount': 100, 'columnCount': 15}}}]
    }).execute()
    spreadsheet_id = spreadsheet['spreadsheetId']
    # print('https://docs.google.com/spreadsheets/d/' + spreadsheetId)

    return spreadsheet_id


def permission_to_spreadsheet(spreadsheet_id):
    drive_service = apiclient.discovery.build('drive', 'v3', http=httpAuth)
    access = drive_service.permissions().create(
        fileId=spreadsheet_id,
        body={'type': 'user', 'role': 'writer', 'emailAddress': 'furthertwoant@gmail.com'},
        fields='id'
    ).execute()

    return access


def write_into_sheet(game, price, update_date):
    spreadsheet_id = "18hrtQcTbQMFTfYkntgMYjkP_lFB6k5MQjjOxyI9y_R0"
    results = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {
                    "range": "Games!A2:C2",
                    "majorDimension": "ROWS",
                    "values": [
                        # ["Game", "Price", "Update Date"]
                        [game, price, update_date]
                    ]
                }
            ]
    }).execute()

    return results


game = "Chronos before the ashen"
price = 1500
update_date = date.today().strftime("%d-%m-%Y")
spreadsheet_id = "18hrtQcTbQMFTfYkntgMYjkP_lFB6k5MQjjOxyI9y_R0"

permission_to_spreadsheet(spreadsheet_id)
write_into_sheet(game, price, update_date)
