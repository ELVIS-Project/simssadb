from django.db import models
from database.models.custom_base_model import CustomBaseModel
from django.contrib.auth.models import User
from database.models.institution import Institution


class Profile(CustomBaseModel):
    """Extends the user model to allow for extra data"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL,
                                    null=True, blank=True)

    def __str__(self):
        return "{0}".format(self.user.username)

    def prepare_summary(self):
        pass

    def detail(self):
        pass

    class Meta(CustomBaseModel.Meta):
        db_table = 'profile'
