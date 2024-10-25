from __future__ import annotations

from django.urls import path, include

from losb.api.v1.views import (
    UserRetrieveView,
    UserNameUpdateView,
    UserCityUpdateView,
    UserBirthdayAPIView,
    UserPhoneUpdateView,
    CityListView, TechSupportAPIView,
)

app_name = 'losb'


urlpatterns = [
    # path('', include(router.urls)),
    path('cities/', CityListView.as_view(), name='cities'),
    path('tech-support', TechSupportAPIView.as_view(), name='tech-support'),
    path('user', UserRetrieveView.as_view(), name='user-detail'),
    path('user/name', UserNameUpdateView.as_view(), name='user-name'),
    path('user/city', UserCityUpdateView.as_view(), name='user-city'),
    path('user/birthday', UserBirthdayAPIView.as_view(), name='user-birthday'),
    path('user/phone', UserPhoneUpdateView.as_view(), name='user-phone'),
]
