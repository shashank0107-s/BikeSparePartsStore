from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
# importing url resolution function
from django.urls import  reverse,reverse_lazy

# to help load the template file
from django.template import loader

#to help return an http response to the user for any given request
from django.http import HttpResponse


# importing the generic class based views for CRUD operations
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View

# Create your views here.
def home(request):
    return render(request, 'home.html')
    #querying the database and getting a collection of products class objecs from the records
    products = Product.objects.all()

    #creating a context dictionary to be used to render the template with info
    context = {
        'product_list': products, #the key we create here,
                                    #will be availlable

        'current_page': 'home'
    }
    template = loader.get_template('home.html')
    return HttpResponse(template.render(context, request))


def aboutView(request):
    context = {
        'current_page' : 'about'

    }
    template = loader.get_template('about.html')
    return HttpResponse(template.render(context, request))

def contactsView(request):
    context = {
        
                     

    }
    template = loader.get_template('contacts.html')
    return HttpResponse(template.render(context, request))

#views for adding, editing and deleting products
# C R U D
# Create
class AddProducts(CreateView):
    model = Product
    fields = ['name', 'price', 'desc', 'pic', 'stock']
    template_name = 'addproduct.html'
    success_url = reverse_lazy('homepage')  





    

#read - show details of  each product
class ProductDetails(DetailView):
    model = Product
    template_name = 'prod_details.html'
    context_object_name = 'prod'

#update
from django.urls import reverse
class UpdateProducts(UpdateView):
    model = Product
    fields = '__all__'
    template_name = 'editProduct.html'

    def get_success_url(self):
        return reverse('prod_details', kwargs={'pk': self.object.pk})

#delete
class DeleteProducts(DeleteView):
    model = Product
    template_name = 'delProduct.html'
    success_url = reverse_lazy('homepage')
    
## search results
def searchView(request):
    query = request.GET.get('search_text')
    # fetch the query text from GET request

    results = Product.objects.filter(name__icontains= query)
    # collect the product objects matching the name
    #this runs 'SELECT' FROM product WHERE name LIKE '%query%';
    #icontains is case insensitive
    #contains is case sensitive

    context = {
        'items': results,
        'query': query
    }
    template = loader.get_template('searchResults.html')
    return HttpResponse(template.render(context, request))

def home(request):
    products = Product.objects.all()  # Fetch all products from the database
    context = {
        'product_list': products,  # Pass the product list to the template
        'current_page': 'home'  # Set the current page for navigation
    }

    return render(request, 'home.html', context)  # Ensure 'home.html' exists in your templates folder

def about(request):
    return render(request, 'about.html')  # Add this view

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Logic to add the product to the cart (e.g., session or database)
    # For now, redirect back to the homepage or another page
    return redirect('homepage')

def view_cart(request):
    # Logic to retrieve cart items (e.g., from session or database)
    cart_items = []  # Replace with actual cart retrieval logic
    return render(request, 'cart.html', {'cart_items': cart_items})


