from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from django.shortcuts import render, redirect, HttpResponse
from .models import Order, OrderItem
from .serializers import (
    CustomPageNumberPagination,
    OrderItemSerializer,
    OrderSerializer,
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


def test(request):
    return render(request, "/index.html")
