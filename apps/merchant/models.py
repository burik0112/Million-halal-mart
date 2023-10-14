from django.db import models
from model_utils.models import TimeStampedModel


class Order(TimeStampedModel, models.Model):
    user = models.ForeignKey("customer.Profile", on_delete=models.CASCADE, related_name='order')
    products = models.ManyToManyField("product.ProductItem", through='OrderItem', related_name='order')
    

class OrderItem(TimeStampedModel, models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitem')
    product = models.ForeignKey("product.ProductItem", on_delete=models.CASCADE, related_name='orderitem')
    quantity = models.IntegerField(default=0)
    