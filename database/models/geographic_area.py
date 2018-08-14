from django.db import models

from database.models.custom_base_model import CustomBaseModel


class GeographicArea(CustomBaseModel):
    """A geographic area that can be part of another area"""
    name = models.CharField(max_length=200,
                            help_text='The name of the Geographic Area')
    part_of = models.ForeignKey('self', on_delete=models.CASCADE, null=True,
                                blank=True,
                                help_text='The "parent area" of this '
                                          'Geographic Area. '
                                          'Example: Montreal has as '
                                          'parent area Quebec',
                                related_name='child_areas')
    authority_control_url = models.URLField(null=True, blank=True,
                                            help_text='An URI linking to an '
                                                      'authority control '
                                                      'description of this '
                                                      'Geographic Area')
    authority_control_key = models.IntegerField(unique=True, blank=True,
                                                null=True,
                                                help_text='The identifier of '
                                                          'this Geographic '
                                                          'Area in the '
                                                          'authority control')

    def __str__(self):
        return "{0}".format(self.name)


    def prepare_summary(self):
        summary = {'display': self.__str__(),
                   'url': self.get_absolute_url(),
                   'parent_area': self.part_of
                   }

        return summary

    def detail(self):
        detail_dict = {
            'title':             self.name,
            'parent_area':       self.part_of,
            'child_areas':       list(self.child_areas.all()),
            'authority_control': self.authority_control_url
            }

        return detail_dict

    class Meta:
        db_table = 'geographic_area'
