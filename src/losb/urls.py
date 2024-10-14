# from __future__ import annotations
#
# from django.contrib import admin
# from django.urls import include, path
# from drf_spectacular.views import (
#     SpectacularAPIView,
#     SpectacularRedocView,
#     SpectacularSwaggerView,
# )
# from rest_framework.versioning import URLPathVersioning
#
# app_urls = [
#     path('', include('userprofile.api.urls')),
# ]
# api_urls = [
#     path('api/', include(app_urls)),
# ]
#
# swagger_urls = [
#     # YOUR PATTERNS
#     path('schema/v1/', SpectacularAPIView.as_view(
#         versioning_class=URLPathVersioning,
#         api_version='v1',
#         patterns=api_urls,
#     ), name='schema'),
#     # Optional UI:
#     path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
#     path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
# ]
#
# urlpatterns = [
#     # path('', include(swagger_urls)),
#     # path('', include(api_urls)),
#     path('admin/', admin.site.urls),
# ]
