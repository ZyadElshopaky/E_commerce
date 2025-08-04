from django.shortcuts import render
from products.products_list import eproducts

def home(request):
    return render(request,'home.html',{'products':eproducts})

def products(request):
    return render(request, 'products/products.html',{'products':eproducts})

def products_details(request, product_id):
    for product in eproducts:
        if product['id'] == product_id:
            return render(request, 'products/products_details.html', {'product': product})
    return render(request, '404.html', status=404)
