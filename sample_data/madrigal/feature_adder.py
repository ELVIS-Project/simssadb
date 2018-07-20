import os
import sys
import ntpath
import fnmatch
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

print('Adding extracted features...')

mediatype = 'symbolic_music/'
mediapath = getattr(settings, "MEDIA_ROOT", None)
mediapath = mediapath + mediatype

# Hardcoded with jSymbolic for now
software = Software.objects.get(name='jSymbolic', version='2.2')

filepath_xml = os.getcwd()
filepath_xml += '/sample_data/madrigal/MedRen18_SafeFeatures.xml'

tree = ET.ElementTree(file=filepath_xml)
root = tree.getroot()

# Get dataset for each file
for dataset in root.iter('data_set'):
    filepath_dataset = dataset.find('data_set_id').text
    filename_dataset = ntpath.basename(filepath_dataset)

    # Check if file has been uploaded
    for filename_media in os.listdir(mediapath):
        if fnmatch.fnmatch(filename_media, filename_dataset):

            symbolic_music_file = SymbolicMusicFile.objects.get(
                file=mediatype+filename_media
            )

            # Iterate through all the features
            for feature in dataset.iter('feature'):
                feature_name = feature.find('name').text

                ext_feature = ExtractedFeature(
                    name=feature_name,
                    extracted_with=software,
                    feature_of=symbolic_music_file
                )

                feature_values = []
                for v in feature.findall('v'):
                    feature_values.append(v.text)

                ext_feature.value = feature_values

                ext_feature.save()
