from django.shortcuts import render
from .models import *

def home(request):
    menus = Menu.objects.all()
    context = {'menus':menus}
    return render(request, 'store/home.html', context)

def cart(request):
    context = {}
    return render(request, 'store/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)

