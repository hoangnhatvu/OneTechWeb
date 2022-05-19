from django.db import models
from django.urls import reverse

# Create your models here.
class Blog_Single(models.Model):
    title = models.CharField(max_length=100, unique = True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='photos/blogs')
    content = models.TextField(max_length=1000)

    def get_url(self):
        return reverse('product_detail', args=[self.slug])

    def __str__(self):
        return self.title