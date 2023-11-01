from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from ..models import Phone, Ticket, Good, Category
from django.views import View
from django.views.generic.edit import CreateView
from .forms import PhoneProductItemForm, TicketProductItemForm, GoodProductItemForm, PhoneCategoryCreateForm


class PhoneListView(ListView):
    model = Phone
    template_name = "phone_list.html"  # your template name
    context_object_name = "phones"

    def get_queryset(self):
        return Phone.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any extra context here
        return context


class CreatePhoneView(View):
    template_name = "product/phone_create.html"

    def get(self, request):
        form = PhoneProductItemForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = PhoneProductItemForm(
            request.POST, request.FILES
        )  # request.FILES ni o'tkazish
        if form.is_valid():
            form.save()
            return redirect("phone-list")
        return render(request, self.template_name, {"form": form})


class PhoneCategoryCreateView(CreateView):
    model = Category
    form_class = PhoneCategoryCreateForm
    template_name = "product/category_create.html"  # Replace with your template path

    def form_valid(self, form):
        # You can add any additional processing here if needed
        return super().form_valid(form)

    def post(self, request):
        form = PhoneProductItemForm(
            request.POST, request.FILES
        )  # request.FILES ni o'tkazish
        if form.is_valid():
            form.save()
            return redirect("create_phone")
        return render(request, self.template_name, {"form": form})



class TicketListView(ListView):
    model = Ticket
    template_name = "product/ticket_list.html"  # your template name
    context_object_name = "tickets"

    def get_queryset(self):
        return Ticket.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any extra context here
        return context


class TicketView(View):
    template_name = "product/ticket_create.html"

    def get(self, request):
        form = TicketProductItemForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = TicketProductItemForm(
            request.POST, request.FILES
        )  # request.FILES ni o'tkazish
        if form.is_valid():
            form.save()
            return redirect("ticket-list")
        return render(request, self.template_name, {"form": form})


class GoodListView(ListView):
    model = Good
    template_name = "product/good_list.html"  # your template name
    context_object_name = "goods"

    def get_queryset(self):
        return Good.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any extra context here
        return context


class GoodView(View):
    template_name = "product/good_create.html"

    def get(self, request):
        form = GoodProductItemForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = GoodProductItemForm(
            request.POST, request.FILES
        )  # request.FILES ni o'tkazish
        if form.is_valid():
            form.save()
            return redirect("good-list")
        return render(request, self.template_name, {"form": form})
