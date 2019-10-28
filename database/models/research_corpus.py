"""Defines a ResearchCorpus model"""
from django.db import models

from database.models.custom_base_model import CustomBaseModel
from django.contrib.postgres.fields import ArrayField


class ResearchCorpus(CustomBaseModel):
    """A collection of files that can be used in specific empirical studies.

    Attributes
    ----------
    title : models.CharField
        The title of this ResearchCorpus

    files : models.ManyToManyField
        References to the Files contained in this ResearchCorpus

    studies : models.fields.related_descriptors.ReverseManyToOneDescriptor
        References to the studies that use this ResearchCorpus

    doi_links : models.ArrayField
        An array of URLs linking to Zenodo
    """

    title = models.CharField(
        max_length=200, blank=False, help_text="The title of this Research Corpus"
    )
    files = models.ManyToManyField(
        "File",
        related_name="in_corpora",
        help_text="The Symbolic Music Files that his Research Corpus contains",
    )
    doi_links = ArrayField(
        models.URLField(
            blank=True,
            null=True,
            help_text="An DOI linking to a research corpus saved in Zenodo ",
        ),
        null=True,
        blank=True,
    )

    class Meta(CustomBaseModel.Meta):
        db_table = "research_corpus"
        verbose_name_plural = "Research Corpora"

    def __str__(self):
        return "{0}".format(self.title)
