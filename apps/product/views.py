import re
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.conf import settings
from rest_framework.generics import ListAPIView
from rest_framework import views, status
from rest_framework.response import Response
from django.db.models import Q, Exists, OuterRef, F, Sum, Value, BooleanField

from django.db.models import Prefetch
from apps.customer.models import Favorite
from .models import Category, Good, Image, Phone, SubCategory, Ticket, ProductItem
from .serializers import (
    CategorySerializer,
    CustomPageNumberPagination,
    GoodSerializer,
    GoodVariantSerializer,
    ImageSerializer,
    PhoneSerializer,
    PhoneVariantSerializer,
    SubCategorySerializer,
    TicketSerializer,
    TicketPopularSerializer,
    PhonePopularSerializer,
    GoodPopularSerializer,
    TicketVariantSerializer,
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
        "product__product_type",
    ]
    pagination_class = CustomPageNumberPagination


class PhoneListAPIView(ListAPIView):
    queryset = (
        Phone.objects.all()
        .order_by("-pk")
        .select_related("product")
        .prefetch_related("product__images")
    )
    serializer_class = PhoneSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["category", "product", "product__product_type"]

    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return (
                Phone.objects.all()
                .order_by("-pk")
                .select_related("product")
                .prefetch_related("product__images")
                .annotate(is_favorite=Value(False, output_field=BooleanField()))
            )
        else:
            favorites_subquery = Favorite.objects.filter(
                user=user.profile, product_id=OuterRef("product_id")
            )
            return (
                Phone.objects.all()
                .order_by("-pk")
                .select_related("product")
                .prefetch_related("product__images")
                .annotate(is_favorite=Exists(favorites_subquery))
            )


class GoodListAPIView(ListAPIView):
    queryset = (
        Good.objects.select_related("product")
        .prefetch_related("product__images")
        .all()
        .order_by("-pk")
    )
    serializer_class = GoodSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = [
        "sub_cat",
        "product",
        "product__product_type",
    ]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return (
                Good.objects.all()
                .order_by("-pk")
                .select_related("product")
                .prefetch_related("product__images")
                .annotate(is_favorite=Value(False, output_field=BooleanField()))
            )
        else:
            favorites_subquery = Favorite.objects.filter(
                user=user.profile, product_id=OuterRef("product_id")
            )
            return (
                Good.objects.all()
                .order_by("-pk")
                .select_related("product")
                .prefetch_related("product__images")
                .annotate(is_favorite=Exists(favorites_subquery))
            )


class GoodVariantsAPIView(views.APIView):
    def get(self, request, product_type):
        # Good obyektlarini olish
        goods = (
            Good.objects.filter(product__product_type=product_type)
            .select_related("product")
            .prefetch_related("product__images")
        )

        # Agar mahsulotlar topilmasa, 404 xatosini qaytarish
        if not goods.exists():
            return Response(
                {"detail": "No goods found with this product_type."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Serializer yordamida ma'lumotlarni formatlash
        serializer = GoodVariantSerializer(
            goods, many=True, context={"request": request}
        )

        return Response(serializer.data)

class TicketVariantsAPIView(views.APIView):
    def get(self, request, product_type):
        tickets = (
            Ticket.objects.filter(product__product_type=product_type)
            .select_related("product")
            .prefetch_related("product__images")
        )

        if not tickets.exists():
            return Response(
                {"detail": "No tickets found with this product_type."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TicketVariantSerializer(
            tickets, many=True, context={"request": request}
        )

        return Response(serializer.data)

class PhoneVariantsAPIView(views.APIView):
    def get(self, request, product_type):
        phones = (
            Phone.objects.filter(product__product_type=product_type)
            .select_related("product")
            .prefetch_related("product__images")
        )

        if not phones.exists():
            return Response(
                {"detail": "No phones found with this product_type."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PhoneVariantSerializer(
            phones, many=True, context={"request": request}
        )

        return Response(serializer.data)

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
        return (
            Ticket.objects.select_related("product")
            .prefetch_related("product__images")
            .annotate(sold_count=Sum("product__sold_products__quantity"))
            .order_by("-sold_count")
        )


class PopularPhonesAPIView(ListAPIView):
    queryset = Phone.objects.all()
    serializer_class = PhonePopularSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return (
            Phone.objects.select_related("product")
            .prefetch_related("product__images")
            .annotate(sold_count=Sum("product__sold_products__quantity"))
            .order_by("-sold_count")
        )


class PopularGoodAPIView(ListAPIView):
    queryset = Good.objects.all()
    serializer_class = GoodPopularSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):

        user = self.request.user
        sold_count_subquery = Sum("product__sold_products__quantity")
        if user.is_anonymous:
            return (
                Good.objects.select_related("product")
                .prefetch_related("product__images")
                .annotate(sold_count=sold_count_subquery)
                .annotate(is_favorite=Value(False, output_field=BooleanField()))
                .order_by("-sold_count")
            )

        else:
            favorites_subquery = Favorite.objects.filter(
                user=user.profile, product_id=OuterRef("product_id")
            )
            return (
                Good.objects.all()
                .order_by("-pk")
                .select_related("product")
                .prefetch_related("product__images")
                .annotate(is_favorite=Exists(favorites_subquery))
            )


class NewTicketsListView(ListAPIView):
    queryset = Ticket.objects.all().order_by("product__created")
    serializer_class = TicketSerializer
    pagination_class = CustomPageNumberPagination


class NewPhonesListView(ListAPIView):
    queryset = Phone.objects.all().order_by("product__created")
    serializer_class = PhoneSerializer
    pagination_class = CustomPageNumberPagination


class NewGoodsListView(ListAPIView):
    queryset = (
        Good.objects.all()
        .select_related("product")
        .prefetch_related("product__images")
        .order_by("product__created")
    )
    serializer_class = GoodSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return (
                Good.objects.all()
                .select_related("product")
                .prefetch_related("product__images")
                .order_by("product__created")
                .annotate(is_favorite=Value(False, output_field=BooleanField()))
            )
        else:
            favorites_subquery = Favorite.objects.filter(
                user=user.profile, product_id=OuterRef("product_id")
            )
            return (
                Good.objects.all()
                .select_related("product")
                .prefetch_related("product__images")
                .order_by("product__created")
                .annotate(is_favorite=Exists(favorites_subquery))
            )


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
        user = self.request.user
        if self.request.user.is_anonymous:
            return (
                Good.objects.filter(product__new_price__lt=F("product__old_price"))
                .select_related("product")
                .prefetch_related("product__images")
                .annotate(is_favorite=Value(False, output_field=BooleanField()))
            )
        favorites_subquery = Favorite.objects.filter(
            user=user.profile, product_id=OuterRef("product_id")
        )
        queryset = (
            Good.objects.filter(product__new_price__lt=F("product__old_price"))
            .select_related("product")
            .prefetch_related("product__images")
            .annotate(is_favorite=Exists(favorites_subquery))
        )
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
