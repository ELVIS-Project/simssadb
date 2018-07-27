from django.contrib.postgres.fields import DateRangeField
from django.db import models

from database.models.custom_base_model import CustomBaseModel
from database.models.institution import Institution
from database.models.person import Person


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

    @staticmethod
    def clean_date(date_range):
        date = None
        if date_range is not None:
            if date_range.lower is not None and date_range.upper is not None:
                if date_range.lower.year == date_range.upper.year:
                    date = str(date_range.upper.year)
                else:
                    date = str(date_range.lower.year) + '-' + str(date_range.upper.year)
            if date_range.lower is not None and date_range.upper is None:
                date = str(date_range.lower.year)
            if date_range.lower is None and date_range.upper is not None:
                date = str(date_range.upper.year)
        return date

    def _prepare_summary(self):
        summary = {'display': self.__str__(),
                   'url': self.get_absolute_url(),
                   }
        return summary

    def get_portions(self):
        portions = set()
        for source in self.source_set.all():
            portions.add(source)
        return portions

    def get_related(self):
        related = {
            'portions': {'list': list(self.get_portions()),
                         'model_name': 'Items',
                         'model_count': len(self.get_portions())
                         }
        }

        return related

    def detail(self):
        detail_dict = {
            'title': self.__str__(),
            'editorial_notes': self.editorial_notes,
            'publication_date': self.clean_date(self.publication_date),
            'publisher_(person)': self.person_publisher,
            'publisher_(institution)': self.institution_publisher,
            'link': self.url,
            'in_archives': list(self.in_archive.all()),
            'related': self.get_related()
        }

        return detail_dict

    class Meta(CustomBaseModel.Meta):
        db_table = 'collection_of_sources'
        verbose_name_plural = 'Collections of Sources'
