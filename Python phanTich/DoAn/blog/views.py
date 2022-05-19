from django.shortcuts import render
from .models import Blog_Single

# Create your views here.
def Blog(request):
    blogs = Blog_Single.objects.filter.all()
    context = {
        'blogs': blogs
    }
    return render(request, 'blog/blog.html', context)

def Blog_Single(request, blog_single_slug = 0):
    blog_single = Blog_Single.objects.get(slug=blog_single_slug)
    context = {
        'blog_single': blog_single
    }
    return render(request, 'blog/blog_single.html', context)