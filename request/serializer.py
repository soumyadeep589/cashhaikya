from rest_framework import serializers

from .models import Request

__author__ = "soumyadeep"


class RequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = "__all__"
