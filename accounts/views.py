from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from .models import CustomUser
from django.contrib import messages
from .forms import *

def signup_user(request):
    form = SignupForm() 
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Submitted successfully!")
            return redirect("role_selection")
        else:
            messages.error(request, "There was an error.")
            return render(request, "accounts/signup.html", {"form": form})
    return render(request, "accounts/signup.html", {"form": form})

# Login ser
def login_user(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            try:
                user = CustomUser.objects.get(email__iexact=email)
            except CustomUser.DoesNotExist:
                user = None

            if user is not None and user.check_password(password):
                if user.is_active:
                    login(request, user)
                    messages.success(request, "Logged in successfully!")
                    next_url = request.GET.get("next")
                    if next_url and url_has_allowed_host_and_scheme(
                        url=next_url,
                        allowed_hosts={request.get_host()},
                        require_https=request.is_secure(),
                    ):
                        return redirect(next_url)
                    return redirect("home")
                else:
                    messages.error(request, "Account is deactivated.")
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_user(request):
    logout(request)
    return redirect("home")

def home(request):
    return render(request,"home.html")

@login_required(login_url="login")
def select_role_view(request):
    if  request.user.is_seller :
        return redirect("seller")
    
    if request.method == "POST":
        role = request.POST.get("role")
        print(role)
        if role == "buyer":
            return redirect("home")
        elif role == "seller":
            seller=CustomUser.objects.get(id=request.user.id)
            seller.is_seller=True
            seller.save()
            return redirect(request,"seller")
        elif role == "admin":
            return redirect("contact_us")
    return render(request, "accounts/role_selection.html")

@login_required(login_url="login")
def seller(request):
    if not request.user.is_seller :
        return redirect("seller")
    return render(request, 'accounts/seller.html')