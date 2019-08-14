from django.apps import apps
from django.db.models import QuerySet


class FileMixin:
    source_instantiations: QuerySet

    @property
    def files(self) -> QuerySet:
        file_model = apps.get_model("database", "file")
        files = file_model.objects.filter(
            id__in=self.source_instantiations.all().values_list("files", flat=True)
        )
        return files

    @property
    def files_count(self) -> QuerySet:
        count = self.files.count()
        return count
