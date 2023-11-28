from apps.customer.models import Profile
from django.views.generic import ListView


class UserListView(ListView):
    model = Profile
    template_name = "customer/users/users_list.html"  # your template name
    context_object_name = "users"

    def get_queryset(self):
        return Profile.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
