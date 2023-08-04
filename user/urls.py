from django.urls import path
from user import views

urlpatterns = [
    # path(r"api/gen-otp", views.GenerateOTP.as_view()),
    path(r"api/verify-otp", views.VerifyOTP.as_view()),
    path(r"api/register", views.Register.as_view()),
    path(r"api/login", views.Login.as_view()),
    path(r"api/logout", views.Logout.as_view()),
    path(r"api/user-info", views.UserInfo.as_view()),
]
