from haystack import indexes

from database.models.musical_work import MusicalWork
from database.models.section import Section
from database.models.symbolic_music_file import SymbolicMusicFile


class WorkSectionPartAbstractIndex(indexes.SearchIndex):
    composers = indexes.MultiValueField(null=True, faceted=True)
    dates = indexes.MultiValueField(null=True,
                                    model_attr='composers_dates',
                                    faceted=True)
    places = indexes.MultiValueField(null=True,
                                     model_attr='composers_locations')
    sym_formats = indexes.MultiValueField(null=True,
                                          model_attr='symbolic_music_formats')
    audio_formats = indexes.MultiValueField(null=True,
                                            model_attr='audio_formats')
    text_formats = indexes.MultiValueField(null=True,
                                           model_attr='text_formats')
    image_formats = indexes.MultiValueField(null=True,
                                            model_attr='image_formats')
    certainty = indexes.BooleanField(null=True,
                                     model_attr='certainty_of_attributions',
                                     faceted=True)
    languages = indexes.MultiValueField(null=True,
                                        model_attr='languages')

    def prepare_composers(self, obj):
        return [composer['person'] for composer in obj.composers]

    def get_model(self):
        return self.model


class MusicalWorkIndex(WorkSectionPartAbstractIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    sacred_or_secular = indexes.BooleanField(model_attr='sacred_or_secular',
                                             null=True,
                                             faceted=True)
    instruments = indexes.MultiValueField(null=True, faceted=True)
    styles = indexes.MultiValueField(null=True, faceted=True)
    types = indexes.MultiValueField(null=True, faceted=True)

    def get_model(self):
        return MusicalWork

    def prepare_instruments(self, obj):
        return [instrument.name for instrument in obj.instrumentation]

    def prepare_styles(self, obj):
        return [style.name for style in obj.genres_as_in_style.all()]

    def prepare_types(self, obj):
        return [type.name for type in obj.genres_as_in_type.all()]


class SectionIndex(WorkSectionPartAbstractIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    instruments = indexes.MultiValueField(null=True, faceted=True)

    def prepare_instruments(self, obj):
        return [instrument.name for instrument in obj.instrumentation]

    def get_model(self):
        return Section


class SymbolicMusicFileIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    composers = indexes.MultiValueField(null=True, faceted=True)
    certainty = indexes.BooleanField(null=True,
                                     model_attr='certainty',
                                     faceted=True)
    sacred_or_secular = indexes.BooleanField(model_attr='sacred_or_secular',
                                             null=True,
                                             faceted=True)
    instruments = indexes.MultiValueField(null=True, faceted=True)
    styles = indexes.MultiValueField(null=True, faceted=True)
    types = indexes.MultiValueField(null=True, faceted=True)
    file_format = indexes.CharField(null=True, faceted=True,
                                    model_attr='file_type')

    def prepare_composers(self, obj):
        return [composer.name for composer in obj.composers]

    def prepare_instruments(self, obj):
        return [instrument.name for instrument in obj.instrumentation]

    def prepare_styles(self, obj):
        return [style.name for style in obj.genres_as_in_style.all()]

    def prepare_types(self, obj):
        return [type.name for type in obj.genres_as_in_type.all()]

    def get_model(self):
        return SymbolicMusicFile
