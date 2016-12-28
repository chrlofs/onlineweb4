from apps.api.utils import APIVersionOneRouter
from apps.splash.api.views import SplashEventViewSet

urlpatterns = []

router = APIVersionOneRouter()
router.register('splash-events', SplashEventViewSet)
