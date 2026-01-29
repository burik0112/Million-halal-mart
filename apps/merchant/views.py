from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import SearchFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView, RetrieveAPIView, GenericAPIView,
)
from django.utils.translation import gettext_lazy as _
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, permissions, parsers
from django.db import transaction
from django.db.models import Prefetch
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from drf_spectacular.utils import extend_schema

from apps.product.models import Image, ProductItem
from .models import Order, OrderItem, Information, Service, SocialMedia, Bonus, LoyaltyCard
from .serializers import (
    CustomPageNumberPagination,
    OrderItemSerializer,
    OrderSerializer,
    InformationSerializer,
    OrderStatusUpdateSerializer,
    ServiceSerializer,
    OrderListSerializer,
    OrderCreateSerializer,
    SocialMediaSerializer,
    BonusSerializer, LoyaltyCardSerializer, UserBonusSerializer, CartAddSerializer,
    CheckoutSerializer, ReceiptUploadSerializer, OrderDetailSerializer,
)
from apps.dashboard.main import bot


# Create your views here.


@extend_schema(tags=["Merchant"])
class OrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if (
                serializer.validated_data.get("status") == "in_cart"
                and Order.objects.filter(user=request.user, status="in_cart").exists()
        ):
            return Response(
                {"detail": "You already have an in-cart order."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


@extend_schema(tags=["Merchant"])
class OrderListAPIView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["user__full_name"]
    filterset_fields = ["user__full_name", "status"]
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Bu metod faqat autentifikatsiya qilingan foydalanuvchiga tegishli orderlarni qaytaradi.
        """
        user = self.request.user
        if user.is_anonymous:
            return Order.objects.none()

        # Efficiently prefetching related data
        # product_prefetch = Prefetch(
        #     'products',
        #     queryset=ProductItem.objects.all()
        #     .select_related('phones', 'tickets', 'goods')  # Optimize OneToOne relations
        #     .prefetch_related(
        #         Prefetch('images', queryset=Image.objects.all(), to_attr='prefetched_images')
        #     )
        # )

        # return (
        #     Order.objects.filter(user=user.profile)
        #     .prefetch_related(
        #         product_prefetch,  # Products with optimized related objects
        #         'orderitem', # Order items linked to the order
        #         'orderitem__product'
        #     )
        #     .order_by("-created")  # Most recent orders first
        # )

        product_prefetch = Prefetch(
            'product',
            queryset=ProductItem.objects.all()
            .select_related('phones', 'tickets', 'goods')
            .prefetch_related(
                'images'  # Prefetch all related images without using a custom attribute
            )  # Optimize OneToOne relations
            # .prefetch_related(
            #     Prefetch('images', queryset=Image.objects.all(), to_attr='prefetched_images')
            # )
        )

        # Ensure that 'orderitem' prefetches not only 'product' but also detailed relationships
        order_items_prefetch = Prefetch(
            'orderitem',
            queryset=OrderItem.objects.all().prefetch_related(product_prefetch)
        )

        return (
            Order.objects.filter(user=user.profile)
            .prefetch_related(order_items_prefetch, 'orderitem__product')
            .prefetch_related('products')
            .order_by("-created_at")  # Most recent orders first
        )


@extend_schema(tags=["Merchant"])
class OrderRetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all().order_by("-pk")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=["Merchant"])
class OrderItemCreateAPIView(CreateAPIView):
    queryset = OrderItem.objects.all().order_by("-pk")
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        """
        Bu metod serializerga qo'shimcha kontekstni o'tkazish uchun ishlatiladi.
        """
        context = super(OrderItemCreateAPIView, self).get_serializer_context()
        context["request"] = self.request
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Multi-language success message for product addition
        success_message = {
            "en": _("The product has been successfully added to the cart"),
            "uz": _("Maxsulot savatga muvafaqqiyatli qo'shildi"),
            "ru": _("Товар успешно добавлен в корзину"),
            "kr": _("제품이 장바구니에 성공적으로 추가되었습니다"),
        }

        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": success_message, "order_item": serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


@extend_schema(tags=["Merchant"])
class OrderItemListAPIView(ListAPIView):
    queryset = OrderItem.objects.all().order_by("-pk")
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=["Merchant"])
class OrderItemRetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Login qilgan userni aniqlaymiz
        user_profile = self.request.user.profile
        # Faqat shu userga tegishli bo'lgan "savatdagi" narsalarni qaytaramiz
        return OrderItem.objects.filter(order__user=user_profile)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        order = instance.order
        self.perform_destroy(instance)
        order.update_total_amount()

        success_message = {
            "uz": "Maxsulot savatdan o'chirib tashlandi",
            "ru": "Товар удален из корзины",
            "en": "The product has been removed from the cart",
            "kr": _("제품이 장바구니에서 제거되었습니다"),
        }
        return Response({"message": success_message}, status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Merchant"])
class InformationListAPIView(ListAPIView):
    queryset = Information.objects.all().order_by("-pk")
    serializer_class = InformationSerializer
    permission_classes = [AllowAny]


@extend_schema(tags=["Merchant"])
class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id, *args, **kwargs):
        with transaction.atomic():
            try:

                # Check the original Order
                original_order = Order.objects.get(
                    id=order_id, user=request.user.profile
                )

                if original_order.status in ["approved", "sent", "cancelled"]:
                    new_order = Order.objects.create(
                        user=request.user.profile, status="pending"
                    )
                    for item in original_order.orderitem_set.all():
                        OrderItem.objects.create(
                            order=new_order,
                            product=item.product,
                            quantity=item.quantity,
                        )
                    order = new_order
                else:
                    order = original_order

                update_data = request.data.copy()
                update_data["status"] = "pending"
                serializer = OrderStatusUpdateSerializer(order, data=update_data)
                if serializer.is_valid():
                    serializer.save()
                    # Logic for sending message to a bot
                    bot(order)

                    # Multi-language success message for order creation
                    success_message = {
                        "en": _("Order created successfully"),
                        "uz": _("Buyurtma muvafaqqiyatli yaratildi"),
                        "ru": _("Заказ успешно создан"),
                        "kr": _("주문이 성공적으로 생성되었습니다"),
                    }

                    return Response(
                        {
                            "status": "success",
                            "order_id": order.id,
                            "message": success_message,
                        }
                    )
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Order.DoesNotExist:
                return Response(
                    {"status": "error", "message": "Order not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )


@extend_schema(tags=["Merchant"])
class ServiceListAPIView(ListAPIView):
    queryset = Service.objects.all().order_by("-pk")
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=["Merchant"])
class SocialMeadiaAPIView(ListAPIView):
    queryset = SocialMedia.objects.all().order_by("-pk")
    serializer_class = SocialMediaSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=["Merchant"])
class BonusPIView(ListAPIView):
    queryset = Bonus.objects.all().order_by("pk")
    serializer_class = BonusSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=["Merchant"])
class MyLoyaltyCardAPIView(APIView):
    # Только залогиненный пользователь может получить данные
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Возвращает карту лояльности ТОГО пользователя, который сделал запрос
        """
        try:
            # 1. Получаем профиль текущего пользователя через токен
            user_profile = request.user.profile

            # 2. Ищем карту, которая принадлежит этому профилю
            card = LoyaltyCard.objects.get(profile=user_profile)

            # 3. Отдаем данные в сериализатор
            serializer = LoyaltyCardSerializer(card)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except AttributeError:
            # Если у юзера вдруг нет профиля
            return Response({"error": "Profile not found"}, status=status.HTTP_400_BAD_REQUEST)
        except LoyaltyCard.DoesNotExist:
            # Если карта еще не создана
            return Response({"detail": "Loyalty card not found for this user"}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(tags=["Merchant"])
class MyBonusScreenAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 🔥 ENG MUHIM JOY
        profile = request.user.profile

        serializer = UserBonusSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartManageAPIView(APIView):
    serializer_class = CartAddSerializer

    @swagger_auto_schema(request_body=CartAddSerializer)
    def post(self, request):
        serializer = CartAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order, _ = Order.objects.get_or_create(user=request.user.profile, status='in_cart')
        product_id = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        if quantity > 0:
            OrderItem.objects.update_or_create(order=order, product_id=product_id, defaults={'quantity': quantity})
        else:
            OrderItem.objects.filter(order=order, product_id=product_id).delete()

        order.update_total_amount()
        return Response({"message": "Savat yangilandi", "total": order.total_amount})


# --- 2. BUYURTMA BERISH (CHECKOUT) ---
class CheckoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CheckoutSerializer

    @swagger_auto_schema(request_body=CheckoutSerializer)
    def post(self, request):
        user_profile = request.user.profile
        # Savatdagi buyurtmani topamiz
        order = Order.objects.filter(user=user_profile, status='in_cart').first()

        if not order or not order.orderitem.exists():
            return Response({"error": "Savat bo'sh"}, status=400)

        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 1. Location obyektini serializerdan olamiz
        location_obj = serializer.validated_data['location']

        # 2. Buyurtmaga biriktiramiz va saqlaymiz
        order.location = location_obj
        order.comment = serializer.validated_data.get('comment', '')
        order.status = 'pending'
        order.save()

        # 3. Javob qaytaramiz (manzil matni bilan birga)
        return Response({
            "message": "Buyurtmangiz adminga yuborildi. Tasdiqlangach to'lov qilishingiz mumkin.",
            "order_id": order.id,
            "status": "pending",
            "delivery_address": order.location.address,  # <--- MANA SHU YERDA MANZIL CHIQADI
            "total_amount": order.total_amount
        })


# --- 3. CHEK YUKLASH ---

class UploadReceiptAPIView(APIView):
    # Parserlar faylni qabul qilish uchun shart
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="To'lov chekini yuklash",
        description="Aynan shu yerda 'Choose File' tugmasi chiqishi shart",
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'order_number': {
                        'type': 'string',
                        'description': 'Buyurtma raqami (ORD123...)'
                    },
                    'payment_receipt': {
                        'type': 'string',
                        'format': 'binary',  # MANA SHU QATOR TUGMANI CHIQARADI
                        'description': 'To\'lov cheki (JPG, PNG yoki PDF)'
                    }
                },
                'required': ['order_number', 'payment_receipt']
            }
        },
        responses={200: {"message": "Muvaffaqiyatli"}}
    )
    def post(self, request):
        user_profile = request.user.profile

        # Ma'lumotlarni olish
        ord_num = request.data.get('order_number')
        receipt_file = request.FILES.get('payment_receipt')

        if not ord_num or not receipt_file:
            return Response({"error": "Order raqami va rasm yuborilishi shart"}, status=400)

        # Buyurtmani qidiramiz
        order = Order.objects.filter(
            user=user_profile,
            order_number=ord_num,
            status='awaiting_payment'
        ).first()

        if not order:
            return Response({"error": "To'lov kutilayotgan buyurtma topilmadi"}, status=404)

        # Saqlash
        order.payment_receipt = receipt_file
        order.status = 'check_pending'
        order.save()

        return Response({"message": "Chek yuklandi, admin tasdig'ini kuting."}, status=200)


# --- 4. BUYURTMA DETALI (TIMELINE BILAN) ---
class OrderDetailAPIView(APIView):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user.profile)
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)

class MyOrdersListView(ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Savatda bo'lmagan, ya'ni haqiqiy buyurtma bo'lgan narsalar
        return Order.objects.filter(user=self.request.user.profile).exclude(status='in_cart').order_by('-pk')