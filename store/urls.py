from django.urls import path
from . import views

urlpatterns=[
    path('',views.home_page,name = "home_page"),
    path('store/',views.store,name = "store"),
    path('brands/',views.brands,name = "brands"),
    path('cart/',views.cart,name = "cart"),
    path('contact/',views.contactUs,name = "contact"),
    path('checkout/',views.checkout,name = "checkout"),
    
    # path('search_product/',views.searchProduct,name = "searchProduct"),
    # path('update_item/',views.updateItem,name = "update_item"),
    path('process_order/',views.processOrder,name = "process_order"),



]