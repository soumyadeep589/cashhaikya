from django.urls import path
from user import views

urlpatterns = [
    # path(r"api/gen-otp", views.GenerateOTP.as_view()),
    path(r"verify-otp", views.VerifyOTP.as_view()),
    path(r"register", views.Register.as_view()),
    path(r"login", views.Login.as_view()),
    path(r"logout", views.Logout.as_view()),
    path(r"user-info", views.UserInfo.as_view()),
]
