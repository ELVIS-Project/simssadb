from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import ResearchCorpusSerializer
from database.models.research_corpus import ResearchCorpus
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, UpdateView, DeleteView)


class ResearchCorpusViewSet(GenericModelViewSet):
    queryset = ResearchCorpus.objects.all()
    serializer_class = ResearchCorpusSerializer


class CreateResearchCorpusView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    fields = '__all__'
    model = ResearchCorpus
    template_name = 'form.html'