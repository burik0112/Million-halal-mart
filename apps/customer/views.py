from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework import generics
from twilio.rest import Client
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .utils import generate_otp
from .models import Favorite, Location, News, Profile, ViewedNews
from .serializers import (
    CustomPageNumberPagination,
    FavoriteSerializer,
    LocationSerializer,
    NewsSerializer,
    ProfileSerializer,
    ViewedNewsSerializer,
    FavoriteListSerializer
)

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
    filterset_fields = ["user__full_name", "address"]
    pagination_class = CustomPageNumberPagination


class LocationRetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class NewsListAPIView(ListAPIView):
    queryset = News.objects.all().order_by("-pk")
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]  # Add both filter backends
    search_fields = ["description"]
    filterset_fields = ["description"]
    pagination_class = CustomPageNumberPagination


class ViewedNewsCreateAPIView(CreateAPIView):
    queryset = ViewedNews.objects.all()
    serializer_class = ViewedNewsSerializer


class FavoriteCreateAPIView(CreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class FavoriteListAPIView(ListAPIView):
    queryset = Favorite.objects.all().order_by("-pk")
    serializer_class = FavoriteListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]  
    filterset_fields = ["user", "product"]
    search_fields = ["product__name", "user__full_name"]
    pagination_class = CustomPageNumberPagination
    
    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).order_by("-pk")


class FavoriteRetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer




class SendOTPView(generics.GenericAPIView):
    serializer_class = ProfileSerializer  

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        otp = generate_otp()

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"Your OTP code is {otp}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )

        # OTPni bazaga saqlash
        profile = Profile.objects.get(phone_number=phone_number)
        profile.otp = otp
        profile.save()

        return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)

class VerifyOTPView(generics.GenericAPIView):
    serializer_class = ProfileSerializer  

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')

        # OTPni bazadan tekshirish
        profile = Profile.objects.get(phone_number=phone_number)
        if profile.otp == otp:
            return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

