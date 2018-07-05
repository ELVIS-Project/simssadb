from django.db import models
from database.models.custom_base_model import CustomBaseModel
from database.models.geographic_area import GeographicArea


class Institution(CustomBaseModel):
    """A real world institution (usually academic)"""
    name = models.CharField(max_length=255, blank=False,
                            help_text='The name of the Institution')
    located_at = models.ForeignKey(GeographicArea, on_delete=models.CASCADE,
                                   null=True,
                                   help_text='The area in which the '
                                             'Institution is located')
    website = models.URLField(null=True, blank=False,
                              help_text='A link to the website of the '
                                        'Institution')


    def __str__(self):
        return "{0}".format(self.name)

    class Meta(CustomBaseModel.Meta):
        db_table = 'institution'
