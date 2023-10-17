from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .models import Profile, Location, News, ViewedNews, Favorite


from .serializers import (
    ProfileSerializer,
    LocationSerializer,
    CustomPageNumberPagination,
    NewsSerializer,
    ViewedNewsSerializer,
    FavoriteSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

# Create your views here.


class ProfileCreateAPIView(CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileListAPIView(ListAPIView):
    queryset = Profile.objects.all().order_by("-pk")
    serializer_class = ProfileSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]  # Add both filter backends
    search_fields = ["full_name", "phone_number"]
    pagination_class = CustomPageNumberPagination


class ProfileRetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class LocationCreateAPIView(CreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class LocationListAPIView(ListAPIView):
    queryset = Location.objects.all().order_by("-pk")
    serializer_class = LocationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]  # Add both filter backends
    search_fields = ["user__full_name", "address"]
    pagination_class = CustomPageNumberPagination


class LocationRetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class NewsCreateAPIView(CreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class NewsListAPIView(ListAPIView):
    queryset = News.objects.all().order_by("-pk")
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]  # Add both filter backends
    search_fields = ["description"]
    pagination_class = CustomPageNumberPagination


class NewsRetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class ViewedNewsCreateAPIView(CreateAPIView):
    queryset = ViewedNews.objects.all()
    serializer_class = ViewedNewsSerializer


class ViewedNewsListAPIView(ListAPIView):
    queryset = ViewedNews.objects.all().order_by("-pk")
    serializer_class = ViewedNewsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]  # Add both filter backends
    search_fields = ["user__ful_name"]
    pagination_class = CustomPageNumberPagination


class ViewedNewsRetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = ViewedNews.objects.all()
    serializer_class = ViewedNewsSerializer


class FavoriteCreateAPIView(CreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class FavoriteListAPIView(ListAPIView):
    queryset = Favorite.objects.all().order_by("-pk")
    serializer_class = FavoriteSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]  # Add both filter backends
    search_fields = ["product__name", "product__category__name", "user__full_name"]
    pagination_class = CustomPageNumberPagination


class FavoriteRetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
