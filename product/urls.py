from django.urls import path

from .views import product_products,detail_product,add_to_cart,update_cart,checkout

app_name = "product"

urlpatterns = [
    path('',product_products,name='products'),
    path('product_detail/<int:product_id>', detail_product, name='detail'),
    path('add-to-cart/', add_to_cart, name='add-to-cart'),
    path('update-cart/', update_cart, name='update-cart'),
    path('checkout/', checkout, name='checkout'),

]