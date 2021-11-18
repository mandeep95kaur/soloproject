from django.db import models
from datetime import datetime
import re
from django.contrib.auth.models import User


CATEGORY_CHOICES = (
    ('N', 'Non-veg'),
    ('V', 'Vegetarian'),
    ('D', 'Drinks')
)

STATE_CHOICES =(
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('CA', 'California'),
    ('FL', 'Florida'),
    ('GA', 'Gorgia'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('NY', 'New York')
)



class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(choices=STATE_CHOICES,max_length=50)
    zipcode = models.IntegerField()


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField()
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    image = models.ImageField(upload_to='productimg')

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    content = models.CharField(max_length=255)
    rating = models.IntegerField()
    creater = models.ForeignKey(User, on_delete=models.CASCADE)
    review_by = models.ManyToManyField(User, related_name="reviewer")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    

