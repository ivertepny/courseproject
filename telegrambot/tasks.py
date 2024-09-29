import requests

from orders.models import Order
from telegrambot.models import TeleSettings
from celery import shared_task


@shared_task
def send_telegram():
    settings = TeleSettings.objects.get(pk=1)
    token = str(settings.tg_token)
    chat_id = str(settings.tg_chat_id)
    order_first_name = Order.objects.values_list('first_name', flat=True).last()
    order_last_name = Order.objects.values_list('last_name', flat=True).last()
    text_message = TeleSettings.objects.values_list('message', flat=True).first()
    text = f"{text_message} {order_first_name} {order_last_name}"

    api = 'https://api.telegram.org/bot'
    method = api + token + '/sendMessage'
    req = requests.post(method, data={
        'chat_id': chat_id,
        'text': text
    })