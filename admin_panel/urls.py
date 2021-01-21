from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_panel, name="admin_panel"),

    path('update_order_status/', views.update_order_status, name="update_order"),
    path('products/', views.products, name="products"),
    path('makeChanges/', views.makeChanges, name="makeChanges"),
    path('registered_users/', views.registered_users, name="registered_users"),
    path('deleteUsers/', views.deleteUsers, name="deleteUsers"),
    
]
