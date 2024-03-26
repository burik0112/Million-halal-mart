from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, permissions
from django.db import transaction
from django.db.models import Prefetch
from rest_framework.response import Response
from .models import Order, OrderItem, Information, Service, SocialMedia, Bonus
from .serializers import (
    CustomPageNumberPagination,
    OrderItemSerializer,
    OrderSerializer,
    InformationSerializer,
    OrderStatusUpdateSerializer,
    ServiceSerializer,
    OrderListSerializer,
    OrderCreateSerializer,
    SocialMediaSerializer,
    BonusSerializer,
)
from apps.dashboard.main import bot

# Create your views here.


class OrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if (
            serializer.validated_data.get("status") == "in_cart"
            and Order.objects.filter(user=request.user, status="in_cart").exists()
        ):
            return Response(
                {"detail": "You already have an in-cart order."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class OrderListAPIView(ListAPIView):
    serializer_class = OrderListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["user__full_name"]
    filterset_fields = ["user__full_name", "status"]
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Bu metod faqat autentifikatsiya qilingan foydalanuvchiga tegishli orderlarni qaytaradi.
        """
        user = self.request.user
        return Order.objects.filter(user=user.profile).order_by("-pk").prefetch_related(
            Prefetch("orderitem", queryset=OrderItem.objects.select_related("product").prefetch_related("product__phone", "product__ticket", "product__good","product__image")),
        )


class OrderRetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemCreateAPIView(CreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        """
        Bu metod serializerga qo'shimcha kontekstni o'tkazish uchun ishlatiladi.
        """
        context = super(OrderItemCreateAPIView, self).get_serializer_context()
        context["request"] = self.request
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Multi-language success message for product addition
        success_message = {
            "en": _("The product has been successfully added to the cart"),
            "uz": _("Maxsulot savatga muvafaqqiyatli qo'shildi"),
            "ru": _("Товар успешно добавлен в корзину"),
            "kr": _("제품이 장바구니에 성공적으로 추가되었습니다"),
        }

        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": success_message, "order_item": serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class OrderItemListAPIView(ListAPIView):
    queryset = OrderItem.objects.all().order_by("-pk")
    serializer_class = OrderItemSerializer
    # pagination_class = CustomPageNumberPagination


class OrderItemRetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        order = instance.order
        self.perform_destroy(instance)
        order.update_total_amount()  # Update the order's total amount after deleting the item

        # Multi-language success message for product removal
        success_message = {
            "en": _("The product has been removed from the cart"),
            "uz": _("Maxsulot savatdan o'chirib tashlandi"),
            "ru": _("Товар удален из корзины"),
            "kr": _("제품이 장바구니에서 제거되었습니다"),
        }

        return Response({"message": success_message}, status=status.HTTP_204_NO_CONTENT)


class InformationListAPIView(ListAPIView):
    queryset = Information.objects.all().order_by("-pk")
    serializer_class = InformationSerializer


class CheckoutView(APIView):
    def post(self, request, order_id, *args, **kwargs):
        with transaction.atomic():
            try:
                # Check the original Order
                original_order = Order.objects.get(
                    id=order_id, user=request.user.profile
                )

                if original_order.status in ["approved", "sent", "cancelled"]:
                    new_order = Order.objects.create(
                        user=request.user.profile, status="pending"
                    )
                    for item in original_order.orderitem_set.all():
                        OrderItem.objects.create(
                            order=new_order,
                            product=item.product,
                            quantity=item.quantity,
                        )
                    order = new_order
                else:
                    order = original_order

                update_data = request.data.copy()
                update_data["status"] = "pending"

                serializer = OrderStatusUpdateSerializer(order, data=update_data)
                if serializer.is_valid():
                    serializer.save()
                    # Logic for sending message to a bot
                    bot(order)

                    # Multi-language success message for order creation
                    success_message = {
                        "en": _("Order created successfully"),
                        "uz": _("Buyurtma muvafaqqiyatli yaratildi"),
                        "ru": _("Заказ успешно создан"),
                        "kr": _("주문이 성공적으로 생성되었습니다"),
                    }

                    return Response(
                        {
                            "status": "success",
                            "order_id": order.id,
                            "message": success_message,
                        }
                    )
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Order.DoesNotExist:
                return Response(
                    {"status": "error", "message": "Order not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )


class ServiceListAPIView(ListAPIView):
    queryset = Service.objects.all().order_by("-pk")
    serializer_class = ServiceSerializer


class SocialMeadiaAPIView(ListAPIView):
    queryset = SocialMedia.objects.all().order_by("-pk")
    serializer_class = SocialMediaSerializer


class BonusPIView(ListAPIView):
    queryset = Bonus.objects.all().order_by("pk")
    serializer_class = BonusSerializer
