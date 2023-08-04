from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from utils.notification import notify

from .permission import UserPermission
from .serializer import (
    RequestCreateSerializer,
    RequestCloseSerializer,
    CallListSerializer,
    RequestUpdateSerializer,
    RequestSerializer,
    UserSerializer,
    CreateCallSerializer
)
from .models import Request, CallList


class RequestViewSet(ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [UserPermission]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == "create":
            serializer_class = RequestCreateSerializer
        if self.action == "close":
            serializer_class = RequestCloseSerializer
        if self.action == "partial_update":
            serializer_class = RequestUpdateSerializer
        return serializer_class

    def get_queryset(self):
        queryset = self.queryset
        request_type = self.request.query_params.get("type")
        if request_type is not None:
            queryset = self.queryset.filter(
                is_active=True, status="RQ", is_deleted=False, type=request_type
            )
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data
        data["opened_by"] = request.user.id
        user_name = request.user.name
        request_type = "cash" if data["type"] == "C" else "bank"
        amount = data["amount"]
        serializer = self.get_serializer(data=data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            notify(title="Attention !!!", body=f"{user_name} has requested {amount} rupees in {request_type}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def delete(self, request, pk=None):
        obj = self.get_object()
        obj.is_deleted = True
        obj.status = "DL"
        obj.save()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def close(self, request, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=kwargs.get("pk"))
        if instance.closed_to is None:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            if serializer.validated_data.get("closed_to") == instance.opened_by:
                return Response(
                    {"error": "can not be closed with same opened by"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            with transaction.atomic():
                self.perform_update(serializer)
                closed_to = serializer.validated_data.get("closed_to")
                closed_to.transactions += 1 if closed_to.transactions is None else 1
                closed_to.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK,
                )
        return Response({"error": "already closed"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def history(self, request, *args, **kwargs):
        requests = (
            self.get_queryset()
            .filter(opened_by=request.user, is_active=True)
            .exclude(status="RQ")
        )
        serializer = self.get_serializer(requests, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def active(self, request, *args, **kwargs):
        request = self.get_queryset().filter(
            opened_by=request.user, is_active=True, status="RQ", is_deleted=False
        )
        if request.exists():
            request = request.first()
            call_list = CallList.objects.filter(request=request)
            call_serializer = CallListSerializer(call_list, many=True)
            serializer = self.get_serializer(request)
            return Response(
                {"request": serializer.data, "call_list": call_serializer.data}
            )
        return Response(status=status.HTTP_404_NOT_FOUND)


class CallViewSet(ModelViewSet):
    queryset = CallList.objects.all()
    serializer_class = CallListSerializer
    permission_classes = [UserPermission]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == "create":
            serializer_class = CreateCallSerializer
        return serializer_class

    def create(self, request, *args, **kwargs):
        data = request.data
        data["called_by"] = request.user.id
        # request_of_called_by = Request.objects.filter(
        #     opened_by=request.user, is_active=True, status="RQ", is_deleted=False
        # ).first()
        serializer = self.get_serializer(data=data)
        with transaction.atomic():
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
