from django.contrib import admin
from .models import Product
from .models import Category
from .models import Customer
from .models import Order
from .models import Contact
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'desc', 'image')



admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Contact)

