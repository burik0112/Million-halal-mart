from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from .models import Order, OrderItem, Information, Service, SecialMedia
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
    queryset = Order.objects.all().order_by("-pk")
    serializer_class = OrderListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["user__full_name"]
    filterset_fields = ["user__full_name", "status"]
    pagination_class = CustomPageNumberPagination


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


class OrderItemListAPIView(ListAPIView):
    queryset = OrderItem.objects.all().order_by("-pk")
    serializer_class = OrderItemSerializer
    pagination_class = CustomPageNumberPagination


class OrderItemRetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class InformationListAPIView(ListAPIView):
    queryset = Information.objects.all().order_by("-pk")
    serializer_class = InformationSerializer


class CheckoutView(APIView):
    def post(self, request, order_id, *args, **kwargs):
        try:
            order = Order.objects.get(
                id=order_id, status="in_cart", user=request.user.profile
            )

            # Mijoz tomonidan yuborilgan ma'lumotlarni qabul qilish
            update_data = request.data.copy()
            # Statusni 'pending'ga o'zgartirish
            update_data["status"] = "pending"

            serializer = OrderStatusUpdateSerializer(order, data=update_data)
            if serializer.is_valid():
                serializer.save()
                # Botga xabar yuborish logikasi
                bot(order)
                return Response({"status": "success", "order_id": order.id})
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
    queryset = SecialMedia.objects.all().order_by("-pk")
    serializer_class = SocialMediaSerializer
