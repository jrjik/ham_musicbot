from django.contrib import admin
from users.models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id',)
    search_fields = ('telegram_id',)
