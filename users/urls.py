from django.urls import path

from .views import *


urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('signup/', signup, name='signup'),
]