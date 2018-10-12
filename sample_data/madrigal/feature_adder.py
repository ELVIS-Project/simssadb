import fnmatch
import ntpath
import os
import sys
import xml.etree.cElementTree as ET

proj_path = "../../"

# This is so mpythoy local_settings.py gets loaded.
os.chdir(proj_path)

# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simssadb.settings")

sys.path.append(os.getcwd())

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
from django.conf import settings

application = get_wsgi_application()

from database.models.extracted_feature import ExtractedFeature
from database.models.software import Software
from database.models.symbolic_music_file import SymbolicMusicFile
from database.models.feature_type import FeatureType

print('Adding extracted features...')

mediatype = '/Users/gustavo/Development/simssadb/media/symbolic_music'
mediapath = getattr(settings, "MEDIA_ROOT", None)

print(mediapath)
print(mediatype)

# Hardcoded with jSymbolic for now
software, created = Software.objects.get_or_create(name='jSymbolic',
                                                 version='2.3')
software.save()

filepath_xml = os.getcwd()
filepath_xml += '/sample_data/madrigal/MedRen18_SafeFeatures.xml'

tree = ET.ElementTree(file=filepath_xml)
root = tree.getroot()
ext_features = []

# Get dataset for each file
for dataset in root.iter('data_set'):
    filepath_dataset = dataset.find('data_set_id').text
    filename_dataset = ntpath.basename(filepath_dataset)

    # Check if file has been uploaded
    for filename_media in os.listdir(mediatype):
        if fnmatch.fnmatch(filename_media, filename_dataset):
            file = 'symbolic_music/' + filename_media
            symbolic_music_file = SymbolicMusicFile.objects.get(file=file)

            print(symbolic_music_file)

            # Iterate through all the features
            for feature in dataset.iter('feature'):
                feature_name = feature.find('name').text

                feature_def = FeatureType.objects.get(name__exact=feature_name)

                if feature_def is None:
                    raise Exception

                ext_feature = ExtractedFeature(
                        instance_of_feature=feature_def,
                        extracted_with=software,
                        feature_of=symbolic_music_file)

                feature_values = []
                for v in feature.findall('v'):
                    feature_values.append(v.text)

                ext_feature.value = feature_values

                ext_features.append(ext_feature)

                print(ext_feature)

db_features = ExtractedFeature.objects.all()

for feature in db_features:
    assert(feature.instance_of_feature is not None)

for feature in ext_features:
    feature.save()
