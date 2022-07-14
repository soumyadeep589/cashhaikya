from django.urls import path
from request import views

urlpatterns = [
    path(r'api/create', views.CreateRequestView.as_view(), name='create-request'),
]
