from rest_framework import serializers
from losb.models import User, City, Phone, SMSVerification


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ('code', 'number')


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('name',)


class UserSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    phone = PhoneSerializer()

    class Meta:
        model = User
        fields = ('telegram_id', 'avatar', 'name', 'phone', 'city', 'bday')


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name',)


class UserCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('city',)


class UserBdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('bday',)


class UserPhoneSerializer(serializers.ModelSerializer):
    number = serializers.CharField()

    class Meta:
        model = Phone
        fields = ('code', 'number')


class SMSVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSVerification
        fields = ('otp',)


class UserPhoneVerificationSerializer(serializers.ModelSerializer):
    phone = PhoneSerializer()

    class Meta:
        model = SMSVerification
        fields = ('otp', 'phone')


class BotUrlSerializer(serializers.Serializer):
    url = serializers.CharField()
