from rest_framework.viewsets import ModelViewSet

from .serializer import RequestCreateSerializer
from .models import Request


class RequestViewSet(ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestCreateSerializer
