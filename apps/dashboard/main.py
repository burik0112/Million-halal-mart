from django.shortcuts import render, redirect, get_object_or_404
from apps.merchant.models import Information
from django.views.generic import ListView
from django.views import View
from decouple import config
from django.core.exceptions import ImproperlyConfigured


def get_env_value(env_variable):
    try:
        return config(env_variable)
    except KeyError:
        error_msg = "Set the {} environment variable".format(env_variable)
        raise ImproperlyConfigured(error_msg)


CHANNEL = get_env_value("CHANNEL")
BOT_TOKEN = get_env_value("BOT_TOKEN")


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


def bot(order):
    text4channel = f"""Yangi buyurtma:\nBuyurtma raqami: {order.id}\nFoydalanuvchi: {order.user.full_name}\nTel raqami: {order.user.phone_number}\nManzili: {order.user.locaton}\nMahsulotlar: {order.products}\nIzoh: {order.comment}\nJami: {order.total_amount}"""
    url = f"https://api.telegram.org/{BOT_TOKEN}/sendMessage?chat_id={CHANNEL}&text={text4channel}"
    return url
