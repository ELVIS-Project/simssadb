"""Define a ExperimentalStudy model."""
from django.db import models

from database.models.custom_base_model import CustomBaseModel


class ExperimentalStudy(CustomBaseModel):
    """An empirical study based on a particular Research Corpus.

    Attributes
    ----------
    ExperimentalStudy.title : models.CharField
        The title of the Experimental Study

    ExperimentalStudy.published : models.BooleanField
        Whether or not the Experimental Study was published

    ExperimentalStudy.date : models.DateField
        The date in which the Experimental Study was published or performed

    ExperimentalStudy.link : models.URLField
        A link to the a paper of the Experimental Study

    ExperimentalStudy.research_corpus_used : models.ForeignKey
        A reference to the Research Corpus upon which the Experimental Study
        is based

    ExperimentalStudy.institution : models.ForeignKey
        A reference to the Institution related to this ExperimentalStudy

    ExperimentalStudy.authors : models.CharField
        The authors of this Experimental Study

    See Also
    --------
    database.models.CustomBaseModel
    database.models.ResearchCorpus
    database.models.Institution
    """

    title = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        help_text="The title of the Experimental Study",
    )
    link = models.URLField(
        blank=True, help_text="A link to a paper of the Experimental Study"
    )
    research_corpus_used = models.ForeignKey(
        "ResearchCorpus",
        on_delete=models.PROTECT,
        related_name="studies",
        null=True,
        help_text="The Research Corpus "
        "upon which this "
        "Experimental Study is "
        "based",
    )

    class Meta(CustomBaseModel.Meta):
        db_table = "experimental_study"
        verbose_name_plural = "Experimental Studies"

    def __str__(self):
        return "{0}".format(self.title)
