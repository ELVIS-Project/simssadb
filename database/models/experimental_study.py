from django.db import models
from database.models.custom_base_model import CustomBaseModel
from database.models.research_corpus import ResearchCorpus
from database.models.institution import Institution
from django.contrib.auth.models import User
from database.models.extracted_feature import ExtractedFeature


class ExperimentalStudy(CustomBaseModel):
    """An empirical study based on Files from a particular Research Corpus"""
    title = models.CharField(max_length=200, blank=False,
                             help_text='The title of the Experimental Study')
    published = models.BooleanField(default=False,
                                    help_text='Whether or not the '
                                              'Experimental Study was '
                                              'published')
    date = models.DateField(null=True, help_text='The date in which the '
                                                 'Experimental Study'
                                                 'was published or performed')
    link = models.URLField(blank=True, help_text='A link to a paper of the '
                                                 'Experimental Study')
    features_used = models.ManyToManyField(ExtractedFeature,
                                           help_text='The set of Extracted '
                                                     'Features used in this '
                                                     'study')
    research_corpus_used = models.ForeignKey(ResearchCorpus,
                                             on_delete=models.PROTECT,
                                             null=True,
                                             help_text='The Research Corpus '
                                                       'upon which this '
                                                       'Experimental Study is '
                                                       'based')
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL,
                                    null=True, help_text='An Institution '
                                                         'related to this '
                                                         'Experimental Study')
    authors = models.ManyToManyField(User, help_text='The Users that '
                                                     'authored this study')

    def __str__(self):
        return "{0}".format(self.title)

    def prepare_summary(self):
        summary = {
                'display': self.title,
                'url': self.get_absolute_url(),
                'research_corpus': self.research_corpus_used.title
                }

        return summary

    def get_related(self):
        related = {
            'features': {'list': self.features_used.all(),
                         'model_name': 'Features Used',
                         'model_count': self.features_used.count()
                         },
        }

        return related

    def detail(self):
        detail_dict = {
            'title': self.title,
            'research_corpus_used': self.research_corpus_used
            'published': self.published,
            'date': self.date,
            'link': self.link,
            'institution': self.institution,
            'authors': list(self.authors),
        }

        return detail_dict


    class Meta(CustomBaseModel.Meta):
        db_table = 'experimental_study'
        verbose_name_plural = 'Experimental Studies'
