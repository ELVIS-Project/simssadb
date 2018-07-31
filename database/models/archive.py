"""Define an Archive model"""
from django.db import models

from database.models.collection_of_sources import CollectionOfSources
from database.models.custom_base_model import CustomBaseModel
from database.models.institution import Institution


class Archive(CustomBaseModel):
    """A location where Sources and Collections of Sources are stored.

    e.g: A database or a library.

    Attributes
    ----------
    Archive.name : models.CharField
        The name of the archive.

    Archive.collections: models.ManyToManyField
        References to CollectionsOfSources contained by this Archive.

    Archive.institution: models.ForeignKey
        Reference to the Institution this Archive is part of.

    See Also
    --------
    database.models.CustomBaseModel
    database.models.CollectionsOfSources
    database.models.Institution

    """
    name = models.CharField(max_length=200, blank=False, null=False,
                            help_text='The name of the Archive')
    collections = models.ManyToManyField(CollectionOfSources,
                                         related_name='in_archive',
                                         help_text='CollectionsOfSources that '
                                                   'belong '
                                                   'to this Archive')

    institution = models.ForeignKey(Institution, null=True,
                                    on_delete=models.SET_NULL,
                                    help_text='The Institution that this '
                                              'Archive is part of')

    class Meta(CustomBaseModel.Meta):
        db_table = 'archive'

    def __str__(self):
        return "{0}".format(self.name)

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
            'display':               self.name,
            'number_of_collections': self.collections.count(),
            'url':                   self.get_absolute_url()
            }
        return summary

    def detail(self):
        """Get all the data about this instance relevant to a user.

        Useful when displaying this object in a detail-type view

        Returns
        -------
        detail_dict : dict
            A dictionary containing the relevant data about this instance

        Warnings
        --------
        This method causes database calls and can be expensive, avoid using in a
        loop

        """
        detail_dict = {
            'title':       self.name,
            'institution': self.institution,
            'sources':     self.collections.all()
            }

        return detail_dict
