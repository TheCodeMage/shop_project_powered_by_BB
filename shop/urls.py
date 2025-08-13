from django.urls import path
from . import views

urlpatterns = [
    # Home & Shop
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('shop/product/<int:product_id>/', views.product_detail, name='product_detail'),

    # Cart
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_quantity, name='update_quantity'),
    path('cart/remove-item/<int:item_id>/', views.remove_item, name='remove_item'),
    path('cart/checkout/', views.checkout, name='checkout'),
    path('cart/add-with-quantity/<int:product_id>/', views.add_to_cart_with_quantity, name='add_to_cart_with_quantity'),
    path('cart/count/', views.get_cart_count, name='get_cart_count'),

    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
