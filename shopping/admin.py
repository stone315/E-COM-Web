from django.contrib import admin
from .models import Product, Log, Order, Payment
# Register your models here.

admin.site.register(Product)
admin.site.register(Log)
admin.site.register(Order)
admin.site.register(Payment)
