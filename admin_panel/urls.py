from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_panel, name="admin_panel"),

    path('update_order_status/', views.update_order_status, name="update_order"),
    path('products/', views.products, name="products"),
    path('makeChanges/', views.makeChanges, name="makeChanges"),

    #----------USERS------------#
    path('registered_users/', views.registered_users, name="registered_users"),
    path('deleteUsers/', views.deleteUsers, name="deleteUsers"),
    path('editUsers/<int:pk>/', views.editUsers, name="editUsers"), 
    path('SaveEditedUser/<int:pk>/', views.SaveEditedUser, name="SaveEditedUser"),   

    path('new_product/', views.Upload_New_Product_View, name="upload_new_product"),
    
]
