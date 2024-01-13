from apps.merchant.models import Information, Service
from decouple import config
from django.core.exceptions import ImproperlyConfigured
import requests
import urllib.parse
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views import View
from .forms import ReminderForm, AgrementForm, ShipmentForm, PrivacyForm, AboutUsForm, SupportForm, PaymentForm


def edit_reminder(request, pk):
    info = get_object_or_404(Information, pk=pk)
    if request.method == "POST":
        form = ReminderForm(request.POST, instance=info)
        if form.is_valid():
            form.save()
            return redirect("info-list")
    else:
        form = ReminderForm(instance=info)

    return render(request, "information/edit_reminder.html", {"form": form})


def edit_agreement(request, pk):
    info = get_object_or_404(Information, pk=pk)
    if request.method == "POST":
        form = AgrementForm(request.POST, instance=info)
        if form.is_valid():
            form.save()
            return redirect("info-list")
    else:
        form = AgrementForm(instance=info)

    return render(request, "information/edit_agreement.html", {"form": form})


def edit_shipment(request, pk):
    info = get_object_or_404(Information, pk=pk)
    if request.method == "POST":
        form = ShipmentForm(request.POST, instance=info)
        if form.is_valid():
            form.save()
            return redirect("info-list")
    else:
        form = ShipmentForm(instance=info)

    return render(request, "information/edit_shipment.html", {"form": form})

def edit_privacy(request, pk):
    info = get_object_or_404(Information, pk=pk)
    if request.method == "POST":
        form = PrivacyForm(request.POST, instance=info)
        if form.is_valid():
            form.save()
            return redirect("info-list")
    else:
        form = PrivacyForm(instance=info)

    return render(request, "information/edit_privacy.html", {"form": form})

def edit_aboutus(request, pk):
    info = get_object_or_404(Information, pk=pk)
    if request.method == "POST":
        form = AboutUsForm(request.POST, instance=info)
        if form.is_valid():
            form.save()
            return redirect("info-list")
    else:
        form = AboutUsForm(instance=info)

    return render(request, "information/edit_aboutus.html", {"form": form})

def edit_support(request, pk):
    info = get_object_or_404(Information, pk=pk)
    if request.method == "POST":
        form = SupportForm(request.POST, instance=info)
        if form.is_valid():
            form.save()
            return redirect("info-list")
    else:
        form = SupportForm(instance=info)

    return render(request, "information/edit_support.html", {"form": form})

def edit_payment(request, pk):
    info = get_object_or_404(Information, pk=pk)
    if request.method == "POST":
        form = PaymentForm(request.POST, instance=info)
        if form.is_valid():
            form.save()
            return redirect("info-list")
    else:
        form = PaymentForm(instance=info)

    return render(request, "information/edit_payment.html", {"form": form})