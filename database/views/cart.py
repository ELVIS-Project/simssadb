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
        print(self.request.session["cart"])
        files = File.objects.filter(id__in=self.request.session["cart"])
        context["files"] = files
        return context


