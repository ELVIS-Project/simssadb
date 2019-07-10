from django.views.generic import DetailView
from database.models import GeographicArea


class GeographicAreaDetailView(DetailView):
    model = GeographicArea
    context_object_name = "geographic_area"
