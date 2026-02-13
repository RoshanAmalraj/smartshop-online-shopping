from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('login',login,name='log'),
    path('elec',elec,name='elec'),
    path('Register',Register,name='reg'),
    path('cart',cart,name='cart'),
    path('delete/<str:cid>',delete,name='delete'),
    path('elec/<str:name>',elecs,name='elecs'),
    path('elec/<str:cname>/<str:pname>',p_details,name='p'),
    path('addcart',addcard,name="addcart"),
    path('logout',logout,name='logout'),
]
