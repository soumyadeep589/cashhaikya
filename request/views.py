from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from .permission import UserPermission
from .serializer import (
    RequestCreateSerializer,
    RequestCloseSerializer,
    CallListSerializer,
)
from .models import Request, CallList


class RequestViewSet(ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestCreateSerializer
    permission_classes = [UserPermission]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == "close":
            serializer_class = RequestCloseSerializer
        return serializer_class

    def create(self, request, *args, **kwargs):
        data = request.data
        data["opened_by"] = request.user.id
        serializer = self.get_serializer(data=data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
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
        serializer = self.get_serializer(request, many=True)
        return Response(serializer.data)


class CallViewSet(ModelViewSet):
    queryset = CallList.objects.all()
    serializer_class = CallListSerializer
    permission_classes = [UserPermission]

    def create(self, request, *args, **kwargs):
        data = request.data
        data["called_by"] = request.user.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
