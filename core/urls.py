from django.urls import path
from .views import *

urlpatterns = [
    path('contact_us', contact_us, name='contact_us'),
    # path('/role_selection/', role_selection, name='role_selection'),
    # path('/seller', seller, name='seller'),
]
