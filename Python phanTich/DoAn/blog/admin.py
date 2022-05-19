from django.contrib import admin
from .models import Blog_Single

class Blog_SingleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug')

# Register your models here.
admin.site.register(Blog_Single, Blog_SingleAdmin)
