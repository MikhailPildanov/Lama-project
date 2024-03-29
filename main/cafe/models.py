from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12, null=True)
    
    def __str__(self):
        return self.user.username

class Menu(models.Model):
    name = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    image = models.ImageField(null=True, blank=True)
    category = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)
        
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Food(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    description = models.TextField(null=True)
    image = models.ImageField(null=True, blank=True)
    status = models.BooleanField(default=True)
    category = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order_time = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(null=True)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    street = models.CharField(max_length=200, null=True)
    house = models.CharField(max_length=200, null=True)
    flat = models.CharField(max_length=200, null=True)
    level = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.street

class OrderItem(models.Model):
    food = models.ForeignKey(Food, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default = 0, null=True, blank=True)

    @property
    def get_total(self):
        total = self.food.price * self.quantity
        return total
    
