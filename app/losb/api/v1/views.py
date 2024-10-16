from __future__ import annotations

from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from losb.api.v1.serializers import (
    UserSerializer,
    UserNameSerializer,
    UserCitySerializer,
    UserBdaySerializer,
    UserPhoneSerializer, CitySerializer,
)
from losb.models import City



@extend_schema_view(
    get=extend_schema(
        responses={
            200: CitySerializer,
        },
        summary='Список городов России',
        description='Возвращает список городов России',
    ),
)
class CityListView(generics.ListAPIView):
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated,]
    pagination_class = None
    queryset = City.objects.all()

@extend_schema_view(
    get=extend_schema(
        responses={
            200: UserSerializer,
        },
        summary='Профиль пользователя',
        description='Возвращает профиль пользователя',
    ),
)
class UserRetrieveView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]

    def get_object(self):
        return self.request.user

@extend_schema_view(
    update=extend_schema(
        responses={
            200: UserNameSerializer,
        },
        summary='Изменение имени пользователя',
    ),
)
class UserNameUpdateView(generics.UpdateAPIView):
    serializer_class = UserNameSerializer
    permission_classes = [IsAuthenticated,]

    def get_object(self):
        return self.request.user

@extend_schema_view(
    update=extend_schema(
        responses={
            200: UserCitySerializer,
        },
        summary='Изменение города пользователя',
    ),
)
class UserCityUpdateView(generics.UpdateAPIView):
    serializer_class = UserCitySerializer
    permission_classes = [IsAuthenticated,]

    def get_object(self):
        return self.request.user

@extend_schema_view(
    update=extend_schema(
        responses={
            200: UserBdaySerializer,
        },
        summary='Изменение даты рождения пользователя',
    ),
)
class UserBdayUpdateView(generics.UpdateAPIView):
    serializer_class = UserBdaySerializer
    permission_classes = [IsAuthenticated,]
    # TODO: allow only posting
    def get_object(self):
        return self.request.user

@extend_schema_view(
    update=extend_schema(
        responses={
            200: UserPhoneSerializer,
        },
        summary='Изменение телефона пользователя',
    ),
)
class UserPhoneUpdateView(generics.UpdateAPIView):
    serializer_class = UserBdaySerializer
    permission_classes = [IsAuthenticated,]
    # TODO: change logic
    def get_object(self):
        return self.request.user

