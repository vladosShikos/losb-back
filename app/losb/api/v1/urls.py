from __future__ import annotations

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from losb.api.v1.views import UserRetrieveVew


app_name = 'losb'

router = DefaultRouter()
# router.register(r'user', UserViewSet, basename='user')


urlpatterns = [
    path('', include(router.urls)),
    path('user', UserRetrieveVew.as_view(), name='user-detail'),
]