from django.db import models
# from orders import models


class TeleSettings(models.Model):
    tg_token = models.CharField(max_length=255, verbose_name="Telegram Token")
    tg_chat_id = models.CharField(max_length=255, verbose_name="Telegram Chat ID")
    message = models.TextField()

    def __str__(self):
        return self.tg_chat_id


