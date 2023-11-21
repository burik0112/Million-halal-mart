from django.urls import path
from .views import PopularTicketsAPIView, PopularPhonesAPIView, PopularGoodAPIView, TicketsOnSaleListView, PhonesOnSaleListView, GoodsOnSaleListView
from . import views

urlpatterns = [
    path("categories/list/", views.CategoryListAPIView.as_view()),
    path("subcats/list/", views.SubCategoryListAPIView.as_view()),

    path("tickets/list/", views.TicketListAPIView.as_view()),
    path("new-tickets/list/", views.NewTicketsListView.as_view()),
    path("popular-tickets/list/", PopularTicketsAPIView.as_view()),
    path("sale-tickets/list/", TicketsOnSaleListView.as_view()),

    path("phones/list/", views.PhoneListAPIView.as_view()),
    path("new-phones/list/", views.NewPhonesListView.as_view()),
    path("popular-phones/list/", PopularPhonesAPIView.as_view()),
    path("sale-phones/list/", PhonesOnSaleListView.as_view()),

    path("goods/list/", views.GoodListAPIView.as_view()),
    path("new-goods/list/", views.NewGoodsListView.as_view()),
    path("popular-goods/list/", PopularGoodAPIView.as_view()),
    path("sale-goods/list/", GoodsOnSaleListView.as_view()),


    path("images/list/", views.ImageListAPIView.as_view()),
]
