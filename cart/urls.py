from django.urls import path
from .views import *

urlpatterns = [
    path('', cart_view, name='cart'),
    path('add/', cart_add, name='add'),
    path('delete/', cart_delete, name='delete'),
    path('payment/', payment, name='payment'),
]