from django.urls import path

from . import views

urlpatterns = [
    path("category/list", views.CategoryListAPIView.as_view()),
    path("category/retriev", views.CategoryListAPIView.as_view()),
    path("subcat/list", views.SubCategoryListAPIView.as_view()),
    path("ticket/list", views.TicketListAPIView.as_view()),
    path("phone/list", views.PhoneListAPIView.as_view()),
    path("good/list", views.GoodListAPIView.as_view()),
    path("image/list", views.ImageListAPIView.as_view()),
]
