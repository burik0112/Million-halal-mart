from django.urls import path

from . import views

urlpatterns = [
    path("profile/create", views.ProfileCreateAPIView.as_view()),
    path("profile/<int:pk>/retriev", views.ProfileRetrieveUpdateDelete.as_view()),
    
    path("location/create", views.LocationCreateAPIView.as_view()),
    path("location/list", views.LocationListAPIView.as_view()),
    path("location/<int:pk>/retriev", views.LocationRetrieveUpdateDelete.as_view()),
    
    path("news/list", views.NewsListAPIView.as_view()),
    
    path("viewed/create", views.ViewedNewsCreateAPIView.as_view()),
    path("viewed/list", views.ViewedNewsCreateAPIView.as_view()),
    
    path("favorite/create", views.FavoriteCreateAPIView.as_view()),
    path("favorite/list", views.FavoriteListAPIView.as_view()),
    path("favorite/<int:pk>/retriev", views.FavoriteRetrieveUpdateDelete.as_view()),
    
    path('send_otp/', views.SendOTPView.as_view(), name='send_otp'),
    path('verify_otp/', views.VerifyOTPView.as_view(), name='verify_otp'),

]
