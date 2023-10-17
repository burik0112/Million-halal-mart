from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .models import Category, SubCategory, ProductItem, Ticket, Phone, Good, Image

from .serializers import (
    CategorySerializer,
    SubCategorySerializer,
    CustomPageNumberPagination,
    ProductItemSerializer,
    TicketSerializer,
    PhoneSerializer,
    GoodSerializer,
    ImageSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

# Create your views here.


class CategoryCreateAPIView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all().order_by("-pk")
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]  # Add both filter backends
    search_fields = ["name"]
    pagination_class = CustomPageNumberPagination


class CategoryRetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryCreateAPIView(CreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class SubCategoryListAPIView(ListAPIView):
    queryset = SubCategory.objects.all().order_by("-pk")
    serializer_class = SubCategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]  # Add both filter backends
    search_fields = ["name", "category__name"]
    pagination_class = CustomPageNumberPagination


class SubCategoryRetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class TicketCreateAPIView(CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class TicketListAPIView(ListAPIView):
    queryset = Ticket.objects.all().order_by("-pk")
    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]  # Add both filter backends
    search_fields = ["product__name", "product__category__name", "event_name"]
    pagination_class = CustomPageNumberPagination


class TicketRetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class PhoneCreateAPIView(CreateAPIView):
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer


class PhoneListAPIView(ListAPIView):
    queryset = Phone.objects.all().order_by("-pk")
    serializer_class = PhoneSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]  # Add both filter backends
    search_fields = [
        "product__name",
        "product__category__name",
        "brand_name",
        "model_name",
    ]
    pagination_class = CustomPageNumberPagination


class PhoneRetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer


class GoodCreateAPIView(CreateAPIView):
    queryset = Good.objects.all()
    serializer_class = GoodSerializer


class GoodListAPIView(ListAPIView):
    queryset = Good.objects.all().order_by("-pk")
    serializer_class = GoodSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]  # Add both filter backends
    search_fields = ["product__name", "product__category__name", "name", "ingredients"]
    pagination_class = CustomPageNumberPagination


class GoodRetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Good.objects.all()
    serializer_class = GoodSerializer


class ImageCreateAPIView(CreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class ImageListAPIView(ListAPIView):
    queryset = Image.objects.all().order_by("-pk")
    serializer_class = ImageSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]  # Add both filter backends
    search_fields = ["product__name", "product__category__name", "name"]
    pagination_class = CustomPageNumberPagination


class ImageRetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
