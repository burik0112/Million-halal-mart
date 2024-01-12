from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import ProductItem


# @receiver(pre_save, sender=ProductItem)
# def update_old_price(sender, instance, **kwargs):
#     if instance.pk:
#         # Eski obyektni bazadan olish
#         old_instance = sender.objects.get(pk=instance.pk)
#         # Agar yangi narx o'zgargan bo'lsa, eski narxni yangilaymiz
#         if old_instance.new_price != instance.new_price:
#             instance.old_price = old_instance.new_price
