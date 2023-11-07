from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from apps.product.models import ProductItem, Good, Phone, Ticket
from .models import Favorite, Location, News, Profile, ViewedNews


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = "__all__"


class ViewedNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewedNews
        fields = "__all__"


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = "__all__"

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"

class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = "__all__"

class GoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Good
        fields = "__all__"

class ProductItemForFavouriteSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(read_only=True)
    phones = PhoneSerializer(read_only=True)
    goods = GoodSerializer(read_only=True)

    class Meta:
        model = ProductItem
        fields = "__all__"

class FavoriteListSerializer(serializers.ModelSerializer):
    product = ProductItemForFavouriteSerializer()

    class Meta:
        model = Favorite
        fields = "__all__"

