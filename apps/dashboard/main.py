from django.shortcuts import render, redirect, get_object_or_404
from apps.merchant.models import Information
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView


def index(request):
    return render(request, "index.html")


def dashboard(request):
    return render(request, "base.html")

def get_info(request):
    return render(request, "dashboard/info_list.html")