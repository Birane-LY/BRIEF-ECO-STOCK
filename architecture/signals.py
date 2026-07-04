from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Order

@receiver(post_save , sender=Order)
def alert_and_notifications(sender, instance, created, **kwargs):
  """ A trigger will be automatically fired when an Order is saved  """
  product = instance.product
  should_alert, is_expired = product.verify_state()

  if should_alert and product.warehouse and product.warehouse.manager:
    manager = product.warehouse.manager
    warehouse_name = product.warehouse.name

    if is_expired:
      message = f"URGENT: Le produit '{product.name}' dans l'entrepôt '{warehouse_name}' a atteint sa date de péremption !"
    else:
      days_left = (product.expiration_date - timezone.now().date()).days
      message = f"ATTENTION: Le produit '{product.name}' dans l'entrepôt '{warehouse_name}' expire dans {days_left} jours."

    print(f"[SIGNAL] Notification envoyée à {manager.name} : {message}")