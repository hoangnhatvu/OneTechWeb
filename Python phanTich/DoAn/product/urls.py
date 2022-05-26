from django.urls import path
from . import views

urlpatterns = [
    path('search/<str:description>', views.search, name='search'),
<<<<<<< HEAD
=======
    # path('category/<str:category>/', views.search, name='product_category'),
>>>>>>> ea204b3d38bcb43884b9557e2c7a9d93e4591eee
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
]