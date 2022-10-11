from rest_framework.routers import DefaultRouter

from request.views import RequestViewSet, CallViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"requests", RequestViewSet)
router.register(r"calls", CallViewSet)
urlpatterns = router.urls
