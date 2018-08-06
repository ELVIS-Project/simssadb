from haystack import indexes

from database.models.genre import Genre
from database.models.geographic_area import GeographicArea
from database.models.institution import Institution
from database.models.instrument import Instrument
from database.models.musical_work import MusicalWork
from database.models.person import Person
from database.models.section import Section


class InstrumentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Instrument


class GenreIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Genre


class InstitutionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    url = indexes.CharField(model_attr='website')

    def get_model(self):
        return Institution


class PersonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)

    def get_model(self):
        return Person


class GeographicAreaIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)

    def get_model(self):
        return GeographicArea


class WorkSectionPartAbstractIndex(indexes.SearchIndex):
    composers = indexes.MultiValueField(null=True, faceted=True)
    dates = indexes.MultiValueField(null=True,
                                    model_attr='dates_of_composition',
                                    faceted=True)
    places = indexes.MultiValueField(null=True,
                                     model_attr='places_of_composition',
                                     faceted=True)
    sym_formats = indexes.MultiValueField(null=True,
                                          model_attr='symbolic_music_formats',
                                          faceted=True)
    audio_formats = indexes.MultiValueField(null=True,
                                            model_attr='audio_formats',
                                            faceted=True)
    text_formats = indexes.MultiValueField(null=True,
                                           model_attr='text_formats',
                                           faceted=True)
    image_formats = indexes.MultiValueField(null=True,
                                            model_attr='image_formats',
                                            faceted=True)
    certainty = indexes.BooleanField(null=True,
                                     model_attr='certainty_of_attribution',
                                     faceted=True)
    languages = indexes.MultiValueField(null=True,
                                        model_attr='languages',
                                        faceted=True)

    def prepare_composers(self, obj):
        return [composer['person'] for composer in obj.composers]

    def prepare_sym_formats(self, obj):
        if obj.symbolic_music_formats:
            return list(obj.symbolic_music_formats)
        else:
            return None

    def get_model(self):
        return self.model


class MusicalWorkIndex(WorkSectionPartAbstractIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    religiosity = indexes.BooleanField(model_attr='religiosity', null=True,
                                       faceted=True)
    instruments = indexes.MultiValueField(null=True, faceted=True)
    styles = indexes.MultiValueField(null=True, faceted=True)
    types = indexes.MultiValueField(null=True, faceted=True)

    def prepare_instruments(self, obj):
        return [instrument.name for instrument in obj.instrumentation]

    def prepare_styles(self, obj):
        return [style.name for style in obj.genres_as_in_style.all()]

    def prepare_types(self, obj):
        return [type.name for type in obj.genres_as_in_type.all()]

    def get_model(self):
        return MusicalWork

class SectionIndex(WorkSectionPartAbstractIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    instruments = indexes.MultiValueField(null=True, faceted=True)

    def prepare_instruments(self, obj):
        return [instrument.name for instrument in obj.instrumentation]

    def get_model(self):
        return Section
