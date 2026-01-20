import random
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveUpdateAPIView,
)
# = shu qimni man qoshidim 
# ADDED FOR SWAGGER
# ===============================
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# ===============================
# ADDED FOR SWAGGER
# ===============================
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status, permissions
from django.db import IntegrityError, transaction
from rest_framework_simplejwt.tokens import RefreshToken
from twilio.rest import Client
from django.conf import settings
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .utils import generate_otp
from .models import Favorite, Location, News, Profile, ViewedNews, Banner
from django.contrib.auth import get_user_model
User = get_user_model()

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
    SetPasswordSerializer
)
from ..merchant.models import Referral
User = get_user_model()
class LoginView(APIView):

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="JWT token",
                examples={
                    "application/json": {
                        "refresh": "string",
                        "access": "string",
                        "full_name": "Test User",
                        "message": "Muvaffaqiyatli kirdingiz"
                    }
                }
            )
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'full_name': serializer.validated_data['profile'].full_name,
                'message': "Muvaffaqiyatli kirdingiz"
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.


class ProfileCreateAPIView(CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer



class ProfileUpdate(APIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        user = self.request.user
        try:
            profile = user.profile

        except:
            profile = None
            return Response({"error": "Profile not found"}, status=status.HTTP_400_B)
        serializer = self.serializer_class(profile, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProfileDelete(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.delete()
        return Response(
            {"message": "User has been successfully deleted"},
            status=status.HTTP_200_OK,
        )


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
    # filterset_fields = ["user", "product"]
    search_fields = ["product__name", "user__full_name"]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Favorite.objects.none()
        # qs = (
        #     Favorite.objects.filter(user=self.request.user.profile)
        #     .select_related("product", "user")
        #     .order_by("-pk")
        # )
        qs = (
            Favorite.objects.all()
            .order_by("-pk")
            .select_related("product__tickets", "product__goods", "product__phones")
            .prefetch_related("product__images")
        )
        return qs


class FavoriteRetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


from django.db import transaction
from django.db.models import F

from drf_yasg.utils import swagger_auto_schema

class RegisterView(APIView):
    @swagger_auto_schema(
    request_body=RegisterSerializer,
    responses={
        200: "OTP sent",
        400: "Bad request"
    }
)
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data["phone_number"]
        full_name = serializer.validated_data.get("full_name", "")
        referral_code = serializer.validated_data.get("referral_code")

        otp_code = str(random.randint(1000, 9999))

        with transaction.atomic():
            user, _ = User.objects.get_or_create(username=phone_number)
            profile, profile_created = Profile.objects.get_or_create(
                origin=user,
                defaults={
                    "full_name": full_name,
                    "phone_number": phone_number,
                    "otp": otp_code
                }
            )

            if not profile_created:
                profile.otp = otp_code
                profile.save()

            # Логика реферала
            if profile_created and referral_code:
                try:
                    referrer = Profile.objects.get(referral_code=referral_code)
                    if referrer != profile:
                        # ВАЖНО: Ставим сразу статус 'rewarded'
                        Referral.objects.create(
                            referrer=referrer,
                            referee=profile,
                            status='rewarded' # Теперь бонус начислится сам через метод save()
                        )
                except Profile.DoesNotExist:
                    pass

        send_otp_sms(phone_number, otp_code)

        return Response({
            "message": "OTP code sent to your phone",
            "referral_code": profile.referral_code,
            "otp_debug": otp_code
        })


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



# ===== VIEW =====
class SetPasswordView(APIView):

    @swagger_auto_schema(
        request_body=SetPasswordSerializer,
        responses={
            200: "Password set successfully",
            400: "Bad request"
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = SetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data["phone_number"]
        new_password = serializer.validated_data["new_password"]

        try:
            user = User.objects.get(username=phone_number)
            user.set_password(new_password)
            user.save()

            token, _ = Token.objects.get_or_create(user=user)

            return Response(
                {
                    "token": token.key,
                    "message": "Password set successfully"
                },
                status=status.HTTP_200_OK
            )

        except User.DoesNotExist:
            return Response(
                {"message": "User not found"},
                status=status.HTTP_404_NOT_FOUND
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


class LatestUnviewedNewsView(APIView):
    def get(self, request, *args, **kwargs):
        latest_news = News.get_latest_unviewed_news(request.user.profile)
        if latest_news:
            serializer = NewsSerializer(latest_news)
            return Response(serializer.data)
        return Response(
            {"message": "Barcha yangiliklar ko'rilgan"},
            status=status.HTTP_404_NOT_FOUND,
        )


class MarkNewsAsViewed(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ViewedNewsSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Yangilik o'qildi sifatida belgilandi"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

