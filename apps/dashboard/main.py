from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Sum
from apps.merchant.models import Information, Service, Order
from apps.customer.models import Banner, Profile
from apps.product.models import SoldProduct, Ticket, Good, Phone, ProductItem
from decouple import config
from django.core.exceptions import ImproperlyConfigured
import requests
import urllib.parse
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views import View
from .forms import ServiceEditForm, InformationEditForm
from apps.dashboard.forms import BannerForm, NewsForm, NewsEditForm
from apps.customer.models import News
from datetime import date
from django.db.models import Q
from collections import defaultdict
from django.db.models import Sum
from django.db.models import Sum

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
    today = date.today()
    orders = Order.objects.all()
    order_today = Order.objects.filter(
        Q(created__date=today) & Q(status='sent'))
    customers = Profile.objects.all()
    customers_today_count = Profile.objects.filter(created__date=today).count()

    revenue = Order.objects.filter(status='sent').aggregate(
        total_amount_sum=Sum('total_amount'))['total_amount_sum']
    revenue = revenue/1000 if revenue else 0.0
    revenue=round(revenue, 2)

    revenue_today = Order.objects.filter(Q(created__date=today) & Q(status='sent')).aggregate(
        total_amount_sum=Sum('total_amount'))['total_amount_sum']
    revenue_today = revenue_today / 1000 if revenue_today else 0.0
    revenue_today = round(revenue_today, 2)

    recent = orders.order_by('-created')[:25]

    top_selling_products = SoldProduct.objects.all()
    data = defaultdict(list)

    
    for i in top_selling_products:
        product_item = i.product
        item_data = {
            'quantity': i.quantity,
            'revenue': product_item.new_price * i.quantity if product_item.new_price else product_item.old_price * i.quantity
        }

        if hasattr(product_item, 'tickets'):
            t = Ticket.objects.get(product_id=product_item.pk)
            item_data.update({
                'title': t.event_name,
                'price': product_item.new_price if product_item.new_price else product_item.old_price,
                'image': get_first_image_url(product_item),
            })

            existing_item = next(
                (item for item in data['tickets'] if item['title'] == t.event_name), None)
            if existing_item:
                existing_item['quantity'] += i.quantity
                existing_item['revenue'] += item_data['revenue']
            else:
                data['tickets'].append(item_data)

        elif hasattr(product_item, 'phones'):
            p = Phone.objects.get(id=product_item.pk)
            item_data.update({
                'title': p.model_name,
                'price': product_item.new_price if product_item.new_price else product_item.old_price,
                'image': get_first_image_url(product_item),
            })

            existing_item = next(
                (item for item in data['phones'] if item['title'] == p.model_name), None)
            if existing_item:
                existing_item['quantity'] += i.quantity
                existing_item['revenue'] += item_data['revenue']
            else:
                data['phones'].append(item_data)

        elif hasattr(product_item, 'goods'):
            g = Good.objects.get(id=product_item.pk)
            item_data.update({
                'title': g.name,
                'price': product_item.new_price if product_item.new_price else product_item.old_price,
                'image': get_first_image_url(product_item),
            })

            existing_item = next(
                (item for item in data['goods'] if item['title'] == g.name), None)
            if existing_item:
                existing_item['quantity'] += i.quantity
                existing_item['revenue'] += item_data['revenue']
            else:
                data['goods'].append(item_data)

        else:
            print("This ProductItem is not associated with any specific type.")

        product_item.available_quantity += i.quantity
        product_item.save()

    comments=[]
    # for o in orders.order_by('-created'):
    #     com={}
    #     if o.comment and o.id not in com:
    #         com['id']=o.id
    #         com["user"]=o.user.full_name
    #         com["date"]=o.created
    #         com["comment"]=o.comment
    #     comments.append(com)
    orders_with_comments = Order.objects.exclude(comment='')
    most_expensive = []
    for order in orders.filter(status='sent').order_by('-total_amount')[:5]:
        order_info = {
            'id': order.id,
            'user': order.user.full_name,
            'price': round(order.total_amount / 1000, 2),
        }
        most_expensive.append(order_info)

    products_with_quantity = (
    Good.objects.filter(product__available_quantity__lt=50)
    .values('name_uz', 'product__available_quantity')
    .order_by('-product__available_quantity')[:10]
    )
    return render(request, "base.html", {'products_with_quantity':products_with_quantity,'most_expensive':most_expensive,'comments':orders_with_comments,'top_products': top_selling_products, 'customers_today': customers_today_count, 'orders': orders, 'customers': customers, 'revenue': revenue, 'recent': recent, 'order_today': order_today, 'revenue_today': revenue_today, 'data': data})


