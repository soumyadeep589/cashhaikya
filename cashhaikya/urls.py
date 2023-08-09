from django.contrib import admin
from django.urls import path, include

from cashhaikya.routers import router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/user/", include("user.urls")),
    path("api/v1/", include(router.urls)),
]
