from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    amount = models.FloatField()
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.description