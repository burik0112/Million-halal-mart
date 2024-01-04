from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView
from apps.product.models import Phone, Ticket, Good, Category, SubCategory
from apps.customer.models import News
from django.views import View
from django.views.generic.edit import CreateView
from .forms import (
    PhoneProductItemForm,
    NewsForm,
    TicketProductItemForm,
    GoodProductItemForm,
    PhoneCategoryCreateForm,
    TicketCategoryCreateForm,
    PhoneEditForm,
    GoodCategoryCreateForm,
    TicketEditForm,
    NewsForm,
    GoodEditForm,
)


class PhoneListView(ListView):
    model = Phone
    template_name = "product/electronics/phone_list.html"  # your template name
    context_object_name = "phones"

    def get_queryset(self):
        return Phone.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PhoneCreateView(View):
    template_name = "product/electronics/phone_create.html"

    def get(self, request):
        form = PhoneProductItemForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = PhoneProductItemForm(
            request.POST, request.FILES
        )  # request.FILES ni o'tkazish
        if form.is_valid():
            print(form.data)
            form.save()
            return redirect("phone_list")
        return render(request, self.template_name, {"form": form})


class PhoneCategoryCreateView(CreateView):
    model = Category
    form_class = PhoneCategoryCreateForm
    template_name = "product/category_create.html"
    success_url = reverse_lazy("create_phone")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "Create New Phone Category"
        return context

    def form_valid(self, form):
        form.instance.main_type = "p"
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Formada xatolar mavjud:", form.errors)
        return super().form_invalid(form)


class TicketListView(ListView):
    model = Ticket
    template_name = "product/tickets/ticket_list.html"  # your template name
    context_object_name = "tickets"

    def get_queryset(self):
        return Ticket.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any extra context here
        return context


class TicketCreateView(View):
    template_name = "product/tickets/ticket_create.html"

    def get(self, request):
        form = TicketProductItemForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = TicketProductItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("ticket-list")
        else:
            print(form.errors)
            return render(request, self.template_name, {"form": form})


class TicketCategoryCreateView(CreateView):
    model = Category
    form_class = TicketCategoryCreateForm
    template_name = "product/category_create.html"
    success_url = reverse_lazy("ticket_create")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "Create New Ticket Category"
        return context

    def form_valid(self, form):
        form.instance.main_type = "t"
        return super().form_valid(form)


class GoodListView(ListView):
    model = Good
    template_name = "product/goods/good_list.html"
    context_object_name = "goods"

    def get_queryset(self):
        return Good.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class GoodCategoryCreateView(CreateView):
    model = SubCategory
    form_class = GoodCategoryCreateForm
    template_name = "product/category_create.html"
    success_url = reverse_lazy("good_create")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "Create New Good Category"
        return context

    def form_valid(self, form):
        form.instance.main_type = "f"
        return super().form_valid(form)


class GoodCreateView(View):
    template_name = "product/goods/good_create.html"

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


class GoodEditDeleteView(View):
    template_name = "product/goods/good_edit.html"

    def get(self, request, pk):
        good = get_object_or_404(Good, pk=pk)
        form = GoodEditForm(instance=good)
        return render(request, self.template_name, {"form": form, "good": good})

    def post(self, request, pk):
        good = get_object_or_404(Good, pk=pk)
        if "edit" in request.POST:
            form = GoodEditForm(request.POST, instance=good)
            if form.is_valid():
                form.save()
                return redirect("good-list")
        elif "delete" in request.POST:
            product_item = good.product
            good.delete()  # Delete the Good instance
            product_item.delete()  # Delete the associated ProductItem
            return redirect("good-list")  # Redirect to good list
        return render(request, self.template_name, {"form": form, "good": good})


class PhoneEditDeleteView(View):
    template_name = "product/electronics/edit_delete_phone.html"

    def get(self, request, pk):
        phone = get_object_or_404(Phone, pk=pk)
        form = PhoneEditForm(instance=phone)
        return render(request, self.template_name, {"form": form, "phone": phone})

    def post(self, request, pk):
        phone = get_object_or_404(Phone, pk=pk)
        if "edit" in request.POST:
            form = PhoneEditForm(request.POST, instance=phone)
            if form.is_valid():
                form.save()
                # Redirect to phone list or detail view
                return redirect("phone_list")
        elif "delete" in request.POST:
            product_item = phone.product
            phone.delete()  # Delete the Phone instance
            product_item.delete()  # Delete the associated ProductItem
            return redirect("phone_list")  # Redirect to phone list
        return render(request, self.template_name, {"form": form, "phone": phone})


class PhoneDeleteView(View):
    def post(self, request, pk):
        phone = get_object_or_404(Phone, pk=pk)
        product_item = phone.product
        phone.delete()  # Delete the Phone instance
        product_item.delete()  # Delete the associated ProductItem
        return redirect("phone_list")  # Redirect to phone list


class TicketEditDeleteView(View):
    template_name = "product/tickets/edit_delete_ticket.html"

    def get(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)
        form = TicketEditForm(instance=ticket)
        return render(request, self.template_name, {"form": form, "ticket": ticket})

    def post(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)
        if "edit" in request.POST:
            form = TicketEditForm(request.POST, instance=ticket)
            if form.is_valid():
                form.save()
                return redirect("ticket-list")
        elif "delete" in request.POST:
            product_item = ticket.product
            ticket.delete()  # Delete the Phone instance
            product_item.delete()  # Delete the associated ProductItem
            return redirect("ticket-list")  # Redirect to phone list
        return render(request, self.template_name, {"form": form, "ticket": ticket})


class TicketDeleteView(View):
    def post(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)
        product_item = ticket.product
        ticket.delete()  # Delete the Phone instance
        product_item.delete()  # Delete the associated ProductItem
        return redirect("ticket-list")  # Redirect to phone list


class GoodDeleteView(View):
    def post(self, request, pk):
        ticket = get_object_or_404(Good, pk=pk)
        product_item = ticket.product
        ticket.delete()  # Delete the Phone instance
        product_item.delete()  # Delete the associated ProductItem
        return redirect("good-list")  # Redirect to phone list


class NewsListView(ListView):
    model = News
    template_name = "customer/news/news_list.html"
    context_object_name = "news"

    def get_queryset(self):
        return News.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class NewsCreateView(View):
    template_name = "customer/news/news_create.html"

    def get(self, request):
        form = NewsForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("news-list")
        else:
            print(form.errors)
            return render(request, self.template_name, {"form": form})
