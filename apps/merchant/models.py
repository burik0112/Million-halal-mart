from django.db import models
from model_utils.models import TimeStampedModel


class Order(TimeStampedModel, models.Model):
    STATUS_CHOICES = (
        ("in_cart", "In Cart"),
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("sent", "Sent"),
        ("cancelled", "Cancelled"),
    )
    user = models.ForeignKey(
        "customer.Profile", on_delete=models.CASCADE, related_name="order"
    )
    products = models.ManyToManyField(
        "product.ProductItem", through="OrderItem", related_name="order"
    )
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="in_cart")

    total_amount = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)

    def update_total_amount(self):
        self.total_amount = sum(
            item.product.price * item.quantity for item in self.orderitem_set.all()
        )
        self.save()


class OrderItem(TimeStampedModel, models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderitem")
    product = models.ForeignKey(
        "product.ProductItem", on_delete=models.CASCADE, related_name="orderitem"
    )
    quantity = models.IntegerField(default=0)


class Information(TimeStampedModel, models.Model):
    reminder = models.TextField(blank=True)
    agreement = models.TextField(blank=True)
    shipment_terms = models.TextField(blank=True)
    privacy_policy = models.TextField(blank=True)
    about_us = models.TextField(blank=True)
    support_center = models.TextField(blank=True)

    def __str__(self) -> str:
        return str(self.created)
