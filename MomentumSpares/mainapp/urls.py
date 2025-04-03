from django.urls import path #importing the path function from django

from . import views #importing the views from the mainapp to access the functions
urlpatterns = [
    path("",views.homeView,name='homepage'), #this is the path to the home page
    path("about",views.aboutView,name='aboutpage'),
    
    path('products/<int:pk>',views.ProductDetails.as_view(),name='prod_details'),#R
    path('products/add',views.AddProducts.as_view(),name='addprod'),#C
    path('products/edit/<int:pk>',views.UpdateProducts.as_view(),name='edit_prod'),#U
    path('products/delete/<int:pk>',views.DeleteProducts.as_view(),name='del_prod'),#D
   # search path
   path('products/search', views.searchView, name='search')
]
