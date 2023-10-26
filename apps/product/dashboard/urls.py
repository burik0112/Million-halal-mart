from django.urls import path
from .views import PhoneListView, CreatePhoneView

urlpatterns = [
    path('create-phone/', CreatePhoneView.as_view(), name='create_phone'),
    path('phones/', PhoneListView.as_view(), name='phone_list'),
]
