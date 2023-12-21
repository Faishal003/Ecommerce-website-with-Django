from django.urls import path
from App_Payment import views

app_name = 'App_Payment'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('pay/', views.payment, name='payment'),
    path('status/', views.complete, name='complete'),
    path('purchase/<val_id>/<tran_id>/', views.purchased, name='purchase'),
    path('order/', views.order_view, name='orders'),
]