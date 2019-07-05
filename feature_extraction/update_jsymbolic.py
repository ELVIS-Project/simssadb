import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simssadb.settings")
import django

django.setup()
from database.models.symbolic_music_file import SymbolicMusicFile
from feature_extraction.feature_parsing import *
from database.signals import run_jsymbolic

version = "2.2"
path_feature_description = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    "feature_extraction",
    "jSymbolic_2_2_user",
    "feature_definitions.xml",
)
software, created = Software.objects.get_or_create(name="jSymbolic", version=version)

if __name__ == "__main__":
    # Execute these codes into a console

    all_symbolic_files = SymbolicMusicFile.objects.all()
    ExtractedFeature.objects.all().delete()
    FeatureType.objects.all().delete()  # Clear out feature definitions and create new ones
    parse_feature_types(
        path_feature_description, software
    )  # Build feature description infrastructure
    # The main function will re-extract all the features when there is a new jsymbolic version available
    for file in all_symbolic_files:
        run_jsymbolic(file)
