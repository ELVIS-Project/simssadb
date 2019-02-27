from database.models import CustomBaseModel
from django.db import models


class FeatureFile(CustomBaseModel):
    file_type = models.CharField(max_length=10, help_text='The format of the '
                                                          'File')
    file_size = models.PositiveIntegerField(null=True, blank=True,
                                            help_text='The size of the File '
                                                      'in bytes')
    file = models.FileField(upload_to='feature_files/',
                            help_text='The actual file')
    symbolic_music_file = models.ForeignKey('SymbolicMusicFile',
                                            related_name='feature_files',
                                            null=False,
                                            help_text='The Symbolic Music '
                                                      'File that the features '
                                                      'were extracted from',
                                            on_delete=models.CASCADE)
    extracted_with = models.ForeignKey('Software',
                                       on_delete=models.PROTECT,
                                       related_name='feature_files',
                                       null=False, blank=False,
                                       help_text='The Software used to extract'
                                                 'these features')
