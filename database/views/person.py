from django.views.generic import DetailView, ListView
from database.models import Person
from extra_views import SearchableListMixin


class PersonDetailView(DetailView):
    model = Person
    context_object_name = "person"


class PersonListView(SearchableListMixin, ListView):
    model = Person
    search_fields = [
        "surname",
        "given_name",
    ]
    context_object_name = "persons"
    queryset = Person.objects.order_by("surname")
    paginate_by = 100
