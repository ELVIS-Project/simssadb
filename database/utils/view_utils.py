import warnings
from typing import *

from django.db.models.manager import Manager
from django.db.models.query import QuerySet

from database.models.custom_base_model import CustomBaseModel


class DetailedAttribute(NamedTuple):
    attribute_name: str = ''
    fields: List[str] = []
    badge_field: Optional[str] = None


def make_fields_dict(instance: CustomBaseModel,
                     fields_list: List[str]) -> dict:
    fields_dict = {}
    if fields_list:
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
    summary_dict['absolute_url'] = instance.get_absolute_url

    if badge_field:
        summary_dict['badge_name'] = badge_field
        badge_list = getattr(instance, badge_field)
        if isinstance(badge_list, Manager):
            badge_count = badge_list.count()
        elif isinstance(badge_list, Iterable) and not isinstance(badge_list,
                                                                 str):
            badge_list = list(badge_list)
            badge_count = len(badge_list)
        elif isinstance(badge_list, Sized):
            badge_count = len(badge_list)
        else:
            badge_count = 1
        summary_dict['badge_count'] = badge_count

    return summary_dict


def make_related_dict(instance: CustomBaseModel,
                      related_models: List[DetailedAttribute]) -> dict:
    related_dict = {}
    if related_models:
        for model in related_models:
            try:
                objects = getattr(instance, model.attribute_name)

                if isinstance(objects, Manager):
                    objects = objects.all()

                if not isinstance(objects, QuerySet):
                    raise TypeError

                model_name = objects.model.get_verbose_name_plural()
                model_count = objects.count()
                objects = list(objects)

                summary_list = []
                for value in objects:
                    summary = make_summary_dict(value,
                                                model.fields,
                                                model.badge_field)
                    summary_list.append(summary)

                sub_dict = {
                    'list':        summary_list,
                    'model_name':  model_name,
                    'model_count': model_count
                    }

                related_dict.update({model.attribute_name: sub_dict})

            except AttributeError:
                warnings.simplefilter('always')
                warning_string = 'Did not find the field ' \
                                 + model.attribute_name + ' specified in ' \
                                                          'related_fields.'
                warnings.warn(warning_string)

            except TypeError:
                warnings.simplefilter('always')
                warning_string = 'The field ' + \
                                 model.attribute_name + ' does not refer to a' \
                                                        ' QuerySet'
                warnings.warn(warning_string)

    return related_dict


def make_detail_dict(instance: CustomBaseModel,
                     detail_fields: List[str],
                     related_models: List[DetailedAttribute]) -> dict:
    detail_dict = make_fields_dict(instance, detail_fields)
    detail_dict['title'] = instance.display_name
    related_dict = make_related_dict(instance, related_models)
    detail_dict['related'] = related_dict

    return detail_dict
