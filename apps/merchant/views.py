from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Order, OrderItem, Information
from .serializers import (
    CustomPageNumberPagination,
    OrderItemSerializer,
    OrderSerializer,
    InformationSerializer,
    OrderStatusUpdateSerializer,
)

# Create your views here.


class OrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderListAPIView(ListAPIView):
    queryset = Order.objects.all().order_by("-pk")
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["user__full_name"]
    filterset_fields = ["user__full_name"]
    pagination_class = CustomPageNumberPagination


class OrderRetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemCreateAPIView(CreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


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

from apps.dashboard.main import bot

class CheckoutView(APIView):
    def post(self, request, order_id, *args, **kwargs):
        try:
            order = Order.objects.get(id=order_id, status="in_cart", user=request.user)
            serializer = OrderStatusUpdateSerializer(order, data={"status": "pending"})
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
