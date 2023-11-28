from django.db import models
from model_utils.models import TimeStampedModel


class Order(TimeStampedModel, models.Model):
    user = models.ForeignKey(
        "customer.Profile", on_delete=models.CASCADE, related_name='order')
    products = models.ManyToManyField(
        "product.ProductItem", through='OrderItem', related_name='order')
    comment=models.TextField(blank=True)

class OrderItem(TimeStampedModel, models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='orderitem')
    product = models.ForeignKey(
        "product.ProductItem", on_delete=models.CASCADE, related_name='orderitem')
    quantity = models.IntegerField(default=0)


class Information(TimeStampedModel, models.Model):
    reminder = models.TextField(blank=True)
    agreement = models.TextField(blank=True)
    shipment_terms = models.TextField(blank=True)
    privacy_policy = models.TextField(blank=True)
    about_us = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.created
