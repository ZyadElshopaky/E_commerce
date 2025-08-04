from django.shortcuts import render

def contact_us(request):
    return render(request, 'core/contact_us.html')

def role_selection(request):
    return render(request, 'core/role_selection.html')

def seller(request):
    return render(request, 'core/seller.html')
