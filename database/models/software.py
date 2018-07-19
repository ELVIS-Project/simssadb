from django.db import models
from database.models.custom_base_model import CustomBaseModel


class Software(CustomBaseModel):
    """A Software that encoded, validated or extracted features from a file"""
    name = models.CharField(blank=False, max_length=100,
                            help_text='The name of the Software')
    version = models.CharField(blank=False, default='1.0', max_length=10,
                               help_text='The version of the Software')
    configuration_file = models.FileField(blank=True, null=True,
                                          help_text='A file that describes '
                                                    'how the Software was '
                                                    'configured when '
                                                    'performing an encoding, '
                                                    'validation or extracting '
                                                    'task')

    def __str__(self):
        return "{0}".format(self.name)

    def prepare_summary(self):
        summary = {'display': self.__str__(),
                   'url': self.get_absolute_url()
                   }
        return summary


    class Meta(CustomBaseModel.Meta):
        db_table = 'software'
