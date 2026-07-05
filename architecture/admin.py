from django.contrib import admin
from .models import WareHouseManager, Warehouse, Product, Order

@admin.register(WareHouseManager)
class WareHouseManagerAdmin(admin.ModelAdmin):
    """ Admin configuration for WareHouseManager model. """
    list_display = ('name', 'age' 'email')
    search_fields = ('name',)

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    """ Admin configuration for Warehouse model. """
    list_display = ('name', 'location', 'capacity', 'container_capacity', 'status', 'manager')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'location')
    readonly_fields = ('created_at',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Admin configuration for Product model. """
    list_display = ('name', 'quantity', 'weight', 'state', 'expiration_date', 'warehouse')
    list_filter = ('state', 'expiration_date', 'warehouse')
    search_fields = ('name',)
    actions = ('trigger_verify_state',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """ Admin configuration for Order model. """
    list_display = ('id', 'product', 'quantity_ordered', 'order_status', 'created_at')
    list_filter = ('order_status', 'created_at')
    search_fields = ('product__name',)
    readonly_fields = ('created_at',)
