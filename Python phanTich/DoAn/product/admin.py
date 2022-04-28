from django.contrib import admin
from .models import Products,Category

class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

# Register your models here.
admin.site.register(Products, AdminProduct)
admin.site.register(Category)
