from django.contrib import admin
from .models import *


class TelegramUsersAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'telegram_username')


admin.site.register(Profile, TelegramUsersAdmin)