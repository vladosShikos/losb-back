from __future__ import annotations

from django.urls import include, path

urlpatterns = [
    path('v1/losb/', include('losb.api.v1.urls')),
]
