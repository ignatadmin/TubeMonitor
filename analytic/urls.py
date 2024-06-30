from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('toplist/videos', cache_page(3600)(csrf_exempt(TopListVideos.as_view())), name='toplist_videos'),
    path('toplist/channels/', cache_page(3600)(csrf_exempt(TopListChannels.as_view())), name='toplist_channels'),
    path('channel', csrf_exempt(channel), name='channel'),
    path('video', csrf_exempt(video), name='video'),
]
