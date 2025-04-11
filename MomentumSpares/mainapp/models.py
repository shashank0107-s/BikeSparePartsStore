from django.db import models

# Create your models here.
# In the models module imported above, there is a class called `Model`.
# Automatic ORM(Object Relational Mapping) methods are already pre-designed in this class

# Now let's create the schema for our project
# We need products

# Any time we make any changes in the class definitions, especially the variables, 
# we need to run two commands.
# 1. python manage.py makemigrations <app_name>
#       -> This generates python scripts inside the app's migrations folder.
#       -> It will track the models.py and check for changes.
#       -> Necessary DDL statements will be generated to be sent to the DB 
# 2. python manage.py migrate
#       -> It executes the scripts, thereby running the DDL operations.
class Product(models.Model):
    # list out all the object variables below and initialize with certian classes.
    # refer https://docs.djangoproject.com/en/5.1/ref/models/fields/#model-field-types
    # for the classes to use for initializing the attributes.

    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField(null=False)
    desc = models.TextField()
    pic = models.ImageField(upload_to="products/", null = False)
    stock = models.PositiveIntegerField(default = 1)