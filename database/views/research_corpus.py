from django.views.generic import DetailView, ListView, View, TemplateView
from database.models import ResearchCorpus, File
from extra_views import SearchableListMixin
from django.http import JsonResponse
import json

class ResearchCorpusDetailView(DetailView):
    model = ResearchCorpus
    template_name = "detail.html"


class ResearchCorpusListView(SearchableListMixin, ListView):
    model = ResearchCorpus
    search_fields = ["title"]
    queryset = ResearchCorpus.objects.order_by("title")
    paginate_by = 100
    template_name = "list.html"


class AddFileToResearchCorpus(View):
    def get(self, request, *args, **kwargs):
        print("Get request!")
        return JsonResponse({"hello": "world"})

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        corpus = ResearchCorpus.objects.get(id=data["research_corpus"])
        file = File.objects.get(id=data["file"])
        corpus.files.add(file)
        response = {"file_name": file.__str__(), "research_corpus": corpus.__str__(), }
        return JsonResponse(response)

class ButtonTestView(TemplateView):
    template_name = "button_test.html"
