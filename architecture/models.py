import math
from django.db import models
from datetime import timedelta
from django.utils import timezone
from .enums import WareHouseStatus, ProductStatus, OrderStatus

SURFACE_AREA = 14.77
EFFICIENCY_RATIO = 0.75

class WareHouseManager(models.Model):
  name = models.CharField(max_length=200)
  age = models.IntegerField()
  email = models.EmailField(max_length=100, unique=True, null=True, blank=True)

  class Meta:
    verbose_name = "Manager"
    verbose_name_plural = "Managers"
 
  def __str__(self):
    return f"{self.name} - {self.age} - {self.email}"

class Warehouse(models.Model):
  name = models.CharField(max_length=100)
  location = models.CharField(max_length=255)
  capacity = models.FloatField()
  manager = models.ForeignKey(WareHouseManager, on_delete=models.SET_NULL, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  status = models.CharField(max_length=20, choices=WareHouseStatus.choices, default=WareHouseStatus.INACTIVE)
  
  class Meta:
    verbose_name = "Entrepôt"
    verbose_name_plural = "Entrepôts"

  @property
  def container_capacity(self):
    """ Getter: Calculates total capacity for warehouse and the number of containers """
    # If capacity is negative, force the use of 0
    safe_capacity = max(0, self.capacity) 
    usable_area = safe_capacity * EFFICIENCY_RATIO
    containers_on_ground = math.floor(usable_area/SURFACE_AREA)
    return containers_on_ground
  
  @container_capacity.setter
  def container_capacity(self, target_capacity):
    """ Setter: Calculates the exact ground needed for a target capacity """
    # If the input is negative, automatically reset it to 0
    if target_capacity < 0:
        target_capacity = 0
        
    required_surface = (target_capacity * SURFACE_AREA) / EFFICIENCY_RATIO
    self.capacity = required_surface

  def __str__(self):
      return f"{self.name} - {self.capacity} m²"
  
class Product(models.Model):
  name = models.CharField(max_length=100)
  quantity = models.IntegerField()
  weight = models.IntegerField()
  consumer_date = models.DateField()
  expiration_date = models.DateField(null=True, blank=True)
  state = models.CharField(max_length=20, choices=ProductStatus.choices, default=ProductStatus.DISPONIBLE)
  warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=True)

  class Meta:
    verbose_name = "Produit"
    verbose_name_plural = "Produits"

  def __str__(self):
    return self.name

  def verify_state(self):
    """ Update a product's status and return True if it's necessary to make an alert """
    today = timezone.now().date()
    expiration_limit = today + timedelta(days=30)

    if self.expiration_date is None:
      self.state = ProductStatus.INDISPONIBLE

      return False

    elif self.expiration_date <= today:
      self.state = ProductStatus.EXPIRATION
     
      return True

    elif self.expiration_date <= expiration_limit:
      self.state = ProductStatus.EXPIRATION
     
      return True

    elif self.order_set.filter(order_status=OrderStatus.IN_PROGRESS).exists():
      self.state = ProductStatus.RESERVED

    else:
      self.state = ProductStatus.DISPONIBLE

    return False

  def save(self, *args, **kwargs):
    """ Automatically runs verification logic before saving to the database """
    self.verify_state()
    super().save(*args, **kwargs)


class Order(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity_ordered = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  order_status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.IN_PROGRESS)

  class Meta:
    verbose_name = "Commande"
    verbose_name_plural = "Commandes"

  def __str__(self):
    return f"Commande #{self.id} - {self.product.name}"
