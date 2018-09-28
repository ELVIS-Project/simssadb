"""Define a Institution model"""
from django.db import models

from database.models.custom_base_model import CustomBaseModel


class Institution(CustomBaseModel):
    """A real world institution (usually academic).

    Attributes
    ----------
    Institution.name : models.CharField
        The name of this Institution

    Institution.located_at : models.ForeignKey
        Reference to the GeographicArea where this Institution is located

    Institution.website : models.URLField
        A link to the website of this Institution

    Institution.archives : models.ManyToOneRel
        References to the Archives located at this Institution

    Institution.published : models.ManyToOneRel
        References to the CollectionsOfSources published by this Institution

    Institution.studies : models.ManyToOneRel
        References to the ExperimentalStudies related to this Institution

    See Also
    --------
    database.models.CustomBaseModel
    database.models.GeographicArea
    database.models.Archive
    database.models.CollectionOfSources
    database.models.ExperimentalStudies
    """
    name = models.CharField(max_length=255,
                            blank=False,
                            help_text='The name of the Institution')
    located_at = models.ForeignKey('GeographicArea',
                                   on_delete=models.CASCADE,
                                   related_name='institutions',
                                   null=True,
                                   help_text='The area in which the '
                                             'Institution is located')
    website = models.URLField(blank=True,
                              help_text='A link to the website of the '
                                        'Institution')

    class Meta(CustomBaseModel.Meta):
        db_table = 'institution'

    def __str__(self):
        return "{0}".format(self.name)
