
from django.urls import path
from . import views
from .views import (
    LoyaltyCardByProfileAPIView,
    MyBonusScreenAPIView,
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

    # Loyalty cards (AUTH orqali, IDsiz)
    path(
        "loyalty-cards/",
        LoyaltyCardByProfileAPIView.as_view(),
        name="loyalty-cards-by-profile",
    ),

    # 🔥 ENG MUHIM QISM
    # faqat login bo‘lgan user uchun, ID YO‘Q
    path(
        "my-bonus/",
        MyBonusScreenAPIView.as_view(),
        name="my-bonus",
    ),
    path(
    "my-loyalty-card/",
    views.MyLoyaltyCardAPIView.as_view(),
    name="merchant-my-loyalty-card",
),

]
#  shu mmanimcha togri aka ishlayapti 