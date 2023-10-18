from django.db import models
from model_utils.models import TimeStampedModel


# Create your models here.
class Category(TimeStampedModel, models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="category")
    desc = models.TextField()
    stock = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name


class SubCategory(TimeStampedModel, models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategory')
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="subcategory")
    desc = models.TextField()
    stock = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name


class ProductItem(TimeStampedModel, models.Model):
    CHOICES = (
        (0, "KG"),
        (1, "DONA"),
        (2, "L"),
        (3, "PAKET"),
    )
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='productitem')
    name = models.CharField(max_length=255)
    desc = models.TextField()
    price = models.DecimalField(decimal_places=1, max_digits=10, default=0)
    measure = models.IntegerField(choices=CHOICES, default=0)
    available_quantity = models.PositiveIntegerField(default=0)
    stock = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class Ticket(models.Model):
    event_name = models.CharField(max_length=255)
    product = models.OneToOneField(ProductItem, on_delete=models.CASCADE, related_name='tickets')
    event_date = models.DateField(auto_now=True)

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
    product = models.OneToOneField(ProductItem, on_delete=models.CASCADE, related_name='phones')
    brand_name = models.CharField(max_length=255)
    model_name = models.CharField(max_length=255)
    ram = models.IntegerField(choices=RAM, default=0)
    storage = models.IntegerField(choices=STORAGE, default=0)

    def __str__(self) -> str:
        return self.brand_name


class Good(models.Model):
    name = models.CharField(max_length=255)
    product = models.OneToOneField(ProductItem, on_delete=models.CASCADE, related_name='goods')
    ingredients = models.CharField(max_length=255, blank=True)
    expire_date = models.DateField()

    def __str__(self) -> str:
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to="images")
    name = models.CharField(max_length=255)
    product = models.OneToOneField(ProductItem, on_delete=models.CASCADE, related_name='images')

    def __str__(self) -> str:
        return self.name
