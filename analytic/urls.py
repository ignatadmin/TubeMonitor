from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('toplist/videos', TopListVideos.as_view(), name='toplist_videos'),
    path('toplist/channels/', TopListChannels.as_view(), name='toplist_channels'),
    path('channel', channel_data, name='channel'),
    path('video', video_data, name='video'),
]
