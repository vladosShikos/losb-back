from __future__ import annotations

from random import SystemRandom

from django.utils import timezone
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from losb.schema import TelegramIdJWTSchema  # do not remove, needed for swagger

from app import settings
from losb.api.v1.exceptions import BirthdayAlreadyRegistered, SmsVerificationResendCooldown, PhoneAlreadyVerified, \
    SmsVerificationAttemptsExceeded, SmsVerificationNotSend, SmsVerificationExpired, SmsVerificationFailed
from losb.api.v1.serializers import (
    UserSerializer,
    UserNameSerializer,
    UserCitySerializer,
    UserBdaySerializer,
    UserPhoneSerializer,
    CitySerializer, BotUrlSerializer, UserPhoneVerificationSerializer, PhoneVerificationSerializer, PhoneSerializer,
    UseRPhoneSerializer,
)
from losb.models import City, User


# TODO: Put swagger docs inside classes
# TODO: request object inside post calls not used, using self instead. Why?

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
    permission_classes = [IsAuthenticated, ]
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
    permission_classes = [IsAuthenticated, ]

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
    permission_classes = [IsAuthenticated, ]
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
    permission_classes = [IsAuthenticated, ]
    http_method_names = ["put"]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        city = City.objects.get(id=serializer.data['city'])
        response_serializer = CitySerializer(city)

        return Response(response_serializer.data)


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
            raise BirthdayAlreadyRegistered

        serializer = UserBdaySerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(self.request.user, serializer.validated_data)
        return Response(serializer.data)


class UserPhoneUpdateView(APIView):
    permission_classes = [IsAuthenticated, ]
    http_method_names = ["post", "put"]

    @staticmethod
    def get_otp():
        return "".join(SystemRandom().choice('123456789') for _ in range(settings.SMS_VERIFICATOIN_CODE_DIGITS))

    # TODO: check swagger docs, you're up to some tinkering
    @extend_schema(
        request=UserPhoneSerializer,
        responses={
            200: Response(status=status.HTTP_200_OK),
            403: SmsVerificationResendCooldown,
            409: PhoneAlreadyVerified,
        },
        summary='Запросить код подтверждения',
        description='Отправляет otp код на указанный номер телефона',
    )
    def post(self, request):
        # TODO: add validation at the beginning of each request
        serializer = UserPhoneSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        if (self.request.user.phone.code == serializer.data['code'] and
            self.request.user.phone.phone == serializer.data['phone']):
            raise PhoneAlreadyVerified
        if self.request.user.sms_verification:
            td = timezone.now() - self.request.user.sms_verification.created_at
            if td.seconds < settings.SMS_VERIFICATION_RESEND_COOLDOWN:  # not sure about tz
                raise SmsVerificationResendCooldown(
                    detail=f'You must wait for {settings.SMS_VERIFICATION_RESEND_COOLDOWN - td.seconds} seconds'
                           f' before requesting a new SMS verification code.')

        code = self.get_otp()
        response_serializer = PhoneVerificationSerializer(data={'code': code})
        response_serializer.is_valid(raise_exception=True)
        self.request.user.sms_verification = response_serializer.save()
        self.request.user.save()

        # send verification code, handle api errors

        return Response(data={"code":code}, status=status.HTTP_200_OK)

    @extend_schema(
        request=UserPhoneVerificationSerializer,
        responses={
            200: UserPhoneSerializer,
            403: PhoneAlreadyVerified | SmsVerificationExpired | SmsVerificationAttemptsExceeded | SmsVerificationFailed,
            409: SmsVerificationNotSend,
        },
        summary='Верифицировать код подтверждения',
        description='Верифицирует код подтверждения, в случаи успеха обновляет номер телефона пользователя',
    )
    def put(self, request):
        if not self.request.user.sms_verification:
            raise SmsVerificationNotSend

        serializer = UserPhoneVerificationSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        if self.request.user.phone == serializer.data['phone']:
            raise PhoneAlreadyVerified  # TODO: should never trigger, remove later
        td = timezone.now() - self.request.user.sms_verification.created_at
        if td.seconds > settings.SMS_VERIFICATION_RESEND_COOLDOWN:
            self.request.user.sms_verification.delete()
            raise SmsVerificationExpired
        if self.request.user.sms_verification.attempts > settings.SMS_VERIFICATION_ATTEMPTS:
            self.request.user.sms_verification.delete()
            raise SmsVerificationAttemptsExceeded

        if self.request.user.sms_verification.code != serializer.data['code']:
            self.request.user.sms_verification.attempts += 1
            self.request.user.sms_verification.save()
            raise SmsVerificationFailed
        response_serializer = PhoneSerializer(data=serializer.data['phone'])
        response_serializer.is_valid(raise_exception=True)
        # make it a transaction
        self.request.user.phone = response_serializer.save()
        self.request.user.save()
        self.request.user.sms_verification.delete()
        return Response(response_serializer.data)


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
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return {'url': settings.TECHSUPPORT_BOT_URL}
