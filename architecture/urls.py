from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WarehouseViewSet, WareHouseManagerViewSet, ProductViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'warehouses', WarehouseViewSet, basename='warehouse')
router.register(r'managers', WareHouseManagerViewSet, basename='warehousemanager')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]
