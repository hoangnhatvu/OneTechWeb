from .models import Category, Product

def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)

def list_view_product(request):
    list_view = Product.objects.all().order_by('-last_visit')
    return dict(list_view=list_view)