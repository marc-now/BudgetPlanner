from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    name = models.CharField(max_length=32)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")

class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)

class Subcategory(models.Model):
    name = models.CharField(max_length=32)
    category = models.ForeignKey(Category, null=False ,on_delete=models.CASCADE, related_name="subcategories")

    class Meta:
        unique_together = ('category', 'name')

class Entry(models.Model):
    title = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=12, decimal_places=2)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="entries")
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name="expenses")
    subcategory = models.ForeignKey(Subcategory, null=True, blank=True, on_delete=models.SET_NULL, related_name="expenses")
    description = models.CharField(max_length=256, null=True, blank=True,)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.title} - {self.value} - {self.date}"