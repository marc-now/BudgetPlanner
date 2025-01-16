from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    name = odels.CharField(max_length=32)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")

class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)

class Entry(models.Model):
    title = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=8, decimal_places=2)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="entries")
    category - model.ForeignKey(Category, related_name="expenses")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{title} - {value} - {date}"