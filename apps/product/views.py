from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from django.db.models import Sum, Count
from rest_framework.response import Response

from .models import Category, Good, Image, Phone, SubCategory, Ticket
from .serializers import (
    CategorySerializer,
    CustomPageNumberPagination,
    GoodSerializer,
    ImageSerializer,
    PhoneSerializer,
    SubCategorySerializer,
    TicketSerializer,
    TicketPopularSerializer,
    PhonePopularSerializer,
    GoodPopularSerializer
)

# Create your views here.


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all().order_by("-pk")
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]  
    search_fields = ["name", "main_type"]
    filterset_fields = ["name", "main_type"]
    pagination_class = CustomPageNumberPagination


class SubCategoryListAPIView(ListAPIView):
    queryset = SubCategory.objects.all().order_by("-pk")
    serializer_class = SubCategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]  
    filterset_fields = ["category"]
    pagination_class = CustomPageNumberPagination


class TicketListAPIView(ListAPIView):
    queryset = Ticket.objects.all().order_by("-pk")
    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]  
    filterset_fields = ["product",]
    pagination_class = CustomPageNumberPagination


class PhoneListAPIView(ListAPIView):
    queryset = Phone.objects.all().order_by("-pk")
    serializer_class = PhoneSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]  
    filterset_fields = [
        "category",
        "product"
    ]

    pagination_class = CustomPageNumberPagination


class GoodListAPIView(ListAPIView):
    queryset = Good.objects.all().order_by("-pk")
    serializer_class = GoodSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]  
    filterset_fields = [
        "sub_cat",
        "product",
    ]
    pagination_class = CustomPageNumberPagination


class ImageListAPIView(ListAPIView):
    queryset = Image.objects.all().order_by("-pk")
    serializer_class = ImageSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]  
    filterset_fields = ["product"]
    pagination_class = CustomPageNumberPagination

class FamousTickets(ListAPIView):
    queryset = Ticket.objects.all().order_by("-pk")
    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]  
    filterset_fields = ["product",]
    pagination_class = CustomPageNumberPagination

class PopularTicketsAPIView(ListAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketPopularSerializer
    pagination_class = CustomPageNumberPagination
    

    def get_queryset(self):
       
        return Ticket.objects.annotate(
            sold_count=Sum('product__sold_products__quantity')
        ).order_by('-sold_count')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class PopularPhonesAPIView(ListAPIView):
    queryset = Phone.objects.all()
    serializer_class = PhonePopularSerializer
    pagination_class = CustomPageNumberPagination
    

    def get_queryset(self):
       
        return Phone.objects.annotate(
            sold_count=Sum('product__sold_products__quantity')
        ).order_by('-sold_count')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
class PopularGoodAPIView(ListAPIView):
    queryset = Good.objects.all()
    serializer_class = GoodPopularSerializer
    pagination_class = CustomPageNumberPagination
    

    def get_queryset(self):
       
        return Good.objects.annotate(
            sold_count=Sum('product__sold_products__quantity')
        ).order_by('-sold_count')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
