from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import *


urlpatterns = [
    path('token', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
    path('page-path', PagePathView.as_view()),
    path("me", ChangeUsernameView.as_view()),
    path("is-username-unique", IsUsernameUniqueView.as_view())
]
