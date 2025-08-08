from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from products.models import Product
from django.http import JsonResponse,HttpResponse
import json
# @login_required(login_url="login")
def cart_view(request):
    cart = request.session.get('cart', {})
    products=[]
    product_qs = Product.objects.filter(id__in=list(cart.keys()))
    for p in product_qs:
        products.append({
            "id": p.id,
            "title": p.title,
            "image": p.image,
            "price" : p.price,
            "qty": cart[str(p.id)]["quantity"]  
        })
        print(cart[str(p.id)]["quantity"])
    
    return render(request, 'cart/cart.html', context={"products": products })
def cart_add(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id__ = str(data.get('id'))
        qty = int(data.get('qty', 1))
        print( id__,qty)
        try:
            product = Product.objects.get(id=id__)
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)
        if  product.stock == 0:
            del cart[id__]
        elif  qty > product.stock:
            qty = product.stock

        cart = request.session.get('cart', {})

        
        cart[id__] = {
            'quantity': qty
        }
        request.session['cart'] = cart
        request.session.modified = True
        return JsonResponse({"Response":"Done"})
    return HttpResponse("404")


def cart_delete(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id__ = str(data.get('id'))
            cart = request.session.get('cart', {})
            if id__ in cart:
                del cart[id__]
                request.session['cart'] = cart
                request.session.modified = True
                return JsonResponse({"removed_id": id__})
            else:
                return JsonResponse({"error": "Item not found in cart."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return HttpResponse("Method not allowed", status=405)
@login_required
def payment(request):
    return render(request, 'cart/payment.html')