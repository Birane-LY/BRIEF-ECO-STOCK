from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .models import Warehouse, WareHouseManager, Product, Order
from .serializers import WarehouseSerializer, WareHouseManagerSerializer, ProductSerializer, OrderSerializer

class WarehouseViewSet(viewsets.ModelViewSet):
  queryset = Warehouse.objects.all()
  serializer_class = WarehouseSerializer

  @action(detail=True, methods=['get'])
  def audit(self, request, pk=None):
      """ Audit the warehouse by returning the total number of associated products. """
      warehouse = self.get_object()
      total_products = warehouse.product_set.count()
      return Response({
          "warehouse": warehouse.name,
          "total_products": total_products
      }, status=status.HTTP_200_OK)

  def get_permissions(self):
      if self.action in ['list', 'retrieve', 'audit']:
          permission_classes = [AllowAny]
      elif self.action == 'create':
          permission_classes = [IsAuthenticated]
      else:
          permission_classes = [IsAdminUser]
      return [permission() for permission in permission_classes]

class WareHouseManagerViewSet(viewsets.ModelViewSet):
  queryset = WareHouseManager.objects.all()
  serializer_class = WareHouseManagerSerializer

  def get_permissions(self):
      if self.action in ['list', 'retrieve']:
          permission_classes = [AllowAny]
      elif self.action == 'create':
          permission_classes = [IsAuthenticated]
      else:
          permission_classes = [IsAdminUser]
      return [permission() for permission in permission_classes]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['post'], url_path='move')
    def move_product(self, request, pk=None):
        """ Transfer the product to another warehouse if it is not expired. """
        product = self.get_object()
        
        if product.state == "expiration":
            return Response(
                {"error": "On ne peut pas déplacer un produit périmé."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        target_warehouse_id = request.data.get('warehouse_id')
        if not target_warehouse_id:
            return Response(
                {"error": "L'ID de l'entrepôt est obligatoire."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            target_warehouse = Warehouse.objects.get(id=target_warehouse_id)
            
            product.warehouse = target_warehouse
            product.save()
            
            return Response({
                "message": "Product moved successfully.",
                "product": product.name,
                "new_warehouse": target_warehouse.name
            }, status=status.HTTP_200_OK)
            
        except (Warehouse.DoesNotExist, ValueError, ValidationError):
            return Response(
                {"error": "Entrepôt ciblé non trouvé ou ID invalide."}, 
                status=status.HTTP_404_NOT_FOUND
            )


    @action(detail=True, methods=['get'])
    def audit(self, request, pk=None):
        """ Audit the specific product's state and return if alert is needed. """
        product = self.get_object()
        has_alert, is_expired = product.verify_state()
        return Response({
            "status": "Audited",
            "current_state": product.state,
            "has_alert": has_alert,
            "is_expired": is_expired
        }, status=status.HTTP_200_OK)
    
        
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        elif self.action in ['create', 'move_product', 'audit']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
            
class OrderViewSet(viewsets.ModelViewSet):
  queryset = Order.objects.all()
  serializer_class = OrderSerializer

  def get_permissions(self):
      if self.action in ['list', 'retrieve']:
          permission_classes = [AllowAny]
      elif self.action == 'create':
          permission_classes = [IsAuthenticated]
      else:
          permission_classes = [IsAdminUser]
      return [permission() for permission in permission_classes]
