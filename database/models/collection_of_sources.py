"""Define a CollectionOfSources model"""
from django.contrib.postgres.fields import DateRangeField
from django.db import models

from database.mixins.helper_functions import clean_date
from database.models.custom_base_model import CustomBaseModel
from database.models.institution import Institution
from database.models.person import Person


class CollectionOfSources(CustomBaseModel):
    """A reference to one or more Sources grouped together.

    Examples: a book of masses, an album of songs.

    Attributes
    ----------
    CollectionOfSources.title : models.CharField
        The title of this Collection of Sources.

    CollectionOfSources.editorial_notes : models.TextField
        Any editorial notes the user deems necessary.

    CollectionOfSources.date : postgres.fields.DateRangeField
        The date of this Collection of Sources.

    CollectionOfSources.person_publisher : models.ForeignKey
        Reference to the Person that published this Collection of Sources.

    CollectionOfSources.institution_publisher : models.Institution
        Reference to the Institution that published this Collection of Sources.

    CollectionOfSources.url : models.URLField
        A URL that identifies this Collection of Sources.

    See Also
    --------
    database.models.CustomBaseModel
    database.models.Sources
    database.models.Person
    database.models.Institution
    database.models.Archive

    """
    title = models.CharField(max_length=200, blank=False,
                             help_text='The title of this Collection of '
                                       'Sources')
    editorial_notes = models.TextField(null=True, blank=True,
                                       help_text='Any editorial notes the '
                                                 'user deems necessary')
    date = DateRangeField(null=True, blank=True,
                          help_text='The date of this Collection of Sources')
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
    url = models.URLField(null=True, blank=True, help_text='An URL that '
                                                           'identifies this '
                                                           'Collection of '
                                                           'Sources')

    class Meta(CustomBaseModel.Meta):
        db_table = 'collection_of_sources'
        verbose_name_plural = 'Collections of Sources'

    def __str__(self):
        return "{0}".format(self.title)

    def _prepare_summary(self):
        """Prepare a dictionary that summarizes an instance of this model.

        Useful when listing many instances in a list-type view

        Returns
        -------
        summary : dict
            A dictionary containing the essential data to display this object
            in a list-type view

        See Also
        --------
        database.models.CustomBaseModel.summary: the property that validates
        the returned dictionary and exposes it to other classes

        """
        summary = {
            'display': self.__str__(),
            'url':     self.get_absolute_url(),
            }
        return summary

    def _get_related(self):
        """Get a dictionary listing the related objects of this instance.

        Returns
        -------
        related : dict
            A dictionary of dictionaries listing the related objects of this
            instance. Each entry of related is a dictionary with the following
            entries:
            * list: an iterable of related objects
            * model_name: the name to be displayed when listing these objects
            * model_count: the number of objects in the iterable

        """
        # QuerySet does not evaluate here, will evaluate when template calls it
        items = self.sources.all()
        related = {
            'portions': {
                'list':        items,
                'model_name':  'Items',
                'model_count': items.count()  # Will generate a query to count
                }
            }

        return related

    def detail(self):
        """Get all the data about this instance relevant to a user.

        Useful when displaying this object in a detail-type view.

        Returns
        -------
        detail_dict : dict
            A dictionary containing the relevant data about this instance.

        Warnings
        --------
        This method causes database calls and can be expensive, avoid using in a
        loop.

        """
        detail_dict = {
            'title':                   self.__str__(),
            'editorial_notes':         self.editorial_notes,
            'date':                    clean_date(self.date),
            'publisher_(person)':      self.person_publisher,
            'publisher_(institution)': self.institution_publisher,
            'link':                    self.url,
            'in_archives':             list(self.in_archive.all()),
            'related':                 self._get_related()
            }

        return detail_dict
