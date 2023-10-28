from django.urls import path
from .views import (
    PhoneListView,
    CreatePhoneView,
    TicketView,
    TicketListView,
    GoodListView,
    GoodView,
    CreatePhoneCategory
)

urlpatterns = [
    path("create-phone/", CreatePhoneView.as_view(), name="create_phone"),
    path("phone-category/", CreatePhoneCategory.as_view(), name="create_phone_category"),

    path("phones/", PhoneListView.as_view(), name="phone_list"),
    path("ticket-create/", TicketView.as_view(), name="ticket_create"),
    path("tickets/", TicketListView.as_view(), name="ticket-list"),
    path("good-create/", GoodView.as_view(), name="good_create"),
    path("goods/", GoodListView.as_view(), name="good-list"),
]
