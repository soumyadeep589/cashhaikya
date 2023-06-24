from rest_framework.routers import DefaultRouter
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

from request.views import RequestViewSet, CallViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"requests", RequestViewSet)
router.register(r"calls", CallViewSet)
router.register('devices', FCMDeviceAuthorizedViewSet)

urlpatterns = router.urls
