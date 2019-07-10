from django.views.generic import DetailView
from database.models import Person


class PersonDetailView(DetailView):
    model = Person
    context_object_name = "person"
