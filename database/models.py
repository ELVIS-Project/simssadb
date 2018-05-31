from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.TextField(max_length=100, blank=True)
    title = models.TextField(max_length=100, blank=True)
