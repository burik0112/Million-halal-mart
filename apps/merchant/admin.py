from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import *

# Register your models here.


class InformationAdmin(admin.ModelAdmin):
    list_display = [
        "reminder",
        "agreement",
        "shipment_terms",
        "privacy_policy",
        "about_us",
        "support_center",
        "payment_data",
    ]


class ServiceAdmin(admin.ModelAdmin):
    list_display = ["delivery_fee"]


class SecialMediaAdmin(admin.ModelAdmin):
    list_display = ["telegram", "instagram", "whatsapp", "phone_number", "imo", "kakao"]


admin.site.register(Information, InformationAdmin)
admin.site.register(OrderItem)
admin.site.register(Service, ServiceAdmin)
admin.site.register(SecialMedia, SecialMediaAdmin)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Agar siz yangi Order yaratayotganda bitta bo'sh OrderItem qo'shmoqchi bo'lsangiz


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ("user", "status", "total_amount", "created", "modified")
    search_fields = ("user__full_name", "status")
    list_filter = ("status",)


# Ro'yxatdan o'tkazish
admin.site.register(Order, OrderAdmin)
