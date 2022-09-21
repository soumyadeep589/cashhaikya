from django.contrib import admin
from django.urls import path, include

from cashhaikya.routers import router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("v1/user/", include("user.urls")),
    path("v1/api/", include(router.urls)),
]
