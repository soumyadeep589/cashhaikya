from rest_framework import serializers

from .models import Request, CallList, CustomUser

__author__ = "soumyadeep"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'transactions', 'phone']


class RequestCreateSerializer(serializers.ModelSerializer):
    opened_by = UserSerializer()

    class Meta:
        model = Request
        fields = ['id', 'amount', 'opened_by', 'type']

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


class RequestUpdateSerializer(serializers.ModelSerializer):
    opened_by = UserSerializer()

    class Meta:
        model = Request
        fields = ['id', 'amount', 'opened_by', 'type']


class RequestCloseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = "__all__"


class CallListSerializer(serializers.ModelSerializer):
    called_by = UserSerializer()

    class Meta:
        model = CallList
        fields = ['id', "called_by"]
