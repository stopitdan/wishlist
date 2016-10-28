from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import datetime

import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate(self, data):
        print(data['password'])
        errors = []
        if len(data['name']) < 3:
            errors.append("Your name must be at least 3 characters long.")
            if not data['name'].isalpha():
                errors.append("Your name can't have numbers")
        if len(data['username']) < 3:
            errors.append("Your username must be at least 3 characters long.")
        same = User.objects.filter(username=data['username'])
        if same:
            errors.append("Username has already been taken.")
        if len(data['password']) < 8:
            errors.append("Your password must be at least 8 characters long.")
        if not data['password'] == data['password_confirm']:
            errors.append("Passwords do not match")
        if len(errors) == 0:
            pw_hash = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(name=data['name'], username=data['username'], hire_date=data['hire_date'], password = pw_hash)
            return(True, user)
        else:
            return(False, errors)
            
    def login(self ,data):
        try:
            user = User.objects.get(username = data['username'])
            password = data['password'].encode()
            if bcrypt.checkpw(password, user.password.encode()):
                print(user.password)
                return(True, user)
            else:
                return(False, "WRONG PASSSWORD MAN")
        except ObjectDoesNotExist:
            return(False, "Account not found")


class User(models.Model):
    name = models.CharField(max_length = 30)
    username = models.CharField(max_length = 30)
    password = models.CharField(max_length = 250)
    hire_date = models.DateField(default=datetime.date.today)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
