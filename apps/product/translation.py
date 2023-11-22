from modeltranslation.translator import register, TranslationOptions
from .models import Category, SubCategory, ProductItem, Ticket, Phone, Good, Image,  SoldProduct


@register(Category)
class ConnectTranslationOptions(TranslationOptions):
    fields = ('name', 'desc')

@register(SubCategory)
class ConnectTranslationOptions(TranslationOptions):
    fields = ( 'name', 'desc')

@register(ProductItem)
class ConnectTranslationOptions(TranslationOptions):
    fields = ('desc')

@register(Ticket)
class ConnectTranslationOptions(TranslationOptions):
    fields = ('event_name',)

@register(Phone)
class ConnectTranslationOptions(TranslationOptions):
    fields = ('model_name', )

@register(Good)
class ConnectTranslationOptions(TranslationOptions):
    fields = ('name', 'ingredients')

@register(Image)
class ConnectTranslationOptions(TranslationOptions):
    fields = ('name', )
