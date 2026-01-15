from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import *

# Register your models here.
class NewsAdmin(admin.ModelAdmin):
    list_display=['start_date','title', 'end_date', 'description']
class ProfileAdmin(admin.ModelAdmin):
    list_display=['phone_number','full_name', 'created']
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Location)
admin.site.register(News, NewsAdmin)
admin.site.register(ViewedNews)
admin.site.register(Favorite)
admin.site.register(Banner)

