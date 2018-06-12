from django.db import models
from database.models.custom_base_model import CustomBaseModel
from django.contrib.postgres.fields import ArrayField
from database.models.software import Software
from database.models.symbolic_music_file import SymbolicMusicFile


class ExtractedFeature(CustomBaseModel):
    """Content-based data extracted from a file"""
    name = models.CharField(max_length=200, blank=False)
    value = ArrayField(
            ArrayField(
                    models.FloatField()
            )
    )
    extracted_with = models.ForeignKey(Software, on_delete=models.PROTECT,
                                       null=False, blank=False)

    feature_of = models.ForeignKey(SymbolicMusicFile, on_delete=models.CASCADE,
                                   null=False, blank=False)

    def __str__(self):
        return "{0}".format(self.name)

    class Meta(CustomBaseModel.Meta):
        db_table = 'extracted_feature'
