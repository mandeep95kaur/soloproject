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
    



class ReviewManager(models.Manager):

    def basic_validator(self, post_data):
        errors = {}
        if len(post_data['review']) < 10:
            errors['review'] = 'Review should be at least ten characters long.'
        if int(post_data['rating']) < 1 or int(post_data['rating']) > 5:
            errors['rating'] = 'Review should be 1 to 5 stars.'
        return errors

class Review(models.Model):
    content = models.TextField()
    rating = models.IntegerField()
    user = models.ForeignKey(User, related_name = "reviews", on_delete = models.CASCADE)
    review_by = models.ManyToManyField(User, related_name="reviewer")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ReviewManager()


