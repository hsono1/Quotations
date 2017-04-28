from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
from datetime import date, datetime, timedelta

EMAIL_REGEX = re.compile (r'^[a-zA-Z0-9.+_]+@[a-zA-Z0-9._-]+[a-zA-Z]+$')
NAME_REGEX = re.compile (r'^[a-zA-Z]+$')

class UserManager(models.Manager):
    def val_Reg(self, postData):
        status = True
        errorlist = []
        if not NAME_REGEX.match(postData['first_name']):
            errorlist.append("Not a valid first name!")
        if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
            errorlist.append("Name must have at least 2 letters")
            status = False
        if not NAME_REGEX.match(postData['last_name']):
            errorlist.append("Not a valid last name")
            status = False
        if not EMAIL_REGEX.match(postData['email']):
            errorlist.append("Not a valid email")
            status = False
        if len(postData['password']) < 8:
            errorlist.append("Password must be at least 8 characters")
            status = False
        if postData['password'] != postData['confirm']:
            errorlist.append("Passwords do not match!")
            status = False
        if len(User.objects.filter(email=postData['email'])) > 0:
            errorlist.append("Email is already registered!")
            status = False
        if status == False:
            return {'errors': errorlist}
        else:
            password = postData['password']
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            user = User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], password=hashed)
            return {'register': user}

    def val_Login(self, postData):
        user = User.objects.filter(email=postData['email'])
        status = True
        errorlist = []
        if len(postData['email']) < 1 or len(postData['password']) < 1 :
            errorlist.append("Please enter valid email and password")
            return {'errors': errorlist}
        if not EMAIL_REGEX.match(postData['email']):
            errorlist.append("Not a valid email")
            return {'errors': errorlist}
        if len(user) < 1:
            errorlist.append("You need to register first")
            status = False
        if status == False:
            return {'errors': errorlist}
        else:
            if bcrypt.hashpw(postData['password'].encode(), user[0].password.encode()) == user[0].password:
                return {'register': user[0]}
            else:
                errorlist.append("Incorrect Password")
                return {'errors': errorlist}



class User(models.Model):
    objects = UserManager()
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Quote(models.Model):
    author = models.CharField(max_length= 255)
    message = models.TextField(max_length = 1000)
    creator = models.ForeignKey(User, related_name= "u_creator", null= True)
    favorites = models.ManyToManyField(User, null=True)







