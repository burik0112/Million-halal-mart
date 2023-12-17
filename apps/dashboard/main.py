from django.shortcuts import render
from apps.merchant.models import Information
from django.views.generic import ListView
from decouple import config
from django.core.exceptions import ImproperlyConfigured
import requests
import urllib.parse
import json


def get_env_value(env_variable):
    try:
        return config(env_variable)
    except KeyError:
        error_msg = "Set the {} environment variable".format(env_variable)
        raise ImproperlyConfigured(error_msg)


CHANNEL = int(get_env_value("CHANNEL"))
BOT_TOKEN = get_env_value("BOT_TOKEN")
CHANNEL_USERNAME = '@openai_chat_gpt_robot'


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


def bot(order):
    text4channel = f"""Yangi buyurtma:\nBuyurtma raqami: {order.id}\nFoydalanuvchi: {order.user.full_name}\nTel raqami: {order.user.phone_number}\nManzillar:\n"""
    for location in order.user.location.all():
        text4channel += f"  - {location.address}\n"

    text4channel += f"Mahsulotlar: {order.products}\nIzoh: {order.comment}\nJami: {order.total_amount}"
    inline_keyboard = [
        [{"text": "Yes", "callback_data": f"yes|{order.id}"},
            {"text": "No", "callback_data": f"no|{order.id}"}]
    ]
    reply_markup = {
        "inline_keyboard": inline_keyboard,
        "resize_keyboard": True,
        "one_time_keyboard": False,
        "selective": False,
        "row_width": 2
    }
    encoded_reply_markup = urllib.parse.quote(json.dumps(reply_markup))
    url = f"""https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id=419717087&text={text4channel}&reply_markup={encoded_reply_markup}"""
    # 419717087
    # 542470747
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"Error: {e}"
