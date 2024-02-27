from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth import login


def home(request):
    menus = Menu.objects.all()
    context = {'menus':menus}
    return render(request, 'store/home.html', context)

def menu_detail(request, id):
    foods = Food.objects.filter(menu=id)
    menu = Menu.objects.get(id=id)
    categories = set(food.category for food in foods)
    context = {'foods':foods, 'menu':menu, 'categories':categories}
    return render(request, 'store/menu_detail.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, status=0)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)

def register(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            phone = form.cleaned_data.get('phone')
            user = form.save(commit=False)
            user.username = username
            user.save()
            Customer.objects.create(user=user, phone=phone) 
            login(request, user)
            return redirect('/')

    return render(request, 'user/register.html', {
        'form':form
    })

@login_required
def profile(request):
    user = request.user
    customer = None
    if Customer.objects.filter(user=user):
        customer = user.customer
    context = {'user':user, 'customer':customer}
    return render(request, 'user/profile.html', context)


@login_required
def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('home')
    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {'u_form': u_form}

    return render(request, 'user/profile_update.html', context)
