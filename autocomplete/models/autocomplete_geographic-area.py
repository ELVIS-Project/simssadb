from django.db import models


class AutocompleteGeographicArea(models.Model):
    name = models.CharField(max_length=200, help_text="The name of the Geographic Area")
    part_of = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text='The "parent area" of this '
        "Geographic Area. "
        "Example: Montreal has as "
        "parent area Quebec",
        related_name="child_areas",
    )
    authority_control_url = models.URLField(
        blank=True,
        null=True,
        help_text="An URI linking to an "
        "authority control "
        "description of this "
        "Geographic Area",
    )
    authority_control_key = models.IntegerField(
        unique=True,
        blank=True,
        null=True,
        help_text="The identifier of "
        "this Geographic "
        "Area in the "
        "authority control",
    )

    class Meta(CustomBaseModel.Meta):
        db_table = "autocomplete-geographic-area"
