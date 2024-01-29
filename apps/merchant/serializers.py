from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from apps.product.serializers import (
    ProductItemSerializer,
)
from .models import Bonus
from apps.product.models import Phone, Ticket, Good
from .models import Order, OrderItem, Information, Service, SocialMedia


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ("total_amount", "status", "comment")


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ("delivery_fee",)


class OrderItemDetailsSerializer(serializers.ModelSerializer):
    product = ProductItemSerializer(read_only=True)
    product_type = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = "__all__"

    def get_product_type(self, obj):
        product_item = obj.product
        if hasattr(product_item, "phones"):
            return {
                "type": "Phone",
                "details": PhoneSerializer(product_item.phones).data,
            }
        elif hasattr(product_item, "tickets"):
            return {
                "type": "Ticket",
                "details": TicketSerializer(product_item.tickets).data,
            }
        elif hasattr(product_item, "goods"):
            return {"type": "Good", "details": GoodSerializer(product_item.goods).data}
        return None


class OrderListSerializer(serializers.ModelSerializer):
    # products = ProductItemSerializer(read_only=True, many=True)
    orderitem = OrderItemDetailsSerializer(
        many=True, read_only=True, source="get_order_items"
    )

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ("delivery_fee",)


class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = OrderItem
        fields = "__all__"

    def create(self, validated_data):
        user = self.context["request"].user
        product = validated_data.get("product")
        order, created = Order.objects.get_or_create(
            user=user.profile, status="in_cart"
        )
        validated_data["order"] = order

        order_item, item_created = OrderItem.objects.get_or_create(
            order=order,
            product=product,
            defaults={"quantity": validated_data.get("quantity", 0)},
        )
        if not item_created:
            order_item.quantity += validated_data.get("quantity", 0)
            order_item.save()
        order.update_total_amount()
        return order_item


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"


class GoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Good
        fields = "__all__"


class OrderItemListSerializer(serializers.ModelSerializer):
    product = ProductItemSerializer(read_only=True)
    product_type = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = "__all__"

    def get_product_type(self, obj):
        product_item = obj.product
        if hasattr(product_item, "phones"):
            return {
                "type": "Phone",
                "details": PhoneSerializer(product_item.phones).data,
            }
        elif hasattr(product_item, "tickets"):
            return {
                "type": "Ticket",
                "details": TicketSerializer(product_item.tickets).data,
            }
        elif hasattr(product_item, "goods"):
            return {"type": "Good", "details": GoodSerializer(product_item.goods).data}
        return None


class InformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Information
        fields = "__all__"


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status", "comment"]

    def update(self, instance, validated_data):
        instance.status = validated_data.get("status", instance.status)
        instance.comment = validated_data.get("comment", instance.comment)
        instance.save()
        return instance


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = "__all__"


class BonusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bonus
        fields = "__all__"
