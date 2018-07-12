from django.db import models
from database.models.custom_base_model import CustomBaseModel
from database.models.person import Person
from database.models.institution import Institution
from django.contrib.postgres.fields import DateRangeField


class CollectionOfSources(CustomBaseModel):
    """
    A reference to one or more Sources grouped together

    Examples: a book of masses, an album of songs
    """
    title = models.CharField(max_length=200, blank=False,
                             help_text='The title of the Collection of Sources')
    editorial_notes = models.TextField(null=True, blank=True,
                                       help_text='Any editorial notes the '
                                                 'user deems necessary')
    publication_date = DateRangeField(null=True, blank=True,
                                      help_text='The date this Collection of '
                                                'Sources was published')
    person_publisher = models.ForeignKey(Person, on_delete=models.SET_NULL,
                                         null=True, blank=True,
                                         help_text='The Person who published '
                                                   'this Collection of Sources')
    institution_publisher = models.ForeignKey(Institution,
                                              on_delete=models.SET_NULL,
                                              null=True, blank=True,
                                              help_text='The Institution who '
                                                        'published this '
                                                        'Collection of Sources')
    url = models.URLField(null=True, blank=True, help_text='An URI that '
                                                           'identifies this '
                                                           'Collection of '
                                                           'Sources')

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
                                              default=PHYSICAL,
                                              help_text='Specifies if the '
                                                        'Collection of '
                                                        'Sources is Physical '
                                                        'or Electronic')

    def __str__(self):
        return "{0}".format(self.title)

    def __prepare_summary(self):
        summary = {'display': self.__str__(),
                   'url': self.get_absolute_url(),
                   }
        return summary


    class Meta(CustomBaseModel.Meta):
        db_table = 'collection_of_sources'
        verbose_name_plural = 'Collections of Sources'
