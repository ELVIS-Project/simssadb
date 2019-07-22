from django.views.generic import DetailView, ListView
from database.models import File
from extra_views import SearchableListMixin

class FileDetailView(DetailView):
    model = File
    context_object_name = "file"


class FileListView(SearchableListMixin, ListView):
    model = File
    search_fields = ["file_type", "file_format"]
    queryset = File.objects.order_by("id")
    paginate_by = 100
    template_name = "list.html"
