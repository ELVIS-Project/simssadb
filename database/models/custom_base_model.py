from django.db import models
from django.urls import reverse


class MissingSummaryValue(Exception):
    """Exception class for when a value is missing in the summary dictionary"""
    pass


class CustomBaseModel(models.Model):
    """Base model that contains common fields for other models"""
    date_created = models.DateTimeField(auto_now_add=True,
                                        help_text='The date this entry was '
                                                  'created')
    date_updated = models.DateTimeField(auto_now=True,
                                        help_text='The date this entry was '
                                                  'updated')

    def get_reverse_detail_name(self):
        return self.__class__.__name__.lower() + '-detail'

    def get_absolute_url(self):
        return reverse(self.get_reverse_detail_name(), kwargs={'pk': self.pk})

    @property
    def lower_case_name(self):
        return self.__class__.__name__.lower()

    def summary(self):
        """Returns a summary of this instance of the model for display purposes"""
        summary = self.prepare_summary()

        if 'display' not in summary:
            raise MissingSummaryValue('Missing "display" key-value pair in summary dictionary')
        if 'url' not in summary:
            raise MissingSummaryValue('Missing "url" key-value pair in summary dictionary')

        return summary

    def prepare_summary(self):
        """
        Abstract method that must be implemented by all child classes

        The __prepare_summary function must return a dictionary with the data that
        summarizes each instance of the model. It must has at least a 'display' key and a 'url' key
        """
        raise NotImplementedError


    class Meta:
        abstract = True
        app_label = 'database'
