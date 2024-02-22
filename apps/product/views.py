from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.conf import settings
from rest_framework.generics import ListAPIView
from rest_framework import views, status
from django.db.models import Sum, Count
from rest_framework.response import Response
from django.db.models import F
from django.db.models import Q
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
    GoodPopularSerializer,
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
    filterset_fields = [
        "product",
    ]
    pagination_class = CustomPageNumberPagination


class PhoneListAPIView(ListAPIView):
    queryset = Phone.objects.all().order_by("-pk")
    serializer_class = PhoneSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["category", "product"]

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
    filterset_fields = [
        "product",
    ]
    pagination_class = CustomPageNumberPagination


class PopularTicketsAPIView(ListAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketPopularSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return Ticket.objects.annotate(
            sold_count=Sum("product__sold_products__quantity")
        ).order_by("-sold_count")


class PopularPhonesAPIView(ListAPIView):
    queryset = Phone.objects.all()
    serializer_class = PhonePopularSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return Phone.objects.annotate(
            sold_count=Sum("product__sold_products__quantity")
        ).order_by("-sold_count")


class PopularGoodAPIView(ListAPIView):
    queryset = Good.objects.all()
    serializer_class = GoodPopularSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return Good.objects.annotate(
            sold_count=Sum("product__sold_products__quantity")
        ).order_by("-sold_count")


class NewTicketsListView(ListAPIView):
    queryset = Ticket.objects.all().order_by("product__created")
    serializer_class = TicketSerializer
    pagination_class = CustomPageNumberPagination


class NewPhonesListView(ListAPIView):
    queryset = Phone.objects.all().order_by("product__created")
    serializer_class = PhoneSerializer
    pagination_class = CustomPageNumberPagination


class NewGoodsListView(ListAPIView):
    queryset = Good.objects.all().order_by("product__created")
    serializer_class = GoodSerializer
    pagination_class = CustomPageNumberPagination


class TicketsOnSaleListView(ListAPIView):
    serializer_class = TicketSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):

        queryset = Ticket.objects.filter(product__new_price__lt=F("product__old_price"))
        return queryset


class PhonesOnSaleListView(ListAPIView):
    serializer_class = PhoneSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = Phone.objects.filter(product__new_price__lt=F("product__old_price"))
        return queryset


class GoodsOnSaleListView(ListAPIView):
    serializer_class = GoodSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = Good.objects.filter(product__new_price__lt=F("product__old_price"))
        return queryset


class MultiProductSearchView(views.APIView):
    def get(self, request):
        search_query = request.query_params.get("search", None)
        if not search_query:
            return Response(
                {"message": "No search query provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        def build_query_for_model(model, field_name):
            query = Q()
            modeltranslation_languages = settings.MODELTRANSLATION_LANGUAGES
            for lang in modeltranslation_languages:
                query |= Q(**{f"{field_name}_{lang}__icontains": search_query})
            return query

        context = {"request": request}
        results = {
            "tickets": TicketSerializer(
                Ticket.objects.filter(build_query_for_model(Ticket, "event_name")),
                many=True,
                context=context,
            ).data,
            "phones": PhoneSerializer(
                Phone.objects.filter(build_query_for_model(Phone, "model_name")),
                many=True,
                context=context,
            ).data,
            "goods": GoodSerializer(
                Good.objects.filter(build_query_for_model(Good, "name")),
                many=True,
                context=context,
            ).data,
        }

        return Response(results)
