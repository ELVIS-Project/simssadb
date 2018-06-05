from django.db import models
from database.models.custom_base_model import CustomBaseModel
from django.contrib.auth.models import User


class Profile(CustomBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.TextField(max_length=100, blank=True)
    title = models.TextField(max_length=100, blank=True)


    class Meta(CustomBaseModel.Meta):
        db_table = 'profile'
