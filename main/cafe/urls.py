from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('cart/', views.home, name="cart"),
    path('checkout/', views.home, name="checkout"),
]
