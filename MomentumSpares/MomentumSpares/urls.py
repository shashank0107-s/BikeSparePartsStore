"""
URL configuration for shop419 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from cart import views  # Import the views module from the cart app

# adding this line to support hosting of static files
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainapp.urls')), # to include the paths configured in the app, here
    path('', include('cart.urls')),
    path('', include('payments.urls')),
    path('auth/', include('authentication.urls')), # including our authentication app urls
    path('auth/', include('django.contrib.auth.urls')), # including django's inbuilt auth urls
    path('orders/', include('orders.urls')),  # Ensure this is unique
     path('payments/',include('payments.urls')),  # Reference the checkout view   
    ]

# the following line allows us to use the given media path during development
if settings.DEBUG == True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)