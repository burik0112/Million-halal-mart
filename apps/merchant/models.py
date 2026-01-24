from datetime import timedelta, date

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils import timezone
from model_utils.models import TimeStampedModel
from django.db.models import F
from ckeditor.fields import RichTextField
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from django.db.models import F, fields, ExpressionWrapper

from apps.customer.models import Profile, Location
from apps.product.models import ProductItem


class Order(TimeStampedModel, models.Model):
    STATUS_CHOICES = (
        ("in_cart", "Savatchada"),
        ("pending", "Kutilmoqda"),
        ("approved", "Tasdiqlandi"),
        ("sent", "Yuborildi"),
        ("cancelled", "Bekor qilindi"),
    )

    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="order"
    )
    products = models.ManyToManyField(
        ProductItem, through="OrderItem", related_name="order"
    )
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="in_cart")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    total_amount = models.DecimalField(decimal_places=0, max_digits=20, default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    # ---------------- LOYALTY BONUS ----------------
    def create_loyalty_pending_bonus(self):
        if LoyaltyPendingBonus.objects.filter(order=self).exists():
            return

        total = Decimal(0)

        items = self.orderitem.all()
        if not items.exists():
            return

        for item in items:
            price = (
                item.product.new_price
                if item.product.new_price > 0
                else item.product.old_price
            )
            total += price * item.quantity

        if total <= 0:
            return

        LoyaltyPendingBonus.objects.create(
            profile=self.user,
            order=self,
            username=self.user.full_name or self.user.phone_number,
            order_amount=total,
        )

    # ---------------- SAVE ----------------
    def save(self, *args, **kwargs):
        old_status = None
        if self.pk:
            old_status = Order.objects.get(pk=self.pk).status

        # 1️⃣ Сохраняем order, чтобы был pk
        super().save(*args, **kwargs)

        # 2️⃣ Считаем сумму заказа
        total = Decimal(0)
        items = self.orderitem.all()

        for item in items:
            price = (
                item.product.new_price
                if item.product.new_price > 0
                else item.product.old_price
            )
            total += price * item.quantity

        # 4️⃣ Создаём pending bonus ТОЛЬКО при переходе в sent
        if self.status == "sent" and old_status != "sent":
            self.create_loyalty_pending_bonus()

    # ---------------- STOCK UPDATE ----------------
    def update_product_stock(self):
        for item in self.orderitem.all():
            product_item = item.product
            product_item.available_quantity -= item.quantity
            if product_item.available_quantity < 0:
                raise ValidationError(f"Not enough product: {product_item.name}")
            product_item.save()

    # ---------------- HELPER METHODS ----------------
    def get_status_display_value(self):
        return dict(self.STATUS_CHOICES).get(self.status, "Unknown")

    def get_order_items(self):
        return self.orderitem.all().order_by("-pk")


class OrderItem(TimeStampedModel, models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderitem")
    product = models.ForeignKey(
        "product.ProductItem",
        on_delete=models.CASCADE,
        related_name="orderitem",
        null=True,
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


class SocialMedia(TimeStampedModel, models.Model):
    telegram = models.CharField(max_length = 255,blank=True, null=True)
    instagram = models.CharField(max_length = 255,blank=True, null=True)
    whatsapp = models.CharField(max_length = 255,blank=True, null=True)
    phone_number = models.CharField(max_length = 255,blank=True, null=True)
    imo = models.CharField(max_length = 255,blank=True, null=True)
    kakao = models.CharField(max_length = 255,blank=True, null=True)
    tiktok = models.CharField(max_length = 255,blank=True, null=True)

    def __str__(self) -> str:
        return "SocialMedias"


class Service(TimeStampedModel, models.Model):
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    def __str__(self) -> str:
        return "Service"


class Bonus(TimeStampedModel, models.Model):
    title = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(default=0, decimal_places=0, max_digits=10)
    percentage = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title if len(self.title) > 0 else str(self.amount)


class LoyaltyCard(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name='loyalty_card'
    )
    current_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    cycle_start = models.DateField()
    cycle_end = models.DateField()
    cycle_days = models.PositiveIntegerField(default=60)
    cycle_number = models.PositiveIntegerField(default=1)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




    def __str__(self):
        return f"LoyaltyCard({self.profile})"


class LoyaltyPendingBonus(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
    )

    profile = models.ForeignKey(
        "customer.Profile",
        on_delete=models.CASCADE
    )
    order = models.OneToOneField(
        "merchant.Order",
        on_delete=models.CASCADE,
        related_name="pending_bonus"
    )

    order_name = models.CharField(max_length=255)
    order_amount = models.DecimalField(max_digits=20, decimal_places=0)

    percent = models.PositiveIntegerField(null=True, blank=True)
    bonus_amount = models.DecimalField(
        max_digits=20,
        decimal_places=0,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Автоматический расчёт bonus_amount:
        - только если статус approved
        - только если percent указан
        """
        if self.status == "approved" and self.percent:
            # Приводим к Decimal для точного вычисления
            self.bonus_amount = Decimal(self.order_amount) * Decimal(self.percent) / Decimal(100)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_name} | {self.order_amount}"


class Referral(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('rewarded', 'Rewarded'),
        ('expired', 'Expired'),
    )

    referrer = models.ForeignKey(
        'customer.Profile',  # <--- ИСПРАВЬ ЗДЕСЬ (добавь customer.)
        on_delete=models.CASCADE,
        related_name='referrals_made'
    )
    referee = models.ForeignKey(
        'customer.Profile',  # <--- ИСПРАВЬ ЗДЕСЬ (добавь customer.)
        on_delete=models.CASCADE,
        related_name='referrals_received'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Логика автоматического начисления при создании
        if not self.pk and self.status == 'rewarded':
            super().save(*args, **kwargs)
            self.make_rewarded_logic()
            return

        # Логика при обновлении статуса
        if self.pk:
            old_status = Referral.objects.get(pk=self.pk).status
            if old_status == 'pending' and self.status == 'rewarded':
                self.make_rewarded_logic()

        super().save(*args, **kwargs)

    def make_rewarded_logic(self):
        from .models import LoyaltyCard
        with transaction.atomic():
            card, created = LoyaltyCard.objects.get_or_create(
                profile=self.referrer,
                defaults={
                    'cycle_start': date.today(),
                    'cycle_end': date.today() + timedelta(days=60),
                    'current_balance': 0
                }
            )
            card.current_balance = F('current_balance') + 5000
            card.save()

    class Meta:
        unique_together = ('referrer', 'referee')

    def __str__(self):
        return f"{self.referrer.full_name} -> {self.referee.full_name}"


class WalletTransaction(models.Model):
    TYPE_CHOICES = (
        ('loyalty', 'Loyalty'),
        ('referral', 'Referral'),
        ('spend', 'Spend'),
    )

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='wallet_transactions'
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES
    )
    reference_id = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction({self.user_id}, {self.type}, {self.amount})"

