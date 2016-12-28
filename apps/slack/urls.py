from apps.api.utils import APIVersionOneRouter
from apps.slack import views

urlpatterns = []

router = APIVersionOneRouter()
router.register('slack', views.InviteViewSet, base_name='slack')
