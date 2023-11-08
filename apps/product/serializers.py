from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination

from .models import (Category, Good, Image, Phone, ProductItem, SubCategory,
                     Ticket)
from .utils import ProductItemCreatorMixin


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"


class ProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductItem
        fields = "__all__"


class TicketSerializer(ProductItemCreatorMixin):
    product = ProductItemSerializer()

    class Meta:
        model = Ticket
        fields = "__all__"

    def create(self, validate_data):
        product = self.create_pruduct(validate_data)
        return Ticket.objects.create(**validate_data, product=product)


class PhoneSerializer(ProductItemCreatorMixin):
    product = ProductItemSerializer()

    class Meta:
        model = Phone
        fields = "__all__"

    def create(self, validate_data):
        product = self.create_pruduct()
        return Phone.objects.create(**validate_data, product=product)


class GoodSerializer(ProductItemCreatorMixin):
    product = ProductItemSerializer()

    class Meta:
        model = Good
        fields = "__all__"

    def create(self, validate_data):
        product = self.create_pruduct()
        return Good.objects.create(**validate_data, product=product)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"

class TicketPopularSerializer(serializers.ModelSerializer):
    product = ProductItemSerializer()
    sold_count = serializers.IntegerField(read_only=True) 

    class Meta:
        model = Ticket
        fields = ['event_name', 'event_date', 'sold_count','product']

class PhonePopularSerializer(serializers.ModelSerializer):
    product = ProductItemSerializer()
    sold_count = serializers.IntegerField(read_only=True) 

    class Meta:
        model = Phone
        fields = "__all__"

class GoodPopularSerializer(serializers.ModelSerializer):
    product = ProductItemSerializer()
    sold_count = serializers.IntegerField(read_only=True) 

    class Meta:
        model = Good
        fields = "__all__"