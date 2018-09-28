"""Define a GeographicArea model"""
from django.apps import apps
from django.db import models
from django.db.models import QuerySet

from database.models.custom_base_model import CustomBaseModel


class GeographicArea(CustomBaseModel):
    """A geographic area that can be part of another area

    Attributes
    ----------
    GeographicArea.name :
        The name of this GeographicArea

    GeographicArea.part_of : models.ForeignKey
        The parent area of this GeographicArea (e.g. Montreal has Quebec as
        parent area)

    GeographicArea.child_areas : model.ManyToOneRel
        References to the child areas of this GeographicArea

    GeographicArea.birth_location_of : models.ManyToOneRel
        References to Persons that were born in this GeographicArea

    GeographicArea.death_location_of : models.ManyToOneRel
        References to Persons that died in this GeographicArea

    GeographicArea.contributions : models.ManyToOneRel
        References to the Contributions made in this GeographicArea

    GeographicArea.institutions : models.ManyToOneRel
        References to the Institutions located in this GeographicArea

    See Also
    --------
    database.models.CustomBaseModel
    database.models.Person
    database.models.Contribution
    database.models.Institution
    """
    name = models.CharField(max_length=200,
                            help_text='The name of the Geographic Area')
    part_of = models.ForeignKey('self', on_delete=models.CASCADE,
                                null=True,
                                blank=True,
                                help_text='The "parent area" of this '
                                          'Geographic Area. '
                                          'Example: Montreal has as '
                                          'parent area Quebec',
                                related_name='child_areas')
    authority_control_url = models.URLField(blank=True,
                                            help_text='An URI linking to an '
                                                      'authority control '
                                                      'description of this '
                                                      'Geographic Area')
    authority_control_key = models.IntegerField(unique=True,
                                                blank=True,
                                                null=True,
                                                help_text='The identifier of '
                                                          'this Geographic '
                                                          'Area in the '
                                                          'authority control')

    def __str__(self):
        return "{0}".format(self.name)

    class Meta:
        db_table = 'geographic_area'
