from django.shortcuts import render

# Import Views
from django.views.generic import ListView, DetailView

# Import Models
from App_Shop.models import Product

# Mixins
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class Home(ListView):
    model = Product
    template_name = 'App_Shop/home.html'

class ProductDetail(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'App_Shop/product_detail.html'