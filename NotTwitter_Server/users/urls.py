from django.urls import path
from .views import *

urlpatterns = [
    path('loginout/', Loginout.as_view()),
    path('signupdown/', Signupdown.as_view()),
    path('nickname/', NicknameView.as_view())
]