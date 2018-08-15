from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import PersonSerializer
from database.models.person import Person
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, UpdateView, DeleteView)
from database.models.person import Person
from database.forms import PersonForm
from django.db.models import Count

class PersonViewSet(GenericModelViewSet):
    queryset = Person.objects.annotate(work_count=Count('works_contributed_to')).filter(work_count__gte=1).prefetch_related('works_contributed_to', 'sections_contributed_to').order_by(
        'surname', 'given_name') # only return person with actual musical works
    serializer_class = PersonSerializer


class CreatePersonView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    form_class = PersonForm
    model = Person
    template_name = 'form.html'
