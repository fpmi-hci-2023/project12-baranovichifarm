from django.db import models
from django.contrib import admin


class Customer(models.Model):
    email = models.EmailField(unique=True)
    lastname = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.email


admin.site.register(Customer)