from modeltranslation.translator import register, TranslationOptions
from .models import Category, SubCategory, ProductItem, Ticket, Phone, Good, Image,  SoldProduct


@register(Category)
class ConnectTranslationOptions(TranslationOptions):
    fields = ('name', 'desc')

@register(SubCategory)
class ConnectTranslationOptions(TranslationOptions):
    fields = ('category__name', 'name', 'desc')

@register(ProductItem)
class ConnectTranslationOptions(TranslationOptions):
    fields = ('desc')

@register(Ticket)
class ConnectTranslationOptions(TranslationOptions):
    fields = ('event_name', 'product__desc', 'category__name', 'category_desc')

@register(Phone)
class ConnectTranslationOptions(TranslationOptions):
    fields = ('model_name', 'product__desc', 'category__name', 'category_desc')

@register(Good)
class ConnectTranslationOptions(TranslationOptions):
    fields = ('name', 'product__desc', 'sub_cat__name', 'sub_cat_desc', 'ingredients')

@register(Image)
class ConnectTranslationOptions(TranslationOptions):
    fields = ('name', 'product__desc')
