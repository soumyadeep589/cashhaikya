from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from .permission import UserPermission
from .serializer import RequestCreateSerializer
from .models import Request


class RequestViewSet(ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestCreateSerializer
    permission_classes = [UserPermission]

    def create(self, request, *args, **kwargs):
        data = request.data
        data["opened_by"] = request.user.id
        serializer = self.get_serializer(data=data)
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
