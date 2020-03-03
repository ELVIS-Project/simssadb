from django.views.generic.base import TemplateView
from typing import *
from database.models import File, ResearchCorpus
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
import json


class CartView(TemplateView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not "cart" in self.request.session or self.request.session["cart"] is None:
            self.request.session["cart"] = []
        files = File.objects.filter(id__in=self.request.session["cart"])
        context["files"] = files
        return context


@require_POST
def add_to_cart(request: HttpRequest) -> JsonResponse:
    if not "cart" in request.session:
        request.session["cart"] = []

    data = json.loads(request.body)

    if "file_id" in data:
        file_id = int(data["file_id"])
        file = File.objects.get(id=data["file_id"])
        request.session["cart"].append(file_id)
        response = {"file_name": file.__str__()}

    elif "corpus_id" in data:
        corpus_id = data["corpus_id"]
        corpus = get_object_or_404(ResearchCorpus, pk=corpus_id)
        file_ids = [int(i)
                    for i in corpus.files.all().values_list("id", flat=True)]
        request.session["cart"].extend(file_ids)
        response = {"corpus_name": corpus.__str__()}

    elif "search_results_file_ids" in data:
        search_results_file_ids = [int(i)
                                   for i in data["search_results_file_ids"]]
        request.session["cart"].extend(search_results_file_ids)
        response = {}

    # Removes duplicates but preserves the order of insertion
    request.session["cart"] = list(dict.fromkeys(request.session["cart"]))
    request.session.modified = True
    return JsonResponse(response)


@require_POST
def remove_from_cart(request: HttpRequest) -> JsonResponse:
    data = json.loads(request.body)
    file_id = int(data["file_id"])
    file = File.objects.get(id=data["file_id"])
    request.session["cart"].remove(file_id)
    request.session.modified = True
    response = {"file_name": file.__str__()}
    return JsonResponse(response)

@require_POST
def clear_cart(request: HttpRequest) -> JsonResponse:
    request.session["cart"].clear()
    request.session.modified = True
    response = {}
    return JsonResponse(response)
