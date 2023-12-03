from django.shortcuts import render, redirect, get_object_or_404
from apps.merchant.models import Information
from django.views.generic import ListView
from django.views import View


def index(request):
    return render(request, "index.html")


def dashboard(request):
    return render(request, "base.html")


class InformationView(ListView):
    model = Information
    template_name = "dashboard/info_list.html"  # your template name
    context_object_name = "infos"

    def get_queryset(self):
        return Information.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

