from django.urls import path

from .views import *


urlpatterns = [
    path('<str:page_path>', CardView.as_view()),
]
