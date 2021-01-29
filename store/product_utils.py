from . models import *
from users.models import Users
from .forms import RecommendProductForm
from django.shortcuts import redirect
from .views import store
import json
from django.http import JsonResponse
def recommend_product(request):
    data = json.loads(request.body.decode("utf-8"))
    # total_recommendations = Product.objects.values('total_recommendations', flat=True)
    PRODUCT_ID = data['productId']
    print("product id:",PRODUCT_ID)
    product = Product.objects.only('total_recommendations').get(id=PRODUCT_ID)
    product.total_recommendations += 1
    product.save()

    USER = Users.objects.get(name=request.session['user'])
    update_user_recommends(USER,PRODUCT_ID)
    return JsonResponse('Item was added', safe=False)
    # return redirect('/store/')

def update_user_recommends(user,product_id):
    if product_id not in user.products_recommend:
        user.products_recommend+=str(product_id+',')
        user.save()
    else:
        print('You already recommend it')
    
