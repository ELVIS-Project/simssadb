from django.db import models


class AutocompleteInstrument(models.Model):
    name = models.CharField(
        max_length=200, help_text="The name of the Instrument or Voice"
    )

    class Meta(models.Model.Meta):
        db_table = "autocomplete-person"
