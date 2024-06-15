from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('toplist', views.toplist, name='toplist'),
    path('channel/<str:id>', views.channel, name='channel'),

]
