import xml.etree.cElementTree as et
from database.models.extracted_feature import ExtractedFeature
from database.models.feature_type import FeatureType
from database.models.software import Software


def parse_feature_types(feature_type_file_path, software):

    tree = et.ElementTree(file=feature_type_file_path)
    root = tree.getroot()
    print('Creating feature definition infrastructure')
    for feature in root.iter('feature'):
        name = feature.find('name').text
        code = feature.find('code').text
        description = feature.find('description').text
        dimensions = int(feature.find('parallel_dimensions').text)
        feature, created = FeatureType.objects.get_or_create(name=name,
                                                             code=code,
                                                             description=description,
                                                             dimensions=dimensions,
                                                             software=software)
        if created is False: break


def parse_feature_values(feature_values_file_path, symbolic_music_file, software):
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
        ext_feature.save()
