from django.contrib.auth.models import User
from django.db import models
from model_utils.models import TimeStampedModel

# Create your models here.


class Profile(TimeStampedModel, models.Model):
    LANG = (("uz", "UZ"), ("ru", "RU"), ("en", "EN"), ("kr", "KR"))
    origin = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=17)
    lang = models.CharField(max_length=2, choices=LANG, default="uz")
    cashback = models.IntegerField(default=0)
    otp = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return self.origin.username


class Location(TimeStampedModel, models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="location")
    address = models.CharField(max_length=510)
    active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.active:
            Location.objects.filter(user=self.user).exclude(id=self.id).update(
                active=False
            )

        super(Location, self).save(*args, **kwargs)


class News(TimeStampedModel, models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="media/news")
    active = models.BooleanField(default=True)

    @classmethod
    def get_latest_unviewed_news(cls, user):
        # Foydalanuvchining ko'rmagan yangiliklarini topish
        viewed_news_ids = user.viewednews.values_list("news", flat=True)
        latest_news = (
            cls.objects.exclude(id__in=viewed_news_ids)
            .filter(active=True)
            .order_by("-start_date")
            .first()
        )
        return latest_news


class ViewedNews(TimeStampedModel, models.Model):
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="viewednews"
    )
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="viewednews")

    def __str__(self) -> str:
        return self.user.full_name


class Favorite(TimeStampedModel, models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(
        "product.ProductItem", on_delete=models.CASCADE, related_name="favorite"
    )

    class Meta:
        unique_together = ("user", "product")

    def __str__(self) -> str:
        return f"{self.user.origin.username} - {self.product.desc}"


class Banner(TimeStampedModel, models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to="media/banner")
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title
