from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('dish-list/', views.dish_list, name='dish_list'),
    path('add-to-cart/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/update/<int:dish_id>/', views.cart_update, name='cart_update'),
    path('cart/remove/<int:dish_id>/', views.cart_remove, name='cart_remove'),
]
