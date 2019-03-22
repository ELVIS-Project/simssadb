from database.models.symbolic_music_file import SymbolicMusicFile
from django.db.models.signals import post_save
from django.dispatch import receiver
import feature_extraction.feature_extraction
from feature_extraction.feature_parsing import *
from database.models.feature_file import FeatureFile
import os
from django.core.files import File


@receiver(post_save, sender=SymbolicMusicFile)
def run_jsymbolic(sender, instance, **kwargs):
    software, created = Software.objects.get_or_create(name='jSymbolic',
                                                       version='2.3')
    path = os.path.join(os.getcwd(), 'media', instance.file.name)
    path_feature_description = os.path.join(os.getcwd(), 'feature_extraction', 'feature_definitions.xml')
    path_feature_value = os.path.join(os.getcwd(), 'media', 'symbolic_music', 'extracted_features',
                                      os.path.split(instance.file.name)[-1]) \
                         + '_feature_values.xml'
    feature_path = os.path.join(os.getcwd(), 'media', 'symbolic_music', 'extracted_features',
                                os.path.split(instance.file.name)[-1]) + '_feature_values'
    feature_path_file = [feature_path + '.xml', feature_path + '.csv', feature_path + '.arff']
    print(path)
    print(os.path.exists(path))
    feature_extraction.feature_extraction.driver(path)

    parse_feature_types(path_feature_description, software)
    parse_feature_values(path_feature_value, instance, software)
    for item in feature_path_file:  # save all the feature files in the DB
        filename, ext = os.path.splitext(item)
        size = os.path.getsize(item)
        f_feature = File(open(item, 'r'))
        FeatureFile.objects.get_or_create(file_type=ext, file_size=size, file=item, symbolic_music_file=instance,
                                      extracted_with=software)
