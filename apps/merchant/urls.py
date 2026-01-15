from django.urls import path

from . import views
from .views import LoyaltyCardByProfileAPIView, LoyaltyCardDetailAPIView

urlpatterns = [
    path("order/create/", views.OrderCreateAPIView.as_view()),
    path("order/list/", views.OrderListAPIView.as_view()),
    path("order/<int:pk>/retriev/", views.OrderRetrieveUpdateDelete.as_view()),
    path("order-item/create/", views.OrderItemCreateAPIView.as_view()),
    path("order-item/list/", views.OrderItemListAPIView.as_view()),
    path("order-item/<int:pk>/retriev/", views.OrderItemRetrieveUpdateDelete.as_view()),
    path("checkout/<int:order_id>/", views.CheckoutView.as_view(), name="checkout"),
    path("information/", views.InformationListAPIView.as_view(), name="info"),
    path("service/", views.ServiceListAPIView.as_view(), name="service"),
    path("social-media-urls/", views.SocialMeadiaAPIView.as_view()),
    path("bonus-list/", views.BonusPIView.as_view()),
    path('loyalty-cards/', LoyaltyCardByProfileAPIView.as_view(), name='loyalty-cards-by-profile'),
    path('loyalty-cards/<int:pk>/', LoyaltyCardDetailAPIView.as_view(), name='loyalty-card-detail'),
]
