"""Define a ExperimentalStudy model"""
from django.db import models

from database.models.custom_base_model import CustomBaseModel
from database.models.institution import Institution
from database.models.research_corpus import ResearchCorpus


class ExperimentalStudy(CustomBaseModel):
    """An empirical study based on Files from a particular Research Corpus

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
    title = models.CharField(max_length=200, blank=False,
                             help_text='The title of the Experimental Study')
    published = models.BooleanField(default=False,
                                    help_text='Whether or not the '
                                              'Experimental Study was '
                                              'published')
    date = models.DateField(null=True, help_text='The date in which the '
                                                 'Experimental Study'
                                                 'was published or performed')
    link = models.URLField(blank=True,
                           null=True,
                           help_text='A link to a paper of the Experimental '
                                     'Study')
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
    authors = models.CharField(max_length=200, null=True,
                               help_text='The authors of this Experimental '
                                         'Study')

    class Meta(CustomBaseModel.Meta):
        db_table = 'experimental_study'
        verbose_name_plural = 'Experimental Studies'

    def __str__(self):
        return "{0}".format(self.title)

    def _prepare_summary(self):
        """Prepare a dictionary that summarizes an instance of this model.

        Useful when listing many instances in a list-type view.

        Returns
        -------
        summary : dict
            A dictionary containing the essential data to display this object
            in a list-type view.

        See Also
        --------
        database.models.CustomBaseModel.summary: the property that validates
        the returned dictionary and exposes it to other classes.

        """
        summary = {
            'display':         self.title,
            'url':             self.get_absolute_url(),
            'research_corpus': self.research_corpus_used.title
            }

        return summary

    def detail(self):
        """Get all the data about this instance relevant to a user.

        Useful when displaying this object in a detail-type view.

        Returns
        -------
        detail_dict : dict
            A dictionary containing the relevant data about this instance.

        Warnings
        --------
        This method causes database calls and can be expensive, avoid using in a
        loop.

        """
        detail_dict = {
            'title':                self.title,
            'research_corpus_used': self.research_corpus_used,
            'published':            self.published,
            'date':                 self.date,
            'link':                 self.link,
            'institution':          self.institution,
            'authors':              self.authors,
            }

        return detail_dict
