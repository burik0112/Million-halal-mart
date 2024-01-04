from django.db import models
from model_utils.models import TimeStampedModel
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone


# Create your models here.
class Category(TimeStampedModel, models.Model):
    PRODUCT_TYPE = (("f", "Food"), ("p", "Phone"), ("t", "Ticket"))
    main_type = models.CharField(
        max_length=1, choices=PRODUCT_TYPE, default="f")
    name = models.CharField(blank=True, max_length=255)
    image = models.ImageField(upload_to="category")
    desc = models.TextField(blank=True)
    # stock = models.IntegerField(default=0)
    # bonus = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class SubCategory(TimeStampedModel, models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="subcategory"
    )
    name = models.CharField(blank=True, max_length=255)
    image = models.ImageField(upload_to="subcategory")
    desc = models.TextField(blank=True, null=True)
    # stock = models.IntegerField(default=0)
    # bonus = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class ProductItem(TimeStampedModel, models.Model):
    CHOICES = (
        (0, "KG"),
        (1, "DONA"),
        (2, "L"),
        (3, "PAKET"),
    )

    desc = models.TextField()
    # price = models.DecimalField(decimal_places=0, max_digits=10, default=0)
    old_price = models.DecimalField(
        decimal_places=2, max_digits=10, null=True, blank=True, default=0
    )
    new_price = models.DecimalField(
        decimal_places=2, max_digits=10, null=True, blank=True, default=0
    )
    measure = models.IntegerField(choices=CHOICES, default=0)
    available_quantity = models.PositiveIntegerField(default=0)
    # stock = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)
    is_favorite = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    @property
    def price_reduction_percentage(self):
        """Agar yangi narx eski narxdan past bo'lsa, foizni qaytaradi."""
        if self.old_price and self.new_price < self.old_price:
            return round((1 - self.new_price / self.old_price) * 100, 2)
        return 0

    def __str__(self) -> str:
        return str(self.created)

    def get_measure_display(self):
        """Get the human-readable measure label."""
        return dict(self.CHOICES).get(self.measure, "Unknown")


class Ticket(models.Model):
    event_name = models.CharField(max_length=255)
    product = models.OneToOneField(
        ProductItem, on_delete=models.CASCADE, related_name="tickets"
    )
    event_date = models.DateField(auto_now=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="tickets"
    )

    def __str__(self) -> str:
        return self.event_name


class Phone(models.Model):
    STORAGE = (
        (0, "32 GB"),
        (1, "64 GB"),
        (2, "128 GB"),
        (3, "256 GB"),
        (4, "512 GB"),
        (5, "1 TB"),
        (6, "2 TB"),
    )
    RAM = (
        (0, "4 GB"),
        (1, "6 GB"),
        (2, "8 GB"),
        (3, "12 GB"),
        (4, "16 GB"),
        (5, "32 GB"),
    )
    COLOR_CHOICES = (
        ("red", "Red"),
        ("blue", "Blue"),
        ("green", "Green"),
        ("black", "Black"),
        ("white", "White"),
        ("gold", "Gold"),
        ("silver", "Silver"),
    )
    CONDITION = (
        ("good", "Good"),
        ("exc", "Excellent"),
        ("used", "Used"),
        ("new", "New"),
    )
    color = models.CharField(
        max_length=10,
        choices=COLOR_CHOICES,
        default="black",
    )
    condition = models.CharField(
        max_length=10,
        choices=CONDITION,
        default="new",
    )
    product = models.OneToOneField(
        ProductItem, on_delete=models.CASCADE, related_name="phones"
    )
    model_name = models.CharField(max_length=255)
    ram = models.IntegerField(choices=RAM, default=0)
    storage = models.IntegerField(choices=STORAGE, default=0)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="phones"
    )

    def get_ram_display(self):
        return dict(self.RAM).get(self.ram, "Unknown")

    def get_storage_display(self):
        return dict(self.STORAGE).get(self.storage, "Unknown")

    def get_color_display(self):
        return dict(self.COLOR_CHOICES).get(self.color, "Unknown")

    def get_condition_display(self):
        return dict(self.CONDITION).get(self.condition, "Unknown")

    def __str__(self) -> str:
        return self.model_name


class Good(models.Model):
    name = models.CharField(max_length=255)
    product = models.OneToOneField(
        ProductItem, on_delete=models.CASCADE, related_name="goods"
    )
    ingredients = models.CharField(max_length=255, blank=True)
    expire_date = models.DateField(null=True)
    sub_cat = models.ForeignKey(
        "product.SubCategory", on_delete=models.SET_NULL, null=True
    )

    def __str__(self) -> str:
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to="images")
    name = models.CharField(max_length=255)
    product = models.ForeignKey(
        ProductItem, on_delete=models.CASCADE, related_name="images"
    )

    def __str__(self) -> str:
        return self.name


class SoldProduct(TimeStampedModel, models.Model):
    product = models.ForeignKey(
        ProductItem, on_delete=models.SET_NULL, null=True, related_name="sold_products"
    )
    user = models.ForeignKey(
        "customer.Profile", on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(decimal_places=0, default=0, max_digits=20)
    quantity = models.PositiveIntegerField(default=0)

    def __int__(self) -> int:
        return self.id
