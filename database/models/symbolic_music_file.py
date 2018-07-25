from django.db import models
from database.models.file import File
from database.models.source import Source
from database.models.instrument import Instrument
import os


class SymbolicMusicFile(File):
    """
    Manifestation of a Musical Instance as a digital music file

    Generated from a Source by a Symbolic Encoder
    """
    instruments_used = models.ManyToManyField(Instrument,
                                              help_text='The Instruments used '
                                                        'in this Symbolic File')

    manifests = models.ForeignKey(Source,
                                  related_name='manifested_by_sym_files',
                                  on_delete=models.CASCADE, null=False,
                                  help_text='The Source manifested by this '
                                            'Symbolic File')
    file = models.FileField(upload_to='symbolic_music/',
                            help_text='The actual file')

    def __str__(self):
        filename = os.path.basename(self.file.name)
        return "{0}".format(filename)

    def prepare_summary(self):
        summary = {'display':   self.__str__(),
                   'file_type': self.file_type,
                   'source':    self.manifests,
                   'url':       self.get_absolute_url()
                   }
        return summary

    def get_related(self):
        related = {
            'features': {'list': self.extractedfeature_set.all().exclude(name__contains='Histogram').order_by('name'),
                         'model_name': 'Features',
                         'model_count': self.extractedfeature_set.exclude(name__contains='Histogram').count()
                         }
        }
        return related

    def detail(self):
        detail_dict = {
            'title':          self.__str__(),
            'file_type':      self.file_type,
            'version':        self.version,
            'file_size':      self.file_size,
            'encoding_date':  self.encoding_date,
            'encoded_with':   self.encoded_with,
            'validated_by':   self.validated_by.__str__(),
            'extra_metadata': self.extra_metadata,
            'source':         self.manifests,
            'file':           self.file,
            'related':        self.get_related()
        }

        return detail_dict

    class Meta:
        db_table = 'symbolic_music_file'
