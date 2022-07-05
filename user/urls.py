from django.urls import path
from user import views

urlpatterns = [
    path(r"api/gen-otp", views.GenerateOTP.as_view()),
    path(r"api/verify-otp", views.VerifyOTP.as_view()),
    path(r"api/test", views.Test.as_view()),
]
