from django.contrib import admin
from .models import *


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
admin.site.register(Service, ServiceAdmin)


class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ["telegram", "instagram", "whatsapp", "phone_number", "imo", "kakao"]
admin.site.register(SocialMedia, SocialMediaAdmin)


admin.site.register(Information, InformationAdmin)
class BonusaAdmin(admin.ModelAdmin):
    list_display = ["amount", "percentage", "title", "created", "modified", 'active']
admin.site.register(Bonus, BonusaAdmin)

admin.site.register(OrderItem)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Agar siz yangi Order yaratayotganda bitta bo'sh OrderItem qo'shmoqchi bo'lsangiz


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ("user", "status", "total_amount", "created", "modified")
    search_fields = ("user__full_name", "status")
    list_filter = ("status",)

admin.site.register(Order, OrderAdmin)
