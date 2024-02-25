from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class Customer(AbstractBaseUser):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=12, null=True)
    
    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['phone']
    def __str__(self):
        return self.name

class Menu(models.Model):
    name = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    image = models.ImageField(null=True, blank=True)

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

    def __iter__(self):
        return [self.menu,
                self.name,
                self.price,
                self.description,
                self.status]
    
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

    def __str__(self):
        return str(self.id)

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
    
