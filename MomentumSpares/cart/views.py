from django.shortcuts import render, redirect, get_object_or_404
from mainapp.models import Product
from .models import CartItem  # Only import CartItem from cart.models
from orders.models import Order  # Import Order from orders.models
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


# Create your views here.

# C - Creating cart items

@login_required
def addToCart(request, product_id):
    this_product = Product.objects.get(id = product_id) # fetching the product object
    # When adding product to cart, we need to check if the same user has added the same product
    # to cart before, in that case, we will not create a new cart item, rather just increment 
    # quantity

    cart_item, created = CartItem.objects.get_or_create(product = this_product, user = request.user)
    cart_item.quantity += 1
    # above two statements are equivalent to `INSERT into table ... on duplicate key UPDATE ...` 
    cart_item.save() # save changes to SQL through Update

    return redirect('view_cart')

# R - Read Cartitems
@login_required
def viewCart(request):
    template = 'cart.html'
    cart_items = CartItem.objects.filter(user = request.user) 
    # the above statement is equivalent to : SELECT * FROM cartitem WHERE user = <USER_ID>;
    total_price = sum(float(item.product.price) * item.quantity for item in cart_items)

    context = {
        'cart_items' : cart_items,
        'total_price' : total_price
    }
    return render( request, template, context)


# D

def remFromCart(request, cart_item_id):
    this_cart_item = CartItem.objects.get(id = cart_item_id)
    this_cart_item.delete() # deletes the associated record as well as the cartitem obj in memory

    return redirect('view_cart')


# function based views for implementing the API endpoints for cart quantity updations
@login_required
def addQuantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    overall_total = sum(item.get_total_price() for item in CartItem.objects.filter(user=request.user))
    context = {
        'quantity': cart_item.quantity, 
        'total_price': cart_item.get_total_price(), 
        'overall_total': overall_total
        }
    return JsonResponse(context)

@login_required
def remQuantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        overall_total = sum(item.get_total_price() for item in CartItem.objects.filter(user=request.user))
        context = {
            'quantity': cart_item.quantity, 
            'total_price': cart_item.get_total_price(), 
            'overall_total': overall_total}
        return JsonResponse(context)
    else:
        cart_item.delete()
        overall_total = sum(item.get_total_price() for item in CartItem.objects.filter(user=request.user))
        context = {
            'quantity': 0, 
            'total_price': 0, 
            'overall_total': overall_total
            }
        return JsonResponse(context)

from django.contrib import messages
from django.http import HttpResponseBadRequest

def place_order(request):
    if request.method == 'POST':
        # Add logic to process the order
        # Example: Save order details, clear the cart, etc.
        messages.success(request, "Your order has been placed successfully!")
        return redirect('homepage')  # Redirect to the homepage or an order confirmation page
    return redirect('cart')  # Redirect back to the cart if accessed via GET

def checkout(request, order_id=None):
    if not order_id:
        return HttpResponseBadRequest("Order ID is required.")
    # Use the order_id in your logic
    return render(request, 'checkout.html', {'order_id': order_id})

def cart_view(request):
    # Fetch the current user's active order
    order = Order.objects.filter(user=request.user, status='active').first()
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(float(item.product.price) * item.quantity for item in cart_items)

    context = {
        'order': order,  # Pass the order object to the template
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart/cart.html', context)
