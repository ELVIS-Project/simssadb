from django.db import models
from database.models.custom_base_model import CustomBaseModel
from database.models.person import Person
from database.models.institution import Institution
from django.contrib.postgres.fields import DateRangeField


class CollectionOfSources(CustomBaseModel):
    """A reference to one or more sources grouped together

    Ex: a book of masses, an album of songs
    """
    title = models.CharField(max_length=200, blank=False)
    editorial_notes = models.TextField(null=True, blank=True)
    publication_date = DateRangeField(null=True, blank=True)
    person_publisher = models.ForeignKey(Person, on_delete=models.SET_NULL,
                                         null=True, blank=True)
    institution_publisher = models.ForeignKey(Institution,
                                              on_delete=models.SET_NULL,
                                              null=True, blank=True)
    url = models.URLField(null=True, blank=True)

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


    def __str__(self):
        return "{0}".format(self.title)

    class Meta(CustomBaseModel.Meta):
        db_table = 'collection_of_sources'
        verbose_name_plural = 'Collections of Sources'
