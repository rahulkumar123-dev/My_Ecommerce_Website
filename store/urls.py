from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
  path('', views.product_list, name='product-list'),
  path('product/<int:product_id>/', views.product_detail, name='product-cart'),
  path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
  path('ajax/update-cart/', views.ajax_update_cart, name='ajax-update-cart'),
  path('buy-now/<int:product_id>/', views.buy_now, name='buy-now'),
  path('cart/', views.view_cart, name='cart'),
  path('update-cart/', views.update_cart, name='update-cart'),
  path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove-from-cart'),
  path('checkout/', views.checkout, name='checkout'),
  path('thankyou/', views.thankyou, name='thankyou'),
  path('order-history/', views.order_history, name='order-history'),
  path('return-order/<int:order_id>/', views.return_order, name='return-order'),
  path('get-cities/<int:state_id>/', views.get_cities, name='get-cities'),
  path('login/', views.user_login, name='login'),
  path('logout/', views.user_logout, name='logout'),
  path('register/', views.register, name='register'),
]