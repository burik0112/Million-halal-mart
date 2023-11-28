from apps.customer.models import Profile
from apps.merchant.models import Order
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, HttpResponse


class UserListView(ListView):
    model = Profile
    template_name = "customer/users/users_list.html"
    context_object_name = "users"

    def get_queryset(self):
        return Profile.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UserOrdersView(DetailView):
    model = Profile
    template_name = "customer/users/user_orders_list.html"

    def get_context_data(self, **kwargs):
        context = super(UserOrdersView, self).get_context_data(**kwargs)
        orders = Order.objects.filter(user__id=self.kwargs['pk'])
        if orders:
            print(orders)
            context["orders"] = orders
        else:
            context["no_orders_message"] = "This user has no orders."

        return context
