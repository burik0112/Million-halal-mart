from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import *

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['main_type', 'name', 'desc']


admin.site.register(Category, CategoryAdmin)


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['category', 'name', 'desc']


admin.site.register(SubCategory, SubCategoryAdmin)


class ProductItemAdmin(admin.ModelAdmin):
    list_display = ['desc', 'price', 'available_quantity', 'measure']


admin.site.register(ProductItem, ProductItemAdmin)


class TicketAdmin(admin.ModelAdmin):
    list_display = ['event_name', 'product', 'event_date', 'category']


admin.site.register(Ticket, TicketAdmin)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ['model_name', 'ram', 'storage', 'category', 'color']
admin.site.register(Phone, PhoneAdmin)
class GoodAdmin(admin.ModelAdmin):
    list_display = ['name', 'product', 'ingredients', 'expire_date', 'sub_cat']
admin.site.register(Good, GoodAdmin)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'product']
admin.site.register(Image, ImageAdmin)
class SoldProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'product', 'quantity']
admin.site.register(SoldProduct, SoldProductAdmin)
