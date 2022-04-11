from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Product
from .models import Category
from .models import Customer
from .models import Contact
from .models import Order
from django.views import View
from .middlewares.auth import auth_middleware
from django.utils.decorators import method_decorator


# Create your views here.
class Index(View):
    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        products = None
        categories = Category.get_all_categories()
        catrgotyId = request.GET.get('category')
        if catrgotyId:
            products = Product.get_all_products_by_categoryid(catrgotyId)
        else:
            products = Product.get_all_products()

        data = {'products': products,
                'categories': categories}
        print('Your are :', request.session.get('email'))
        return render(request, 'index.html', data)

    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1

                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print(cart)
        return redirect('Homepage')


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        print(name, email, phone, address)
        contacts = Contact(name = name, email= email, phone = phone, address = address)
        contacts.save()
    return render(request, 'contact.html')


def tracker(request):
    return HttpResponse("We are at Tracker page")


def search(request):
    return HttpResponse("We are at search page")


def productView(request):
    return HttpResponse("We are at Product Views page")


class checkout(View):

    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_ids(list(cart.keys()))
        print(address, phone, customer, cart, products)
        for product in products:
            order = Order(customer=Customer(id=customer), product=product, price=product.price, address=address,
                          phone=phone, quantity=cart.get(str(product.id)))
            order.placeorder()
        request.session['cart'] = {}
        return redirect('Cart')

class OrderView(View):

    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request, 'order.html', {'orders':orders})

def validateCustomer(customer):
    error_message = None

    if not customer.first_name:
        error_message = "First Name Required !!"
    elif len(customer.first_name) < 4:
        error_message = "First Name must be 4 char long and more"
    elif not customer.last_name:
        error_message = "Last Name Required !! "
    elif len(customer.last_name) < 4:
        error_message = "Last Name must be 4 char long and more"
    elif not customer.phone:
        error_message = "Phone Number Required!!"
    elif len(customer.phone) < 10:
        error_message = "Phone Number must be 10 char long"
    elif not customer.password:
        error_message = "Password must be required"
    elif len(customer.password) < 6:
        error_message = "Password must be 6 char long"
    elif not customer.email:
        error_message = "Email must be required !!"
    elif customer.isExits():
        error_message = "Email Already Registered !!"

    return error_message


def registerUser(request):
    first_name = request.POST.get('firstname')
    last_name = request.POST.get('lastname')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    password = request.POST.get('password')

    value = {
        'first_name': first_name,
        'last_name': last_name,
        'phone': phone,
        'email': email

    }

    error_message = None
    customer = Customer(first_name=first_name, last_name=last_name, phone=phone, email=email, password=password)
    error_message = validateCustomer(customer)
    # saving
    if not error_message:
        customer.password = make_password(customer.password)
        customer.save()
        return redirect('Homepage')
    else:
        data = {
            'error': error_message,
            'value': value
        }
        return render(request, 'signup.html', data)


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')

    else:
        return registerUser(request)


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):

        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                request.session['email'] = email
                return redirect('Homepage')
            else:
                error_message = "Email or Password invalid !!"
        else:
            error_message = "Email or Password invalid !!"

        return render(request, 'login.html', {'error': error_message})


def logout(request):
    request.session.clear()
    return redirect('Login')


class cart(View):
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_ids(ids)
        print(products)
        return render(request, 'cart.html', {'products': products})
