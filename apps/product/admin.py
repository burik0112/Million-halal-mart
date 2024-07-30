from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import *

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["main_type", "name", "desc", "created"]


admin.site.register(Category, CategoryAdmin)


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ["category", "name_uz", "desc"]


admin.site.register(SubCategory, SubCategoryAdmin)


class ProductItemAdmin(admin.ModelAdmin):
    list_display = [
        "created",
        "desc_uz",
        "product_type",
        "old_price",
        "new_price",
        "available_quantity",
        "measure",
    ]
    list_editable = ["product_type"]


admin.site.register(ProductItem, ProductItemAdmin)


class TicketAdmin(admin.ModelAdmin):
    list_display = ["event_date", "event_name", "product", "category"]


admin.site.register(Ticket, TicketAdmin)


class PhoneAdmin(admin.ModelAdmin):
    list_display = ["category", "model_name", "ram", "storage", "color"]


admin.site.register(Phone, PhoneAdmin)


class GoodAdmin(admin.ModelAdmin):
    list_display = ["expire_date", "name", "product", "ingredients", "sub_cat"]


admin.site.register(Good, GoodAdmin)


class ImageAdmin(admin.ModelAdmin):
    list_display = ["id", "image", "name", "product"]


admin.site.register(Image, ImageAdmin)


class SoldProductAdmin(admin.ModelAdmin):
    list_display = ["user", "amount", "product", "quantity"]


admin.site.register(SoldProduct, SoldProductAdmin)
