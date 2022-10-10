from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from .permission import UserPermission
from .serializer import RequestCreateSerializer, RequestCloseSerializer
from .models import Request


class RequestViewSet(ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestCreateSerializer
    permission_classes = [UserPermission]

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
        obj.save()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def close(self, request, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=kwargs.get("pk"))
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
