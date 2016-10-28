from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from ..loginreg.models import User
import datetime

# Create your models here.

class ProductManager(models.Manager):
    
    def productvalidate(self, data):
        errors = []
        if data['name'] == "" or data['name'] == '':
            errors.append("Product name cannot be blank!")
        return errors
    def createproduct (self, data, user):
        self.create(name=data['name'], users=User.objects.get(id=user))  #maybe change to self

    def join (self, trip_id, user_id):
        self.get(id=trip_id).join.add(user_id)

    def delete (self, trip_id, user_id):
        self.get(id=trip_id).join.remove(user_id)

class Product(models.Model):
    name = models.CharField(default="product", max_length = 30)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    join = models.ManyToManyField(User, related_name="Users_In_Trip")
    users = models.ForeignKey(User)
    objects=ProductManager()
