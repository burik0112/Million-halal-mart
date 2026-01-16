from django.urls import path


from .views import (
    GoodVariantsAPIView,
    NewPhonesListView,
    PhoneListAPIView,
    NewTicketsListView,
    PhoneVariantsAPIView,
    TicketListAPIView,
    SubCategoryListAPIView,
    CategoryListAPIView,
    PopularTicketsAPIView,
    PopularPhonesAPIView,
    PopularGoodAPIView,
    TicketVariantsAPIView,
    TicketsOnSaleListView,
    PhonesOnSaleListView,
    GoodsOnSaleListView,
    GoodListAPIView,
    NewGoodsListView,
    ImageListAPIView,
    MultiProductSearchView, WholesaleProductAPIView, RegularProductListAPIView,
)

urlpatterns = [
    path("categories/list/", CategoryListAPIView.as_view()),
    path("subcats/list/", SubCategoryListAPIView.as_view()),
    path("tickets/list/", TicketListAPIView.as_view()),
    path("new-tickets/list/", NewTicketsListView.as_view()),
    path("popular-tickets/list/", PopularTicketsAPIView.as_view()),
    path("sale-tickets/list/", TicketsOnSaleListView.as_view()),
    path("phones/list/", PhoneListAPIView.as_view()),
    path("new-phones/list/", NewPhonesListView.as_view()),
    path("popular-phones/list/", PopularPhonesAPIView.as_view()),
    path("sale-phones/list/", PhonesOnSaleListView.as_view()),
    path("goods/list/", GoodListAPIView.as_view()),
    path('good-variants/<uuid:product_type>/', GoodVariantsAPIView.as_view(), name='good-variants'),
    path('ticket-variants/<uuid:product_type>/', TicketVariantsAPIView.as_view(), name='ticket-variants'),
    path('phone-variants/<uuid:product_type>/', PhoneVariantsAPIView.as_view(), name='phone-variants'),
    path("new-goods/list/", NewGoodsListView.as_view()),
    path("popular-goods/list/", PopularGoodAPIView.as_view()),
    path("sale-goods/list/", GoodsOnSaleListView.as_view()),
    path("images/list/", ImageListAPIView.as_view()),
    path("product-search/", MultiProductSearchView.as_view()),
    # Oddiy xaridorlar uchun endpoint
    path('products/', RegularProductListAPIView.as_view(), name='product-list'),

    # Faqat optomchilar uchun alohida oyna (endpoint)
    path('wholesale-shop/', WholesaleProductAPIView.as_view(), name='wholesale-list'),
]
