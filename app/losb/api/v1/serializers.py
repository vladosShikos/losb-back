from rest_framework import serializers

from losb.models import User, City, Phone

class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ('code','phone')

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id','name',)

class UserSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    class Meta:
        model = User
        fields = ('telegram_id','avatar','name', 'phone', 'city')

class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name',)


class UserCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('city',)

class UserBdaySerializer(serializers.Serializer):
    bday = serializers.DateField()

class UserPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('phone',)
