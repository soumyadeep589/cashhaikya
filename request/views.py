from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from .serializer import RequestCreateSerializer
from .models import Request


class RequestViewSet(ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestCreateSerializer

    @action(detail=True, methods=["post"])
    def delete(self, request, pk=None):
        obj = self.get_object()
        obj.is_deleted = True
        obj.save()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)
