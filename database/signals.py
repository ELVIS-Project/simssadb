import os
from database.models import File
from database.models.musical_work import MusicalWork
from django.db.models.signals import post_save
from django.dispatch import receiver
from feature_extraction.feature_extracting import *
from feature_extraction.feature_parsing import *
from database.tasks import async_call
from database.tasks import driver
from database.models.feature_file import FeatureFile
from django.core import serializers
from django.db.models import Value
from django.contrib.postgres.search import SearchVector
from functools import reduce
from django.db import models
import operator


@receiver(post_save, sender=File)
def run_jsymbolic(instance, **kwargs):
    jsymbolic_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
        "feature_extraction",
        "jSymbolic_2_2_user",
        "jSymbolic2.jar",
    )
    jsymbolic_config_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
        "feature_extraction",
        "jSymbolic_2_2_user",
        "jSymbolicDefaultConfigs.txt",
    )
    # TODO: This needs change when jsymbolic is updated
    path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
        "media",
        instance.file.name,
    )
    converted_file_name = os.path.split(instance.file.name)[-1]
    if (
        converted_file_name.split(".")[-1].lower() != "mid"
        and converted_file_name.split(".")[-1].lower() != "midi"
    ):
        converted_file_name += (
            ".midi"
        )  # The file is first converted into midi and then get feature extracted

    feature_path = (
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
            "media",
            "user_files",
            "extracted_features",
            converted_file_name,
        )
        + "_feature_values"
    )
    feature_config_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
        "media",
        "jSymbolicDefaultConfigs.txt",
    )  # We need to copy the config file to this path so that it can be downloaded
    feature_definition_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
        "media",
        "feature_definitions.xml",
    )  # We need to copy the config file to this path so that it can be downloaded
    feature_path_file = [
        feature_path + ".xml",
        feature_path.replace(".xml.", ".csv.") + ".csv",
        feature_path.replace(".xml.", ".arff.") + ".arff",
    ]  # jsymbolic rename the xml.midi file
    # in a weired way
    print(path)
    print(os.path.exists(path))
    # instance_json = serializers.serialize('json', [instance, ])
    async_task(
        jsymbolic_file,
        jsymbolic_config_file,
        path,
        feature_path_file,
        instance.pk,
        feature_config_file,
        feature_definition_file,
    )
    # async_call.delay(jsymbolic_file, jsymbolic_config_file, path)


@shared_task
# def async_call(jsymbolic_file, jsymbolic_config_file, path):
def async_task(
    jsymbolic_file,
    jsymbolic_config_file,
    path,
    feature_path_file,
    instance_pk,
    feature_config_file,
    feature_definition_file,
):
    path_feature_description = os.path.join(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
        "feature_extraction",
        "jSymbolic_2_2_user",
        "feature_definitions.xml",
    )
    version = "2.2"
    software, created = Software.objects.get_or_create(
        name="jSymbolic", version=version
    )
    extracted = driver(jsymbolic_file, jsymbolic_config_file, path)
    instance = File.objects.get(pk=instance_pk)
    if extracted:
        parse_feature_types(path_feature_description, software)
        feature_values_parsed = parse_feature_values(feature_path_file[0], instance, software)
        if feature_values_parsed:
            for item in feature_path_file:  # save all the feature files in the DB
                filename, ext = os.path.splitext(item)
                FeatureFile.objects.get_or_create(
                    file_type=ext,
                    file=item,
                    features_from_file=instance,
                    config_file=feature_config_file,
                    feature_definition_file=feature_definition_file,
                    extracted_with=software,
                )


@receiver(post_save, sender=MusicalWork)
def on_save(instance, **kwargs):
    index_components = instance.index_components()
    pk = instance.pk

    search_vectors = []

    for weight, data in index_components.items():
        search_vectors.append(
            SearchVector(Value(data, output_field=models.TextField()), weight=weight)
        )
    instance.__class__.objects.filter(pk=pk).update(
        search_document=reduce(operator.add, search_vectors)
    )
