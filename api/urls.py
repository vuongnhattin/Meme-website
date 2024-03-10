from django.contrib import admin
from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('items/', views.ItemView.as_view(), name='items'),
    path('items/<int:pk>', views.SingleItemView.as_view(), name='single_item'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/<int:pk>', views.SingleCartView.as_view(), name='single_cart'),
    path('download/<int:pk>', views.download_single_file, name='single_download'),
    path('download/', views.download_multiple_files, name='download'),
]
