from django.db.models import Count

from database.models.genre_as_in_type import GenreAsInType
from database.views.generic_model_viewset import GenericModelViewSet


class GenreAsInTypeViewSet(GenericModelViewSet):
    queryset = GenreAsInType.objects.annotate(work_count=Count('type')). \
        filter(work_count__gte=1). \
        prefetch_related('type').order_by('name')
