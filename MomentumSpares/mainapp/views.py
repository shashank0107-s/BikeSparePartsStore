from django.shortcuts import render
from .models import Product

# importing url resolution tools
from django.urls import reverse, reverse_lazy

# to help load the template file
from django.template import loader

# to help return an Http response to the user for any given request
from django.http import HttpResponse

# importing the generic class based views for CRUD operations

from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

# Create your views here.

def homeView(request):
    # querying the DB and getting a collection of Product class objects from the records
    products = Product.objects.all() # select * from Product;
    # creating a context dictionary to be used to render the template with info
    context = {
        'product_list' : products, # the key we create here, 
                                # will be available as a variable in template design
                                # in 'home.html'
        'current_page' : 'home'
    }
    template = loader.get_template('home.html')
    return HttpResponse(template.render(context, request))

def aboutView(request):

    context = {
        'current_page' : 'about'
    }
    template = loader.get_template('about.html')
    return HttpResponse(template.render(context, request))



# Views for adding, editing and deleting products
 
# C R U D
# Create
class AddProduct(CreateView):
    model = Product
    fields = ['name', 'price','desc','pic','stock']
    template_name = 'addProduct.html'
    success_url = reverse_lazy('homepage') 

# Read -> show details of each product
class ProductDetails(DetailView):
    model = Product
    template_name = 'prod_details.html'
    context_object_name = 'prod'

# Update ->

class UpdateProduct(UpdateView):
    model = Product
    fields = '__all__'
    template_name = 'editProduct.html'

    # overriding a method to produce dynamic redirection according to product id.
    def get_success_url(self):
        return reverse('prod_details', kwargs = {'pk' : self.object.pk})
    
# Delete 
class DeleteProduct(DeleteView):
    model = Product
    template_name = 'delProduct.html'
    success_url = reverse_lazy('homepage')


## Search results

def searchView(request):
    query = request.GET.get('search_text') 
    # fetch the query text from GET request 
    
    results = Product.objects.filter(name__icontains = query) 
    # collect the product objects matching the name
    # This runs 'SELECT * FROM product WHERE name like '%<query>%';
    # icontains is case-insensitive
    # contains can be used for case-sensitive
    
    context = {
        'items' : results,
        'query' : query
    }
    template = loader.get_template('searchResults.html')
    return HttpResponse(template.render(context, request))
    