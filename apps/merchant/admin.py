from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import *

# Register your models here.
admin.site.register(Order)
admin.site.register(Information)
admin.site.register(OrderItem)
