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
    NewsListView,
    NewsCreateView,
    GoodDeleteView,
)
from .users import (UserListView, UserOrdersView)
from .main import (dashboard, InformationView)
urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("product/create-phone/", PhoneCreateView.as_view(), name="create_phone"),
    path("product/phone-category/",
         PhoneCategoryCreateView.as_view(), name="phone_category"),
    path("product/phones/", PhoneListView.as_view(), name="phone_list"),
    path('product/phones/edit-delete/<int:pk>/',
         PhoneEditDeleteView.as_view(), name='edit_delete_phone'),
    path('product/phone/<int:pk>/delete/',
         PhoneDeleteView.as_view(), name='delete_phone'),

    path("product/ticket-create/", TicketCreateView.as_view(), name="ticket_create"),
    path("product/ticket-category/", TicketCategoryCreateView.as_view(),
         name="ticket_category"),
    path("product/tickets/", TicketListView.as_view(), name="ticket-list"),
    path('product/ticket/edit-delete/<int:pk>/',
         TicketEditDeleteView.as_view(), name='edit_delete_ticket'),
    path('product/ticket/<int:pk>/delete/',
         TicketDeleteView.as_view(), name='delete_ticket'),

    path("product/good-create/", GoodCreateView.as_view(), name="good_create"),
    path("product/good-category/",
         GoodCategoryCreateView.as_view(), name="good_category"),
    path("product/goods/", GoodListView.as_view(), name="good-list"),
    path("product/good/edit-delete/<int:pk>/",
         GoodEditDeleteView.as_view(), name='edit-delete-good'),
    path('product/good/<int:pk>/delete/',
         GoodDeleteView.as_view(), name='delete_good'),


    path("product/news/", NewsListView.as_view(), name="news-list"),
    path("product/news-create/", NewsCreateView.as_view(), name="news-create"),

    path("users/", UserListView.as_view(), name="users-list"),
    path("users/<int:pk>/order", UserOrdersView.as_view(), name="user-orders-list"),

    path('info/list/', InformationView.as_view(), name='info-list'),


]
