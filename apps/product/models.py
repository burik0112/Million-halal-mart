from django.db import models
from model_utils.models import TimeStampedModel


class Category(TimeStampedModel, models.Model):
    PRODUCT_TYPE = (("f", "Oziq-ovqat"), ("p", "Telefon"), ("t", "Chipta"))
    main_type = models.CharField(max_length=1, choices=PRODUCT_TYPE, default="f")
    name = models.CharField(blank=True, max_length=255)
    image = models.ImageField(upload_to="category")
    desc = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

    def get_type_display(self):
        """Get the human-readable main_type label."""
        return dict(self.PRODUCT_TYPE).get(self.main_type, "Unknown")


class SubCategory(TimeStampedModel, models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="subcategory"
    )
    name = models.CharField(blank=True, max_length=255)
    image = models.ImageField(upload_to="subcategory")
    desc = models.TextField(blank=True, null=True)
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
    old_price = models.DecimalField(
        decimal_places=0, max_digits=10, null=True, blank=True, default=0
    )
    new_price = models.DecimalField(
        decimal_places=0, max_digits=10, null=True, blank=True, default=0
    )
    weight = models.FloatField(default=1, blank=True)
    measure = models.IntegerField(choices=CHOICES, default=0)
    available_quantity = models.PositiveIntegerField(default=0)
    bonus = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    @property
    def sale(self):
        if self.new_price == 0:
            return 0
            """Agar yangi narx eski narxdan past bo'lsa, foizni qaytaradi."""
        elif self.old_price and self.new_price < self.old_price:
            return round(abs(1 - self.new_price / self.old_price) * 100)
        return 0

    def price_changed(self):
        """Narx o'zgarganligini tekshiradi."""
        return self.old_price > self.new_price

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
    event_date = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="tickets"
    )

    def __str__(self) -> str:
        return self.event_name

    def save(self, *args, **kwargs):
        self.product.measure = (
            1  # Assuming 1 corresponds to "DONA" in the CHOICES tuple
        )
        self.product.save()
        super().save(*args, **kwargs)


class Phone(models.Model):
    STORAGE = (
        ("16 GB", "16 GB"),
        ("32 GB", "32 GB"),
        ("64 GB", "64 GB"),
        ("128 GB", "128 GB"),
        ("256 GB", "256 GB"),
        ("512 GB", "512 GB"),
        ("1 TB", "1 TB"),
        ("2 TB", "2 TB"),
        ("other", "Boshqa"),
    )
    RAM = (
        ("2 GB", "2 GB"),
        ("4 GB", "4 GB"),
        ("6 GB", "6 GB"),
        ("8 GB", "8 GB"),
        ("12 GB", "12 GB"),
        ("16 GB", "16 GB"),
        ("32 GB", "32 GB"),
        ("64 GB", "64 GB"),
        ("other", "Boshqa"),
    )
    COLOR_CHOICES = (
        ("red", "Red"),
        ("blue", "Blue"),
        ("pink", "Pink"),
        ("green", "Green"),
        ("black", "Black"),
        ("white", "White"),
        ("gold", "Gold"),
        ("silver", "Silver"),
        ("other", "Boshqa"),
    )
    CONDITION = (
        ("good", "Yaxshi"),
        ("exc", "A'lo"),
        ("used", "Foydalanilgan"),
        ("new", "Yangi"),
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
    ram = models.CharField(choices=RAM, default=0)
    storage = models.CharField(choices=STORAGE, default=0)
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

    def save(self, *args, **kwargs):
        self.product.measure = 1
        self.product.save()
        super().save(*args, **kwargs)


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
    user = models.ForeignKey("customer.Profile", on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(decimal_places=0, default=0, max_digits=20)
    quantity = models.PositiveIntegerField(default=0)

    def __int__(self) -> int:
        return self.id
