from django.urls import path

from .views import *


urlpatterns = [
    path('cards/<int:pk>', RetrieveUpdateCardView.as_view()),
    path('fields', CreateFieldView.as_view()),
    path('fields/<int:pk>', UpdateFieldView.as_view()),
]
