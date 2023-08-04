from rest_framework import serializers

from .models import CustomUser

__author__ = "soumyadeep"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'phone']