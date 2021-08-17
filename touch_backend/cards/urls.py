from django.urls import path

from .views import *


urlpatterns = [
    path('cards/<str:page_path>', RetrieveUpdateCardView.as_view()),
    path("cards/<str:page_path>/qr", RetrieveQRView.as_view()),
    path('fields', CreateFieldView.as_view()),
    path('fields/<int:pk>', UpdateDestroyFieldView.as_view()),
]
