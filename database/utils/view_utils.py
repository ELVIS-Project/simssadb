import warnings
from typing import *

from django.db.models.manager import Manager
from django.db.models.query import QuerySet

from database.models.custom_base_model import CustomBaseModel


def make_related_objects_dict(relationship_name: str,
                              related_object_fields: List[str],
                              badge: Optional[str] = None) -> dict:
    return {
        'relationship_name': relationship_name,
        'fields':            related_object_fields,
        'badge':             badge
        }


def make_fields_dict(instance: CustomBaseModel,
                     fields_list: List[str]) -> dict:
    fields_dict = {}

    for field in fields_list:
        key = field
        try:
            value = getattr(instance, field)
            if isinstance(value, Manager):
                value = list(value.all())
            elif isinstance(value, Iterable) and not isinstance(value, str):
                value = list(value)

            fields_dict.update({key: value})
        except AttributeError:
            warnings.simplefilter('always')
            warning_string = 'Did not find the field ' \
                             + key + ' specified in fields_list'
            warnings.warn(warning_string)

    return fields_dict


def make_summary_dict(instance: CustomBaseModel,
                      fields_list: List[str],
                      badge_field: str = None) -> dict:
    summary_dict = make_fields_dict(instance, fields_list)
    summary_dict['display'] = instance.display_name
    summary_dict['absolute_url'] = instance.absolute_url

    if badge_field:
        summary_dict['badge_name'] = badge_field
        badge_list = getattr(instance, badge_field)
        if isinstance(badge_list, Manager):
            badge_list = list(badge_list.all())

        if isinstance(badge_list, Iterable) and not isinstance(badge_list,
                                                               str):
            badge_list = list(badge_list)

        if isinstance(badge_list, Sized):
            badge_count = len(badge_list)
        else:
            badge_count = 1
        summary_dict['badge_count'] = badge_count

    return summary_dict


def make_related_dict(instance: CustomBaseModel,
                      related_objects: List[dict]) -> dict:
    related_dict = {}

    for related_object in related_objects:
        key = related_object['object_name']
        sub_fields = related_object['fields']

        if 'badge' in related_object:
            badge_field = related_object['badge']
        else:
            badge_field = None

        try:
            value_list = getattr(instance, key)

            if isinstance(value_list, Manager):
                value_list = value_list.all()

            if not isinstance(value_list, QuerySet):
                raise TypeError

            model_name = value_list.model.get_verbose_name_plural()
            value_list = list(value_list)
            model_count = len(value_list)

            summary_list = []
            for value in value_list:
                summary = make_summary_dict(value,
                                            sub_fields,
                                            badge_field)
                summary_list.append(summary)

            sub_dict = {
                'list':        summary_list,
                'model_name':  model_name,
                'model_count': model_count
                }

            related_dict.update({key: sub_dict})

        except AttributeError:
            warnings.simplefilter('always')
            warning_string = 'Did not find the field ' \
                             + key + ' specified in related_fields.'
            warnings.warn(warning_string)

        except TypeError:
            warnings.simplefilter('always')
            warning_string = 'The field ' + key + ' does not refer to a ' \
                                                  'QuerySet'
            warnings.warn(warning_string)

    return related_dict


def make_detail_dict(instance: CustomBaseModel,
                     detail_fields: List[str],
                     related_objects: List[dict]) -> dict:
    detail_dict = make_fields_dict(instance, detail_fields)
    detail_dict['title'] = instance.display_name
    related_dict = make_related_dict(instance, related_objects)
    detail_dict['related'] = related_dict

    return detail_dict
