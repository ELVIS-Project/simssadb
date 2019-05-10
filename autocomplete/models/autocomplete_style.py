from django.db import models


class AutocompleteStyle(models.Model):
    name = models.CharField(max_length=200,
                            blank=False,
                            help_text='The name of the GenreAsInStyle')

    class Meta:
        db_table = 'autocomplete-style'
