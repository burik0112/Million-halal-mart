from django.urls import path

from . import views

urlpatterns = [
    path("category/create", views.CategoryCreateAPIView.as_view()),
    path("category/list", views.CategoryListAPIView.as_view()),
    path("category/retriev", views.CategoryListAPIView.as_view()),
    
    path("subcat/create", views.SubCategoryCreateAPIView.as_view()),
    path("subcat/list", views.SubCategoryListAPIView.as_view()),
    path("subcat/retriev", views.SubCategoryRetrieveUpdateDelete.as_view()),
    
    path("ticket/create", views.TicketCreateAPIView.as_view()),
    path("ticket/list", views.TicketListAPIView.as_view()),
    path("ticket/retriev", views.TicketRetrieveUpdateDelete.as_view()),
    
    path("phone/create", views.PhoneCreateAPIView.as_view()),
    path("phone/list", views.PhoneListAPIView.as_view()),
    path("phone/retriev", views.PhoneRetrieveUpdateDelete.as_view()),
    
    path("good/create", views.GoodCreateAPIView.as_view()),
    path("good/list", views.GoodListAPIView.as_view()),
    path("good/retriev", views.GoodRetrieveUpdateDelete.as_view()),
    
    path("image/create", views.ImageCreateAPIView.as_view()),
    path("image/list", views.ImageListAPIView.as_view()),
    path("image/retriev", views.ImageRetrieveUpdateDelete.as_view()),
]
