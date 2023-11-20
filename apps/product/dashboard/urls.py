from django.urls import path
from .views import (
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
    GoodDeleteView
)

urlpatterns = [
    path("create-phone/", PhoneCreateView.as_view(), name="create_phone"),
    path("phone-category/", PhoneCategoryCreateView.as_view(), name="phone_category"),
    path("phones/", PhoneListView.as_view(), name="phone_list"),
    path('phones/edit-delete/<int:pk>/',
         PhoneEditDeleteView.as_view(), name='edit_delete_phone'),
    path('phone/<int:pk>/delete/', PhoneDeleteView.as_view(), name='delete_phone'),

    path("ticket-create/", TicketCreateView.as_view(), name="ticket_create"),
    path("ticket-category/", TicketCategoryCreateView.as_view(),
         name="ticket_category"),
    path("tickets/", TicketListView.as_view(), name="ticket-list"),
    path('ticket/edit-delete/<int:pk>/',
         TicketEditDeleteView.as_view(), name='edit_delete_ticket'),
    path('ticket/<int:pk>/delete/',
         TicketDeleteView.as_view(), name='delete_ticket'),

    path("good-create/", GoodCreateView.as_view(), name="good_create"),
    path("good-category/", GoodCategoryCreateView.as_view(), name="good_category"),
    path("goods/", GoodListView.as_view(), name="good-list"),
    path("good/edit-delete/<int:pk>/",GoodEditDeleteView.as_view(),name='edit-delete-good'),
    path('good/<int:pk>/delete/',
         GoodDeleteView.as_view(), name='delete_good'),


    path("news/", NewsListView.as_view(), name="news-list"),
    path("news-create/", NewsCreateView.as_view(), name="news-create"),


]
