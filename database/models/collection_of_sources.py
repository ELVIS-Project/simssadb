from django.db import models
from database.models.custom_base_model import CustomBaseModel
from database.models.source import Source


class CollectionOfSources(CustomBaseModel):
    """A reference to one or more sources grouped together

    Ex: a book of masses, an album of songs
    """
    title = models.CharField(max_length=200, blank=False)
    publication_date = models.DateField(null=True, blank=True)
    editorial_notes = models.TextField(null=True, blank=True)

    # This is to limit the choices, but since there are only two we could
    # have a boolean?
    PHYSICAL = 'p'
    ELECTRONIC = 'e'
    PHYSICAL_OR_ELECTRONIC = (
        (PHYSICAL, 'Physical'),
        (ELECTRONIC, 'Electronic')
    )
    physical_or_electronic = models.CharField(max_length=1,
                                              choices=PHYSICAL_OR_ELECTRONIC,
                                              default=PHYSICAL)

    sources = models.ManyToManyField(Source, related_name='in_collection')

    def __str__(self):
        return "{0}".format(self.title)

    class Meta(CustomBaseModel.Meta):
        db_table = 'collection_of_sources'
        verbose_name_plural = 'Collections of Sources'
