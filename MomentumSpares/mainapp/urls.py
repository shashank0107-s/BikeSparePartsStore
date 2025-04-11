from django.urls import path

from .views import homeView, aboutView, AddProduct, ProductDetails, UpdateProduct, DeleteProduct, searchView
# importing the views from the mainapp to access the functions

urlpatterns = [
    path("", homeView, name='homepage'),
    path("about", aboutView, name="aboutpage"),

    path('products/add',            AddProduct.as_view(),     name='add_prod'),       # C
    path('products/<int:pk>',       ProductDetails.as_view(), name='prod_details'),   # R
    path('products/edit/<int:pk>',  UpdateProduct.as_view(),  name = 'edit_prod'),    # U 
    path('products/del/<int:pk>',   DeleteProduct.as_view(),  name = 'del_prod'),     # D

    # Search path
    path('products/search', searchView, name = 'search')
]