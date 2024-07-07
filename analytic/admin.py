from django.contrib import admin
from .models import *


class ListTopVideosAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'view_count', 'made_for_kids')


class ListTopChannelsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'channel_id', 'country', 'made_for_kids')


admin.site.register(ListTopVideos, ListTopVideosAdmin)
admin.site.register(ListTopChannels, ListTopChannelsAdmin)
