from django.urls import path
from . views import *


urlpatterns = [
    path("",home,name="home"),
    path("addtocard/<int:pk>",addtocard,name='addtocard'),
    path("addtocart/",cart,name="cart"),
    path("deletecart/<int:pk>",deletecart,name='deletecart'),
    path("payment/",payment,name='payment'),
    path('payment-status', payment_status, name='payment-status')
]