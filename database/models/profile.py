from django.db import models
from database.models.custom_base_model import CustomBaseModel
from django.contrib.auth.models import User
from database.models.institution import Institution


class Profile(CustomBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL,
                                    null=True)
    title = models.TextField(max_length=100, blank=True)


    class Meta(CustomBaseModel.Meta):
        db_table = 'profile'
