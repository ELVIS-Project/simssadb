from database.views.generic_model_viewset import GenericModelViewSet
from database.models.encoder import Encoder
from database.serializers.encoder import EncoderSerializer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, UpdateView, DeleteView)


class EncoderViewSet(GenericModelViewSet):
    queryset = Encoder.objects.all()
    serializer_class = EncoderSerializer


class CreateEncoderView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    fields = '__all__'
    model = Encoder
    template_name = 'form.html'
