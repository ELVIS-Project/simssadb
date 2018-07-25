from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import PersonSerializer
from database.models.person import Person
from drf_haystack.viewsets import HaystackViewSet
from database.serializers import PersonSearchSerializer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, UpdateView, DeleteView)
from database.models.person import Person
from database.forms import PersonForm


class PersonViewSet(GenericModelViewSet):
    queryset = Person.objects.all().prefetch_related('works_contributed_to',
                                                     'sections_contributed_to').order_by('surname', 'given_name')
    serializer_class = PersonSerializer


class CreatePersonView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    form_class = PersonForm
    model = Person


class PersonSearchView(HaystackViewSet):
    index_models = [Person]
    serializer_class = PersonSearchSerializer
