import requests
import zipfile
import io
import os
from database.models import File, FeatureFile, ResearchCorpus
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from database.utils.view_utils import zip_files


@require_safe
def download_file(request, is_content: bool, pk: int) -> FileResponse:
    if is_content:
        file_object = get_object_or_404(File, pk=pk)
    else:
        file_object = get_object_or_404(FeatureFile, pk=pk)
    response = FileResponse(file_object.file, as_attachment=True)
    return response


@require_safe
def download_content_file(request, pk: int) -> FileResponse:
    return download_file(request, is_content=True, pk=pk)


@require_safe
def download_feature_file(request, pk: int) -> FileResponse:
    return download_file(request, is_content=False, pk=pk)

    response = HttpResponse(zip_file.getvalue(), content_type="application/zip")
    response["Content-Disposition"] = f"attachment; filename={research_corpus.title}.zip"
    zip_file.close()
    return response
