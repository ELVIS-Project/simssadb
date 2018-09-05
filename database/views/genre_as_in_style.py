from django.db.models import Count

from database.models.genre_as_in_style import GenreAsInStyle
from database.views.generic_model_viewset import GenericModelViewSet


class GenreAsInStyleViewSet(GenericModelViewSet):
    queryset = GenreAsInStyle.objects.annotate(work_count=Count('style')). \
        filter(work_count__gte=1). \
        prefetch_related('style').order_by('name')
