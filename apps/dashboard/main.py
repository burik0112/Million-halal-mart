from django.shortcuts import render
from apps.merchant.models import Information, Service
from django.views.generic import ListView
from decouple import config
from django.core.exceptions import ImproperlyConfigured
import requests
import urllib.parse
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views import View
from .forms import ServiceEditForm, InformationEditForm
from apps.product.models import Phone, Ticket, Good


def get_env_value(env_variable):
    try:
        return config(env_variable)
    except KeyError:
        error_msg = "Set the {} environment variable".format(env_variable)
        raise ImproperlyConfigured(error_msg)


CHANNEL = int(get_env_value("CHANNEL"))
CHAT_ID = int(get_env_value("CHAT_ID"))
BOT_TOKEN = get_env_value("BOT_TOKEN")
CHANNEL_USERNAME = "@openai_chat_gpt_robot"


def index(request):
    return render(request, "index.html")


def dashboard(request):
    return render(request, "base.html")


class InformationView(ListView):
    model = Information
    template_name = "dashboard/info_list.html"
    context_object_name = "infos"

    def get_queryset(self):
        return Information.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class InformationEditView(View):
    template_name = "dashboard/edit_info.html"

    def get(self, request, pk):
        info = get_object_or_404(Information, pk=pk)
        form = InformationEditForm(instance=info)
        return render(request, self.template_name, {"form": form, "info": info})

    def post(self, request, pk):
        info = get_object_or_404(Information, pk=pk)
        if "edit" in request.POST:
            form = InformationEditForm(request.POST, instance=info)
            if form.is_valid():
                form.save()
                return redirect("info-list")
        return render(request, self.template_name, {"form": form, "info": info})


class ServiceView(ListView):
    model = Service
    template_name = "dashboard/service_list.html"
    context_object_name = "services"

    def get_queryset(self):
        return Service.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ServiceEditView(View):
    template_name = "dashboard/edit_service.html"

    def get(self, request, pk):
        service = get_object_or_404(Service, pk=pk)
        form = ServiceEditForm(instance=service)
        return render(request, self.template_name, {"form": form, "service": service})

    def post(self, request, pk):
        service = get_object_or_404(Service, pk=pk)
        if "edit" in request.POST:
            form = ServiceEditForm(request.POST, instance=service)
            if form.is_valid():
                form.save()
                return redirect("service-list")
        return render(request, self.template_name, {"form": form, "service": service})


def bot(order):
    text4channel = f"""🔰Yangi buyurtma:\nBuyurtma raqami: {order.id}\nFoydalanuvchi: {order.user.full_name}\nTel raqami: {order.user.phone_number}\nManzil:\n"""
    for location in order.user.location.all():
        text4channel += f"  - {location.address}\n"
    text4channel +='Mahsulotlar: \n'
    for order_item in order.get_order_items():
        product_details = order.get_product_details(order_item.product, order_item)
        text4channel += f"{product_details}\n"
    text4channel += f"Izoh: {order.comment}\nJami: {order.total_amount}"
    inline_keyboard = [
        [
            {"text": "Yes", "callback_data": f"yes|{order.id}"},
            {"text": "No", "callback_data": f"no|{order.id}"},
        ]
    ]
    reply_markup = {
        "inline_keyboard": inline_keyboard,
        "resize_keyboard": True,
        "one_time_keyboard": False,
        "selective": False,
        "row_width": 2,
    }
    encoded_reply_markup = urllib.parse.quote(json.dumps(reply_markup))
    url = f"""https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text4channel}&reply_markup={encoded_reply_markup}"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"Error: {e}"

