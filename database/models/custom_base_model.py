"""Define a CustomBaseModel to be extended by all other models"""
from django.db import models
from django.urls import reverse


class MissingSummaryValue(Exception):
    """Exception class for when a value is missing in the summary dictionary."""
    pass


class CustomBaseModel(models.Model):
    """Base model that contains common fields for other models."""
    date_created = models.DateTimeField(auto_now_add=True,
                                        help_text='The date this entry was '
                                                  'created')
    date_updated = models.DateTimeField(auto_now=True,
                                        help_text='The date this entry was '
                                                  'updated')

    class Meta:
        abstract = True
        app_label = 'database'

    def get_absolute_url(self):
        """Get the absolute URL for an instance of a model"""
        detail_name = self.__class__.__name__.lower() + '-detail'
        return reverse(detail_name, kwargs={'pk': self.pk})

    def _prepare_summary(self):
        """Abstract method that must be implemented by all child classes."""
        raise NotImplementedError

    @property
    def name(self):
        """Get the verbose_name_plural

        Returns
        -------
        verbose_name_plural: str
            A human friendly name of this model
        """

        return self._meta.verbose_name_plural

    def detail(self):
        """Abstract method that must be implemented by all child classes"""
        raise NotImplementedError

    def summary(self):
        """Return a summary of this instance of the model for display.

        Check if the dictionary has the display and url key:value pairs.

        Raises
        ------
        MissingSummaryValue
            If the dictionary is missing the display or url key:value pairs.

        """
        summary = self._prepare_summary()

        if 'display' not in summary:
            raise MissingSummaryValue(
                    'Missing "display" key-value pair in summary dictionary')
        if 'url' not in summary:
            raise MissingSummaryValue(
                    'Missing "url" key-value pair in summary dictionary')

        return summary
