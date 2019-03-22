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
    converted_file_name = os.path.split(instance.file.name)[-1]
    if converted_file_name.split('.')[-1].lower() != 'mid' and converted_file_name.split('.')[-1].lower() != 'midi':
        converted_file_name += '.midi' # The file is first converted into midi and then get feature extracted
    path_feature_description = os.path.join(os.getcwd(), 'feature_extraction', 'feature_definitions.xml')
    feature_path = os.path.join(os.getcwd(), 'media', 'symbolic_music', 'extracted_features',
                                converted_file_name) + '_feature_values'
    feature_config_file = os.path.join(os.getcwd(), 'feature_extraction', 'jSymbolic_2_2_user', 'jSymbolicDefaultConfigs.txt')
    if not os.path.exists(feature_config_file):
        input('this config file does not exist!')
    feature_path_file = [feature_path + '.xml', feature_path.replace('.xml.', '.csv.') +
                         '.csv', feature_path.replace('.xml.', '.arff.') + '.arff'] # jsymbolic rename the xml.midi file
    # in a weired way
    print(path)
    print(os.path.exists(path))
    extracted = feature_extraction.feature_extraction.driver(path)
    if extracted:
        parse_feature_types(path_feature_description, software)
        parse_feature_values(feature_path_file[0], instance, software)
        for item in feature_path_file:  # save all the feature files in the DB
            filename, ext = os.path.splitext(item)
            size = os.path.getsize(item)
            f_feature = File(open(item, 'r'))
            FeatureFile.objects.get_or_create(file_type=ext, file_size=size, file=item, symbolic_music_file=instance, config_file=feature_config_file,
                                          extracted_with=software)
