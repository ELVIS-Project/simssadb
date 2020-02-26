from django.views.generic import DetailView, ListView
from database.models import ResearchCorpus, File
from extra_views import SearchableListMixin

class ResearchCorpusDetailView(DetailView):
    model = ResearchCorpus
    context_object_name = "researchcorpus"
    template_name = "researchcorpus_detail.html"


class ResearchCorpusListView(SearchableListMixin, ListView):
    model = ResearchCorpus
    search_fields = ["title"]
    queryset = ResearchCorpus.objects.order_by("title")
    paginate_by = 100
    template_name = "list.html"
