from django.urls import path
from .views import *


urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('toplist/videos', toplist_videos, name='toplist_videos'),
    path('toplist/channels', toplist_channels, name='toplist_channels'),
    path('channel/<str:id>', channel, name='channel'),
    path('video/<str:id>', video, name='video'),

]
