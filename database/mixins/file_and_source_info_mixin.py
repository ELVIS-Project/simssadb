"""Define a Mixin to extract info about files and sources"""
from typing import Optional, Set

from django.db.models.query import QuerySet

from database.models.audio_file import AudioFile
from database.models.collection_of_sources import CollectionOfSources
from database.models.encoder import Encoder
from database.models.extracted_feature import ExtractedFeature
from database.models.image_file import ImageFile
from database.models.symbolic_music_file import SymbolicMusicFile
from database.models.text_file import TextFile
from database.models.validator import Validator


class FileAndSourceInfoMixin(object):
    """
    A mixin for Work/Section/Part to access information about Sources and Files
    """
    @property
    def symbolic_files(self) -> QuerySet:
        """Gets all the Symbolic Files related to this Work/Section/Part"""
        ids = []
        source_instantiations_instantiations = self.source_instantiations.all()
        for instantiation in source_instantiations_instantiations:
            ids.extend(list(instantiation.manifested_by_sym_files.values_list(
                    'id', flat=True)))
        files = SymbolicMusicFile.objects.filter(id__in=ids)
        return files

    @property
    def symbolic_music_formats(self) -> Optional[Set[str]]:
        """Gets the formats of all the Symbolic Files related to this
        Work/Section/Part"""
        formats = set()
        files = self.symbolic_files
        for file in files:
            formats.add(file.file_type)
        if len(formats) == 0:
            return None
        return formats

    @property
    def image_files(self) -> QuerySet:
        """Gets all the Image Files related to this Work/Section/Part"""
        ids = []
        source_instantiations = self.source_instantiations.all()
        for source in source_instantiations:
            ids.extend(list(source.manifested_by_image_files.values_list(
                    'id', flat=True)))
        files = ImageFile.objects.filter(id__in=ids)
        return files

    @property
    def image_formats(self) -> Optional[Set[str]]:
        """Gets the formats of all the Image Files related to this
        Work/Section/Part"""
        formats = set()
        files = self.image_files
        for file in files:
            formats.add(file.file_type)
        if len(formats) == 0:
            return None
        return formats

    @property
    def text_files(self) -> QuerySet:
        """Gets all the Symbolic Files related to this Work/Section/Part"""
        ids = []
        source_instantiations = self.source_instantiations.all()
        for instantiation in source_instantiations:
            ids.extend(list(instantiation.manifested_by_text_files.values_list(
                    'id', flat=True)))
        files = TextFile.objects.filter(id__in=ids)
        return files

    @property
    def text_formats(self) -> Optional[Set[str]]:
        """Gets the formats of all the Image Files related to this
        Work/Section/Part"""
        formats = set()
        files = self.text_files
        for file in files:
            formats.add(file.file_type)
        if len(formats) == 0:
            return None
        return formats

    @property
    def audio_files(self) -> QuerySet:
        """Gets all the Symbolic Files related to this Work/Section/Part"""
        ids = []
        source_instantiations = self.source_instantiations.all()
        for instantiation in source_instantiations:
            ids.extend(list(instantiation.manifested_by_audio_files.values_list(
                    'id', flat=True)))
        files = AudioFile.objects.filter(id__in=ids)
        return files

    @property
    def audio_formats(self) -> Optional[Set[str]]:
        """Gets the formats of all the Image Files related to this
        Work/Section/Part"""
        formats = set()
        files = self.audio_files
        for file in files:
            formats.add(file.file_type)
        if len(formats) == 0:
            return None
        return formats

    @property
    def encoders(self) -> QuerySet:
        """Gets all the Encoders for files related to this Work/Section/Part"""
        ids = []
        source_instantiations = self.source_instantiations.all()
        for instantiation in source_instantiations:
            ids.extend(list(instantiation.encoders.values_list(
                    'id', flat=True)))
        encoders = Encoder.objects.filter(id__in=ids)
        return encoders

    @property
    def validators(self) -> QuerySet:
        """Gets all the Validators for files related to this
        Work/Section/Part"""
        ids = []
        source_instantiations = self.source_instantiations.all()
        for instantiation in source_instantiations:
            ids.extend(list(instantiation.validators.values_list(
                    'id', flat=True)))
        validators = Validator.objects.filter(id__in=ids)
        return validators

    @property
    def features(self) -> QuerySet:
        """Gets all the Features extracted from files related to this
        Work/Section/Part"""
        ids = []
        sym_files = self.symbolic_files
        for file in sym_files:
            ids.extend(list(file.features.values_list('id', flat=True)))
        features = ExtractedFeature.objects.filter(id__in=ids)
        return features

    @property
    def collections_of_sources(self) -> QuerySet:
        """Gets all the Collections of Sources related to this
        Work/Section/Part"""
        ids = []
        source_instantiations = self.source_instantiations.all()
        for instantiation in source_instantiations:
            ids.append(instantiation.source.collection_id)
        collections = CollectionOfSources.objects.filter(id__in=ids)
        return collections

    @property
    def languages(self) -> Optional[Set[str]]:
        """Gets all the languages of the Sources and Text Files related to
        this Work/Section/Part"""
        languages = set()
        source_instantiations = self.source_instantiations.all()
        for source in source_instantiations:
            for text_file in source.manifested_by_text_files.all():
                if text_file.languages:
                    for language in text_file.languages:
                        languages.add(language)
        if len(languages) == 0:
            return None
        return languages
