from django.db import models
from database.models.custom_base_model import CustomBaseModel


class CollectionOfSources(CustomBaseModel):
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


    class Meta(CustomBaseModel.Meta):
        db_table = 'collection_of_sources'
