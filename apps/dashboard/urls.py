from django.urls import path
from .product import (
    PhoneListView,
    PhoneCreateView,
    TicketCreateView,
    TicketListView,
    GoodListView,
    GoodCreateView,
    PhoneCategoryCreateView,
    TicketCategoryCreateView,
    PhoneEditDeleteView,
    PhoneDeleteView,
    GoodCategoryCreateView,
    TicketDeleteView,
    TicketEditDeleteView,
    GoodEditDeleteView,
    GoodDeleteView,
    GoodMainCategoryCreateView,
)

from .users import (UserListView, UserOrdersView,
                    UserOrderDetailView, OrdersListView, BlockActivateUserView)
from .main import (dashboard, InformationView,
                   InformationEditView, ServiceView, ServiceEditView, BannerView, BannerActionView, NewsCreateView, NewsListView, NewsEditView, OrdersView, update_order_status)
from .users import (
    UserListView,
    UserOrdersView,
    UserOrderDetailView,
    OrdersListView,
    BlockActivateUserView,
)
from .bot import index

from .information import (
    edit_reminder,
    edit_agreement,
    edit_shipment,
    edit_privacy,
    edit_aboutus,
    edit_support,
    edit_payment
)

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("product/create-phone/", PhoneCreateView.as_view(), name="create_phone"),
    path(
        "product/phone-category/",
        PhoneCategoryCreateView.as_view(),
        name="phone_category",
    ),
    path("product/phones/", PhoneListView.as_view(), name="phone_list"),
    path(
        "product/phones/edit-delete/<int:pk>/",
        PhoneEditDeleteView.as_view(),
        name="edit_delete_phone",
    ),
    path(
        "product/phone/<int:pk>/delete/", PhoneDeleteView.as_view(), name="delete_phone"
    ),
    path("product/ticket-create/", TicketCreateView.as_view(), name="ticket_create"),
    path(
        "product/ticket-category/",
        TicketCategoryCreateView.as_view(),
        name="ticket_category",
    ),
    path("product/tickets/", TicketListView.as_view(), name="ticket-list"),
    path(
        "product/ticket/edit-delete/<int:pk>/",
        TicketEditDeleteView.as_view(),
        name="edit_delete_ticket",
    ),
    path(
        "product/ticket/<int:pk>/delete/",
        TicketDeleteView.as_view(),
        name="delete_ticket",
    ),
    path("product/good-create/", GoodCreateView.as_view(), name="good_create"),
    path(
        "product/good-category/",
        GoodMainCategoryCreateView.as_view(),
        name="good_category",
    ),
    path(
        "product/good-subcategory/",
        GoodCategoryCreateView.as_view(),
        name="good_subcategory",
    ),
    path("product/goods/", GoodListView.as_view(), name="good-list"),
    path("product/good/edit-delete/<int:pk>/",
         GoodEditDeleteView.as_view(), name='edit-delete-good'),
    path('product/good/<int:pk>/delete/',
         GoodDeleteView.as_view(), name='delete_good'),


    path("product/news/", NewsListView.as_view(), name="news-list"),
    path("product/news-create/", NewsCreateView.as_view(), name="news-create"),
    path('product/news/edit/<int:pk>/',
         NewsEditView.as_view(), name='edit_delete_news'),

    path("users/", UserListView.as_view(), name="users-list"),
    path("users/<int:pk>/order", UserOrdersView.as_view(), name="user-orders-list"),
    path("users/order-detail/<int:pk>/", UserOrderDetailView.as_view(), name="user-order-detail"),
    path('block_activate_user/<int:pk>/', BlockActivateUserView.as_view(), name='block_activate_user'),
    
    path("orders/", OrdersListView.as_view(), name="orders-list"),

    path("other/news/", NewsListView.as_view(), name="news-list"),
    path("other/news-create/", NewsCreateView.as_view(), name="news-create"),
    path('other/news/edit/<int:pk>/',
         NewsEditView.as_view(), name='edit_delete_news'),
    path('other/info/list/', InformationView.as_view(), name='info-list'),
    path('other/info/edit/<int:pk>/',
         InformationEditView.as_view(), name='edit_info'),
    path('other/service/list', ServiceView.as_view(), name='service-list'),
    path('other/service/edit/<int:pk>/',
         ServiceEditView.as_view(), name='edit_service'),
    path('other/banners/list/', BannerView.as_view(), name='banner-list'),
    path('other/banner/action/<int:pk>/',
         BannerActionView.as_view(), name='banner-action'),
    path("orders/<int:pk>/", OrdersView.as_view(), name="orders-list"),
    path('update-order-status/<int:pk>/',
         update_order_status, name='update-order-status'),

    path('bot/', index, name='bot'),

    path("info/list/", InformationView.as_view(), name="info-list"),
    path("info/edit/<int:pk>/", InformationEditView.as_view(), name="edit_info"),
    # info
    path("edit-reminder/<int:pk>/", edit_reminder, name="edit_reminder"),
    path("edit-agreement/<int:pk>/", edit_agreement, name="edit_agreement"),
    path("edit-shipment/<int:pk>/", edit_shipment, name="edit_shipment"),
    path("edit-privacy/<int:pk>/", edit_privacy, name="edit_privacy"),
    path("edit-about_us/<int:pk>/", edit_aboutus, name="edit_aboutus"),
    path("edit-support/<int:pk>/", edit_support, name="edit_support"),
    path("edit-payment/<int:pk>/", edit_payment, name="edit_payment"),
    path("service/list", ServiceView.as_view(), name="service-list"),
    path("service/edit/<int:pk>/", ServiceEditView.as_view(), name="edit_service"),
    path("bot/", index, name="bot"),
]
