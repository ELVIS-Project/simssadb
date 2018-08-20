from database.views.generic_model_viewset import GenericModelViewSet
from database.serializers import ContributedToSerializer
from database.models.contributed_to import ContributedTo
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, UpdateView, DeleteView)


class ContributedToViewSet(GenericModelViewSet):
    queryset = ContributedTo.objects.all()
    serializer_class = ContributedToSerializer


class CreateContributedToView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    fields = '__all__'
    model = ContributedTo
    template_name = 'form.html'
