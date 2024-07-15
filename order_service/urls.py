from django.urls import path
from order_service import views

urlpatterns = [
    path('menu-item/', views.MenuItemBaseView.as_view()),
    path('menu-item/<str:pk>/', views.MenuItemDetailView.as_view()),
    path('order/', views.OrderBaseAPIView.as_view()),
    path('order/<str:pk>/', views.OrderDetailView.as_view()),
]