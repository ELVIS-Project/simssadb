from database.models.symbolic_music_file import SymbolicMusicFile
from django.db.models.signals import post_save
from django.dispatch import receiver
import feature_extraction.feature_extraction
from feature_extraction.feature_parsing import *
import os


@receiver(post_save, sender=SymbolicMusicFile)
def run_jsymbolic(sender, instance, **kwargs):
    path = os.path.join(os.getcwd(), 'media', instance.file.name)
    path_feature_description = os.path.join(os.getcwd(), 'feature_extraction', 'feature_definitions.xml')
    path_feature_value = os.path.join(os.getcwd(), 'media', 'symbolic_music', 'extracted_features',
                                            os.path.split(instance.file.name)[-1])\
                         + '_feature_values.xml'
    print(path)
    print(os.path.exists(path))
    feature_extraction.feature_extraction.driver(path)
    parse_feature_types(path_feature_description)
    parse_feature_values(path_feature_value, instance)
