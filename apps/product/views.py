from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView

from .models import Category, Good, Image, Phone, SubCategory, Ticket
from .serializers import (
    CategorySerializer,
    CustomPageNumberPagination,
    GoodSerializer,
    ImageSerializer,
    PhoneSerializer,
    SubCategorySerializer,
    TicketSerializer,
)

# Create your views here.


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all().order_by("-pk")
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]  # Add both filter backends
    search_fields = ["name", "main_type"]
    filterset_fields = ["name", "main_type"]
    pagination_class = CustomPageNumberPagination


class SubCategoryListAPIView(ListAPIView):
    queryset = SubCategory.objects.all().order_by("-pk")
    serializer_class = SubCategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]  # Add both filter backends
    filterset_fields = ["category"]
    pagination_class = CustomPageNumberPagination


class TicketListAPIView(ListAPIView):
    queryset = Ticket.objects.all().order_by("-pk")
    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]  # Add both filter backends
    filterset_fields = ["product",]
    pagination_class = CustomPageNumberPagination


class PhoneListAPIView(ListAPIView):
    queryset = Phone.objects.all().order_by("-pk")
    serializer_class = PhoneSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]  # Add both filter backends
    filterset_fields = [
        "category",
        "product"
    ]

    pagination_class = CustomPageNumberPagination


class GoodListAPIView(ListAPIView):
    queryset = Good.objects.all().order_by("-pk")
    serializer_class = GoodSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]  # Add both filter backends
    filterset_fields = [
        "sub_cat",
        "product",
    ]
    pagination_class = CustomPageNumberPagination


class ImageListAPIView(ListAPIView):
    queryset = Image.objects.all().order_by("-pk")
    serializer_class = ImageSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]  # Add both filter backends
    filterset_fields = ["product"]
    pagination_class = CustomPageNumberPagination
