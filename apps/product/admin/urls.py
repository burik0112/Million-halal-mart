from django.urls import path
from .views import PhoneListView

urlpatterns = [
    path('phones/', PhoneListView.as_view(), name='phone-list'),
]
