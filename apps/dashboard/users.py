from apps.customer.models import Profile
from apps.merchant.models import Order, OrderItem
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
        user = Profile.objects.get(id=self.kwargs['pk'])
        if orders:
            context["orders"] = orders
            context["user"] = user
            
        else:
            context["no_orders_message"] = "This user has no orders."
        return context

class UserOrderDetailView(DetailView):
    model = Order
    template_name = "customer/users/user_order_detail.html"

    def get_context_data(self, **kwargs):
        context = super(UserOrderDetailView, self).get_context_data(**kwargs)
        order = Order.objects.get(id=self.kwargs['pk'])
        order_items = OrderItem.objects.filter(order__id=self.kwargs['pk'])
        user = Profile.objects.get(id=self.kwargs['pk'])

        product_details = []
        for order_item in order_items:
            product_type, details = self.get_product_type(order_item.product)
            product_details.append({"type": product_type, "details": details})

        if order_items:
            context["order_items"] = order_items
            context["user"] = user
            context["order"] = order
            context["product_details"] = product_details
        else:
            context["no_orders_message"] = "This user has no orders."
        print(context)
        return context

    def get_product_type(self, product_item):
        if hasattr(product_item, "phones"):
            return "Phone", {
                "model_name": product_item.phones.model_name,
                "ram": product_item.phones.get_ram_display(),
                "storage": product_item.phones.get_storage_display(),
                "color": product_item.phones.get_color_display(),
                "condition": product_item.phones.get_condition_display(),
            }
        elif hasattr(product_item, "tickets"):
            return "Ticket", {
                "event_name": product_item.tickets.event_name,
                "event_date": product_item.tickets.event_date,
                "category": product_item.tickets.category.name if product_item.tickets.category else None,
            }
        elif hasattr(product_item, "goods"):
            return "Good", {
                "name": product_item.goods.name,
                "ingredients": product_item.goods.ingredients,
                "expire_date": product_item.goods.expire_date,
                "sub_cat": product_item.goods.sub_cat.name if product_item.goods.sub_cat else None,
            }
        return None, None
