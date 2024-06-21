from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth import login
from django.http import JsonResponse
import json, datetime


def home(request):
    menus = Menu.objects.all()
    context = {'menus':menus}
    return render(request, 'store/home.html', context)

def menu_detail(request, id):
    foods = Food.objects.filter(menu=id)
    menu = Menu.objects.get(id=id)
    categories = sorted(list(set(food.category for food in foods)))
    foods_with_energy_by_category = {}
    for category in categories:
        foods_by_catergory = Food.objects.filter(menu=id, category=category)
        energies = []
        for food in foods_by_catergory:
            energy_dict = {}
            if food.energy:
                energy_dict['ккал'] = food.weight_in_grams * food.energy.cal_per_100g // 100
                energy_dict['б/ж/у'] = str(food.weight_in_grams * food.energy.prot_per_100g // 100)+ '/' + str(food.weight_in_grams * food.energy.fat_per_100g // 100) + '/' + str(food.weight_in_grams * food.energy.carbs_per_100g // 100)
            energies.append(energy_dict)
        foods_with_energy_by_category[category] = zip(foods_by_catergory, energies)
            
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, status=0)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']
    
    context = {'foods_with_energy_by_category':foods_with_energy_by_category, 'cartItems':cartItems, 'menu':menu}
    return render(request, 'store/menu_detail.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, status=0)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        total_cals = order.get_cart_cals
        cals_norm = customer.calories_norm
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'get_cart_cals':0}
        cartItems = order['get_cart_items']
        total_cals = order['get_cart_cals']
        cals_norm = 'NaN'

    context = {'items':items, 'order':order, 'cartItems':cartItems, 'total_cals':total_cals, 'cals_norm':cals_norm}
    return render(request, 'store/cart.html', context)

def updateItem(request):
    data = json.loads(request.body)
    foodId = data['foodId']
    action = data['action']

    print('Action:', action)
    print('foodId:', foodId)


    customer = request.user.customer
    food = Food.objects.get(id=foodId)
    order, created = Order.objects.get_or_create(customer=customer, status=0)

    orderItem, created = OrderItem.objects.get_or_create(order=order, food=food)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action =='remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, status='0')
        total = (data['form']['total'])
        order.transaction_id = transaction_id

        order.status = 1
        order.save()

        
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            street=data['shipping']['street'],
            house=data['shipping']['house'],
            flat=data['shipping']['flat'],
            level=data['shipping']['level'],
        )

    else:
        print('User in not logged in..')        
    return JsonResponse('Payment complete!', safe=False)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, status=0)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
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
            user.phone = phone
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
    customer, age = None, None
    if Customer.objects.filter(user=user):
        customer = user.customer
        age = customer.age
        sex = 'Женщина'
        if customer.biological_sex is True:
            sex = 'Мужчина'

    
    context = {'user':user, 'customer':customer, 'age':age, 'sex':sex}
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
