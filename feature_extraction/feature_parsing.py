import fnmatch
import ntpath
import os
import xml.etree.cElementTree as et

from django.conf import settings

from database.models.extracted_feature import ExtractedFeature
from database.models.feature_type import FeatureType
from database.models.software import Software
from database.models.symbolic_music_file import SymbolicMusicFile

software, created = Software.objects.get_or_create(name='jSymbolic',
                                                   version='2.3')
filepath_xml = ''  # TODO: change
ext_features = []
mediatype = '/Users/gustavo/Development/simssadb/media/symbolic_music'
mediapath = getattr(settings, "MEDIA_ROOT", None)


def parse_feature_types(feature_type_file_path):
    tree = et.ElementTree(file=feature_type_file_path)
    root = tree.getroot()

    for feature in root.iter('feature'):
        name = feature.find('name').text
        code = feature.find('code').text
        description = feature.find('description').text
        dimensions = int(feature.find('parallel_dimensions'))

        ExtractedFeature.objects.get_or_create(name=name,
                                               code=code,
                                               description=description,
                                               dimensions=dimensions,
                                               software=software)


def parse_feature_values(feature_values_file_path, symbolic_music_file):
    tree = et.ElementTree(file=feature_values_file_path)
    root = tree.getroot()
    data_set = root.find('data_set')
    for feature in data_set.iter('feature'):
        feature_name = feature.find('name').text

        feature_def = FeatureType.objects.get(name__exact=feature_name)

        if feature_def is None:
            raise Exception

        ext_feature = ExtractedFeature(instance_of_feature=feature_def,
                                       extracted_with=software,
                                       feature_of=symbolic_music_file
                                       )

        feature_values = []
        for v in feature.findall('v'):
            feature_values.append(v.text)

        ext_feature.value = feature_values

        ext_features.append(ext_feature)