def get_first_image_url(product_item):
    first_image = product_item.images.first()
    return first_image.image.url if first_image else None


class InformationView(ListView):
    model = Information
    template_name = "dashboard/information/info_list.html"
    context_object_name = "infos"

    def get_queryset(self):
        return Information.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class InformationEditView(View):
    template_name = "dashboard/information/edit_info.html"

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
            return redirect("info-list")

        return render(request, self.template_name, {"form": form, "info": info})


class ServiceView(ListView):
    model = Service
    template_name = "dashboard/service/service_list.html"
    context_object_name = "services"

    def get_queryset(self):
        return Service.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BannerView(ListView):
    model = Banner
    template_name = "dashboard/banner.html"
    context_object_name = "banners"
    form_class = BannerForm

    def get_queryset(self):
        return Banner.objects.all().order_by('-created')

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
    template_name = "dashboard/service/edit_service.html"

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


class NewsListView(ListView):
    model = News
    template_name = "dashboard/news/news_list.html"
    context_object_name = "news"

    def get_queryset(self):
        return News.objects.all().order_by('-pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class NewsCreateView(View):
    template_name = "dashboard/news/news_create.html"

    def get(self, request):
        form = NewsForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = NewsForm(request.POST, request.FILES)
        print(request.FILES)  # Debugging statement
        if form.is_valid():
            print(form.cleaned_data)  # Debugging statement
            form.save()
            return redirect("news-list")
        else:
            print(form.errors)  # Debugging statement
            return render(request, self.template_name, {"form": form})


class NewsEditView(View):
    template_name = "dashboard/news/edit_delete_news.html"

    def get(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        form = NewsEditForm(instance=news)
        return render(request, self.template_name, {"form": form, "news": news})

    def post(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        form = NewsEditForm(request.POST, request.FILES, instance=news)

        if "edit" in request.POST:
            if form.is_valid():
                form.save()
                return redirect("news-list")
            else:
                print(form.errors)  # Print errors to console for debugging
        elif "delete" in request.POST:
            news = get_object_or_404(News, pk=pk)
            news.delete()  # Delete the Phone instance
            return redirect("news-list")  # Redirect to phone list

        # If it's not a valid form or a delete action, render the form with the existing data
        return render(request, self.template_name, {"form": form, "news": news})


class OrdersView(DetailView):
    model = Profile
    template_name = "customer/orders/orders_list.html"

    def get_context_data(self, **kwargs):
        context = super(OrdersView, self).get_context_data(**kwargs)
        user = get_object_or_404(Profile, id=self.kwargs['pk'])
        orders = Order.objects.filter(user=user)

        if orders:
            context["orders"] = orders
            context["user"] = user
        else:
            context["no_orders_message"] = "Foydalanuvhi hali buyurtma qilmagan"

        return context

    def post(self, request, *args, **kwargs):
        order_id = self.kwargs['pk']
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')

        if new_status in dict(order.STATUS_CHOICES):
            order.status = new_status
            order.save()

        return HttpResponseRedirect(reverse('orders-list', kwargs={'pk': order.user.id}))


def update_order_status(request, pk):
    order = get_object_or_404(Order, id=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(order.STATUS_CHOICES):
            order.status = new_status
            order.save()

    return HttpResponseRedirect(reverse('orders-list', kwargs={'pk': order.user.id}))