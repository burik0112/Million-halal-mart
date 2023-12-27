from django.db import models
from model_utils.models import TimeStampedModel
from django.db.models import F
from ckeditor.fields import RichTextField
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F, fields, ExpressionWrapper


class Order(TimeStampedModel, models.Model):
    STATUS_CHOICES = (
        ("in_cart", "Savatchada"),
        ("pending", "Kutilmoqda"),
        ("approved", "To'lov tasdiqlandi"),
        ("sent", "Yuborildi"),
        ("cancelled", "Bekor qilindi"),
    )
    user = models.ForeignKey(
        "customer.Profile", on_delete=models.CASCADE, related_name="order"
    )
    products = models.ManyToManyField(
        "product.ProductItem", through="OrderItem", related_name="order"
    )
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="in_cart")

    total_amount = models.DecimalField(decimal_places=0, max_digits=20, default=0.00)

    def get_product_details(self, product_item, order_item):
        total_amount = (
            product_item.price * order_item.quantity
            - product_item.price * product_item.stock / 100
        )
        # print(total_amount)

        if hasattr(product_item, "goods"):
            return f"{product_item.goods.name} x {order_item.quantity} {product_item.get_measure_display()} = {total_amount} ₩"
        elif hasattr(product_item, "tickets"):
            return f"{product_item.tickets.event_name} x {order_item.quantity} {product_item.get_measure_display()} = {total_amount} ₩"
        elif hasattr(product_item, "phones"):
            return f"{product_item.phones.model_name}/{product_item.phones.get_ram_display()}/{product_item.phones.get_storage_display()} x {order_item.quantity} {product_item.get_measure_display()} = {total_amount} ₩"
        return "Mahsulot tafsiloti mavjud emas"

    def save(self, *args, **kwargs):
        # self.update_total_amount()
        if self.status == "in_cart":
            existing_order = Order.objects.filter(
                user=self.user, status="in_cart"
            ).exclude(pk=self.pk)
            if existing_order.exists():
                raise ValueError(
                    "Foydalanuvchi allaqachon 'in_cart' statusidagi Orderga ega"
                )
        # Agar yangi holat 'sent' bo'lsa va oldingi holat 'sent' emas bo'lsa
        if self.status == "sent" and self.pk is not None:
            old_status = Order.objects.get(pk=self.pk).status
            if old_status != "sent":
                self.update_product_stock()
        self.update_total_amount()
        super(Order, self).save(*args, **kwargs)

    def update_product_stock(self):
        # Bu yerda 'sent' holatidagi orderlar uchun ProductItem'larni yangilaymiz
        for item in self.orderitem.all():
            product_item = item.product

            # Calculate the new value of available_quantity using annotate
            new_quantity = F("available_quantity") - item.quantity
            product_item_with_updated_quantity = (
                product_item.__class__.objects.filter(id=product_item.id)
                .annotate(
                    new_available_quantity=ExpressionWrapper(
                        new_quantity, output_field=fields.PositiveIntegerField()
                    )
                )
                .values("new_available_quantity")
                .get()
            )

            if product_item_with_updated_quantity["new_available_quantity"] < 0:
                response_data = {"error": "Not enough product"}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            product_item.available_quantity = product_item_with_updated_quantity[
                "new_available_quantity"
            ]
            product_item.save()

    def update_total_amount(self):
        total = 0
        for item in self.orderitem.all():
            # discounted_price = item.product.price * (1 - item.product.stock / 100)
            print(item, "item")
            print(item.product, "product")
            total += item.product.price * item.quantity
        self.total_amount = total

    def get_status_display_value(self):
        """
        Returns the human-readable value for the status.
        """
        return dict(self.STATUS_CHOICES).get(self.status, "Unknown")

    def get_order_items(self):
        """
        Order bilan bog'liq barcha OrderItem'larni qaytaradi.
        """
        return self.orderitem.all()


class OrderItem(TimeStampedModel, models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderitem")
    product = models.ForeignKey(
        "product.ProductItem", on_delete=models.CASCADE, related_name="orderitem", null=True
    )
    quantity = models.IntegerField(default=0)


class Information(TimeStampedModel, models.Model):
    reminder = RichTextField(blank=True, null=True)
    agreement = RichTextField(blank=True, null=True)
    shipment_terms = RichTextField(blank=True, null=True)
    privacy_policy = RichTextField(blank=True, null=True)
    about_us = RichTextField(blank=True, null=True)
    support_center = RichTextField(blank=True, null=True)
    payment_data = RichTextField(blank=True, null=True)

    def __str__(self) -> str:
        return str(self.created)


class SecialMedia(TimeStampedModel, models.Model):
    telegram = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    whatsapp = models.URLField(blank=True, null=True)
    phone_number = models.CharField(blank=True, null=True)
    imo = models.URLField(blank=True, null=True)
    kakao = models.URLField(blank=True, null=True)

    def __str__(self) -> str:
        return "SocialMedias"


class Service(TimeStampedModel, models.Model):
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    def __str__(self) -> str:
        return "Service"
