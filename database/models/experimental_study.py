from django.db import models
from database.models.custom_base_model import CustomBaseModel
from database.models.research_corpus import ResearchCorpus
from database.models.institution import Institution
from django.contrib.auth.models import User


class ExperimentalStudy(CustomBaseModel):
    """An empirical study based on Files from a particular Research Corpus

    """
    title = models.CharField(max_length=200, blank=False)
    published = models.BooleanField(default=False)
    date = models.DateField(null=True)
    link = models.URLField(blank=True)
    research_corpus_used = models.ForeignKey(ResearchCorpus,
                                             on_delete=models.PROTECT,
                                             null=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL,
                                    null=True)
    authors = models.ManyToManyField(User)

    def __str__(self):
        return "{0}".format(self.title)


    class Meta(CustomBaseModel.Meta):
        db_table = 'experimental_study'
        verbose_name_plural = 'Experimental Studies'
