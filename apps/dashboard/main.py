from apps.merchant.models import Information, Service
from apps.customer.models import Banner
from decouple import config
from django.core.exceptions import ImproperlyConfigured
import requests
import urllib.parse
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView,DeleteView, DetailView
from django.views import View
from .forms import ServiceEditForm, InformationEditForm
from apps.dashboard.forms import BannerForm


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
        key = request.GET.get('key', None)
        form = InformationEditForm(instance=info)
        return render(request, self.template_name, {"form": form, "info": info, 'key': key})

    def post(self, request, pk):
        info = get_object_or_404(Information, pk=pk)
        form = InformationEditForm(request.POST, instance=info)

        if "edit" in request.POST and form.is_valid():
            form.save()
            print(request)
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

from django.urls import reverse_lazy

class BannerView(ListView):
    model = Banner
    template_name = "dashboard/banner.html"
    context_object_name = "banners"
    form_class = BannerForm

    def get_queryset(self):
        return Banner.objects.all()

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'banners': self.get_queryset(), 'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('banner-list')
        else:
            return render(request, self.template_name, {'banners': self.get_queryset(), 'form': form})

class BannerActionView(View):
    def post(self, request, *args, **kwargs):
        if 'action' not in request.POST:
            return render(request, 'error.html', {'error_message': 'Action not specified'})

        action = request.POST.get('action')
        
        if action == 'toggle':
            # Toggle the active status
            banner = get_object_or_404(Banner, pk=kwargs['pk'])
            banner.active = not banner.active
            banner.save()
        elif action == 'delete':
            # Delete the banner
            banner = get_object_or_404(Banner, pk=kwargs['pk'])
            banner.delete()

        return redirect('banner-list')
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
    text4channel = f"""🔰 <b>Buyurtma holati:</b> #<i>YANGI</i>\n\n 🔢 <b>Buyurtma raqami:</b> <i>{order.id}</i>\n👤 <b>Mijoz ismi:</b> <i>{order.user.full_name}</i>\n📞 <b>Tel raqami:</b> <i>{order.user.phone_number}</i>\n🏠 <b>Manzili:</b> """
    for location in order.user.location.all():
        text4channel += f"{location.address}\n"
    text4channel += '🛒 <b>Mahsulotlar:</b> \n'
    for order_item in order.get_order_items():
        product_details = order.get_product_details(
            order_item.product, order_item)
        text4channel += f" 🟢 <i>{product_details}</i>\n"
    text4channel += f"📝 <b>Izoh:</b> <i>{order.comment}</i>\n📅 <b>Sana:</b> <i>{order.created.strftime('%Y-%m-%d %H:%M')}</i>\n💸 <b>Jami:</b> <i>{order.total_amount} ₩</i>\n\n⁉️ <u>To`lov amalga oshirilganligini tasdiqlaysizmi?</u>"
    inline_keyboard = [
        [
            {"text": "✅ Ha", "callback_data": f"yes|{order.id}"},
            {"text": "❌ Yo'q", "callback_data": f"no|{order.id}"},
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
    encoded_text4channel = urllib.parse.quote(text4channel)
    url = f"""https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={encoded_text4channel}&reply_markup={encoded_reply_markup}&parse_mode=HTML"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"Error: {e}"
