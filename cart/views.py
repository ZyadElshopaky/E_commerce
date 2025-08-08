from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from products.models import Product
from django.http import JsonResponse,HttpResponse
import json
# @login_required(login_url="login")
def cart_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=list(cart.keys()))
    print(products)
    return render(request, 'cart/cart.html', context={"products": products })
def cart_add(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id__ = str(data.get('id'))
        qty = data.get('qty')
        print( id__,qty)
        cart = request.session.get('cart', {})
        if id__ in cart:
            cart[id__]['quantity'] += qty
        else:
            cart[id__] ={
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
                return JsonResponse({"response": "Item removed from cart."})
            else:
                return JsonResponse({"error": "Item not found in cart."}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return HttpResponse("Method not allowed", status=405)