from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from .models import Order, OrderItem


@receiver(m2m_changed, sender=Order.products.through)
def update_order_total(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        instance.update_total_amount()
        

@receiver(post_save, sender=OrderItem)
def product_price_changed(sender, instance, **kwargs):
        instance.order.update_total_amount()


