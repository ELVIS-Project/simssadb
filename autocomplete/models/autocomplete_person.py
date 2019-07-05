from django.db import models


class AutocompletePerson(models.Model):
    given_name = models.CharField(
        max_length=100,
        blank=False,
        help_text="The given name of this Person",
        default="",
    )
    surname = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text="The surname of this Person, " "leave blank if it is unknown",
    )
    range_date_birth = DateRangeField(
        null=True,
        blank=True,
        help_text="The birth year of this "
        "Person. The format is "
        "YYYY-MM-DD. "
        "If certain, put the "
        "beginning and end of the "
        "range as the same. If "
        "uncertain, enter a range "
        "that is generally accepted",
    )
    range_date_death = DateRangeField(
        null=True,
        blank=True,
        help_text="The death year of this "
        "Person. The format is "
        "YYYY-MM-DD. "
        "If certain, put the "
        "beginning and end of the "
        "range as the same. If "
        "uncertain, enter a range "
        "that is generally accepted",
    )
    authority_control_url = models.URLField(
        blank=True,
        null=True,
        help_text="An URI linking to an "
        "authority control "
        "description of this "
        "Person",
    )
    authority_control_key = models.IntegerField(
        unique=True,
        blank=True,
        null=True,
        help_text="The identifier of " "this Person " "in the authority " "control",
    )

    class Meta(models.Model.Meta):
        db_table = "autocomplete-person"
