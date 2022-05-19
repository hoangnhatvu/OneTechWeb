from django.urls import path
from . import views

urlpatterns = [
    path('blog/',views.Blog, name = 'blog'),
    path('blog/<slug:blog_single_slug>/', views.Blog_Single, name='blog_single'),
]