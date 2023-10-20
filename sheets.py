# Управление таблицами
import httplib2
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials
from config import SHEETS_TITLE
from typing import Any

# ------------------------------------AUTORISATION---------------------------------------
CREDENTIALS_FILE = "google_sheets_api.json"
sheetsCreds = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE, "https://www.googleapis.com/auth/spreadsheets"
)
driveCreds = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE, "https://www.googleapis.com/auth/drive"
)

sheetshttpAuth = sheetsCreds.authorize(httplib2.Http())
# Создание Service-объекта, для работы с таблицами
sheetsService = build("sheets", "v4", http=sheetshttpAuth)

driveHttpAuth = driveCreds.authorize(httplib2.Http())
# Создание Service-объекта, для работы с диском
driveService = build("drive", "v3", http=driveHttpAuth)
# ---------------------------------------------------------------------------------------


# Создание таблицы при регистрации пользователя
def create_new_table(user_id: int) -> Any:
    try:
        # ------------------------------------CREATING TABLE-------------------------------------
        # Настройки первой таблицы TODO: НУЖНО СДЕЛАТЬ НАСТРОЙКИ ПЕРВОЙ ТАБЛИЦЫ ИЛИ ШАБЛОН
        spreadsheet_prop = {
            "properties": {"title": SHEETS_TITLE + str(user_id), "locale": "ru_RU"},
            "sheets": [
                {
                    "properties": {
                        "sheetType": "GRID",
                        "sheetId": 0,
                        "title": "Budget",
                        "gridProperties": {"rowCount": 8, "columnCount": 5},
                    }
                }
            ],
        }

        # Делаем запрос на создание файла с таблицей, запоминаем ответ
        spreadsheet = (
            sheetsService.spreadsheets()
            .create(body=spreadsheet_prop, fields="spreadsheetId")
            .execute()
        )
        # ---------------------------------------------------------------------------------------

        # ------------------------------------GIVING PERMISSION----------------------------------

        # Создание прав доступа
        shareRes = (
            driveService.permissions()
            .create(
                fileId=spreadsheet["spreadsheetId"],
                body={
                    "type": "anyone",
                    "role": "reader",
                },  # доступ на чтение кому угодно
                fields="id",
            )
            .execute()
        )
        # ---------------------------------------------------------------------------------------

        return (
            f'https://docs.google.com/spreadsheets/d/{spreadsheet["spreadsheetId"]}/edit'
            + "\n"
            + shareRes["id"]
        )  # Возврат номера таблицы FIXME: убрать временный вывод

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


# # Добавление пользователя в редакторы TODO: СДЕЛАТЬ ПРОВЕРКУ ID ТАБЛИЦЫ ИЗ БАЗЫ И ПОЛУЧЕНИЕ ID ДЛЯ ИСПОЛЬЗОВАНИЯ
# def add_writer_permission(spreadsheetId: str, user_email: str) -> str:
#     try:
#         shareRes = (
#             driveService.permissions()
#             .create(
#                 fileId=spreadsheet["spreadsheetId"],
#                 body={
#                     "type": "anyone",
#                     "role": "reader",
#                 },  # доступ на чтение кому угодно
#                 fields="id",
#             )
#             .execute()
#         )

#     except HttpError as error:
#         print(f"An error occurred: {error}")
#         return error


def main() -> None:  # FIXME:
    ans = create_new_table(1231412)
    print(ans)


if __name__ == "__main__":
    main()
