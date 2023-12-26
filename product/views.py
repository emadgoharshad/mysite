import json

from django.shortcuts import render,redirect
from django.http import JsonResponse



from account.models import Account
from .models import Product,Payment,Cart,Category,Order


def product_products(request):
    products = Product.objects.all()

    context = {
        'products':products,
    }
    return render(request,'product/products.html',context)


def detail_product(request,product_id):
    product = Product.objects.get(id=product_id)

    dic = {
        'product': product,
    }

    return render(request,'product/product_detail.html',dic)



def add_to_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            product_id = int(request.POST.get('product_id'))
            product_check = Product.objects.filter(id=product_id)

            if product_check:
                if Cart.objects.filter(user=request.user,product=product_id):
                    return JsonResponse({'status': 'this cart is already '})
                else:
                    product_num = 1
                    Cart.objects.create(user=request.user,product_id=product_id,quantity=product_num)
                    return JsonResponse({'status': ' product added successfully '})
            else:
                return JsonResponse({'status':' no such product found'})
        else:
            return JsonResponse({'status': ' login to continue '})
        return redirect('/')




def checkout(request):
    cart_total = 0
    price_total = 0
    cart = Cart.objects.filter(user=request.user)

    for item in cart:
        price_total += (item.product.price) * (item.quantity)
        cart_total += item.quantity

    context = {
        'cart_total':cart_total,
        'price_total' : price_total,
        'cart_items':cart,
        'cart_count':cart.count(),
    }

    return render(request,'product/checkout.html',context)


def update_cart(request):
    data = json.loads(request.body)
    prod_id = data['productId']
    action = data['action']

    cart = Cart.objects.filter(user=request.user,product=prod_id)[0]


    if cart:
        if action == 'add':
            cart.quantity += 1
        if action == 'remove':
            cart.quantity -= 1

        cart.save()

        if cart.quantity == 0:
            cart.delete()

        return JsonResponse({'status':'successfully'})









