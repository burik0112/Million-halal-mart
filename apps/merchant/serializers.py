from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from apps.product.serializers import ProductItemSerializer
from .models import Order, OrderItem, Information, Service, SecialMedia


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


class OrderListSerializer(serializers.ModelSerializer):
    products = ProductItemSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"

    def perform_create(self, serializer):
        user = self.request.user
        try:
            order = Order.objects.get(user=user, status="in_cart")
        except Order.DoesNotExist:
            order = Order.objects.create(user=user, status="in_cart")

        serializer.save(order=order)


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
        model = SecialMedia
        fields = "__all__"
