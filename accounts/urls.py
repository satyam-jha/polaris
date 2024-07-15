from django.urls import path
from accounts import views

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name="registration_view"),
    path('login/', views.LoginAPI.as_view(), name="registration_view"),
    path('location/', views.LiveLocationUpdateAPI.as_view()),
    path('restaurants/', views.RestaurantListAPIView.as_view()),
]