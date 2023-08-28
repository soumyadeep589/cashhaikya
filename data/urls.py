from django.urls import path
from data import views

urlpatterns = [
    path(r"request-deletion", views.delete_user_data, name="delete_user_data"),
]
