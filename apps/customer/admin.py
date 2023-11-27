from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Location)
admin.site.register(News)
admin.site.register(ViewedNews)
admin.site.register(Favorite)
admin.site.register(Banner)
