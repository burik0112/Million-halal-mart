from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from apps.product.models import ProductItem, Good, Phone, Ticket, Image
from .models import Favorite, Location, News, Profile, ViewedNews, Banner


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=17)
    password = serializers.CharField()

    def validate(self, data):
        phone_number = data.get("phone_number")
        password = data.get("password")

        if phone_number and password:
            try:
                profile = Profile.objects.get(phone_number=phone_number)
                user = profile.origin
                if user.check_password(password):
                    data["user"] = user
                    return data
            except Profile.DoesNotExist:
                pass
        raise serializers.ValidationError("Invalid phone number or password")


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "full_name",
            "phone_number",
        ]


class RegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=17)
    full_name = serializers.CharField(max_length=255, required=False, allow_blank=True)

    def validate_phone_number(self, value):
        # Telefon raqamini validatsiya qilish
        # Masalan, formatni tekshirish yoki raqamning mavjudligini tekshirish
        return value


class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=17)
    otp = serializers.CharField(max_length=100)

    def validate(self, data):
        phone_number = data.get("phone_number")
        otp = data.get("otp")

        try:
            profile = Profile.objects.get(phone_number=phone_number)
            if profile.otp != otp:
                raise serializers.ValidationError("Invalid OTP")
        except Profile.DoesNotExist:
            raise serializers.ValidationError("Profile not found")

        return data


class SetPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=17)
    new_password = serializers.CharField(style={"input_type": "password"})

    def validate_new_password(self, value):
        # Bu yerda parolni validatsiya qilish qoidalari qo'shilishi mumkin
        return value


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Location
        fields = "__all__"


class LocationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = "__all__"


class ViewedNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewedNews
        fields = "__all__"


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Favorite
        fields = "__all__"


class TicketForFavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"


class PhoneFavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = "__all__"


class GoodFavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Good
        fields = "__all__"


class ImageForProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["image", "name"]


class ProductItemForFavouriteSerializer(serializers.ModelSerializer):
    tickets = TicketForFavouriteSerializer(read_only=True)
    phones = PhoneFavouriteSerializer(read_only=True)
    goods = GoodFavouriteSerializer(read_only=True)
    images = ImageForProductItemSerializer(many=True, read_only=True)

    class Meta:
        model = ProductItem
        fields = "__all__"


class FavoriteListSerializer(serializers.ModelSerializer):
    product = ProductItemForFavouriteSerializer()

    class Meta:
        model = Favorite
        fields = "__all__"


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"
