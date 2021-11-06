from django.db import models
from datetime import datetime
import re
import bcrypt

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        # Length of the first name
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least two characters long"

        # Length of the last name
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least two characters long"

        # Email matches format
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['email']) == 0:
            errors['email'] = "You must enter an email"
        elif not email_regex.match(postData['email']):
            errors['email'] = "Must be a valid email"

        # Email is unique
        current_users = User.objects.filter(email=postData['email'])
        if len(current_users) > 0:
            errors['duplicate'] = "That email is already in use"

        #Address must be entered
        if len(postData['address'])== 0:
            errors['address'] = "You must enter address"

        #City must be entered
        if len(postData['city'])== 0:
            errors['city'] = "You must enter city" 
        
        #state must be entered
        if len(postData['state'])== 0:
            errors['state'] = "You must enter state"

        # Password was entered (less than 8)
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characers long"
        if postData['password'] != postData['confirm_password']:
            errors['mismatch'] = "Your passwords do not match"

        return errors

    def update_validator(self, postData):
        errors = {}
        # Length of the first name
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least two characters long"

        # Length of the last name
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least two characters long"

        # Email matches format
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['email']) == 0:
            errors['email'] = "You must enter an email"
        elif not email_regex.match(postData['email']):
            errors['email'] = "Must be a valid email"
        
        #Address must be entered
        if len(postData['address'])== 0:
            errors['address'] = "You must enter address"

        #City must be entered
        if len(postData['city'])== 0:
            errors['city'] = "You must enter city" 
        
        #state must be entered
        if len(postData['state'])== 0:
            errors['state'] = "You must enter state"
        
        return errors



    def login_validator(self, postData):
        errors = {}
        check = User.objects.filter(email=postData['login_email'])
        if not check:
            errors['login_email'] = "Email has not been registered."
        else:
            if not bcrypt.checkpw(postData['login_password'].encode(), check[0].password.encode()):
                errors['login_email'] = "Email and password do not match."
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = UserManager()

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


