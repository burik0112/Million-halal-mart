from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import *

# Register your models here.
admin.site.register(Order)


class InformationAdmin(admin.ModelAdmin):
    list_display = ['reminder', 'agreement', 'shipment_terms',
                    'privacy_policy', 'about_us', 'support_center', 'payment_data']


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['delivery_fee']


class SecialMediaAdmin(admin.ModelAdmin):
    list_display = ['telegram', 'instagram',
                    'whatsapp', 'phone_number', 'imo', 'kakao']


admin.site.register(Information, InformationAdmin)
admin.site.register(OrderItem)
admin.site.register(Service, ServiceAdmin)
admin.site.register(SecialMedia, SecialMediaAdmin)
