from django.db import models
from database.models.custom_base_model import CustomBaseModel


class Source(CustomBaseModel):
    title = models.CharField(max_length=200, blank=False)
    publication_date = models.DateField
    editorial_notes = models.TextField()

    PHYSICAL = 'p'
    ELECTRONIC = 'e'
    PHYSICAL_OR_ELECTRONIC_CHOICES = (
        (PHYSICAL, 'Physical'),
        (ELECTRONIC, 'Electronic')
    )
    physical_or_electronic = models.CharField(max_length=1, choices=PHYSICAL_OR_ELECTRONIC_CHOICES,
                                              default=PHYSICAL)


    class Meta(CustomBaseModel):
        db_table = 'source'
