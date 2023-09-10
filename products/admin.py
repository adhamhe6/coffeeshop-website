from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    list_filter = ['is_active']
    search_fields = ['name', 'desc']

admin.site.register(Product, ProductAdmin)