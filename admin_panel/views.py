from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json

from store.models import *
from users.models import *
# Create your views here.


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

    totalProductsSelled = OrderItem.objects.values('order').count()
    totalOrders = OrderItem.objects.values('order').distinct().count()

    context = {
        'orders': orders,
        'total_income': totalIncome,
        'total_products_selled': totalProductsSelled,
        'total_orders': totalOrders

    }

    return render(request, 'index.html', context)


def update_order_status(request):
    data = json.loads(request.body.decode("utf-8"))

    print(data['orderid'])
    # orderID = OrderItem.objects.filter(order_id=data['orderid'])

    # for order in orderID:
    #    order = Order.objects.get(id=orderID)
    #    order.complete = 1
    #    order.save()

    order_items = OrderItem.objects.filter(order_id=data['orderid'])


    for order_item in order_items:
       order = order_item.order
       order.complete = True
       order.save()
    return JsonResponse(data)
