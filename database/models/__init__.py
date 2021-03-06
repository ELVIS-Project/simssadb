"""Defines all the models used in the database application

The models are:

* Archive - A location where Sources are stored
* Contribution - Relates a Person that contributed to a work/section/part
* CustomBaseModel - Base model that contains common fields for other models
* Encoder - A User or Software that encoded a file using a workflow
* EncoderValidatorBaseModel - A base model for Encoder and Validator
* ExperimentalStudy - A study based on Files from a particular Research Corpus
* ExtractedFeature - Content-based data extracted from a file
* FeatureType - A category of Feature of which ExtractedFeatures are instances
* File - Manifestation of a Source Instantiation as a file
* GenreAsInStyle - A musical genre (type of work or style)
* GeographicArea - A geographic area that can be part of another are
* Instrument - An instrument or voice
* MusicalWork - A complete work of music
* Part - A single voice or instrument in a Section of a Musical Work
* Person - A real world person that contributed to a musical work
* ResearchCorpus - A collection of files that can be used in a ExperimentStudy
* Section - A component of a Musical Work e.g. an Aria in an Opera
* Software - A Software that encoded, validated or extracted features files
* Source - A document containing the music of a Musical Work/Section/Part
* SourceInstantiation - An abstract entity defined by the music in a Source
* Validator - A User or Software that verified the quality of files
"""
from database.models.archive import Archive
from database.models.contribution_musical_work import ContributionMusicalWork
from database.models.custom_base_model import CustomBaseModel
from database.models.encoding_workflow import EncodingWorkFlow
from database.models.experimental_study import ExperimentalStudy
from database.models.extracted_feature import ExtractedFeature
from database.models.feature_type import FeatureType
from database.models.file import File
from database.models.genre_as_in_style import GenreAsInStyle
from database.models.genre_as_in_type import GenreAsInType
from database.models.geographic_area import GeographicArea
from database.models.instrument import Instrument
from database.models.language import Language
from database.models.musical_work import MusicalWork
from database.models.part import Part
from database.models.person import Person
from database.models.research_corpus import ResearchCorpus
from database.models.section import Section
from database.models.software import Software
from database.models.source import Source
from database.models.source_instantiation import SourceInstantiation
from database.models.validation_workflow import ValidationWorkFlow
from database.models.source_instantiation import SourceInstantiation
from database.models.feature_file import FeatureFile
from database.models.type_of_section import TypeOfSection
