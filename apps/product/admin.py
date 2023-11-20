from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(ProductItem)
admin.site.register(Ticket)
admin.site.register(Phone)
admin.site.register(Good)
admin.site.register(Image)
admin.site.register(SoldProduct)
