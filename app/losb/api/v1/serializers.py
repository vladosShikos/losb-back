from rest_framework import serializers

from losb.models import User, City, Phone, SmsVerification

class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ('code','phone')

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('name',)

class UserSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    phone = PhoneSerializer()
    class Meta:
        model = User
        fields = ('telegram_id','avatar','name', 'phone', 'city', 'bday')

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
    class Meta:
        model = Phone
        fields = ('code','phone',)

class PhoneVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmsVerification
        fields = ('code',)

class UserPhoneVerificationSerializer(serializers.ModelSerializer):
    code = PhoneVerificationSerializer() # TODO: rename to otp
    class Meta:
        model = Phone
        fields = ('phone','code')


class BotUrlSerializer(serializers.Serializer):
    url = serializers.CharField()