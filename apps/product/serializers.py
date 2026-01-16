from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from apps.customer.models import Favorite

from .models import Category, Good, Image, Phone, ProductItem, SubCategory, Ticket
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


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class ProductItemSerializer(serializers.ModelSerializer):
    current_price = serializers.SerializerMethodField()
    sale = serializers.ReadOnlyField()

    class Meta:
        model = ProductItem
        fields = "__all__"

    def get_current_price(self, obj):
        request = self.context.get('request')
        user = request.user if request else None

        # Optomchi va tasdiqlangan bo'lsa optom narxni ko'rsatish
        if user and user.is_authenticated and getattr(user, 'is_wholesaler', False) and getattr(user, 'is_approved',
                                                                                                False):
            if obj.wholesale_price > 0:
                return obj.wholesale_price

        return obj.new_price


class TicketSerializer(ProductItemCreatorMixin):
    product = ProductItemSerializer()
    is_favorite = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Ticket
        fields = "__all__"

    def get_is_favorite(self, obj):
        if self.context["request"].user.is_anonymous:
            return False
        favorite = Favorite.objects.filter(
            user=self.context["request"].user.profile, product=obj.product
        ).first()
        if favorite is not None:
            return True
        return False

    def create(self, validate_data):
        product = self.create_pruduct(validate_data)
        return Ticket.objects.create(**validate_data, product=product)


class TicketForSearchSerializer(ProductItemCreatorMixin):
    product = ProductItemSerializer()

    class Meta:
        model = Ticket
        fields = "__all__"


class PhoneForSearchSerializer(ProductItemCreatorMixin):
    product = ProductItemSerializer()

    class Meta:
        model = Phone
        fields = "__all__"


class PhoneSerializer(ProductItemCreatorMixin):
    product = ProductItemSerializer()
    is_favorite = serializers.BooleanField(read_only=True)

    def get_is_favorite(self, obj):
        if self.context["request"].user.is_anonymous:
            return False
        favorite = Favorite.objects.filter(
            user=self.context["request"].user.profile, product=obj.product
        ).first()
        if favorite is not None:
            return True
        return False

    class Meta:
        model = Phone
        fields = "__all__"

    def create(self, validate_data):
        product = self.create_pruduct()
        return Phone.objects.create(**validate_data, product=product)


class GoodForSearchSerializer(ProductItemCreatorMixin):
    product = ProductItemSerializer()

    class Meta:
        model = Good
        fields = "__all__"
        read_only_fields = ("images",)


class GoodSerializer(ProductItemCreatorMixin):
    product = ProductItemSerializer()
    is_favorite = serializers.BooleanField(read_only=True)

    class Meta:
        model = Good
        fields = "__all__"
        read_only_fields = ("images",)

    def create(self, validate_data):
        product = self.create_pruduct()
        return Good.objects.create(**validate_data, product=product)


class TicketPopularSerializer(serializers.ModelSerializer):
    product = ProductItemSerializer()
    sold_count = serializers.IntegerField(read_only=True)
    is_favorite = serializers.SerializerMethodField(read_only=True)

    def get_is_favorite(self, obj):
        if self.context["request"].user.is_anonymous:
            return False
        favorite = Favorite.objects.filter(
            user=self.context["request"].user.profile, product=obj.product
        ).first()
        if favorite is not None:
            return True
        return False

    class Meta:
        model = Ticket
        fields = ["event_name", "event_date", "sold_count", "product", "is_favorite"]


class PhonePopularSerializer(serializers.ModelSerializer):
    product = ProductItemSerializer()
    sold_count = serializers.IntegerField(read_only=True)
    is_favorite = serializers.SerializerMethodField(read_only=True)

    def get_is_favorite(self, obj):
        if self.context["request"].user.is_anonymous:
            return False
        favorite = Favorite.objects.filter(
            user=self.context["request"].user.profile, product=obj.product
        ).first()
        if favorite is not None:
            return True
        return False

    class Meta:
        model = Phone
        fields = "__all__"


class GoodPopularSerializer(serializers.ModelSerializer):
    product = ProductItemSerializer()
    sold_count = serializers.IntegerField(read_only=True)
    is_favorite = serializers.BooleanField(read_only=True)

    def get_is_favorite(self, obj):
        if self.context["request"].user.is_anonymous:
            return False
        favorite = Favorite.objects.filter(
            user=self.context["request"].user.profile, product=obj.product
        ).first()
        if favorite is not None:
            return True
        return False

    class Meta:
        model = Good
        fields = "__all__"


class GoodVariantSerializer(serializers.ModelSerializer):
    product = ProductItemSerializer()

    class Meta:
        model = Good
        fields = "__all__"


class PhoneVariantSerializer(serializers.ModelSerializer):
    product = ProductItemSerializer()

    class Meta:
        model = Phone
        fields = "__all__"


class TicketVariantSerializer(serializers.ModelSerializer):
    product = ProductItemSerializer()

    class Meta:
        model = Ticket
        fields = "__all__"


