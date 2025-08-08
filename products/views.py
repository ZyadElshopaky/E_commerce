from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .forms import *

def home(request):
    products=Product.objects.all()
    return render(request,'home.html',{'products':products})

def products(request):
    products=Product.objects.all()
    return render(request, 'products/products.html',{'products':products})

@login_required
def create_product(request):
    if not request.user.is_authenticated or not (
        request.user.is_superuser or getattr(request.user, 'is_seller', False)
    ):
        messages.error(
            request,
            "You are not allowed to add a product because you are not a seller."
        )
        return redirect('profile')
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False) 
            product.created_by = request.user  
            product.save()  
            messages.success(request, "Product added successfully.")
            return redirect("my_products")
    else:
        form = ProductForm()

    return render(request, "products/create_product.html", {"form": form})

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, id=pk, created_by=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('my_products')  
    else:
        form = ProductForm(instance=product, user=request.user)

    return render(request, 'products/product_ edit.html', {'form': form})

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, created_by=request.user)
    if request.method == 'POST':
        product.delete()
    return redirect('my_products')
@login_required
def my_products(request):
    if not request.user.is_authenticated or not (
        request.user.is_superuser or getattr(request.user, 'is_seller', False)
    ):
        messages.error(
            request,
            "You are not allowed to add a product because you are not a seller."
        )
        return redirect('profile')
    products = Product.objects.filter(created_by=request.user)

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id, created_by=request.user)

        title = request.POST.get('title')
        price = request.POST.get('price')
        stock = request.POST.get('stock')

        if title:
            product.title = title
        if price:
            product.price = price
        if stock:
            product.stock = stock

        product.save()
        return redirect('my_products')

    return render(request, 'products/my_products.html', {'products': products})
@never_cache
def products_details(request, product_id):
    product=Product.objects.get(id=product_id)
    qty = None
    cart = request.session.get("cart", {})
    if str(product_id) in cart:
        qty = cart[str(product_id)]["quantity"]
    if product:
        return render(request, 'products/products_details.html', {'product': product,"qty":qty})
    return render(request, '404.html', status=404)
