from django.urls import path
from .views import HomeView, Login, Signup, home, logout, ShopView

urlpatterns = [
    path('',HomeView.as_view(), name = 'homepage'),
    path('home', home , name='home'),

    path('store',ShopView.as_view(), name = 'store'),
    path('login',Login.as_view(), name = 'login'),
    path('signup',Signup.as_view(), name = 'signup'),
    path('logout', logout , name='logout'),
]