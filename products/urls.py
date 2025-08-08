from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("products/category/<int:category_id>/", products, name="products"),
    path("products/<int:product_id>/", products_details, name="products_details"),
    path('products/add/', create_product, name='add_product'),
    path('products/my-products/', my_products, name='my_products'),
    path('products/edit/<int:pk>/', edit_product, name='edit_product'),
    path('products/delete/<int:pk>/', delete_product, name='delete_product'),
     path("chart/", chart, name="chart"),
]
