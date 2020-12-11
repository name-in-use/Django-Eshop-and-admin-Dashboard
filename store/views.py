from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
import json
from . models import *
import datetime
from base64 import b64encode
import base64
from users.models import Users
from .utils import cookieCart, cartData
# Create your views here.


def store(request):
    # call method from utils.py
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    # get username from session
    if 'user' in request.session:
        user = request.session['user']
    else:
        user = "Guest User"

    context = {
        'products': products,
        'user': user,
        # 'images' :[base64.b64encode(product_image.image).decode() for product_image in products],
        'cartItems': cartItems
    }
    return render(request, 'store/store.html', context)


def searchProduct(request):
    data = cartData(request)
    cartItems = data['cartItems']
    if 'user' in request.session:
        user = request.session['user']
    else:
        user = "Guest User"

    product_to_search = request.GET.get('product')
    products = Product.objects.filter(Q(name__icontains=product_to_search))
    # print(products)
    context = {
        'products': products,
        'user': user,
        # 'images' :[base64.b64encode(product_image.image).decode() for product_image in products],
        'cartItems': cartItems
    }
    return render(request, 'store/store.html', context)


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


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    user = data['user']
    customer = Users.objects.get(name=user).id

    print('Action:', action)
    print('productId:', productId)
    print('Customer:', customer)

    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity+1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity-1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
    return JsonResponse("Payment complete", safe=False)
