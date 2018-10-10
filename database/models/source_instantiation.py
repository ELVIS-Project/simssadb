"""Define a SourceInstantiation model"""
from django.core.exceptions import ValidationError
from django.db import models

from database.models import CustomBaseModel


class SourceInstantiation(CustomBaseModel):
    """An abstract entity defined by the music specified by a
    particular Source, which corresponds to a particular
    instantiation of all or part of a Musical Work, Sections or Parts.

    Manifested by Audio, Symbolic, Text or Image files.

    Attributes
    ----------
    SourceInstantiation.source : models.ForeignKey
        Reference to the Source instantiated by this SourceInstantiation

    SourceInstantiation.work : models.ForeignKey
        Reference to a MusicalWork defined in full by this SourceInstantiation

    SourceInstantiation.sections : models.ManyToManyField
        References to Sections defined in full by this SourceInstantiation

    SourceInstantiation.parts : models.ManyToManyField
        References to Parts defined in full by this SourceInstantiation

    SourceInstantiation.manifested_by_audio_files : models.ManyToOneRel
        References to AudioFiles that manifest this SourceInstantiation

    SourceInstantiation.manifested_by_text_files : models.ManyToOneRel
        References to TextFiles that manifest this SourceInstantiation

    SourceInstantiation.manifested_by_image_files : models.ManyToOneRel
        References to ImageFiles that manifest this SourceInstantiation

    SourceInstantiation.manifested_by_sym_files : models.ManyToOneRel
        References to SymbolicMusicFiles that manifest this SourceInstantiation

    See Also
    --------
    database.models.CustomBaseModel
    database.models.Source
    database.models.SymbolicMusicFile
    database.models.TextFile
    database.models.ImageFile
    database.models.AudioFile
    database.models.MusicalWork
    database.models.Section
    database.models.Part
    """
