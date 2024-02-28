from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status, permissions
from django.db import IntegrityError
from twilio.rest import Client
from django.conf import settings
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .utils import generate_otp, user_lang
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
    VerifyOTPSerializer,
    SetPasswordSerializer,
)


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            profile = serializer.validated_data["profile"]
            token, created = Token.objects.get_or_create(user=user)

            profile_serializer = ProfileSerializer(profile)

            return Response(
                {"token": token.key, "profile": profile_serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.


class ProfileCreateAPIView(CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileRetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        language = request.data.get('lang', None)
        user_id = instance.id
        user_lang(language, user_id)

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)


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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        except IntegrityError:
            return Response(
                {"message": "This favorite item already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RemoveFromFavoritesView(APIView):
    def post(self, request, product_id, *args, **kwargs):
        user = request.user

        try:
            favorite = Favorite.objects.get(user=user.profile, product_id=product_id)
            favorite.delete()
            return Response({"status": "success"}, status=status.HTTP_204_NO_CONTENT)
        except Favorite.DoesNotExist:
            return Response(
                {"error": "Item not found in favorites"},
                status=status.HTTP_404_NOT_FOUND,
            )


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
        try:
            otp = generate_otp()
            send_otp_sms(phone_number, otp)
        except Exception as e:
            return Response(
            {
                "message": "OTP yuborishda xatolik yuz berdi."
            },
            status=status.HTTP_408_REQUEST_TIMEOUT,
        )
        user, _ = User.objects.get_or_create(username=phone_number)
        profile, _ = Profile.objects.update_or_create(
            origin=user,
            defaults={"phone_number": phone_number, "full_name": full_name, "otp": otp},
        )

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
        pass


class VerifyRegisterOTPView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data["phone_number"]
        otp = serializer.validated_data["otp"]

        profile = Profile.objects.get(phone_number=phone_number)
        profile.otp = None
        profile.save()

        # Multi-language success message for account activation
        success_message = {
            "en": _("Account activated successfully"),
            "uz": _("Akkount muvafaqqiyatli faollashtirildi"),
            "ru": _("Аккаунт успешно активирован"),
            "kr": _("계정이 성공적으로 활성화되었습니다"),
        }

        return Response(
            {"message": success_message},
            status=status.HTTP_200_OK,
        )


class SetPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data["phone_number"]
        new_password = serializer.validated_data["new_password"]

        try:
            user = User.objects.get(username=phone_number)
            user.set_password(new_password)
            user.save()

            # Foydalanuvchiga token yaratish yoki topish
            token, created = Token.objects.get_or_create(user=user)

            return Response(
                {"token": token.key, "message": "Password set successfully"},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )


class BannerListAPIView(ListAPIView):
    queryset = Banner.objects.all().order_by("-pk")
    serializer_class = BannerSerializer
    pagination_class = CustomPageNumberPagination


class ProfileEditAPIView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Foydalanuvchining profili olindi, agar yo'q bo'lsa, 404 xato qaytariladi
        profile = Profile.objects.get(origin=self.request.user)
        return profile
