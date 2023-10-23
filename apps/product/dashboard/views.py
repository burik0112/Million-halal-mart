from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from ..models import Phone
from django.views import View
from django.views.generic.edit import CreateView
from .forms import PhoneProductItemForm

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

class CreatePhoneView(View):
    template_name = 'product/create_phone.html'

    def get(self, request):
        form = PhoneProductItemForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PhoneProductItemForm(request.POST, request.FILES)  # request.FILES ni o'tkazish
        if form.is_valid():
            form.save()
            return redirect('phone-list')
        return render(request, self.template_name, {'form': form})


    
# class CreatePhoneView(CreateView):
#     form_class = PhoneProductItemForm
#     template_name = 'product/create_phone.html'
#     success_url = reverse_lazy('phone')

#     # def form_valid(self, form):
#     #     form.instance.user = self.request.user  # Agar siz user bilan bog'lashni xohlaysiz
#     #     return super().form_valid(form)

#     def get_form_kwargs(self):
#         kwargs = super(CreatePhoneView, self).get_form_kwargs()
#         kwargs.update({'files': self.request.FILES})
#         return kwargs