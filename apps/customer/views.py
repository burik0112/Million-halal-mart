from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveUpdateDestroyAPIView)

from .models import Favorite, Location, News, Profile, ViewedNews
from .serializers import (CustomPageNumberPagination, FavoriteSerializer,
                          LocationSerializer, NewsSerializer,
                          ProfileSerializer, ViewedNewsSerializer)

# Create your views here.


class ProfileCreateAPIView(CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


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


class NewsListAPIView(ListAPIView):
    queryset = News.objects.all().order_by("-pk")
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]  # Add both filter backends
    search_fields = ["description"]
    pagination_class = CustomPageNumberPagination


class ViewedNewsCreateAPIView(CreateAPIView):
    queryset = ViewedNews.objects.all()
    serializer_class = ViewedNewsSerializer


class FavoriteCreateAPIView(CreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class FavoriteListAPIView(ListAPIView):
    queryset = Favorite.objects.all().order_by("-pk")
    serializer_class = FavoriteSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]  # Add both filter backends
    filter_fields = ["product__category"]
    search_fields = ["product__name", "user__full_name"]
    pagination_class = CustomPageNumberPagination


class FavoriteRetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
