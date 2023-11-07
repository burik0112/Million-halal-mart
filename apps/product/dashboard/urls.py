from django.urls import path
from .views import (
    PhoneListView,
    PhoneCreateView,
    TicketCreateView,
    TicketListView,
    GoodListView,
    GoodView,
    PhoneCategoryCreateView
)

urlpatterns = [
    path("create-phone/", PhoneCreateView.as_view(), name="create_phone"),
    path("phone-category/", PhoneCategoryCreateView.as_view(), name="create_category"),
    path("phones/", PhoneListView.as_view(), name="phone_list"),
    path("ticket-create/", TicketCreateView.as_view(), name="ticket_create"),
    path("tickets/", TicketListView.as_view(), name="ticket-list"),
    path("good-create/", GoodView.as_view(), name="good_create"),
    path("goods/", GoodListView.as_view(), name="good-list"),
]
