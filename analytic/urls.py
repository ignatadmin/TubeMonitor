from django.urls import path, include

from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('toplist', toplist, name='toplist'),
    path('channel/<str:id>', channel, name='channel'),
    path('video/<str:id>', video, name='video'),

]
