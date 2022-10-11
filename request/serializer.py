from rest_framework import serializers

from .models import Request, CallList

__author__ = "soumyadeep"


class RequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = "__all__"

    def validate(self, data):
        """
        check user has any opened request
        """
        user = self.context["request"].user
        if Request.objects.filter(
            opened_by=user, is_deleted=False, status="RQ", closed_to=None
        ).exists():
            raise serializers.ValidationError("user already has opened request")
        return data


class RequestCloseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = "__all__"


class CallListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallList
        fields = "__all__"
