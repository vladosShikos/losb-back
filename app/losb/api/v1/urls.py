from __future__ import annotations

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from losb.api.v1.views import (
    UserRetrieveView,
    UserNameUpdateView,
    UserCityUpdateView,
    UserBdayAPIView,
    UserPhoneUpdateView,
    CityListView,
)

app_name = 'losb'

router = DefaultRouter()
# router.register(r'user', UserViewSet, basename='user')


urlpatterns = [
    path('', include(router.urls)),
    path('cities/', CityListView.as_view(), name='cities'),
    path('user', UserRetrieveView.as_view(), name='user-detail'),
    path('user/name', UserNameUpdateView.as_view(), name='user-name'),
    path('user/city', UserCityUpdateView.as_view(), name='user-city'),
    path('user/bday', UserBdayAPIView.as_view(), name='user-bday'),
    path('user/phone', UserPhoneUpdateView.as_view(), name='user-phone'),
]
