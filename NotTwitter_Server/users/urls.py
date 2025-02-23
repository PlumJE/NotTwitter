from django.urls import path
from .views import *

urlpatterns = [
    path('loginout/', Loginout.as_view()),
    path('userinfo/', UserInfoView.as_view()),
    path('userdetail/', UserDetailView.as_view()),
    path('profileimg/', ProfileImgView.as_view())
]