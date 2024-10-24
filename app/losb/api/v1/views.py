from __future__ import annotations

from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from losb.schema import TelegramIdJWTSchema

from app import settings
from losb.api.v1.exceptions import BdayAlreadySet
from losb.api.v1.serializers import (
    UserSerializer,
    UserNameSerializer,
    UserCitySerializer,
    UserBdaySerializer,
    UserPhoneSerializer,
    CitySerializer, BotUrlSerializer, UserPhoneVerificationSerializer,
)
from losb.models import City, User


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
    http_method_names = ["put"]

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
    http_method_names = ["put"]


    def get_object(self):
        return self.request.user

class UserBdayAPIView(APIView):
    http_method_names = ['post']
    permission_classes = [IsAuthenticated, ]

    @extend_schema(
        request=UserBdaySerializer,
        responses={
            200: UserBdaySerializer,
        },
        summary='Установить дату рождения пользователя',
        description='Устанавливает дату рождения пользователя, если она ещё не была изменена',
    )
    def post(self, request):
        if self.request.user.bday:
            raise BdayAlreadySet

        serializer = UserBdaySerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(self.request.user, serializer.validated_data)
        return Response(serializer.data)

class UserPhoneUpdateView(APIView):
    permission_classes = [IsAuthenticated,]
    http_method_names = ["post","put"]

    @extend_schema(
        request=UserPhoneSerializer,
        responses={
            200: {},
        },
        summary='Запросить код подтверждения',
        description='Отправляет otp код на указанный номер телефона',
    )
    def post(self):
        return self.request.user

    @extend_schema(
        request=UserPhoneVerificationSerializer,
        responses={
            200: UserPhoneSerializer,
            403: {'detail':'Too many attempts'},
            409: {'detail':'Invalid'},
        },
        summary='Верифицировать код подтверждения',
        description='Верифицирует код подтверждения, в случаи успеха обновляет номер телефона пользователя',
    )
    def put(self):
        return self.request.user

@extend_schema_view(
    get=extend_schema(
        responses={
            200: BotUrlSerializer,
        },
        summary='Cсылка на бота поддержки',
    ),
)
class TechSupportAPIView(generics.RetrieveAPIView):
    serializer_class = BotUrlSerializer
    permission_classes = [IsAuthenticated,]

    def get_object(self):
        return {'url':settings.TECHSUPPORT_BOT_URL}