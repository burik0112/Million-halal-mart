from django.db import models
from model_utils.models import TimeStampedModel
from django.db.models import F
from ckeditor.fields import RichTextField


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

    def save(self, *args, **kwargs):
        # Agar yangi holat 'sent' bo'lsa va oldingi holat 'sent' emas bo'lsa
        if self.status == "sent" and self.pk is not None:
            old_status = Order.objects.get(pk=self.pk).status
            if old_status != "sent":
                self.update_product_stock()
        super(Order, self).save(*args, **kwargs)

    def update_product_stock(self):
        # Bu yerda 'sent' holatidagi orderlar uchun ProductItem'larni yangilaymiz
        for item in self.orderitem_set.all():
            product_item = item.product
            product_item.available_quantity = F("available_quantity") - item.quantity
            product_item.save()

    def update_total_amount(self):
        total = 0
        for item in self.orderitem_set.all():
            discounted_price = item.product.price * (1 - item.product.stock / 100)
            total += discounted_price * item.quantity
        self.total_amount = total
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
    payment_data = RichTextField(blank=True)

    def __str__(self) -> str:
        return str(self.created)


class Service(TimeStampedModel, models.Model):
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=1, default=0)

    def __str__(self) -> str:
        return "Service"
