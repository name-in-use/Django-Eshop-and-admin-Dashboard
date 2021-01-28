from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.db.models import Q
import json
from . models import *
from .forms import RecommendProductForm
import datetime
from base64 import b64encode
import base64
from users.models import Users
from .utils import cookieCart, cartData, guestOrder
import itertools
import re
# Create your views here.


def view_omega_brand(request):
    data = cartData(request)
    cartItems = data['cartItems']
    if 'user' in request.session:
        user = request.session['user']
    else:
        user = "Guest User"

    products = Product.objects.filter(Q(name__icontains="omega"))

    context = {
        'products': products,
        'user': user,
        'cartItems': cartItems
    }
    return render(request, 'store/watches.html', context)


def view_gucci_brand(request):
    data = cartData(request)
    cartItems = data['cartItems']
    if 'user' in request.session:
        user = request.session['user']
    else:
        user = "Guest User"

    products = Product.objects.filter(Q(name__icontains="gucci"))

    context = {
        'products': products,
        'user': user,
        'cartItems': cartItems
    }
    return render(request, 'store/watches.html', context)


def home_page(request):
    data = cartData(request)
    cartItems = data['cartItems']
    if 'user' in request.session:
        user = request.session['user']
    else:
        user = "Guest User"

    context = {
        'user': user,
        'cartItems': cartItems
    }

    return render(request, 'store/index.html', context)


def brands(request):
    data = cartData(request)
    cartItems = data['cartItems']
    if 'user' in request.session:
        user = request.session['user']
    else:
        user = "Guest User"

    context = {
        'user': user,
        'cartItems': cartItems
    }
    return render(request, 'store/brands.html', context)


# watches.html
def store(request):
    # call method from utils.py
    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()
    form = RecommendProductForm

    # get username from session
    if 'user' in request.session:
        user = request.session['user']
    else:
        user = "Guest User"

    user_recommendations_ = Users.objects.get(name=user).products_recommend
    print(user_recommendations_)
    print('products found in recommendations:',list(map(int, re.findall('\d+', user_recommendations_))))

    context = {
        'user_recommendations':list(map(int, re.findall('\d+', user_recommendations_))),
        'products': products,
        'user': user,
        'cartItems': cartItems
    }
    return render(request, 'store/watches.html', context)


def searchProduct(request):
    data = cartData(request)
    cartItems = data['cartItems']
    if 'user' in request.session:
        user = request.session['user']
    else:
        user = "Guest User"

    product_to_search = request.GET.get('product')

    products = Product.objects.filter(Q(name__icontains=product_to_search))
    context = {
        'products': products,
        'user': user,
        'cartItems': cartItems
    }
    return render(request, 'store/watches.html', context)


def contactUs(request):
    data = cartData(request)
    cartItems = data['cartItems']
    if 'user' in request.session:
        user = request.session['user']
    else:
        user = "Guest User"
    context = {
        'user': user,
        'cartItems': cartItems
    }
    return render(request, 'store/contact.html', context)

# def searchProduct(request):
#     data = cartData(request)
#     cartItems = data['cartItems']
#     if 'user' in request.session:
#         user = request.session['user']
#     else:
#         user = "Guest User"

#     product_to_search = request.GET.get('product')
#     products = Product.objects.filter(Q(name__icontains=product_to_search))
#     # print(products)
#     context = {
#         'products': products,
#         'user': user,
#         # 'images' :[base64.b64encode(product_image.image).decode() for product_image in products],
#         'cartItems': cartItems
#     }
#     return render(request, 'store/store.html', context)


def cart(request):

   # call method from utils.py
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    # get username from session
    if 'user' in request.session:
        user = request.session['user']
    else:
        user = "Guest User"

    context = {
        'user': user,
        'items': items,
        'order': order,
        'cartItems': cartItems
    }
    return render(request, 'store/cart.html', context)


def checkout(request):

    # call method from utils.py
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    if 'user' in request.session:
        user = request.session['user']
    else:
        user = "Guest User"

    if 'email' in request.session:
        email = request.session['email']
    else:
        email = ""

    context = {
        'user': user,
        'email': email,
        'items': items,
        'order': order,
        'cartItems': cartItems
    }
    return render(request, 'store/checkout.html', context)


# def updateItem(request):
#     data = json.loads(request.body)
#     productId = data['productId']
#     action = data['action']

#     user = data['user']
#     customer = Users.objects.get(name=user).id

#     print('Action:', action)
#     print('productId:', productId)
#     print('Customer:', customer)

#     product = Product.objects.get(id=productId)
#     order, created = Order.objects.get_or_create(
#         customer=customer, complete=False)

#     orderItem, created = OrderItem.objects.get_or_create(
#         order=order, product=product)
#     if action == 'add':
#         orderItem.quantity = (orderItem.quantity+1)
#     elif action == 'remove':
#         orderItem.quantity = (orderItem.quantity-1)
#     orderItem.save()

#     if orderItem.quantity <= 0:
#         orderItem.delete()

#     return JsonResponse('Item was added', safe=False)


@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    # customer=Customer.objects.get(name=request.session['user'])
    # print(customer)
    # order = Order.objects.get_or_create(
    #     customer=customer, complete=False)
    customer, order, customer_id = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    ShippingAddress.objects.create(
        customer=customer_id,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode'],
    )
    return JsonResponse("Payment complete", safe=False)
