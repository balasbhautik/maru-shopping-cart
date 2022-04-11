from django.contrib import admin
from django.urls import path
from .import views
from .views import OrderView
from .views import cart
from .middlewares.auth import auth_middleware
urlpatterns = [
    path("",views.Index.as_view(),name="Homepage"),
    path("about/", views.about, name="AboutUs"),
    path("contact", views.contact, name="ContactUs"),
    path("tracker", views.tracker, name="Tracker"),
    path("search", views.search, name="Search"),
    path("productView", views.productView, name="ProductViews"),
    path("checkout", views.checkout.as_view(), name="Checkout"),
    path("signup", views.signup, name="Signup"),
    path("login", views.Login.as_view(), name="Login"),
    path("logout", views.logout, name="Logout"),
    path("cart", views.auth_middleware(cart.as_view()), name="Cart"),
    path("order", views.auth_middleware(OrderView.as_view()), name="Order")
]