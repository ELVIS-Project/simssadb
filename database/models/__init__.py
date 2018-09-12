"""Defines all the models used in the database application

The models are:

* Archive - A location where Sources and Collections of Sources are stored
* AudioFile - A manifestation of a Source as an digital audio file
* CollectionOfSources - A reference to one or more Sources grouped together
* Contribution - Relates a Person that contributed to a work/section/part
* CustomBaseModel - Base model that contains common fields for other models
* Encoder - A User or Software that encoded a file using a workflow
* EncoderValidatorBaseModel - A base model for Encoder and Validator
* ExperimentalStudy - A study based on Files from a particular Research Corpus
* ExtractedFeature - Content-based data extracted from a file
* File - Base abstract model with fields common to all file types
* GenreAsInStyle - A musical genre (type of work or style)
* GeographicArea - A geographic area that can be part of another are
* ImageFile - A manifestation of a Source as digital images
* Institution - A real world institution (usually academic)
* Instrument - An instrument or voice
* MusicalWork - A complete work of music
* Part - A single voice or instrument in a Section of a Musical Work
* Person - A real world person that contributed to a musical work
* Profile - Extends the user model to allow for extra data
* ResearchCorpus - A collection of files that can be used in a ExperimentStudy
* Section - A component of a Musical Work e.g. an Aria in an Opera
* Software - A Software that encoded, validated or extracted features files
* Source - A document containing the music of a Musical Work/Section/Part
* SymbolicMusicFile - A manifestation of a Source as a symbolic music file
* TextFile - A manifestation of a Source as a digital Text file
* Validator - A User or Software that verified the quality of files

"""
from database.models.archive import Archive
from database.models.audio_file import AudioFile
from database.models.collection_of_sources import CollectionOfSources
from database.models.contribution import Contribution
from database.models.custom_base_model import CustomBaseModel
from database.models.encoder import Encoder
from database.models.encoder_validator_base_model import \
    EncoderValidatorBaseModel
from database.models.experimental_study import ExperimentalStudy
from database.models.extracted_feature import ExtractedFeature
from database.models.file import File
from database.models.genre_as_in_style import GenreAsInStyle
from database.models.geographic_area import GeographicArea
from database.models.image_file import ImageFile
from database.models.institution import Institution
from database.models.instrument import Instrument
from database.models.musical_work import MusicalWork
from database.models.part import Part
from database.models.person import Person
from database.models.profile import Profile
from database.models.research_corpus import ResearchCorpus
from database.models.section import Section
from database.models.software import Software
from database.models.source import Source
from database.models.symbolic_music_file import SymbolicMusicFile
from database.models.text_file import TextFile
from database.models.validator import Validator
from database.models.feature_type import FeatureType
