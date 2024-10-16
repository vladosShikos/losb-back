from rest_framework import serializers

from losb.models import User



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('telegram_id','avatar','name')