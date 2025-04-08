from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homepage'),  # Home view
    path('about/', views.about, name='aboutpage'),  # About view
    path('products/<int:pk>', views.ProductDetails.as_view(), name='prod_details'),  # R
    path('products/add', views.AddProducts.as_view(), name='addproduct'),  # C
    path('products/edit/<int:pk>', views.UpdateProducts.as_view(), name='edit_prod'),  # U
    path('products/delete/<int:pk>', views.DeleteProducts.as_view(), name='del_prod'),  # D
    path('products/search', views.searchView, name='search'),  # Search path
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Add to cart
    path('cart/', views.view_cart, name='view_cart'),  # View cart
]
