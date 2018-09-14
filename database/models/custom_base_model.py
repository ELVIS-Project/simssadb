"""Define a CustomBaseModel to be extended by all other models"""
from typing import List

from django.db import models
from django.urls import reverse


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

    @property
    def display_name(self) -> str:
        """Alias for the __str()__ method, useful for templates.

        Returns
        -------
        display : str
            The display name of this instance.
        """
        return self.__str__()

    @property
    def absolute_url(self) -> str:
        """Get the absolute URL for an instance of a model.

        Returns
        -------
        url : str
            The absolute url of this instance.
        """
        detail_name = self.__class__.__name__.lower() + '-detail'
        return reverse(detail_name, kwargs={'pk': self.pk})

    @classmethod
    def get_verbose_name_plural(cls) -> str:
        """Get a human friendly plural name of a model.

        Returns
        -------
        verbose_name_plural : str
            The verbose name plural of this model.
        """
        return cls._meta.verbose_name_plural

    @classmethod
    def get_fields_and_properties(cls) -> List[str]:
        """List the public fields and properties of a model.

        Returns
        -------
        fields_and_properties: List[str]
            A list of strings representing the public fields and properties of
            this model.
        """
        fields_and_properties = []
        for field in cls._meta.get_fields():
            if not field.name.startswith('_'):
                fields_and_properties.append(field.name)

        attrs = dir(cls)
        for attr in attrs:
            if not attr.startswith('_'):
                if isinstance(getattr(cls, attr), property):
                    fields_and_properties.append(attr)
        return sorted(fields_and_properties)
