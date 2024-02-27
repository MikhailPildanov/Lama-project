from django.contrib import admin
from .models import *

admin.site.register(Customer)
admin.site.register(Menu)
admin.site.register(Food)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(FoodEnergy)