from rest_framework.routers import DefaultRouter

from request.views import RequestViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"requests", RequestViewSet)
urlpatterns = router.urls
