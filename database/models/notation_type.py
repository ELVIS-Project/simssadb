from django.db import models
from database.models.custom_base_model import CustomBaseModel


# This is empty right now but we might add more fields
# Other wise it can just be a field in symbolic file
class NotationType(CustomBaseModel):
    name = models.CharField(max_length=40, blank=False)


    class Meta(CustomBaseModel.Meta):
        db_table = 'notation_type'
