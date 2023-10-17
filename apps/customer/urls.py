from django.urls import path
from . import views

urlpatterns = [
    path("profile/create", views.ProfileCreateAPIView.as_view()),
    path("profile/list", views.ProfileListAPIView.as_view()),
    path("profile/retriev", views.ProfileRetrieveUpdateDelete.as_view()),
    
    path("location/create", views.LocationCreateAPIView.as_view()),
    path("location/list", views.LocationListAPIView.as_view()),
    path("location/retriev", views.LocationRetrieveUpdateDelete.as_view()),
    
    path("news/create", views.NewsCreateAPIView.as_view()),
    path("news/list", views.NewsListAPIView.as_view()),
    path("news/retriev", views.NewsRetrieveUpdateDelete.as_view()),
    
    path("viewed/create", views.ViewedNewsCreateAPIView.as_view()),
    path("viewed/list", views.ViewedNewsCreateAPIView.as_view()),
    path("viewed/retriev", views.ViewedNewsRetrieveUpdateDelete.as_view()),
    
    path("favorite/create", views.FavoriteCreateAPIView.as_view()),
    path("favorite/list", views.FavoriteListAPIView.as_view()),
    path("favorite/retriev", views.FavoriteRetrieveUpdateDelete.as_view()),
]
