from django.urls import path
from App_Shop import views

app_name = 'App_Shop'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('product/<pk>/', views.ProductDetail.as_view(), name='product_detail'),
]