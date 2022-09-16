from django.contrib import admin

from .models import Category, Product, ProductPhoto

admin.site.register([Category, Product, ProductPhoto])
