# Управление таблицами
import httplib2
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials
from config import SHEETS_TITLE, TEMPLATE_ID
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


# Разрешение на просмотр таблицы
def give_permission_read(newFileId: str) -> str:
    # Создание запроса с настройками прав доступа
    shareRes = (
        driveService.permissions()
        .create(
            fileId=newFileId,
            body={
                "type": "anyone",
                "role": "reader",
            },
            fields="id",
        )
        .execute()
    )
    return shareRes["id"]


# Создание таблицы при регистрации пользователя
def create_new_table(user_id: int) -> Any:
    try:
        newFile = (
            driveService.files()
            .copy(fileId=TEMPLATE_ID, body={"name": SHEETS_TITLE})
            .execute()
        )
        permission_res = give_permission_read(newFile["id"])
        # Возврат номера таблицы FIXME: убрать временный вывод
        return (
            f'https://docs.google.com/spreadsheets/d/{newFile["id"]}/edit'
            + "\n"
            + permission_res
        )

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


# Добавление пользователя в редакторы TODO: СДЕЛАТЬ ПРОВЕРКУ ID ТАБЛИЦЫ ИЗ БАЗЫ И ПОЛУЧЕНИЕ ID ДЛЯ ИСПОЛЬЗОВАНИЯ
def add_writer_permission(spreadsheetId: str, user_email: str) -> Any:
    try:
        shareRes = (
            driveService.permissions()
            .create(
                fileId=spreadsheetId,
                body={
                    "type": "user",
                    "role": "writer",
                    "emailAddress": user_email,
                },  # доступ на чтение кому угодно
                fields="id",
            )
            .execute()
        )
        return shareRes["id"]

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error
