from django.forms import model_to_dict
from django.shortcuts import render, redirect

from .serializers import MenuSerializer
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth import login
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
import json, datetime



def home(request):
    menus = Menu.objects.all()
    context = {'menus':menus}
    return render(request, 'store/home.html', context)

def menu_detail(request, id):
    foods = Food.objects.filter(menu=id)
    menu = Menu.objects.get(id=id)
    categories = set(food.category for food in foods)
    context = {'foods':foods, 'menu':menu, 'categories':categories}
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, status=0)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']

    context = {'foods':foods, 'cartItems':cartItems}
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


class MenuAPIView(generics.ListAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class MenuAPIView(APIView):
    def get(self, request):
        menu_list = Menu.objects.all()
        return Response({'menues': MenuSerializer(menu_list, many=True).data})
    
    def post(self, request):
        serializer = MenuSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'menu': serializer.data})
    
    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk is None:
            return Response({"error":"Method PUT not allowed"})
        try:
            instance = Menu.objects.get(pk=pk)
        except:
            return Response({"error":"Object does not exists"})
        
        serializer = MenuSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'menu': serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk is None:
            return Response({"error":"Method DELETE not allowed"})
        try:
            instance = Menu.objects.get(pk=pk)
        except:
            return Response({"error":"Object does not exists"})

        instance.delete()
        return Response({"delete": "success"})


    
