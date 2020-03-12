import requests
import zipfile
import io
import os
from database.models import File, FeatureFile, ResearchCorpus
from django.http import FileResponse, HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_safe
from database.utils.view_utils import zip_files
from datetime import datetime


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


@require_safe
def download_cart(request: HttpRequest) -> HttpResponse:
    file_ids = request.session["cart"]
    feature_files_on = request.GET.get("feature_files_on")
    files = File.objects.filter(id__in=file_ids)
    file_name = datetime.now().strftime('%Y-%m-%d-%H_%M') + "-simssadb-download-cart"
    if feature_files_on:
        feature_files = FeatureFile.objects.filter(features_from_file__in=file_ids)
        zip_file = zip_files(files, file_name, feature_files)
    else:
        zip_file = zip_files(files, file_name)
    response = HttpResponse(zip_file.getvalue(), content_type="application/zip")
    response["Content-Disposition"] = f"attachment; filename={file_name}.zip"
    zip_file.close()
    return response
