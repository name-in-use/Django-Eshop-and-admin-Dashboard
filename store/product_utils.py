from . models import *
from .forms import RecommendProductForm
from django.shortcuts import redirect
from .views import store


def recommend_product(request):
    # total_recommendations = Product.objects.values('total_recommendations', flat=True)
    PRODUCT_ID = request.POST['product']
    # print(PRODUCT_ID) 
    product = Product.objects.only('total_recommendations').get(id=PRODUCT_ID)
    product.total_recommendations +=1
    product.save()
    
   
    return redirect('store')


