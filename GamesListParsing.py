from bs4 import BeautifulSoup
import requests as req
import string
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


def extract_block(url):
    link = req.get(url).text
    soup = BeautifulSoup(link, 'lxml')
    block = soup.find('main', id="main")
    return block


def extract_price(block):
    ext_price = block.find_all('span')[5].text
    price = ""
    for i in ext_price:
        if i in string.digits:
            price = price + i
            price = price[:4]

    return price


def extract_name(block):
    name = block.find_all('h1')[1].text
    return name


def permission_to_spreadsheet(spreadsheet_id):
    drive_service = apiclient.discovery.build('drive', 'v3', http=httpAuth)
    access = drive_service.permissions().create(
        fileId=spreadsheet_id,
        body={'type': 'user', 'role': 'writer', 'emailAddress': 'furthertwoant@gmail.com'},
        fields='id'
    ).execute()

    return access


def write_into_sheet(game, price, update_date, spreadsheet_id, cell_range):
    results = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {
                    "range": cell_range,
                    "majorDimension": "ROWS",
                    "values": [
                        [game, price, update_date]
                    ]
                }
            ]
        }).execute()

    return results


def clear_sheet(spreadsheet_id, cell_range):
    results = service.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id,
        range=cell_range
    ).execute()

    return results


def read_from_sheet(spreadsheet_id):
    cell_range = ["Games!D2:D100"]
    results = service.spreadsheets().values().batchGet(
        spreadsheetId=spreadsheet_id,
        ranges=cell_range,
        valueRenderOption='FORMATTED_VALUE',
        dateTimeRenderOption='FORMATTED_STRING'
    ).execute()

    sheet_values = results['valueRanges'][0]['values']
    return sheet_values


spreadsheet_id = "18hrtQcTbQMFTfYkntgMYjkP_lFB6k5MQjjOxyI9y_R0"
update_date = date.today().strftime("%d-%m-%Y")

# permission_to_spreadsheet(spreadsheet_id)

range_a = 2
range_c = 2


# Изменить cell_range - нужно удалять кол-во записей, которые уже есть в таблице, а не которые добавляются
# Сделать вместе с добавлением четния url из таблицы
def cleaning_sheet(range_a, range_c, urls):
    for item in range(len(urls) - (len(urls) - 1)):
        cell_range = "Games!A" + str(range_a) + ":C" + str(range_c)
        range_a += 1
        range_c += 1
        clear_sheet(spreadsheet_id, cell_range)


def adding_games(range_a, range_c, games):
    for game in games:
        ext_price = extract_price(extract_block(game))
        ext_name = extract_name(extract_block(game))
        for item in range(len(games) - (len(games) - 1)):
            cell_range = "Games!A" + str(range_a) + ":C" + str(range_c)
            range_a += 1
            range_c += 1
            write_into_sheet(ext_name, ext_price, update_date, spreadsheet_id, cell_range)


urls = read_from_sheet(spreadsheet_id)

games = []

for url in urls:
    for i in url:
        game = i
        games.append(game)


cleaning_sheet(range_a, range_c, games)
adding_games(range_a, range_c, games)
