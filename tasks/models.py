from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    description = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    done = models.BooleanField(default=False)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
