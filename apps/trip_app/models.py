from __future__ import unicode_literals
from django.db import models
from datetime import date
from datetime import datetime
import re

# add new manager class for User and a built-in method that validates form data
class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}

        #validate first name
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First name must be at least 2 letters'
        if str.isalpha(postData['first_name']) == False:
            errors['first_name'] = 'Only letters are allowed in first name'

        #validate last name
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 letters'
        if str.isalpha(postData['last_name']) == False:
            errors['last_name'] = 'Only letters are allowed last name'

        #validate email
        if len(postData['email']) < 1:
            errors['email_length'] = 'Email too short'
        if User.objects.filter(email=postData['email']).exists():
            errors['same_email'] = 'Email already used'
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9-.]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid email address'

        #validate password and password confirmation
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        if postData['confirm_password'] != postData['password']:
            errors['password'] = 'Passwords much match'
        
        return errors

    def login_validator(self, postData):
        errors = {}
        
        if len(postData['email']) < 1:
            errors['email_length'] = 'Email too short'
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9-.]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid email address'

        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'

        return errors

class TripManager(models.Manager):
    def trip_validator(self, postData):
        errors = {}

        if len(postData['destination']) < 3:
            errors['Destination'] = 'Must enter Destination of at least 3 characters'

        start_date = datetime.strptime(postData['start_date'], '%Y-%m-%d')
        if start_date < datetime.today():
            errors['start_date_past'] = 'Start date must be a future date'
        if len(postData['start_date']) < 1:
            errors['start_date'] = 'Must enter start date'

        end_date = datetime.strptime(postData['end_date'], '%Y-%m-%d')
        if end_date < datetime.today():
            errors['end_date_past'] = 'End date must be a future date'

        if len(postData['end_date']) < 1:
            errors['end_date'] = 'Must enter end date'

        if len(postData['plan']) < 3:
            errors['plan'] = 'Must enter plan of at least 3 characters'

        return errors




class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #trip_uploaded
    #liked_trips
    objects = UserManager()

    def __repr__(self):
        return f'<User id: {self.id}, First Name: {self.first_name}, Last Name: {self.last_name}, Email: {self.email}, Password: {self.password}>'

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name='trip_uploaded')
    users_who_like = models.ManyToManyField(User, related_name='liked_trips')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()

    def __repr__(self):
        return f'<Trip id: {self.id}, Destination: {self.destination}, Start Date: {self.start_date}, End Date: {self.end_date}, Plan: {self.plan}>'
