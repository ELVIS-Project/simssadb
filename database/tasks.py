from __future__ import absolute_import
from celery import shared_task
from feature_extraction.feature_extracting import extract_features_setup
import os
from feature_extraction.feature_extracting import *
from feature_extraction.feature_parsing import *
from database.models.feature_file import FeatureFile

@shared_task
def async_call(jsymbolic_file, jsymbolic_config_file, path):
# def async_call(jsymbolic_file, jsymbolic_config_file, path, feature_path_file, instance, feature_config_file,
#                feature_definition_file):
    extracted = driver(jsymbolic_file, jsymbolic_config_file, path)


def driver(jsymbolic_file, jsymbolic_config_file, file_path):
    extracted = extract_features_setup(jsymbolic_file, jsymbolic_config_file, file_path)
    return extracted
