from django.views.generic import ListView
from ..models import Phone

class PhoneListView(ListView):
    model = Phone
    template_name = 'phone_list.html'  # your template name
    context_object_name = 'phones'

    def get_queryset(self):
        return Phone.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any extra context here
        return context
