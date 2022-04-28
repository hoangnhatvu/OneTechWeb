from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Customers(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    # to save the data
    def register(self):
        self.save()

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customers.objects.get(email=email)
        except:
            return False

    @staticmethod
    def get_all_customers():
        return Customers.objects.all()

    def isExists(self):
        if Customers.objects.filter(email=self.email):
            return True
        return False
