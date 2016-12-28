# -*- encoding: utf-8 -*-

# API v1
from apps.api.utils import APIVersionOneRouter
from apps.shop import views

urlpatterns = []


router = APIVersionOneRouter()
router.register('orderline', views.OrderLineViewSet)
router.register('transactions', views.TransactionViewSet)
router.register('usersaldo', views.UserViewSet)
router.register('inventory', views.InventoryViewSet)
