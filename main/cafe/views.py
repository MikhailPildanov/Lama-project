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
    context = {}
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
            Customer.objects.create(user=user, phone=phone) 
            user.save()
            login(request, user)
            return redirect('/')

    return render(request, 'user/register.html', {
        'form':form
    })

@login_required
def profile(request):
    return render(request, 'user/profile.html')


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
