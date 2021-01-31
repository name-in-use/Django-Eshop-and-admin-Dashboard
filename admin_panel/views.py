from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from django.db.models import Sum

from .forms import Upload_New_Product_Form
from store.models import *
from users.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect

# database connection
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
# Create your views here.

# ADMIN PANEL HOME


def admin_panel(request):

    orders = OrderItem.objects.select_related(
        'customer').all().order_by('customer')

    # total income
    totalIncome = 0
    for product in OrderItem.objects.all():
        productPrice = Product.objects.get(id=product.product_id).price

        Product_quantity = product.quantity

        total = productPrice*Product_quantity
        totalIncome += total

    # totalProductsSelled = OrderItem.objects.values('order').count()
    totalProductsSelled = OrderItem.objects.aggregate(Sum('quantity'))
    # print(totalProductsSelled)
    totalOrders = OrderItem.objects.values('order').distinct().count()

    context = {
        'orders': orders,
        'total_income': totalIncome,
        'total_products_selled': totalProductsSelled['quantity__sum'],
        'total_orders': totalOrders

    }

    return render(request, 'index.html', context)

# update an order status to DONE


def update_order_status(request):
    data = json.loads(request.body.decode("utf-8"))
    print(data['orderid'])
    order_items = OrderItem.objects.filter(order_id=data['orderid'])
    for order_item in order_items:
        order = order_item.order
        order.complete = True
        order.save()
    return JsonResponse(data)


def registered_users(request):

    users = Users.objects.all()
    context = {
        'users': users
    }
    return render(request, 'users.html', context)


def deleteUsers(request):
    data = json.loads(request.body.decode("utf-8"))
    userID = data['userID']

    user = Users.objects.get(id=userID).delete()

    return JsonResponse(data)

#------------Product managment---------------#


def products(request):
    form = Upload_New_Product_Form()
    products = Product.objects.all()
    total_products = Product.objects.values('name').count()

    context = {
        'total_products':total_products,
        'products': products,
        'new_product_form': form
    }
    return render(request, 'products.html', context)


@csrf_exempt
def makeChanges(request):
    if request.method == 'POST':
        productID = request.POST['productid']
        productNAME = request.POST['productname']
        productPRICE = request.POST['productprice']
        print(productNAME, productPRICE, productID)

        # product = Product.objects.get(id=productID)
        # product.name = productNAME
        # product.price = productPRICE
        # product.save()
        product = Product.objects.filter(id=productID).update(
            name=productNAME, price=productPRICE)

    return HttpResponseRedirect('/adminpanel/products/')


def Upload_New_Product_View(request):
    if request.method == 'POST':

        _id = request.POST['product_id']
        name = request.POST['name']
        price = request.POST['price']
        image = request.POST['image']
        print(image)
        new_product = Product.objects.create(id=_id,name=name,price=price,image=image,total_recommendations='0')
        new_product.save()
        return redirect('products')


