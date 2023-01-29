from django.db import models


# Create your models here.
class Customer(models.Model):
    name = models.TextField()
    gender = models.TextField()
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "Customer"

class Products(models.Model):
    name = models.TextField()
    registerKey = models.TextField()
    customer_id=models.ForeignKey(Customer, on_delete=models.CASCADE)
    activate_IND= models.BooleanField()
    last_modify_date = models.DateTimeField(auto_now=True)
    register_date = models.DateTimeField()#auto_now_add=True

    class Meta:
        db_table = "Products"