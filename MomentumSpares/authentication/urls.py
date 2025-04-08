from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainapp.urls')),  # Include the mainapp URLs
    path('auth/', include('authentication.urls')),  # Include the authentication URLs
]

# filepath: d:\PROJECTS\Bike-spare-parts-Project\MomentumSpares\authentication\urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),  # Signup view
    path('signin/', views.signin, name='signin'),  # Signin view
    path('logout/', views.logout_view, name='logout'),  # Logout view
]