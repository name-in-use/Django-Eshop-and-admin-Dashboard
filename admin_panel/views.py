from django.shortcuts import render
from django.shortcuts import render,redirect

from store.models import *
from users.models import *
# Create your views here.
def admin_panel(request):
    
    orders=OrderItem.objects.select_related('customer').all().order_by('customer')
    
    #total income
    totalIncome = 0
    for product in OrderItem.objects.all():
        productPrice=Product.objects.get(id=product.product_id).price
        
        Product_quantity = product.quantity

        total=productPrice*Product_quantity
        totalIncome+=total
    print(totalIncome)

    totalProductsSelled = OrderItem.objects.values('order').count()
    print('total products selled',totalProductsSelled)

    totalOrders = OrderItem.objects.values('order').distinct().count()
    print('total orders',totalProductsSelled)
    context={
        'orders':orders,
        'total_income':totalIncome,
        'total_products_selled':totalProductsSelled,
        'total_orders':totalOrders
        
    }

    return render(request, 'index.html', context)
