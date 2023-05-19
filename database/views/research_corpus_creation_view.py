from typing import Union

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import FormView
from psycopg2.extras import DateRange
from database.forms.creation_forms import ResearchCorpusForm, FileForm
from database.models import ResearchCorpus, File
from django.views.generic import CreateView

class CreateResearchCorpus(CreateView):
    template_name = 'database/research_corpus_creation_form.html'
    form_class = ResearchCorpusForm
    model = ResearchCorpus