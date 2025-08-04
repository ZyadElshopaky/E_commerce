from django.urls import path
from .views import *
urlpatterns = [
    path("/signup",signup_user,name="signup"),
    path("/logoin",login_user,name="login"),
    path("/logout",logout_user,name="logout"),
    path("/role_selection/",select_role_view,name="role_selection"),
    path("/seller/",seller,name="seller"),
]
