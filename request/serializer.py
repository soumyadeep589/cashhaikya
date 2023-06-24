from rest_framework import serializers

from .models import Request, CallList, CustomUser

__author__ = "soumyadeep"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'transactions', 'phone']


class DateSerializerField(serializers.Field):
    def to_representation(self, value):
        return value.date() if value else None

    def to_internal_value(self, data):
        # This method can be left empty since we don't need it for read-only fields
        pass


class RequestSerializer(serializers.ModelSerializer):
    opened_by = UserSerializer()
    updated_on = DateSerializerField()

    class Meta:
        model = Request
        fields = ['id', 'amount', 'opened_by', 'type', 'status', 'updated_on']


class RequestCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        fields = ['id', 'amount', 'type', 'opened_by']

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
