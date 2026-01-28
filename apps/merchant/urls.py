from django.urls import path
from . import views
from .views import (
    MyBonusScreenAPIView, CartManageAPIView, CheckoutAPIView, ReceiptUploadAPIView,
    OrderDetailAPIView, MyOrdersListView,
)

urlpatterns = [
    # Orders
    path("order/create/", views.OrderCreateAPIView.as_view()),
    path("order/list/", views.OrderListAPIView.as_view()),
    path("order/<int:pk>/retriev/", views.OrderRetrieveUpdateDelete.as_view()),

    # Order items
    path("order-item/create/", views.OrderItemCreateAPIView.as_view()),
    path("order-item/list/", views.OrderItemListAPIView.as_view()),
    path("order-item/<int:pk>/retriev/", views.OrderItemRetrieveUpdateDelete.as_view()),

    # Checkout & info
    path("checkout/<int:order_id>/", views.CheckoutView.as_view(), name="checkout"),
    path("information/", views.InformationListAPIView.as_view(), name="info"),
    path("service/", views.ServiceListAPIView.as_view(), name="service"),
    path("social-media-urls/", views.SocialMeadiaAPIView.as_view()),

    # Bonus
    path("bonus-list/", views.BonusPIView.as_view()),
    path("my-bonus/", MyBonusScreenAPIView.as_view(), name="my-bonus"),
    path("my-loyalty-card/", views.MyLoyaltyCardAPIView.as_view(), name="merchant-my-loyalty-card"),

    # 1. Savatni boshqarish (Mahsulot qo'shish, sonini o'zgartirish yoki o'chirish)
    # Flutterchi JSON yuboradi: {"product": 1, "quantity": 2}
    path('cart/manage/', CartManageAPIView.as_view(), name='cart-manage'),

    # 2. Buyurtmani rasmiylashtirish (Savatni yopish va "To'lov kutilmoqda" holatiga o'tkazish)
    # Flutterchi JSON yuboradi: {"location": 5, "comment": "..."}
    path('cart/checkout/', CheckoutAPIView.as_view(), name='cart-checkout'),

    # 3. To'lov chekini (rasm) yuklash
    # URL format: /api/merchant/order/15/upload-receipt/
    path('order/<int:pk>/upload-receipt/', ReceiptUploadAPIView.as_view(), name='upload-receipt'),

    # 4. Foydalanuvchining barcha buyurtmalari ro'yxati (Buyurtmalarim sahifasi uchun)
    path('orders/', MyOrdersListView.as_view(), name='my-orders-list'),

    # 5. Bitta buyurtmaning batafsil ma'lumoti (Timeline/Vaqt jadvali bilan)
    # URL format: /api/merchant/order/15/detail/
    path('order/<int:pk>/detail/', OrderDetailAPIView.as_view(), name='order-detail'),
    ]
