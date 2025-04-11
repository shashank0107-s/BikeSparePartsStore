from django.urls import path
from cart import views as cart_views

urlpatterns = [
    # ...existing URL patterns...
    path('checkout/<int:order_id>/', cart_views.checkout, name='checkout'),
]