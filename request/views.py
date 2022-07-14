from .serializer import RequestCreateSerializer
from rest_framework import generics
from .models import Request


class CreateRequestView(generics.ListCreateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestCreateSerializer
