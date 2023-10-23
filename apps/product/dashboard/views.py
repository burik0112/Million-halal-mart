from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from ..models import Phone
from django.views import View
from django.views.generic.edit import CreateView
from .forms import PhoneProductItemForm


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
    template_name = "product/create_phone.html"

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


# class TicketListView(ListView):
#     model = Phone
#     template_name = "ticket_list.html"  # your template name
#     context_object_name = "tickets"

#     def get_queryset(self):
#         return Phone.objects.all()

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Add any extra context here
#         return context


# class TicketPhoneView(View):
#     template_name = "product/ticket_create.html"

#     def get(self, request):
#         form = PhoneProductItemForm()
#         return render(request, self.template_name, {"form": form})

#     def post(self, request):
#         form = PhoneProductItemForm(
#             request.POST, request.FILES
#         )  # request.FILES ni o'tkazish
#         if form.is_valid():
#             form.save()
#             return redirect("ticket-list")
#         return render(request, self.template_name, {"form": form})
