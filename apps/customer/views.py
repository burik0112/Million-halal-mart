from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status, permissions
from twilio.rest import Client
from django.conf import settings
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .utils import generate_otp
from .models import Favorite, Location, News, Profile, ViewedNews, Banner
from django.contrib.auth.models import User
from .serializers import (
    CustomPageNumberPagination,
    FavoriteSerializer,
    LocationSerializer,
    NewsSerializer,
    ProfileSerializer,
    ViewedNewsSerializer,
    FavoriteListSerializer,
    BannerSerializer,
    LocationListSerializer,
    LoginSerializer,
    RegisterSerializer,
)


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.profile)


class LocationListAPIView(ListAPIView):
    queryset = Location.objects.all().order_by("-pk")
    serializer_class = LocationListSerializer
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


class NewsRetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class ViewedNewsCreateAPIView(CreateAPIView):
    queryset = ViewedNews.objects.all()
    serializer_class = ViewedNewsSerializer


class FavoriteCreateAPIView(CreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.profile)


class FavoriteListAPIView(ListAPIView):
    permission_class = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Favorite.objects.all().order_by("-pk")
    serializer_class = FavoriteListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["user", "product"]
    search_fields = ["product__name", "user__full_name"]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Favorite.objects.none()

        return (
            Favorite.objects.filter(user=self.request.user.profile)
            .select_related("product", "user")
            .order_by("-pk")
        )


class FavoriteRetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data["phone_number"]
        full_name = serializer.validated_data.get("full_name", "")
        otp = generate_otp()

        user, _ = User.objects.get_or_create(username=phone_number)
        profile, _ = Profile.objects.update_or_create(
            origin=user,
            defaults={"phone_number": phone_number, "full_name": full_name, "otp": otp},
        )

        # SMS yuborishni alohida funksiyaga o'tkazish
        send_otp_sms(phone_number, otp)

        return Response(
            {
                "message": "OTP sent successfully. Please verify to complete registration."
            },
            status=status.HTTP_200_OK,
        )


def send_otp_sms(phone_number, otp):
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=f"Your OTP code is {otp}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number,
        )
    except Exception as e:
        # Xatoliklarni qayd etish va boshqarish
        # Masalan, log qilish yoki xabar yuborishda xatolik haqida xabar berish
        pass


class VerifyRegisterOTPView(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get("phone_number")
        otp = request.data.get("otp")

        try:
            profile = Profile.objects.get(phone_number=phone_number)
            if profile.otp == otp:
                # OTPni tozalash
                profile.otp = None
                profile.save()

                # Token yaratish va qaytarish
                token, created = Token.objects.get_or_create(user=profile.origin)
                return Response({"token": token.key, "message": "Registration successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            return Response({"message": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

class BannerListAPIView(ListAPIView):
    queryset = Banner.objects.all().order_by("-pk")
    serializer_class = BannerSerializer
    pagination_class = CustomPageNumberPagination
