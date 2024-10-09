import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_formatting import Border, CellFormat, format_cell_range, Borders, Color

from orders.models import Order

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

service_account_file_path = os.path.join(os.path.dirname(__file__), '../google_sheet/service-account.json')
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    service_account_file_path, scope
)


def get_google_sheets_client():
    return gspread.authorize(credentials)


def get_user_orders(user):
    orders = Order.objects.filter(initiator_id=user).order_by('id')
    return [
        [
            order.id,
            order.get_status_display(),
            order.created_at.strftime("%Y-%m-%d %H:%M"),
            order.basket_history.get('total_sum', 0),

        ]
        for order in orders
    ]


def write_orders_to_sheet(sheet_id, user, range):
    client = get_google_sheets_client()
    spreadsheet = client.open_by_key(sheet_id)
    sheet = spreadsheet.worksheet("Аркуш1")

    # Отримати замовлення користувача
    orders_data = get_user_orders(user)
    user_name = user.get_full_name() or user.username  # Get user name

    # Створити заголовки
    header = [f"Всі замовлення користувача: {user_name}"]
    columns = ["№ Замовлення", "Статус", "Створенний", "ВСЬОГО"]

    # Записати заголовки
    sheet.merge_cells("A1:E1")
    sheet.update("A1:E1", [header])  # Заголовки
    # форматування з gspread
    sheet.format("A1:E1", {
        "backgroundColor": {
            "red": 0.0,
            "green": 0.0,
            "blue": 0.0
        },
        "horizontalAlignment": "CENTER",
        "textFormat": {
            "foregroundColor": {
                "red": 1.0,
                "green": 1.0,
                "blue": 1.0
            },
            "fontSize": 12,
            "bold": True
        }
    })
    sheet.update("A2:E2", [columns])

    # форматування з gspread_formatting
    format_cell_range(sheet, "A2:E2", CellFormat(
        borders=Borders(
            top=Border("SOLID", Color(0, 0, 0)),
            bottom=Border("SOLID", Color(0, 0, 0)),
            left=Border("SOLID", Color(0, 0, 0)),
            right=Border("SOLID", Color(0, 0, 0))
        )
    ))

    if orders_data:
        sheet.update(f"A3:D{len(orders_data) + 2}", orders_data)

        # Форматування для всіх заповнених клітинок з границями
        format_cell_range(sheet, f"A3:D{len(orders_data) + 2}", CellFormat(
            borders=Borders(
                top=Border("SOLID", Color(0, 0, 0)),
                bottom=Border("SOLID", Color(0, 0, 0)),
                left=Border("SOLID", Color(0, 0, 0)),
                right=Border("SOLID", Color(0, 0, 0))
            )
        ))
    else:
        print("У користувача немає замовлень.")
