from django.urls import path

from . import views

urlpatterns = [
    path("order/create", views.OrderCreateAPIView.as_view()),
    path("order/list", views.OrderListAPIView.as_view()),
    path("order/<int:pk>/retriev", views.OrderRetrieveUpdateDelete.as_view()),
    path("item/create", views.OrderItemCreateAPIView.as_view()),
    path("item/list", views.OrderItemListAPIView.as_view()),
    path("item/<int:pk>/retriev", views.OrderItemRetrieveUpdateDelete.as_view()),
    path("checkout/<int:order_id>/", views.CheckoutView.as_view(), name="checkout"),
    path('information/', views.InformationListAPIView.as_view(), name='info'),
    path('service/', views.ServiceListAPIView.as_view(), name='service'),
]
