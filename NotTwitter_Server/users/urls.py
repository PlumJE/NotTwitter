from django.urls import path
from .views import *

urlpatterns = [
    path('loginout/', Loginout.as_view()),
    path('userinfo/', UserInfoView.as_view())
]