from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'app'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('items/', views.items_view, name='items'),
    path('cart/', views.cart_view, name='cart'),
    path('upload/', views.upload_view, name='upload'),
    path('upload_success/', views.upload_success_view, name='upload_success'),
]
