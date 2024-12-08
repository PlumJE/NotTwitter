from django.urls import path
from .views import *

urlpatterns = [
    path('postlist/', PostlistView.as_view()),
    path('post/', PostView.as_view())
]