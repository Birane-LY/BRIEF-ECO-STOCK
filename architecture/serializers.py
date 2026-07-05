from rest_framework import serializers
from .models import Warehouse, WareHouseManager, Product, Order

class WarehouseSerializer(serializers.ModelSerializer):
  class Meta:
    model = Warehouse
    fields = '__all__'
    

class WareHouseManagerSerializer(serializers.ModelSerializer):
  class Meta:
    model = WareHouseManager
    fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = Product
    fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
  class Meta:
    model = Order
    fields = '__all__'
