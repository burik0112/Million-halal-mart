from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Order


@receiver(m2m_changed, sender=Order.products.through)
def update_order_total(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        instance.update_total_amount()
