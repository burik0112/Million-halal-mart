from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from apps.product.serializers import (
    ProductItemSerializer,
)
from .models import Bonus, LoyaltyCard, Referral
from apps.product.models import Phone, Ticket, Good
from .models import Order, OrderItem, Information, Service, SocialMedia
from ..customer.models import Profile, Location


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
    delivery_fee = serializers.SerializerMethodField()
    # orderitem = OrderItemDetailsSerializer(
    #     many=True, read_only=True, source="get_order_items"
    # )
    orderitem = OrderItemDetailsSerializer(many=True, read_only=True)
    bonus_amount = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"
        # read_only_fields = ("delivery_fee", "bonus_amount")

    def get_delivery_fee(self, obj):
        return obj.delivery_fee

    def get_bonus_amount(self, obj):
        return obj.bonus_amount


class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = OrderItem
        fields = "__all__"

    def create(self, validated_data):
        # Bu qism faqat CreateAPIView da ishlaydi (yangi qo'shishda)
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
        fields = ["status", "comment", "location"]

    def update(self, instance, validated_data):
        instance.status = validated_data.get("status", instance.status)
        instance.comment = validated_data.get("comment", instance.comment)
        instance.location = validated_data.get("location", instance.location)
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


class LoyaltyCardSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='profile.full_name', read_only=True)

    class Meta:
        model = LoyaltyCard
        fields = [
            'id',
            'profile',  # id профиля
            'full_name',  # имя пользователя
            'current_balance',
            'cycle_start',
            'cycle_end',
            'cycle_days',
            'cycle_number',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'full_name', 'created_at', 'updated_at']



class MyReferralHistorySerializer(serializers.ModelSerializer):
    friend_name = serializers.CharField(source='referee.full_name', read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Referral
        fields = ['friend_name', 'status', 'created_at']

class UserBonusSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()
    my_referrals_list = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'full_name', 'referral_code', 'balance', 'my_referrals_list']

    def get_balance(self, obj):
        try:
            return obj.loyalty_card.current_balance
        except:
            return 0

    def get_my_referrals_list(self, obj):
        invites = Referral.objects.filter(referrer=obj).order_by('-created_at')
        return MyReferralHistorySerializer(invites, many=True).data




class CartAddSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    quantity = serializers.IntegerField()

class CheckoutSerializer(serializers.Serializer):
    # Bu maydon ID qabul qiladi (masalan: 5), lekin bizga Location obyektini beradi
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    comment = serializers.CharField(required=False, allow_blank=True)

class ReceiptUploadSerializer(serializers.Serializer):
    order_number = serializers.CharField(
        max_length=50,
        help_text="Buyurtma raqamini kiriting (masalan: ORD123...)"
    )
    payment_receipt = serializers.FileField(
        help_text="To'lov cheki rasmi yoki PDF faylini yuklang"
    )

# 4. Buyurtma tafsilotlari (Rasmda ko'ringan Timeline bilan)
class OrderDetailSerializer(serializers.ModelSerializer):
    # 1. Qo'shimcha maydonlarni e'lon qilamiz
    timeline = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()
    customer_name = serializers.ReadOnlyField(source='user.full_name')
    location_address = serializers.ReadOnlyField(source='location.address')

    class Meta:
        model = Order
        # 2. BU YERGA 'timeline' VA 'items' NI QO'SHISH SHART!
        fields = [
            'id', 'order_number', 'customer_name', 'products', 'comment',
            'status', 'location_address', 'total_amount', 'created_at',
            'delivery_fee', 'timeline', 'items'
        ]

    def get_items(self, obj):
        # Buyurtma ichidagi mahsulotlar ro'yxati
        return [
            {
                "name": i.product.product_type if i.product else "Noma'lum",
                "quantity": i.quantity,
                "price": i.product.new_price if i.product and i.product.new_price > 0 else (i.product.old_price if i.product else 0)
            } for i in obj.orderitem.all()
        ]

    def get_timeline(self, obj):
        # Rasmda ko'ringan Step-by-step holati (faqat bitta metod qoldirdik)
        return {
            "step1_created": True,
            "step2_paid": obj.status in ['waiting_approval', 'approved', 'sent'],
            "step3_approved": obj.status in ['approved', 'sent'],
        }