from django.db import models
import datetime


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=25)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    desc = models.CharField(max_length=300, default='')
    image = models.ImageField(upload_to='media')

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()

    @staticmethod
    def get_products_by_ids(ids):
        return Product.objects.filter(id__in =ids)

    def __str__(self):
        return self.name


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def isExits(self):
        if Customer.objects.filter(email=self.email):
            return True

        return False

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False

    def __str__(self):
        return self.first_name


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price =models.IntegerField()
    address = models.CharField(max_length=50, default="", blank=True)
    phone = models.CharField(max_length=15, default="", blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order\
            .objects.filter(customer = customer_id)\
            .order_by('-date')

    def placeorder(self):
        return self.save()



class Contact(models.Model):
    name = models.CharField(max_length=20, default=None)
    email = models.EmailField()
    phone = models.CharField(max_length=15, default=None)
    address = models.TextField(max_length=100, default=None)